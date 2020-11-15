# coding=utf-8
from time import sleep

from atlassian import Jira

jira = Jira(url="http://localhost:8080/", username="jira-administrator", password="admin")

jira.reindex()

while not jira.reindex_status()["success"]:
    print("Still reindexing...")
    sleep(1)

print("Done.")
