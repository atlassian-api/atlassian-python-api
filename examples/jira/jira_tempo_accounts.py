# coding=utf-8
from atlassian import Jira

jira = Jira(url="http://localhost:8080", username="admin", password="admin")

accounts = jira.tempo_account_get_accounts_by_jira_project(project_id="10140")
for account in accounts:
    print(account)
    jira.tempo_account_associate_with_jira_project(account["id"], project_id="10210")
