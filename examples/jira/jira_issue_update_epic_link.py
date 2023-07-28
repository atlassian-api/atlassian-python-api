"""
    Update the Epic Link for issue(s)
"""

from atlassian.jira import Jira

# the Issues which we want to place to a certain EPIC
update_issues = ["ARA-1233", "ARA-1234"]


def main():
    jira = Jira(url="https://jira.example.com/", username="user", password="pass123")
    epic_link_custom_field_id = "customfield_1404"  # Epic Link Custom Field
    target_epic_issue_key = "ARA-1314"
    for issue_key in update_issues:
        jira.update_issue_field(issue_key, fields={epic_link_custom_field_id: target_epic_issue_key})
        print("updated for {}".format(issue_key))
    print("done")


if __name__ == "__main__":
    main()
