#!/usr/bin/env python3
"""
Step-by-step diagnostics for confluence-space-attachments-download.py.

Checks, in order: Python environment, configuration, DNS, TCP, HTTPS/SSL,
token, space access, page listing, attachment listing, file download and
write access to the output folder.

Configuration is read automatically from confluence-space-attachments-download.py
lying in the same folder. If that file is not found, fill in the section below.

Run:   python confluence-diagnostics.py
Result is printed and saved to confluence-diagnostics.log next to this script.
The token is never written to the log in full.
"""

# Used only when confluence-space-attachments-download.py is not next to this file
CONFLUENCE_URL = 'https://confluence.example.com'
CONFLUENCE_TOKEN = 'PASTE-YOUR-TOKEN-HERE'
SPACE_KEY = 'DOCS'
OUTPUT_DIR = './confluence-export'
VERIFY_SSL = True
DIRECT_CONNECTION = True

import ast
import json
import os
import platform
import socket
import ssl
import sys
import tempfile
import time
import traceback

try:  # Python 3 only, but give a readable message on Python 2
    from urllib.parse import urlparse, urlencode
    from urllib.request import Request, urlopen, getproxies
    from urllib.error import HTTPError, URLError
except ImportError:
    print('ERROR: this script needs Python 3, you are running Python %s' % sys.version.split()[0])
    raise SystemExit(1)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_SCRIPT = os.path.join(SCRIPT_DIR, 'confluence-space-attachments-download.py')
LOG_FILE = os.path.join(SCRIPT_DIR, 'confluence-diagnostics.log')
TIMEOUT = 30

_log = open(LOG_FILE, 'w', encoding='utf-8')
results = []  # (step, status)


def out(msg=''):
    line = '%s  %s' % (time.strftime('%H:%M:%S'), msg) if msg else ''
    print(line)
    _log.write(line + '\n')
    _log.flush()


def step(title):
    out()
    out('=== %s ===' % title)


def ok(name, msg):
    results.append((name, 'OK'))
    out('[OK]   ' + msg)


def warn(name, msg):
    results.append((name, 'WARN'))
    out('[WARN] ' + msg)


def fail(name, msg):
    results.append((name, 'FAIL'))
    out('[FAIL] ' + msg)


def mask(token):
    if not token:
        return '<empty>'
    return '%s...%s (length %d)' % (token[:4], token[-2:], len(token)) if len(token) > 8 else '<too short: %d chars>' % len(token)


