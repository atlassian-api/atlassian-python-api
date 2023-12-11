# coding=utf-8

from six.moves.urllib.parse import quote

from atlassian import Jira

jira = Jira(url="http://localhost:8080", username="admin", password="admin")

EMAIL_SUBJECT = quote("Jira access to project {project_key}")
EMAIL_BODY = quote(
    """I am asking for access to the {project_key} project in Jira.

To give me the appropriate permissions, assign me to a role on the page:
http://localhost:8080/plugins/servlet/project-config/{project_key}/roles

Role:
Users - read-only access + commenting
Developers - work on tasks, editing, etc.
Admin - Change of configuration and the possibility of starting sprints"""
)

MAILTO = '<a href="mailto:{lead_email}?subject={email_subject}&body={email_body}">{lead_name}</a>'

print("|| Project Key || Project Name || Ask for Access ||")

for project in jira.project_leaders():
    print(
        "| {project_key} | {project_name} | {lead_email_link} |".format(
            project_key=project["project_key"],
            project_name=project["project_name"],
            lead_email_link=MAILTO.format(lead_name=project["lead_name"], lead_email=project["lead_email"]),
        )
    )
