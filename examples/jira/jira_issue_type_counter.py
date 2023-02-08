from atlassian import Jira

jira = Jira(url="http://localhost:8080", username="admin", password="admin")

issue_types = jira.get_issue_types()
print("Enter projects category:")
category = input()

for i in issue_types:
    issue_type = i["name"]
    jql_all = 'issuetype = "{0}"'.format(issue_type)
    number = jira.jql(jql_all)["total"]
    jql_of_category = 'issuetype = "{0}" AND category = {1}'.format(issue_type, category)
    number_of_deprecated = jira.jql(jql_of_category)["total"]
    if number > 0:
        percent_of_deprecated = number_of_deprecated / number * 100
    else:
        percent_of_deprecated = 0
    percentage = round(percent_of_deprecated, 1)
    print("{0}, {1}, {2}% of {3}".format(issue_type, number, percentage, category))
