# coding=utf-8
from atlassian import Jira

# This example shoes how to copy custom field value from on issue to another
# define custom field id, in notation customfield_id

custom_field_id = "customfield_102589"
source_issue_key = "TST-1"
destination_issue_key = "TST-2"

jira = Jira(url="http://localhost:8080", username="admin", password="admin")

# get value and save
customfield_value = jira.issue_field_value(source_issue_key, custom_field_id)
# prepare data like this https://developer.atlassian.com/server/jira/platform/jira-rest-api-example-edit-issues-6291632
custom_field_preparation = {custom_field_id: customfield_value}
# update custom field on destination issue
jira.update_issue_field(destination_issue_key, custom_field_preparation)
