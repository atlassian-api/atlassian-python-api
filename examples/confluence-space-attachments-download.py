#!/usr/bin/env python3
"""
Download all attachments from a Confluence Data Center / Server space,
saving them into folders that mirror the page tree of the space.

    <OUTPUT_DIR>/<SPACE>/<Root page>/<Child page>/<Grandchild page>/file.pdf

HOW TO USE
  1. Fill in the CONFIGURATION section below (URL, token, space key).
  2. Run:  python3 confluence-space-attachments-download.py
     Progress is printed to the console and saved to _download.log.

Uses only the public REST API (/rest/api/content), so Confluence enforces
permissions: the token owner sees only what they are allowed to view.

Requires: requests (pip install requests)
"""

# =============================================================================
# CONFIGURATION - fill in before running
# =============================================================================

# Confluence base URL incl. context path, e.g. https://wiki.example.com/confluence
CONFLUENCE_URL = 'https://confluence.example.com'

# Personal Access Token: Avatar (top right) -> Profile -> Personal Access Tokens -> Create token
CONFLUENCE_TOKEN = 'PASTE-YOUR-TOKEN-HERE'

# Space key (visible in the URL: .../display/KEY/... or in Space tools -> Overview)
SPACE_KEY = 'DOCS'

# Where to save files (a <SPACE_KEY> subfolder is created inside)
OUTPUT_DIR = './confluence-export'

# Also download attachments of blog posts (saved under "_Blog posts")
INCLUDE_BLOGPOSTS = False

# Skip files that already exist with the same size (lets you resume an interrupted run)
SKIP_EXISTING = True

# TLS: True = verify using the Windows certificate store (company CAs included) + standard CAs,
#      or path to a CA bundle file, e.g. 'C:/certs/company-ca.pem', or False = no verification (not recommended)
VERIFY_SSL = True

# True = connect to Confluence directly, bypassing the system/company proxy (typical for an internal server)
DIRECT_CONNECTION = True

# Wait for Enter before closing, so the window stays open when started by double-click
PAUSE_AT_END = True

# =============================================================================

import argparse
import csv
import logging
import os
import re
import ssl
import sys
import tempfile
import time
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print('ERROR: the "requests" library is missing. Install it with:')
    print('    "%s" -m pip install requests' % sys.executable)
    if PAUSE_AT_END:
        input('\nPress Enter to close...')
    sys.exit(1)

PAGE_LIMIT = 100
INVALID_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
RESERVED_NAMES = {'CON', 'PRN', 'AUX', 'NUL'} | {'COM%d' % i for i in range(1, 10)} | {'LPT%d' % i for i in range(1, 10)}


def system_ca_bundle():
    """
    'requests' trusts only its own CA list (certifi), not the Windows certificate store,
    so company CAs (e.g. an internal "Issuing CA") are rejected. Build a PEM bundle with
    certifi + trusted Windows ROOT/CA certificates and return its path (None if not Windows).
    """
    if not hasattr(ssl, 'enum_certificates'):  # only exists on Windows
        return None, 0
    pems, count = [], 0
    try:
        import certifi
        with open(certifi.where(), encoding='utf-8') as f:
            pems.append(f.read())
    except (ImportError, OSError):
        pass
    for store in ('ROOT', 'CA'):
        try:
            certificates = ssl.enum_certificates(store)
        except OSError:
            continue
        for der, encoding, trust in certificates:
            # trust is True (all purposes) or a set of OIDs; 1.3.6.1.5.5.7.3.1 = server authentication
            if encoding == 'x509_asn' and (trust is True or '1.3.6.1.5.5.7.3.1' in trust):
                pems.append(ssl.DER_cert_to_PEM_cert(der))
                count += 1
    path = os.path.join(tempfile.gettempdir(), 'confluence-ca-bundle.pem')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(pems))
    return path, count


def resolve_verify(setting):
    """VERIFY_SSL: True -> Windows store + certifi (on Windows), path -> that file, False -> no check."""
    if setting is True:
        path, _ = system_ca_bundle()
        return path or True
    return setting


