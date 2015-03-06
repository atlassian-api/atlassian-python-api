from pprint import pprint
from atlassian import Jira


jira = Jira(
    url="http://localhost:8080",
    username="admin",
    password="admin")

data = jira.rename_sprint(
    sprint_id=195,
    name="2014-10 week 3 - Tools",
    start_date="2014-10-13 11:44",
    end_date="2014-10-20 09:34")

pprint(data)
