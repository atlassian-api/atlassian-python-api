from pprint import pprint
from atlassian import Jira


JQL = "project = DEMO AND status NOT IN (Closed, Resolved) ORDER BY issuekey"

jira = Jira(
    url="http://localhost:8080",
    username="admin",
    password="admin")

data = jira.jql(JQL)
pprint(data)
