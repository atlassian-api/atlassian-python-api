# coding=utf-8
from atlassian import Jira

""" How to add comment"""

jira = Jira(url="https://jira.example.com/", username="gonchik.tsymzhitov", password="admin")

jira.issue_add_comment("TST-11098", "test rest api request")

""" How to add comment with link to another comment """

issue_id = "TST-101"
comment_id = "10001"

new_comment_message = (
    f"Answering to [comment #{comment_id}|{jira.url}browse/{issue_id}?focusedCommentId={comment_id}] ..."
)

jira.issue_add_comment(issue_id, new_comment_message)
