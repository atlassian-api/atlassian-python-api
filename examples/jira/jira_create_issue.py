# coding=utf-8
from atlassian import Jira

jira = Jira(url="https://jira.example.com/", username="gonchik.tsymzhitov", password="admin")

jira.issue_create(
    fields={
        "project": {"key": "TEST"},
        "issuetype": {"name": "Task"},
        "summary": "test rest",
        "description": "rest rest",
    }
)
