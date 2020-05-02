# coding=utf-8
import json
import logging

import requests
from oauthlib.oauth1 import SIGNATURE_RSA
from requests_oauthlib import OAuth1
from six.moves.urllib.parse import urlencode

from atlassian.request_utils import get_default_logger

log = get_default_logger(__name__)


class AtlassianRestAPI(object):
    default_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    experimental_headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                            'X-ExperimentalApi': 'opt-in'}
    form_token_headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                          'X-Atlassian-Token': 'no-check'}
    no_check_headers = {'X-Atlassian-Token': 'no-check'}
    response = None

    def __init__(self, url, username=None, password=None, timeout=60, api_root='rest/api', api_version='latest',
                 verify_ssl=True, session=None, oauth=None, cookies=None, advanced_mode=None, kerberos=None,
                 cloud=False, proxies=None):
        if ('atlassian.net' in url or 'jira.com' in url) \
                and '/wiki' not in url \
                and self.__class__.__name__ in 'Confluence':
            url = self.url_joiner(url, '/wiki')
        self.url = url
        self.username = username
        self.password = password
        self.timeout = int(timeout)
        self.verify_ssl = verify_ssl
        self.api_root = api_root
        self.api_version = api_version
        self.cookies = cookies
        self.advanced_mode = advanced_mode
        self.cloud = cloud
        self.proxies = proxies
        if session is None:
            self._session = requests.Session()
        else:
            self._session = session
        if username and password:
            self._create_basic_session(username, password)
        elif oauth is not None:
            self._create_oauth_session(oauth)
        elif kerberos is not None:
            self._create_kerberos_session(kerberos)
        elif cookies is not None:
            self._session.cookies.update(cookies)

    def _create_basic_session(self, username, password):
        self._session.auth = (username, password)

    def _create_kerberos_session(self, kerberos_service):
        try:
            import kerberos as kerb
        except ImportError as e:
            log.debug(e)
            try:
                import kerberos_sspi as kerb
            except ImportError:
                raise ImportError("No kerberos implementation available")
        __, krb_context = kerb.authGSSClientInit(kerberos_service)
        kerb.authGSSClientStep(krb_context, "")
        auth_header = ("Negotiate " + kerb.authGSSClientResponse(krb_context))
        self._update_header("Authorization", auth_header)
        response = self._session.get(self.url, verify=self.verify_ssl)
        response.raise_for_status()

    def _create_oauth_session(self, oauth_dict):
        oauth = OAuth1(oauth_dict['consumer_key'],
                       rsa_key=oauth_dict['key_cert'], signature_method=SIGNATURE_RSA,
                       resource_owner_key=oauth_dict['access_token'],
                       resource_owner_secret=oauth_dict['access_token_secret'])
        self._session.auth = oauth

    def _update_header(self, key, value):
        """
        Update header for exist session
        :param key:
        :param value:
        :return:
        """
        self._session.headers.update({key: value})

    def log_curl_debug(self, method, url, data=None, headers=None, level=logging.DEBUG):
        """

        :param method:
        :param url:
        :param data:
        :param headers:
        :param level:
        :return:
        """
        headers = headers or self.default_headers
        message = "curl --silent -X {method} -H {headers} {data} '{url}'".format(
            method=method,
            headers=' -H '.join(["'{0}: {1}'".format(key, value) for key, value in headers.items()]),
            data='' if not data else "--data '{0}'".format(json.dumps(data)),
            url=url)
        log.log(level=level, msg=message)

    def resource_url(self, resource):
        return '/'.join([self.api_root, self.api_version, resource])

    @staticmethod
    def url_joiner(url, path, trailing=None):
        url_link = '/'.join(s.strip('/') for s in [url, path])
        if trailing:
            url_link += '/'
        return url_link

    def request(self, method='GET', path='/', data=None, flags=None, params=None, headers=None,
                files=None, trailing=None):
        """

        :param method:
        :param path:
        :param data:
        :param flags:
        :param params:
        :param headers:
        :param files:
        :param trailing: bool
        :return:
        """
        url = self.url_joiner(self.url, path, trailing)
        if params or flags:
            url += '?'
        if params:
            url += urlencode(params or {})
        if flags:
            url += ('&' if params else '') + '&'.join(flags or [])
        if files is None:
            data = None if not data else json.dumps(data)
        self.log_curl_debug(method=method, url=url, headers=headers,
                            data=data)

        headers = headers or self.default_headers
        response = self._session.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            timeout=self.timeout,
            verify=self.verify_ssl,
            files=files,
            proxies=self.proxies
        )
        response.encoding = 'utf-8'

        if self.advanced_mode:
            return response

        log.debug("HTTP: {} {} -> {} {}".format(method, path, response.status_code, response.reason))
        response.raise_for_status()
        return response

    def get(self, path, data=None, flags=None, params=None, headers=None, not_json_response=None, trailing=None):
        """
        Get request based on the python-requests module. You can override headers, and also, get not json response
        :param path:
        :param data:
        :param flags:
        :param params:
        :param headers:
        :param not_json_response: OPTIONAL: For get content from raw requests packet
        :param trailing: OPTIONAL: for wrap slash symbol in the end of string
        :return:
        """
        response = self.request('GET', path=path, flags=flags, params=params, data=data, headers=headers,
                                trailing=trailing)
        if self.advanced_mode:
            return response
        if not_json_response:
            return response.content
        else:
            if not response.text:
                return None
            try:
                return response.json()
            except Exception as e:
                log.error(e)
                return response.text

    def post(self, path, data=None, headers=None, files=None, params=None, trailing=None):
        response = self.request('POST', path=path, data=data, headers=headers, files=files, params=params,
                                trailing=trailing)
        if self.advanced_mode:
            return response
        try:
            return response.json()
        except ValueError:
            log.debug('Received response with no content')
            return None

    def put(self, path, data=None, headers=None, files=None, trailing=None, params=None):
        response = self.request('PUT', path=path, data=data, headers=headers, files=files, params=params,
                                trailing=trailing)
        if self.advanced_mode:
            return response
        try:
            return response.json()
        except ValueError:
            log.debug('Received response with no content')
            return None

    def delete(self, path, data=None, headers=None, params=None, trailing=None):
        """
        Deletes resources at given paths.
        :rtype: dict
        :return: Empty dictionary to have consistent interface.
        Some of Atlassian REST resources don't return any content.
        """
        response = self.request('DELETE', path=path, data=data, headers=headers, params=params, trailing=trailing)
        if self.advanced_mode:
            return response
        try:
            return response.json()
        except ValueError:
            log.debug('Received response with no content')
            return None
