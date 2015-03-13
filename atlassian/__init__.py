import json
import logging
import requests

log = logging.getLogger("atlassian")


class AtlassianRestAPI:

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def log_curl_debug(self, method, path, headers={}, data=None, level=logging.DEBUG):
        message = "curl --silent -X {method} -u '{username}':'{password}' -H {headers} {data} '{url}'".format(
            method=method,
            username=self.username,
            password=self.password,
            headers=' -H '.join(["'{0}: {1}'".format(key, value) for key, value in headers.items()]),
            data='' if not data else "--data '{0}'".format(json.dumps(data)),
            url='{0}{1}'.format(self.url, path))
        log.log(level=level, msg=message)

    def request(self, method='GET', path='/',
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, data=None):
        self.log_curl_debug(method, path, headers, data)
        response = requests.request(
            method=method,
            url='{0}{1}'.format(self.url, path),
            headers=headers,
            data=json.dumps(data),
            auth=(self.username, self.password),
            timeout=60)
        if response.status_code != 200:
            self.log_curl_debug(method, path, headers, data, level=logging.WARNING)
            log.warning(response.json())
            response.raise_for_status()
        else:
            log.debug('Received: {0}'.format(response.json()))
        return response

    def get(self, path, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}):
        return self.request('GET', path, headers).json()

    def post(self, path, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, data=None):
        return self.request('POST', path, headers, data).json()

    def put(self, path, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, data=None):
        return self.request('PUT', path, headers, data).json()

    def delete(self, path, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}):
        return self.request('DELETE', path, headers).json()


from .confluence import Confluence
from .jira import Jira
from .stash import Stash
from .portfolio import Portfolio

__all__ = ['Confluence', 'Jira', 'Stash', 'Portfolio']
