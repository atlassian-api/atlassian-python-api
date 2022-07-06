# coding=utf-8
from atlassian import Jira

jira = Jira(url="http://localhost:8080", username="admin", password="admin")

data = jira.issue("ABC-123")
print(data)
