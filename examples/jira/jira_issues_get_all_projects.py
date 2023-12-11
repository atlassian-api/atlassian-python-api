# coding=utf-8
"""
    Getting Project Issue(s) example
"""

from atlassian import Jira

jira = Jira(url="https://jirasite.co", username="ocean", password="seariver")

if __name__ == "__main__":
    # default will return 50 issues in ascending order
    project_issues_default_50 = jira.get_all_project_issues(project="APA")
    # We can increase the limit by specifying the limit
    project_issues_100 = jira.get_all_project_issues(project="APA", limit=100)
    # Specifying specific fields other than the default jira fields returned
    project_issues_specific = jira.get_all_project_issues(project="APA", fields=["description", "summary"], limit=100)
