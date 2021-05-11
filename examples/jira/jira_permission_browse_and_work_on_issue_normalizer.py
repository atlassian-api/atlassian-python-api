# coding: utf8
from atlassian import Jira

"""
    That example use for normalizing the permission schemes between
    BROWSE_PROJECTS and WORK_ON_ISSUES parameters
"""

""" Login part"""

jira = Jira(url="JIRA_URL", username="ATLASSIAN_LOGIN", password="ATLASSIAN_PASSWORD")

"""Get all permission schemes ID's"""

permission_schemes = jira.get_all_permissionschemes()
scheme_id_list = []
for item in permission_schemes:
    # Get id's (except default)
    if item.get("id") != 0:
        scheme_id_list.append(item.get("id"))

"""Make a func for checking permissions matching"""


def check_if_permissions_match(permission_id):
    browse_projects = []
    work_on_issues = []

    scheme = jira.get_permissionscheme(permission_id, expand="permissions")

    for permission in scheme["permissions"]:
        permission["holder"].pop("expand", None)
        if permission["permission"] == "WORK_ON_ISSUES":
            work_on_issues.append(permission["holder"])
        elif permission["permission"] == "BROWSE_PROJECTS":
            browse_projects.append(permission["holder"])
    if browse_projects == work_on_issues:
        missing_permissions = False
    elif not work_on_issues:
        missing_permissions = browse_projects
    else:
        missing_permissions = []
        for parameter in browse_projects:
            if parameter in work_on_issues:
                pass
            else:
                missing_permissions.append(parameter)
    return missing_permissions


evaluate_flag = True
for id in scheme_id_list:
    result = check_if_permissions_match(id)
    print(result)
    if result and evaluate_flag:
        for item in result:
            grant = dict(holder=item, permission="WORK_ON_ISSUES")
            jira.set_permissionscheme_grant(id, grant)
