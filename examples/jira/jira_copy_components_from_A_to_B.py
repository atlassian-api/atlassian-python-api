# coding=utf-8
from atlassian import Jira

jira = Jira(url="http://localhost:8080/", username="jira-administrator", password="admin")

"""That example show how to copy components from one project into another"""

DST_PROJECT = "PROJECT_B"
SRC_PROJECT = "PROJECT_A"
components = jira.get_project_components(SRC_PROJECT)

for component in components:
    data = {
        "project": DST_PROJECT,
        "description": component.get("description"),
        "leadUserName": component.get("leadUserName"),
        "name": component.get("name"),
        "assigneeType": component.get("assigneeType"),
    }
    jira.create_component(data)
    print(f"{component.get('name')} - component created ")
