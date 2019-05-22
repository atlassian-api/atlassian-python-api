# coding: utf8
import json
import logging
from six.moves.urllib.parse import urlencode
import requests
from oauthlib.oauth1 import SIGNATURE_RSA
from requests_oauthlib import OAuth1


log = logging.getLogger(__name__)


class AtlassianRestAPI(object):
    default_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    experimental_headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                            'X-ExperimentalApi': 'opt-in'}
    form_token_headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                          'X-Atlassian-Token': 'no-check'}

    def __init__(self, url, username=None, password=None, timeout=60, api_root='rest/api', api_version='latest', verify_ssl=True, session=None, oauth=None):
        self.url = url
        self.username = username
        self.password = password
        self.timeout = int(timeout)
        self.verify_ssl = verify_ssl
        self.api_root = api_root
        self.api_version = api_version
        if session is None:
            self._session = requests.Session()
        else:
            self._session = session
        if username and password:
            self._create_basic_session(username, password)
        elif oauth is not None:
            self._create_oauth_session(oauth, timeout)

    def _create_basic_session(self, username, password):
        self._session.auth = (username, password)

    def _create_oauth_session(self, oauth_dict, timeout=60):
        oauth = OAuth1(oauth_dict['consumer_key'],
                       rsa_key=oauth_dict['key_cert'], signature_method=SIGNATURE_RSA,
                       resource_owner_key=oauth_dict['access_token'],
                       resource_owner_secret=oauth_dict['access_token_secret'])
        self._session.auth = oauth

    def log_curl_debug(self, method, path, data=None, headers=None, trailing=None, level=logging.DEBUG):
        """

        :param method:
        :param path:
        :param data:
        :param headers:
        :param trailing: bool flag for trailing /
        :param level:
        :return:
        """
        headers = headers or self.default_headers
        message = "curl --silent -X {method} -H {headers} {data} '{url}'".format(
            method=method,
            headers=' -H '.join(["'{0}: {1}'".format(key, value) for key, value in headers.items()]),
            data='' if not data else "--data '{0}'".format(json.dumps(data)),
            url='{0}'.format(self.url_joiner(self.url, path=path, trailing=trailing)))
        log.log(level=level, msg=message)

    def resource_url(self, resource):
        return '/'.join([self.api_root, self.api_version, resource])

    @staticmethod
    def url_joiner(url, path, trailing):
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
        self.log_curl_debug(method=method, path=path, headers=headers, data=data, trailing=None)
        url = self.url_joiner(self.url, path, trailing)
        if params or flags:
            url += '?'
        if params:
            url += urlencode(params or {})
        if flags:
            url += ('&' if params else '') + '&'.join(flags or [])
        if files is None:
            data = json.dumps(data)

        headers = headers or self.default_headers
        response = self._session.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            timeout=self.timeout,
            verify=self.verify_ssl,
            files=files
        )
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
        answer = self.request('GET', path=path, flags=flags, params=params, data=data, headers=headers,
                              trailing=trailing)
        if not_json_response:
            return answer.content
        else:
            try:
                return answer.json()
            except Exception as e:
                log.error(e)
                return answer.text

    def post(self, path, data=None, headers=None, files=None, params=None, trailing=None):
        try:
            return self.request('POST', path=path, data=data, headers=headers, files=files,
                                params=params, trailing=trailing)
        except ValueError:
            log.debug('Received response with no content')
            return None

    def put(self, path, data=None, headers=None, files=None, trailing=None):
        try:
            return self.request('PUT', path=path, data=data, headers=headers, files=files, 
                                trailing=trailing)
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
        self.request('DELETE', path=path, data=data, headers=headers, params=params, trailing=trailing)
