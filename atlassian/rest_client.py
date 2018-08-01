# coding: utf8
import json
import logging
from six.moves.urllib.parse import urlencode
from six.moves.urllib.parse import urljoin
import requests

log = logging.getLogger('atlassian')


class AtlassianRestAPI(object):
    default_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def __init__(self, url, username, password, timeout=60, api_root='rest/api', api_version='latest', verify_ssl=True):
        self.url = url
        self.username = username
        self.password = password
        self.timeout = int(timeout)
        self.verify_ssl = verify_ssl
        self.api_root = api_root
        self.api_version = api_version
        self._session = requests.Session()
        if username and password:
            self._session.auth = (username, password)

    def log_curl_debug(self, method, path, data=None, headers=None, level=logging.DEBUG):
        headers = headers or self.default_headers
        message = "curl --silent -X {method} -u '{username}':'{password}' -H {headers} {data} '{url}'".format(
            method=method,
            username=self.username,
            password=self.password,
            headers=' -H '.join(["'{0}: {1}'".format(key, value) for key, value in headers.items()]),
            data='' if not data else "--data '{0}'".format(json.dumps(data)),
            url='{0}{1}'.format(self.url, path))
        log.log(level=level, msg=message)

    def resource_url(self, resource):
        return '/'.join([self.api_root, self.api_version, resource])

    def request(self, method='GET', path='/', data=None, flags=None, params=None, headers=None, files=None):
        self.log_curl_debug(method=method, path=path, headers=headers, data=data)
        url = urljoin(self.url, path)
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
        if response.status_code == 200:
            log.debug('Received: {0}\n {1}'.format(response.status_code, response.json()))
        elif response.status_code == 204:
            log.debug('Received: {0}\n "No Content" response'.format(response.status_code))
        elif response.status_code == 404:
            log.error('Received: {0}\n Not Found'.format(response.status_code))
        else:
            log.debug('Received: {0}\n {1}'.format(response.status_code, response))
            self.log_curl_debug(method=method, path=path, headers=headers, data=data, level=logging.DEBUG)
            try:
                log.error(response.json())
            except ValueError:
                log.error(response)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                log.error("HTTP Error occurred")
                log.error('Response is: {content}'.format(content=err.response.content))
        return response

    def get(self, path, data=None, flags=None, params=None, headers=None):
        return self.request('GET', path=path, flags=flags, params=params, data=data, headers=headers).json()

    def post(self, path, data=None, headers=None, files=None):
        try:
            return self.request('POST', path=path, data=data, headers=headers, files=files).json()
        except ValueError:
            log.debug('Received response with no content')
            return None

    def put(self, path, data=None, headers=None, files=None):
        try:
            return self.request('PUT', path=path, data=data, headers=headers, files=files).json()
        except ValueError:
            log.debug('Received response with no content')
            return None

    def delete(self, path, data=None, headers=None):
        """
        Deletes resources at given paths.
        :rtype: dict
        :return: Empty dictionary to have consistent interface.
        Some of Atlassian REST resources don't return any content.
        """
        self.request('DELETE', path=path, data=data, headers=headers)
