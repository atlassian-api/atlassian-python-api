from atlassian import Jira

# Issues can be 1 or more
issues_lst = ["APA-1", "APA-2"]
sprint_id = 103

jira = Jira(url="http://localhost:8080", username="admin", password="admin")

resp = jira.add_issues_to_sprint(sprint_id=sprint_id, issues=issues_lst)