def bypass_proxy(url):
    """Connect to Confluence directly, ignoring the system/company proxy, for this host only."""
    host = urlparse(url).hostname
    for key in ('NO_PROXY', 'no_proxy'):
        current = os.environ.get(key, '')
        os.environ[key] = ','.join(x for x in (current, host) if x)


log = logging.getLogger('confluence-download')


def safe_name(name, max_len=120):
    """Make a title usable as a file/folder name on Windows, macOS and Linux."""
    name = INVALID_CHARS.sub('_', name).strip().rstrip('.')
    if not name:
        name = '_'
    if name.split('.')[0].upper() in RESERVED_NAMES:
        name = '_' + name
    if len(name) > max_len:
        root, ext = os.path.splitext(name)
        name = root[:max_len - len(ext)] + ext
    return name


def human_size(num):
    for unit in ('B', 'KB', 'MB', 'GB'):
        if num < 1024 or unit == 'GB':
            return ('%d %s' if unit == 'B' else '%.1f %s') % (num, unit)
        num /= 1024.0


class Confluence:
    def __init__(self, url, token, verify=True, timeout=120):
        self.url = url.rstrip('/')
        self.session = requests.Session()
        # passed on every request: a session-level verify is overridden by REQUESTS_CA_BUNDLE/CURL_CA_BUNDLE
        self.verify = verify
        self.timeout = timeout
        self.session.headers['Accept'] = 'application/json'
        self.session.headers['Authorization'] = 'Bearer ' + token

    def get(self, path_or_url, params=None, stream=False, retries=4):
        url = path_or_url if path_or_url.startswith('http') else self.url + path_or_url
        for attempt in range(retries + 1):
            wait = 2 ** (attempt + 1)
            try:
                response = self.session.get(url, params=params, stream=stream, timeout=self.timeout, verify=self.verify)
            except requests.exceptions.SSLError:
                raise  # certificate problems do not go away on retry
            except requests.RequestException as e:
                if attempt == retries:
                    raise
                log.warning('Connection problem (%s), retrying in %ds...', e.__class__.__name__, wait)
            else:
                # 429 = rate limiting (DC 7.7+), 5xx = transient server errors
                if response.status_code != 429 and response.status_code < 500:
                    response.raise_for_status()
                    return response
                if attempt == retries:
                    response.raise_for_status()
                retry_after = response.headers.get('Retry-After', '')
                wait = int(retry_after) if retry_after.isdigit() else wait
                log.warning('Server answered HTTP %s, retrying in %ds...', response.status_code, wait)
            time.sleep(wait)

    def paged(self, path, params):
        """Iterate over all results of a paged /rest/api endpoint."""
        start = 0
        while True:
            data = self.get(path, params=dict(params, start=start, limit=PAGE_LIMIT)).json()
            results = data.get('results', [])
            for item in results:
                yield item
            # Confluence may cap 'limit' server-side, so rely on the 'next' link, not on the page size
            if not results or 'next' not in data.get('_links', {}):
                return
            start += len(results)

    def check_space(self, space_key):
        try:
            return self.get('/rest/api/space/' + space_key).json()
        except requests.exceptions.SSLError as e:
            raise SystemExit('ERROR: SSL certificate not trusted: %s\n'
                             'Run confluence-diagnostics.py, or set VERIFY_SSL to your company CA file (.pem/.cer)' % e)
        except requests.HTTPError as e:
            code = e.response.status_code if e.response is not None else None
            if code == 401:
                raise SystemExit('ERROR: token rejected (HTTP 401) - check CONFLUENCE_TOKEN')
            if code in (403, 404):
                raise SystemExit('ERROR: space "%s" does not exist or you have no access to it (HTTP %s)'
                                 % (space_key, code))
            raise

    def space_content(self, space_key, content_type):
        return self.paged('/rest/api/content', {
            'spaceKey': space_key,
            'type': content_type,
            'status': 'current',
            'expand': 'ancestors',
        })

    def attachments(self, content_id):
        return self.paged('/rest/api/content/%s/child/attachment' % content_id, {'expand': 'version'})


