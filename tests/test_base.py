from atlassian import Jira, Confluence, Stash, Portfolio, Bamboo
import os


BAMBOO_URL = os.environ.get('BAMBOO_URL', 'http://localhost:8085')
JIRA_URL = os.environ.get('BAMBOO_URL', 'http://localhost:8080')
CONFLUENCE_URL = os.environ.get('BAMBOO_URL', 'http://localhost:8090')
STASH_URL = os.environ.get('BAMBOO_URL', 'http://localhost:7990')

ATLASSIAN_USER = os.environ.get('ATLASSIAN_USER', 'admin')
ATLASSIAN_PASSWORD = os.environ.get('ATLASSIAN_PASSWORD', 'admin')


class TestBasic(object):

    def test_init_jira(self):
        jira = Jira(
            url=JIRA_URL,
            username=ATLASSIAN_USER,
            password=ATLASSIAN_PASSWORD
        )

    def test_init_confluence(self):
        confluence = Confluence(
            url=CONFLUENCE_URL,
            username=ATLASSIAN_USER,
            password=ATLASSIAN_PASSWORD
        )

    def test_init_stash(self):
        stash = Stash(
            url=STASH_URL,
            username=ATLASSIAN_USER,
            password=ATLASSIAN_PASSWORD
        )

    def test_init_bamboo(self):
        bamboo = Bamboo(
            url=BAMBOO_URL,
            username=ATLASSIAN_USER,
            password=ATLASSIAN_PASSWORD
        )


