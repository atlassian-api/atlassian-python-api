# coding=utf-8
from atlassian import Jira
from pprint import pprint

""" How to get server info with health check"""

jira = Jira(
    url="https://jira.example.com/",
    username='admin',
    password='*******')

pprint(jira.get_server_info(True))
