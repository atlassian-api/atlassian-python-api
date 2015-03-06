import json
import logging
import requests


logging.basicConfig(level=logging.INFO, format="[%(asctime).19s] [%(levelname)s] %(message)s")
logging.getLogger("requests").setLevel(logging.WARNING)
log = logging.getLogger("atlassian")


class AtlassianRestAPI:

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def log_curl_debug(self, method, path, headers={}, data=None):
        command = "curl --silent -X {method} -u '{username}':'{password}' -H {headers} {data} '{url}'".format(
            method=method,
            username=self.username,
            password=self.password,
            headers=' -H '.join(["'{0}: {1}'".format(key, value) for key, value in headers.items()]),
            data='' if not data else "--data '{0}'".format(json.dumps(data)),
            url='{0}{1}'.format(self.url, path))
        log.debug(command)

    def request(self, method='GET', path='/', headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, data=None):
        self.log_curl_debug(method, path, headers, data)
        response = requests.request(
            method=method,
            url='{0}{1}'.format(self.url, path),
            headers=headers,
            data=json.dumps(data),
            auth=(self.username, self.password),
            timeout=60)
        response.raise_for_status()
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