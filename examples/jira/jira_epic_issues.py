# coding=utf-8
from atlassian import Jira

jira = Jira(url="http://localhost:8080", username="admin", password="admin")

data = jira.epic_issues("ABC-123")
print(data)
