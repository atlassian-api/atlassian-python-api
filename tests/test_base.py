# coding: utf8
import os

from atlassian import Jira, Confluence, Bitbucket, Bamboo, Crowd, ServiceDesk, Xray

BAMBOO_URL = os.environ.get("BAMBOO_URL", "http://localhost:8085")
JIRA_URL = os.environ.get("BAMBOO_URL", "http://localhost:8080")
CONFLUENCE_URL = os.environ.get("BAMBOO_URL", "http://localhost:8090")
STASH_URL = os.environ.get("BAMBOO_URL", "http://localhost:7990")
SERVICE_DESK_URL = os.environ.get("SERVICE_DESK_URL", "http://localhost:8080")
XRAY_URL = os.environ.get("XRAY_URL", "http://localhost:8080")

CROWD_URL = os.environ.get("CROWD_URL", "http://localhost:8095/crowd")
CROWD_APPLICATION = os.environ.get("CROWD_APPLICATION", "bamboo")
CROWD_APPLICATION_PASSWORD = os.environ.get("CROWD_APPLICATION_PASSWORD", "admin")

ATLASSIAN_USER = os.environ.get("ATLASSIAN_USER", "admin")
ATLASSIAN_PASSWORD = os.environ.get("ATLASSIAN_PASSWORD", "admin")


class TestBasic:
    def test_init_jira(self):
        Jira(url=JIRA_URL, username=ATLASSIAN_USER, password=ATLASSIAN_PASSWORD)

    def test_init_confluence(self):
        Confluence(url=CONFLUENCE_URL, username=ATLASSIAN_USER, password=ATLASSIAN_PASSWORD)

    def test_init_bitbucket(self):
        Bitbucket(url=STASH_URL, username=ATLASSIAN_USER, password=ATLASSIAN_PASSWORD)

    def test_init_bamboo(self):
        Bamboo(url=BAMBOO_URL, username=ATLASSIAN_USER, password=ATLASSIAN_PASSWORD)

    def test_init_crowd(self):
        Crowd(
            url=CROWD_URL,
            username=CROWD_APPLICATION,
            password=CROWD_APPLICATION_PASSWORD,
        )

    def test_init_service_desk(self):
        ServiceDesk(url=SERVICE_DESK_URL, username=ATLASSIAN_USER, password=ATLASSIAN_PASSWORD)

    def test_init_xray(self):
        Xray(url=XRAY_URL, username=ATLASSIAN_USER, password=ATLASSIAN_PASSWORD)
