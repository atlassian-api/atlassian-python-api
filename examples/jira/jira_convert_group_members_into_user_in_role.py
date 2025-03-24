import logging

from atlassian import Jira

logging.basicConfig(level=logging.ERROR)

jira = Jira(url="http://localhost:8080", username="admin", password="admin")

"""That example show how to copy group members into role members"""


def convert_group_into_users_in_role(project_key, role_id, group_name):
    users = jira.get_all_users_from_group(group=group_name, limit=1000).get("values")
    for user in users:
        jira.add_user_into_project_role(project_key=project_key, role_id=role_id, user_name=user.get("name"))
        print(f"{user.get('name')} added into role_id  {role_id} in {project_key}")


group_name_to_find = "old-developers"
roles = jira.get_all_global_project_roles()
projects = jira.get_all_projects(included_archived=True)
for project in projects:
    for role in roles:
        members_of_role = jira.get_project_actors_for_role_project(project.get("key"), role.get("id"))
        if not members_of_role:
            continue
        for member in members_of_role:
            if member.get("type") == "atlassian-group-role-actor":
                if member.get("name") == group_name_to_find:
                    print(f"{project.get('key')} has {role.get('name')}")
                    convert_group_into_users_in_role(project.get("key"), role.get("id"), group_name_to_find)
