import requests


class Atlassian:

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def get(self, path):
        url = "{0}{1}".format(self.url, path)
        return requests.get(url, auth=(self.username, self.password))

    def post(self, path, data):
        url = "{0}{1}".format(self.url, path)
        return requests.post(url, data, auth=(self.username, self.password))

    def delete(self, path):
        url = "{0}{1}".format(self.url, path)
        return requests.delete(url, auth=(self.username, self.password))


from .jira import Jira