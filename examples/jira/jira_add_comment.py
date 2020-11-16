# coding=utf-8
from atlassian import Jira

""" How to add comment"""

jira = Jira(url="https://jira.example.com/", username="gonchik.tsymzhitov", password="admin")

jira.issue_add_comment("TST-11098", "test rest api request")