def read_config():
    cfg = {'CONFLUENCE_URL': CONFLUENCE_URL, 'CONFLUENCE_TOKEN': CONFLUENCE_TOKEN,
           'SPACE_KEY': SPACE_KEY, 'OUTPUT_DIR': OUTPUT_DIR, 'VERIFY_SSL': VERIFY_SSL,
           'DIRECT_CONNECTION': DIRECT_CONNECTION}
    if not os.path.exists(MAIN_SCRIPT):
        return cfg, 'this file (main script not found next to it)'
    with open(MAIN_SCRIPT, encoding='utf-8-sig') as f:
        tree = ast.parse(f.read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in cfg:
                try:
                    cfg[name] = ast.literal_eval(node.value)
                except ValueError:
                    pass
    if os.environ.get('CONFLUENCE_TOKEN'):
        cfg['CONFLUENCE_TOKEN'] = os.environ['CONFLUENCE_TOKEN']
    return cfg, MAIN_SCRIPT


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


class Http:
    """Same requests as the main script; uses 'requests' if installed, else urllib."""

    def __init__(self, base, token, verify):
        self.base = base.rstrip('/')
        self.token = token
        self.verify = verify
        try:
            import requests
            self.requests = requests
            self.session = requests.Session()
        except ImportError:
            self.requests = None

    def get(self, path, params=None, auth=True, max_bytes=None):
        url = path if path.startswith('http') else self.base + path
        if params:
            url += '?' + urlencode(params)
        headers = {'Accept': 'application/json'}
        if auth:
            headers['Authorization'] = 'Bearer ' + self.token
        started = time.time()
        if self.requests:
            r = self.session.get(url, headers=headers, timeout=TIMEOUT, stream=True, allow_redirects=False,
                                 verify=self.verify)
            body = r.raw.read(max_bytes) if max_bytes else r.content
            status, hdrs = r.status_code, r.headers
            r.close()
        else:
            ctx = ssl.create_default_context(cafile=self.verify if isinstance(self.verify, str) else None)
            if self.verify is False:
                ctx.check_hostname, ctx.verify_mode = False, ssl.CERT_NONE
            try:
                resp = urlopen(Request(url, headers=headers), timeout=TIMEOUT, context=ctx)
                status, hdrs = resp.status, resp.headers
                body = resp.read(max_bytes) if max_bytes else resp.read()
            except HTTPError as e:
                status, hdrs, body = e.code, e.headers, e.read()
        out('       GET %s -> HTTP %s (%.1fs)' % (url, status, time.time() - started))
        return status, hdrs, body


def body_preview(body, n=300):
    text = body.decode('utf-8', 'replace') if isinstance(body, bytes) else str(body)
    text = ' '.join(text.split())
    return text[:n] + ('...' if len(text) > n else '')


def main():
    out('Confluence diagnostics - log file: %s' % LOG_FILE)

    # 1 -----------------------------------------------------------------
    step('1. Python environment')
    out('Python:     %s' % sys.version.replace('\n', ' '))
    out('Executable: %s' % sys.executable)
    out('System:     %s %s (%s)' % (platform.system(), platform.release(), platform.machine()))
    out('Script dir: %s' % SCRIPT_DIR)
    out('Working dir:%s' % os.getcwd())
    out('OpenSSL:    %s' % ssl.OPENSSL_VERSION)
    if sys.version_info < (3, 6):
        fail('python', 'Python 3.6+ required')
    else:
        ok('python', 'Python version is fine')
    try:
        import requests
        ok('requests', 'requests %s installed (%s)' % (requests.__version__, os.path.dirname(requests.__file__)))
        try:
            import certifi
            out('       certifi CA bundle: %s' % certifi.where())
        except ImportError:
            pass
    except ImportError:
        fail('requests', 'requests NOT installed - the main script cannot start. Run:  "%s" -m pip install requests'
             % sys.executable)

    # 2 -----------------------------------------------------------------
    step('2. Configuration')
    cfg, source = read_config()
    out('Read from:  %s' % source)
    out('Main script present: %s' % os.path.exists(MAIN_SCRIPT))
    url, token, space_key = cfg['CONFLUENCE_URL'], cfg['CONFLUENCE_TOKEN'], cfg['SPACE_KEY']
    out('URL:        %r' % url)
    out('Token:      %s' % mask(token))
    out('Space key:  %r' % space_key)
    out('Output dir: %r -> %s' % (cfg['OUTPUT_DIR'], os.path.abspath(cfg['OUTPUT_DIR'])))
    out('VERIFY_SSL: %r' % (cfg['VERIFY_SSL'],))
    out('DIRECT_CONNECTION: %r' % (cfg['DIRECT_CONNECTION'],))
    problems = []
    if 'example.com' in url:
        problems.append('CONFLUENCE_URL still has the example value')
    if not url.startswith(('http://', 'https://')):
        problems.append('CONFLUENCE_URL must start with https:// (or http://)')
    if '/display/' in url or '/pages/' in url or '/spaces/' in url:
        problems.append('CONFLUENCE_URL looks like a page link - use only the base address, e.g. https://wiki.company.com')
    if not token or token.startswith('PASTE-'):
        problems.append('CONFLUENCE_TOKEN is not filled in')
    elif token != token.strip():
        problems.append('CONFLUENCE_TOKEN has spaces/newlines at the beginning or end')
    if not space_key or space_key != space_key.strip():
        problems.append('SPACE_KEY is empty or has spaces')
    if isinstance(cfg['VERIFY_SSL'], str) and not os.path.exists(cfg['VERIFY_SSL']):
        problems.append('VERIFY_SSL points to a file that does not exist: %s' % cfg['VERIFY_SSL'])
    for p in problems:
        fail('config', p)
    if problems:
        return
    ok('config', 'configuration looks complete')

    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)

    # 3 -----------------------------------------------------------------
    step('3. Proxy settings')
    proxies = getproxies()
    out('Proxies seen by Python: %s' % (proxies or 'none'))
    for name in ('HTTP_PROXY', 'HTTPS_PROXY', 'NO_PROXY', 'REQUESTS_CA_BUNDLE', 'SSL_CERT_FILE'):
        for key in (name, name.lower()):
            if os.environ.get(key):
                out('       env %s=%s' % (key, os.environ[key]))
    if cfg['DIRECT_CONNECTION']:
        bypass_proxy(url)
        out('       DIRECT_CONNECTION=True -> proxy bypassed for %s' % host)
    try:
        import requests
        used = requests.utils.get_environ_proxies(url)
        out('       proxy that requests will use for Confluence: %s' % (used.get(parsed.scheme) or 'none (direct)'))
    except ImportError:
        pass
    ok('proxy', 'proxy info collected')

    # 4 -----------------------------------------------------------------
    step('4. DNS: %s' % host)
    try:
        addrs = sorted({a[4][0] for a in socket.getaddrinfo(host, port)})
        ok('dns', '%s resolves to %s' % (host, ', '.join(addrs)))
    except socket.gaierror as e:
        fail('dns', 'cannot resolve %s: %s - wrong address, or VPN not connected?' % (host, e))
        return

    # 5 -----------------------------------------------------------------
    step('5. TCP connection to %s:%d' % (host, port))
    try:
        started = time.time()
        socket.create_connection((host, port), timeout=TIMEOUT).close()
        ok('tcp', 'port %d open (%.2fs)' % (port, time.time() - started))
    except OSError as e:
        if proxies:
            warn('tcp', 'direct connection failed (%s) - may be fine if traffic goes through the proxy' % e)
        else:
            fail('tcp', 'cannot connect: %s - firewall/VPN?' % e)
            return

    # 6 -----------------------------------------------------------------
    step('6. HTTPS / SSL certificate')
    if parsed.scheme == 'https':
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((host, port), timeout=TIMEOUT) as sock:
                with ctx.wrap_socket(sock, server_hostname=host) as tls:
                    cert = tls.getpeercert()
                    issuer = dict(x[0] for x in cert.get('issuer', ()))
                    out('       %s, issuer: %s, valid until: %s' % (tls.version(), issuer.get('organizationName') or issuer.get('commonName'), cert.get('notAfter')))
            ok('ssl-system', 'certificate trusted by the system (OpenSSL) store')
        except ssl.SSLError as e:
            warn('ssl-system', 'system store does not trust the certificate: %s' % e)
        except OSError as e:
            warn('ssl-system', 'could not test directly: %s' % e)
    else:
        warn('ssl-system', 'plain http:// - no TLS')

    verify = resolve_verify(cfg['VERIFY_SSL'])
    if parsed.scheme == 'https':
        step('6b. requests: certifi only vs. Windows certificate store')
        bundle, count = system_ca_bundle()
        out('       Windows store: %s' % ('%d trusted certificates -> %s' % (count, bundle) if bundle else 'not available (not Windows)'))
        try:
            import requests
            variants = [('certifi only', True)] + ([('certifi + Windows store', bundle)] if bundle else [])
            for label, value in variants:
                try:
                    requests.get(url.rstrip('/') + '/status', verify=value, timeout=TIMEOUT)
                    out('       %-24s -> OK' % label)
                except requests.exceptions.SSLError as e:
                    out('       %-24s -> SSL ERROR: %s' % (label, str(e)[:200]))
                except requests.RequestException as e:
                    out('       %-24s -> %s: %s' % (label, type(e).__name__, str(e)[:200]))
        except ImportError:
            pass
        ok('ssl-compare', 'comparison done')

    http = Http(url, token, verify)
    out('HTTP library used for next steps: %s' % ('requests' if http.requests else 'urllib (requests missing)'))
    out('TLS verification used: %s' % (verify,))

    # 7 -----------------------------------------------------------------
    step('7. Confluence reachable (/status, no login)')
    try:
        status, hdrs, body = http.get('/status', auth=False)
        out('       response: %s' % body_preview(body))
        if status == 200 and b'RUNNING' in body:
            ok('status', 'Confluence is RUNNING')
        elif status in (301, 302, 303, 307, 308):
            warn('status', 'redirect to %s - CONFLUENCE_URL may need a different form (context path, https?)' % hdrs.get('Location'))
        else:
            warn('status', 'unexpected answer - is CONFLUENCE_URL the Confluence base address?')
    except Exception as e:
        if 'SSL' in type(e).__name__ or 'CERTIFICATE' in str(e).upper():
            fail('status', 'SSL error: %s\n'
                 '       -> company certificate not trusted. Export the company root + issuing CA (Base-64 .cer) and set VERIFY_SSL to that file path.' % e)
        else:
            fail('status', '%s: %s' % (type(e).__name__, e))
        return

    # 8 -----------------------------------------------------------------
    step('8. Token / login (/rest/api/user/current)')
    status, hdrs, body = http.get('/rest/api/user/current')
    if status == 200:
        user = json.loads(body.decode('utf-8'))
        if user.get('type') == 'anonymous':
            fail('token', 'Confluence treats you as ANONYMOUS - token not accepted (check it was copied fully)')
        else:
            ok('token', 'logged in as: %s (%s)' % (user.get('displayName'), user.get('username')))
    else:
        out('       response: %s' % body_preview(body))
        fail('token', 'HTTP %s - %s' % (status, 'token invalid or expired' if status == 401 else 'unexpected'))
        if status in (401, 403):
            return

    # 9 -----------------------------------------------------------------
    step('9. Space %s' % space_key)
    status, hdrs, body = http.get('/rest/api/space/' + space_key)
    if status == 200:
        space = json.loads(body.decode('utf-8'))
        ok('space', 'space found: %s (%s)' % (space.get('name'), space.get('key')))
    else:
        out('       response: %s' % body_preview(body))
        fail('space', 'HTTP %s - space key wrong (case matters!) or no permission to view it' % status)
        return

    # 10 ----------------------------------------------------------------
    step('10. Listing pages of the space')
    status, hdrs, body = http.get('/rest/api/content', {'spaceKey': space_key, 'type': 'page', 'status': 'current',
                                                         'expand': 'ancestors', 'limit': 25})
    if status != 200:
        out('       response: %s' % body_preview(body))
        fail('pages', 'HTTP %s while listing pages' % status)
        return
    data = json.loads(body.decode('utf-8'))
    pages = data.get('results', [])
    out('       first batch: %d pages, more available: %s' % (len(pages), 'next' in data.get('_links', {})))
    for p in pages[:5]:
        path = ' / '.join([a['title'] for a in p.get('ancestors', [])] + [p['title']])
        out('       - [%s] %s' % (p['id'], path))
    if pages:
        ok('pages', 'pages are visible')
    else:
        fail('pages', 'no pages visible in the space for this user')
        return

    # 11 ----------------------------------------------------------------
    step('11. Attachments (checking up to 25 pages)')
    sample = None
    for p in pages:
        status, hdrs, body = http.get('/rest/api/content/%s/child/attachment' % p['id'], {'limit': 5})
        if status != 200:
            out('       response: %s' % body_preview(body))
            fail('attachments', 'HTTP %s while listing attachments of page %s' % (status, p['id']))
            return
        atts = json.loads(body.decode('utf-8')).get('results', [])
        if atts:
            sample = atts[0]
            out('       page "%s" has attachments, e.g. %s (%s bytes)'
                % (p['title'], sample['title'], sample.get('extensions', {}).get('fileSize')))
            break
    if sample:
        ok('attachments', 'attachments can be listed')
    else:
        warn('attachments', 'none of the first %d pages has attachments (listing works)' % len(pages))

    # 12 ----------------------------------------------------------------
    step('12. Downloading a file (first 64 KB)')
    if sample:
        link = sample['_links']['download']
        dl = link if link.startswith('http') else sample['_links'].get('base', url.rstrip('/')) + link
        status, hdrs, body = http.get(dl, max_bytes=65536)
        if status == 200:
            ok('download', 'download works (%d bytes read, type %s)' % (len(body), hdrs.get('Content-Type')))
        else:
            out('       response: %s' % body_preview(body))
            fail('download', 'HTTP %s while downloading' % status)
    else:
        warn('download', 'skipped - no attachment found to test')

    # 13 ----------------------------------------------------------------
    step('13. Write access to output folder')
    target = os.path.abspath(cfg['OUTPUT_DIR'])
    try:
        os.makedirs(target, exist_ok=True)
        test_file = os.path.join(target, '_write_test.tmp')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        ok('write', 'can write to %s' % target)
    except OSError as e:
        fail('write', 'cannot write to %s: %s' % (target, e))


if __name__ == '__main__':
    try:
        main()
    except Exception:
        results.append(('unexpected', 'FAIL'))
        out('[FAIL] unexpected error:')
        for line in traceback.format_exc().splitlines():
            out('       ' + line)
    out()
    out('=== SUMMARY ===')
    for name, status in results:
        out('  %-12s %s' % (name, status))
    failed = [n for n, s in results if s == 'FAIL']
    out('RESULT: %s' % ('PROBLEMS FOUND: ' + ', '.join(failed) if failed else 'ALL CHECKS PASSED - the main script should work'))
    out('Full log: %s' % LOG_FILE)
    _log.close()
    try:
        input('\nPress Enter to close...')
    except (EOFError, KeyboardInterrupt):
        pass
