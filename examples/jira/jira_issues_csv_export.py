# coding=utf-8
"""Jira issues export to CSV - all or current.
default is ALL
below example uses the current fields
"""

from atlassian import Jira


def main():
    jira = Jira("http://localhost:8080", username="admin", password="admin")
    csv_issues = jira.csv(
        jql='project = "APA" and "Epic Link" = APA-3 ORDER BY created DESC',
        all_fields=False,
    )
    with open("data.csv", "wb") as file_obj:
        file_obj.write(csv_issues)


if __name__ == "__main__":
    main()
