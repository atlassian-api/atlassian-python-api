from atlassian import Jira

jira = Jira(url="http://localhost:8080", username="admin", password="admin")

issue_types = jira.get_issue_types()
print("Enter projects category:")
category = eval(input())

for i in issue_types:
    issue_type = i["name"]
    jql_all = f'issuetype = "{issue_type}"'
    number = jira.jql(jql_all)["total"]
    jql_of_category = f'issuetype = "{issue_type}" AND category = {category}'
    number_of_deprecated = jira.jql(jql_of_category)["total"]
    if number > 0:
        percent_of_deprecated = number_of_deprecated / number * 100
    else:
        percent_of_deprecated = 0
    percentage = round(percent_of_deprecated, 1)
    print(f"{issue_type}, {number}, {percentage}% of {category}")