def page_folder(page, folder_cache, base_dir):
    """Folder path built from the page's ancestors + its own title."""
    parts = [safe_name(a['title']) for a in page.get('ancestors', [])] + [safe_name(page['title'])]
    folder = os.path.join(base_dir, *parts)
    # Titles are unique per space, but sanitising may produce collisions (e.g. "a/b" and "a_b").
    owner = folder_cache.setdefault(folder, page['id'])
    if owner != page['id']:
        folder = '%s (%s)' % (folder, page['id'])
    return folder


def unique_path(path, used):
    if path not in used and not os.path.exists(path):
        used.add(path)
        return path
    root, ext = os.path.splitext(path)
    i = 1
    while '%s (%d)%s' % (root, i, ext) in used or os.path.exists('%s (%d)%s' % (root, i, ext)):
        i += 1
    path = '%s (%d)%s' % (root, i, ext)
    used.add(path)
    return path


def download(confluence, url, target):
    tmp = target + '.part'
    with confluence.get(url, stream=True) as response, open(tmp, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)
    os.replace(tmp, target)


def setup_logging(log_file):
    log.setLevel(logging.INFO)
    fmt = logging.Formatter('%(asctime)s  %(levelname)-7s %(message)s', '%H:%M:%S')
    for handler in (logging.StreamHandler(sys.stdout), logging.FileHandler(log_file, encoding='utf-8')):
        handler.setFormatter(fmt)
        log.addHandler(handler)


def parse_args():
    """Optional command-line overrides of the CONFIGURATION section."""
    parser = argparse.ArgumentParser(description='Download all attachments of a Confluence space into a page-tree folder structure.')
    parser.add_argument('--url', default=CONFLUENCE_URL)
    parser.add_argument('--token', default=os.environ.get('CONFLUENCE_TOKEN') or CONFLUENCE_TOKEN)
    parser.add_argument('--space', default=SPACE_KEY)
    parser.add_argument('--out', default=OUTPUT_DIR)
    parser.add_argument('--blogposts', action='store_true', default=INCLUDE_BLOGPOSTS)
    parser.add_argument('--no-skip-existing', dest='skip_existing', action='store_false', default=SKIP_EXISTING)
    parser.add_argument('--ca-bundle', default=VERIFY_SSL if isinstance(VERIFY_SSL, str) else None)
    return parser.parse_args()


