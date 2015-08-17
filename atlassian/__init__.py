import json
import logging
import requests

log = logging.getLogger("atlassian")


class AtlassianRestAPI:

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def log_curl_debug(self, method, path, data=None, headers={}, level=logging.DEBUG):
        message = "curl --silent -X {method} -u '{username}':'{password}' -H {headers} {data} '{url}'".format(
            method=method,
            username=self.username,
            password=self.password,
            headers=' -H '.join(["'{0}: {1}'".format(key, value) for key, value in headers.items()]),
            data='' if not data else "--data '{0}'".format(json.dumps(data)),
            url='{0}{1}'.format(self.url, path))
        log.log(level=level, msg=message)

    def request(self, method='GET', path='/', data=None,
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'}):
        self.log_curl_debug(method=method, path=path, headers=headers, data=data)
        response = requests.request(
            method=method,
            url='{0}{1}'.format(self.url, path),
            headers=headers,
            data=json.dumps(data),
            auth=(self.username, self.password),
            timeout=60)
        if response.status_code == 200:
            log.debug('Received: {0}'.format(response.json()))
        elif response.status_code == 204:
            log.debug('Received "204 No Content" response')
        else:
            self.log_curl_debug(method=method, path=path, headers=headers, data=data, level=logging.DEBUG)
            log.info(response.json())
            response.raise_for_status()
        return response

    def get(self, path, data=None, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}):
        return self.request('GET', path=path, data=data, headers=headers).json()

    def post(self, path, data=None, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}):
        try:
            return self.request('POST', path=path, data=data, headers=headers).json()
        except ValueError:
            log.debug('Received response with no content')
            return None

    def put(self, path, data=None, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}):
        try:
            return self.request('PUT', path=path, data=data, headers=headers).json()
        except ValueError:
            log.debug('Received response with no content')
            return None

    def delete(self, path, data=None, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}):
        return self.request('DELETE', path=path, data=data, headers=headers).json()


from .confluence import Confluence
from .jira import Jira
from .stash import Stash
from .portfolio import Portfolio

__all__ = ['Confluence', 'Jira', 'Stash', 'Portfolio']
