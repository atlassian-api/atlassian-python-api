#!/usr/bin/env python3

from pprint import pprint
from time import sleep
from atlassian import Jira


jira = Jira(
    url="http://localhost:8080/",
    username="jira-administrator",
    password="admin")

jira.reindex()


while not jira.reindex_status()['success']:
    print('Still reindexing...')
    sleep(1)

pprint('Done.')
