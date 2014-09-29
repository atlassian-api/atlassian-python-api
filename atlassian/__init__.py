import json
import requests


class Atlassian:

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def get(self, path, headers={"Content-Type": "application/json", "Accept": "application/json"}):
        url = "{0}{1}".format(self.url, path)
        return requests.get(url, headers=headers, auth=(self.username, self.password), timeout=60)

    def post(self, path, data=None, headers={"Content-Type": "application/json", "Accept": "application/json"}):
        url = "{0}{1}".format(self.url, path)
        return requests.post(url, json.dumps(data), headers=headers, auth=(self.username, self.password))

    def delete(self, path, headers={"Content-Type": "application/json", "Accept": "application/json"}):
        url = "{0}{1}".format(self.url, path)
        return requests.delete(url, headers=headers, auth=(self.username, self.password))


from .confluence import Confluence
from .jira import Jira