""" Example: Get Comments on a Jira Issue
"""
# coding=utf-8
from atlassian import Jira


def main():
    jira = Jira(url="https://atlassian-python.atlassian.net/", username="martyn.bristow@gmail.com", password="...")

    print("\n*Get Comments on INT-1*")
    comments = jira.issue_get_comments("INT-1")
    print(comments)

    print("\n*Get a single comment on INT-1*")
    comments = jira.issue_get_comment(10000, 10001)
    print(comments)

    print("\n*Get a set of comments*")
    comments = jira.issues_get_comments_by_id(10000, 10002)
    print(comments)


if __name__ == "__main__":
    main()
