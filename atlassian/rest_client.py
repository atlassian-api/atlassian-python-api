# coding: utf8
import json
import logging
from six.moves.urllib.parse import urlencode
import requests

log = logging.getLogger(__name__)


class AtlassianRestAPI(object):
    default_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    experimental_headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                            'X-ExperimentalApi': 'opt-in'}
    form_token_headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                          'X-Atlassian-Token': 'no-check'}

    def __init__(self, url, username, password, timeout=60, api_root='rest/api', api_version='latest', verify_ssl=True,
                 session=None):
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
            self._session.auth = (username, password)

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
        message = "curl --silent -X {method} -u '{username}':'********' -H {headers} {data} '{url}'".format(
            method=method,
            username=self.username,
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

    def request(self, method='GET', path='/', data=None, flags=None, params=None, headers=None, files=None,
                trailing=None):
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
            auth=(self.username, self.password),
            timeout=self.timeout,
            verify=self.verify_ssl,
            files=files
        )
        try:
            if response.text:
                response_content = response.json()
            else:
                response_content = response.content
        except ValueError:
            response_content = response.content
        if response.status_code == 200:
            log.debug('Received: {0}\n {1}'.format(response.status_code, response_content))
        elif response.status_code == 201:
            log.debug('Received: {0}\n "Created" response'.format(response.status_code))
        elif response.status_code == 204:
            log.debug('Received: {0}\n "No Content" response'.format(response.status_code))
        elif response.status_code == 401:
            log.error('Received: {0}\n "UNAUTHORIZED" response'.format(response.status_code))
        elif response.status_code == 404:
            log.error('Received: {0}\n Not Found'.format(response.status_code))
        else:
            log.debug('Received: {0}\n {1}'.format(response.status_code, response))
            self.log_curl_debug(method=method, path=path, headers=headers, data=data, level=logging.DEBUG)
            log.error(response_content)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                log.error("HTTP Error occurred")
                log.error('Response is: {content}'.format(content=err.response.content))
        return response

    def get(self, path, data=None, flags=None, params=None, headers=None, not_json_response=None):
        """
        Get request based on the python-requests module. You can override headers, and also, get not json response
        :param path:
        :param data:
        :param flags:
        :param params:
        :param headers:
        :param not_json_response: OPTIONAL: For get content from raw requests packet
        :return:
        """
        answer = self.request('GET', path=path, flags=flags, params=params, data=data, headers=headers)
        if not_json_response:
            return answer.content
        else:
            try:
                return answer.json()
            except Exception as e:
                log.error(e)
                return

    def post(self, path, data=None, headers=None, files=None, params=None):
        try:
            return self.request('POST', path=path, data=data, headers=headers, files=files, params=params).json()
        except ValueError:
            log.debug('Received response with no content')
            return None

    def put(self, path, data=None, headers=None, files=None):
        try:
            return self.request('PUT', path=path, data=data, headers=headers, files=files).json()
        except ValueError:
            log.debug('Received response with no content')
            return None

    def delete(self, path, data=None, headers=None, params=None):
        """
        Deletes resources at given paths.
        :rtype: dict
        :return: Empty dictionary to have consistent interface.
        Some of Atlassian REST resources don't return any content.
        """
        self.request('DELETE', path=path, data=data, headers=headers, params=params)
