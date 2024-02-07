# coding=utf-8
from atlassian import Jira

""" Examples of updating a issue using operations """

jira = Jira(url="https://jira.example.com/", username="admin", password="password")

""" Adding a labels """

labels = ["example", "atlassian"]

fields = {"labels": [{"add": label} for label in labels]}

jira.edit_issue(issue_id_or_key="ABC-123", fields=fields)

""" Adding a labels and removing another """

add_labels = ["team", "jira"]
remove_labels = ["example", "atlassian"]

fields = {"labels": [{"add": label} for label in add_labels] + [{"remove": label} for label in remove_labels]}

jira.edit_issue(issue_id_or_key="ABC-123", fields=fields)

""" Setting the assignee """

fields = {"assignee": [{"set": {"name": "bob"}}]}

jira.edit_issue(issue_id_or_key="ABC-123", fields=fields)


""" Setting the assignee without notification """

fields = {"assignee": [{"set": {"name": "alice"}}]}

jira.edit_issue(issue_id_or_key="ABC-123", fields=fields, notify_users=False)

""" Manipulating multiple fields """

fields = {"assignee": [{"set": {"name": "bob"}}], "summary": [{"set": "new summary"}], "labels": [{"add": "blog"}]}

jira.edit_issue(issue_id_or_key="ABC-123", fields=fields)
