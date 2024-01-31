from atlassian import Jira

# This feature can be useful if you need to scrap some data from issue description or comments.
jira = Jira(url="http://localhost:8080", username="admin", password="admin")
regex = r"((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\[?\.\]?){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"  # regex for ipv4 address + ipv4 with [.] instead of dot
issue = "TEST-1"  # id of the jira issue
result = jira.scrap_regex_from_issue(issue, regex)
# scrap_regex_from_issue will return results of positive regexes matches from issue description and issue comments.