def main():
    args = parse_args()
    if not args.token or args.token.startswith('PASTE-'):
        raise SystemExit('ERROR: set CONFLUENCE_TOKEN in the CONFIGURATION section at the top of the script')
    if 'example.com' in args.url:
        raise SystemExit('ERROR: set CONFLUENCE_URL in the CONFIGURATION section at the top of the script')

    verify = args.ca_bundle or resolve_verify(VERIFY_SSL)
    if DIRECT_CONNECTION:
        bypass_proxy(args.url)
    confluence = Confluence(args.url, args.token, verify=verify)

    space = confluence.check_space(args.space)
    base_dir = os.path.join(args.out, safe_name(space['key']))
    os.makedirs(base_dir, exist_ok=True)
    setup_logging(os.path.join(base_dir, '_download.log'))
    started = time.time()

    log.info('TLS verification: %s | proxy: %s', verify, 'bypassed' if DIRECT_CONNECTION else 'system settings')
    log.info('Space: %s (%s)', space['name'], space['key'])
    log.info('Output folder: %s', os.path.abspath(base_dir))

    sources = [('page', base_dir)]
    if args.blogposts:
        sources.append(('blogpost', os.path.join(base_dir, '_Blog posts')))

    log.info('Collecting the list of pages...')
    items = []
    for content_type, root in sources:
        for page in confluence.space_content(args.space, content_type):
            items.append((page, root))
            if len(items) % 500 == 0:
                log.info('  ...%d found so far', len(items))
    log.info('Found %d %s. Starting download.', len(items), 'pages/blog posts' if args.blogposts else 'pages')

    folder_cache, used_paths = {}, set()
    stats = {'pages_with_files': 0, 'files': 0, 'skipped': 0, 'errors': 0, 'bytes': 0}
    manifest_path = os.path.join(base_dir, '_attachments_manifest.csv')
    width = len(str(len(items)))

    with open(manifest_path, 'w', newline='', encoding='utf-8-sig') as manifest_file:
        manifest = csv.writer(manifest_file, delimiter=';')
        manifest.writerow(['page_id', 'page_title', 'attachment_id', 'file_name', 'version', 'size', 'local_path', 'status'])

        for index, (page, root) in enumerate(items, 1):
            progress = '[%*d/%d]' % (width, index, len(items))
            attachments = list(confluence.attachments(page['id']))
            if not attachments:
                log.info('%s %s - no attachments', progress, page['title'])
                continue

            stats['pages_with_files'] += 1
            folder = page_folder(page, folder_cache, root)
            os.makedirs(folder, exist_ok=True)
            log.info('%s %s - %d attachment(s) -> %s', progress, page['title'], len(attachments),
                     os.path.relpath(folder, base_dir))

            for att in attachments:
                size = att.get('extensions', {}).get('fileSize')
                target = os.path.join(folder, safe_name(att['title'], max_len=200))
                if args.skip_existing and os.path.exists(target) and size is not None and os.path.getsize(target) == size:
                    used_paths.add(target)
                    status = 'skipped'
                    stats['skipped'] += 1
                    log.info('      = %s (already downloaded)', att['title'])
                else:
                    target = unique_path(target, used_paths)
                    link = att['_links']['download']
                    url = link if link.startswith('http') else att['_links'].get('base', confluence.url) + link
                    try:
                        download(confluence, url, target)
                        status = 'ok'
                        stats['files'] += 1
                        stats['bytes'] += os.path.getsize(target)
                        log.info('      + %s (%s)', att['title'], human_size(os.path.getsize(target)))
                    except Exception as e:  # keep going, report at the end
                        status = 'error: %s' % e
                        stats['errors'] += 1
                        log.error('      ! %s - %s', att['title'], e)

                manifest.writerow([page['id'], page['title'], att['id'], att['title'],
                                   att.get('version', {}).get('number'), size,
                                   os.path.relpath(target, base_dir), status])

    elapsed = int(time.time() - started)
    log.info('=' * 60)
    log.info('DONE in %dm %02ds', elapsed // 60, elapsed % 60)
    log.info('Pages scanned:        %d (with attachments: %d)', len(items), stats['pages_with_files'])
    log.info('Files downloaded:     %d (%s)', stats['files'], human_size(stats['bytes']))
    log.info('Skipped (existing):   %d', stats['skipped'])
    log.info('Errors:               %d', stats['errors'])
    log.info('Manifest:             %s', os.path.abspath(manifest_path))
    return 1 if stats['errors'] else 0


def pause():
    if PAUSE_AT_END:
        try:
            input('\nPress Enter to close...')
        except (EOFError, KeyboardInterrupt):
            pass


if __name__ == '__main__':
    print('Starting Confluence attachments download...')
    exit_code = 1
    try:
        exit_code = main()
    except KeyboardInterrupt:
        print('\nInterrupted - run again to resume (already downloaded files will be skipped).')
        exit_code = 130
    except SystemExit as e:
        if e.code not in (None, 0):
            print(e.code if isinstance(e.code, str) else 'Exit code %s' % e.code)
        exit_code = e.code if isinstance(e.code, int) else 1
    except Exception:
        import traceback
        print('\nUNEXPECTED ERROR - run confluence-diagnostics.py and send its log:')
        traceback.print_exc(file=sys.stdout)
    pause()
    sys.exit(exit_code)
