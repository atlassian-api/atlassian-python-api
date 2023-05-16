# coding=utf-8
from atlassian import Jira

# This example shoes how to add another value to the Labels field
# without losing the previously defined ones already defined

issue_key = "TST-1"
new_tag = "label_to_add_for_test"
jira = Jira(url="http://localhost:8080", username="admin", password="admin")


def jira_add_label(issue_key, new_tag):
    field_name = "labels"
    # get value and save
    field_value = jira.issue_field_value(issue_key, field_name)
    field_value.append(new_tag)
    # prepare data like this
    # https://developer.atlassian.com/server/jira/platform/jira-rest-api-example-edit-issues-6291632
    field_preparation = {field_name: field_value}
    # update custom field on destination issue
    jira.update_issue_field(issue_key, field_preparation)


jira_add_label(issue_key, new_tag)
