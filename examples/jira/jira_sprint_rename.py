# coding=utf-8
from atlassian import Jira

jira = Jira(url="http://localhost:8080", username="admin", password="admin")

data = jira.rename_sprint(
    sprint_id=10,
    name="Here is the name of my new sprint",
    start_date="2014-10-13 11:44",
    end_date="2014-10-20 09:34",
)

print(data)
