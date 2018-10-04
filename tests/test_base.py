# coding: utf8
from atlassian import Jira, Confluence, Bitbucket, Portfolio, Bamboo, Crowd, ServiceDesk
import os


BAMBOO_URL = os.environ.get('BAMBOO_URL', 'http://localhost:8085')
JIRA_URL = os.environ.get('BAMBOO_URL', 'http://localhost:8080')
CONFLUENCE_URL = os.environ.get('BAMBOO_URL', 'http://localhost:8090')
STASH_URL = os.environ.get('BAMBOO_URL', 'http://localhost:7990')
SERVICE_DESK_URL = os.environ.get('SERVICE_DESK_URL', 'http://localhost:8080')

CROWD_URL = os.environ.get('CROWD_URL', 'http://localhost:8095/crowd')
CROWD_APPLICATION = os.environ.get('CROWD_APPLICATION', 'bamboo')
CROWD_APPLICATION_PASSWORD = os.environ.get('CROWD_APPLICATION_PASSWORD', 'admin')

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

    def test_init_bitbucket(self):
        bitbucket = Bitbucket(
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

    def test_init_crowd(self):
        crowd = Crowd(
            url=CROWD_URL,
            username=CROWD_APPLICATION,
            password=CROWD_APPLICATION_PASSWORD)

    def test_init_service_desk(self):
        service_desk = ServiceDesk(
            url=SERVICE_DESK_URL,
            username=ATLASSIAN_USER,
            password=ATLASSIAN_PASSWORD
        )
