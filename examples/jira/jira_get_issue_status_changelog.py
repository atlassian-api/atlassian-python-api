from atlassian import Jira

jira_cloud = Jira(url="<url>", username="username", password="password")
jira_dc = Jira(url="url", token="<token>>")

# example use
jira_cloud.get_issue_status_changelog("TEST-1")
# example output:
# [{'from': 'Closed', 'to': 'In Progress', 'date': '2024-03-17T17:22:29.524-0500'}, {'from': 'In Progress', 'to': 'Closed', 'date': '2024-03-17T14:33:07.317-0500'}, {'from': 'In Progress', 'to': 'In Progress', 'date': '2024-03-16T09:25:52.033-0500'}, {'from': 'To Do', 'to': 'In Progress', 'date': '2024-03-14T19:25:02.511-0500'}]
