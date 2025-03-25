# coding=utf-8
"""
Example: Using enhanced JQL search methods in Jira Cloud.

This script demonstrates:
1. Fetching issues using `enhanced_jql` (nextPageToken-based pagination).
2. Getting an approximate issue count with `approximate_issue_count`.
3. Fetching issues using `enhanced_jql_get_list_of_tickets` (legacy startAt pagination for Data Center users).

⚠️ Note: `enhanced_jql` is recommended for Jira Cloud users as it aligns with Atlassian's new search API.
"""

from atlassian import Jira

# Initialize Jira Cloud instance
jira_cloud = Jira(
    cloud=True,
    url="https://your-jira-instance.atlassian.net",
    username="your-email@example.com",
    password="your-api-token",
)

print("========== Fetching Issues Using enhanced_jql ==========")
issues = jira_cloud.enhanced_jql("updated >= -1d ORDER BY updated DESC", limit=20, fields="*nav")
print(issues)

print("========== Getting Approximate Issue Count ==========")
issue_count = jira_cloud.approximate_issue_count("updated >= -1d ORDER BY updated DESC")
print(issue_count)

print("========== Fetching Issues Using enhanced_jql_get_list_of_tickets ==========")
issues_list = jira_cloud.enhanced_jql_get_list_of_tickets(
    "updated >= -1d ORDER BY updated DESC", limit=300, fields="*nav"
)
print(issues_list)

print("========== Done ==========")
