# coding=utf-8
import argparse
import logging
from os import environ

from atlassian import Jira


def get_project_category_object(project_category_name="DEPRECATED"):
    categories = jira.get_all_project_categories()
    for category in categories:
        if category.get("name") == project_category_name:
            return category
    return None


def get_project_permission_scheme_object(new_scheme="w Archive Permission Scheme"):
    permission_schemes = jira.get_all_permissionschemes()
    for permission_scheme in permission_schemes:
        if permission_scheme.get("name") == new_scheme:
            return permission_scheme
    return None


def get_project_notification_scheme_object(new_scheme="Archived Notification Scheme"):
    schemes = jira.get_all_notification_schemes()
    for scheme in schemes:
        if scheme.get("name") == new_scheme:
            return scheme
    return None


if __name__ == "__main__":
    jira = Jira(
        url=environ.get("JIRA_URL"),
        username=environ.get("ATLASSIAN_USER"),
        password=environ.get("ATLASSIAN_PASSWORD"),
    )
    # Setting the logging level. INFO|ERROR|DEBUG are the most common.
    logging.basicConfig(level=logging.INFO)
    # Initialize argparse module with some program name and additional information
    parser = argparse.ArgumentParser(prog="Jira Archive Projects", description="Simple execution of th project key")
    parser.add_argument("--project", dest="project", default="TEST", help="Jira project key")
    parser.add_argument("--category", dest="category", default="DEPRECATED", help="Project category")
    parser.add_argument(
        "--permission",
        dest="permission",
        default="w Archive Permission Scheme",
        help="Permission scheme",
    )
    parser.add_argument(
        "--notification",
        dest="notification",
        default="Archived Notification Scheme",
        help="Notification scheme",
    )

    # Getting arguments
    args = parser.parse_args()

    # dynamic variables
    archive_category_name = args.category
    archive_project_permission_scheme = args.permission
    archive_notification_scheme = args.notification

    archive_project_key = args.project

    new_project_category = get_project_category_object(archive_category_name)
    new_permission_scheme = get_project_permission_scheme_object(archive_project_permission_scheme)
    new_notification_scheme = get_project_notification_scheme_object(archive_notification_scheme)
    projects = jira.get_all_projects()
    new_project = None
    for project in projects:
        if archive_project_key == project.get("key"):
            new_project = project
            if new_project_category is None:
                print("Did not find the new project category")
            else:
                jira.update_project_category_for_project(archive_project_key, new_project_category.get("id"))

            if new_permission_scheme:
                jira.assign_project_permission_scheme(archive_project_key, new_permission_scheme.get("id"))
            else:
                print("Did not find a permission scheme")

            if new_notification_scheme:
                jira.assign_project_notification_scheme(archive_project_key, new_notification_scheme.get("id"))
            else:
                print("Did not find a notification scheme")
            break
    print("Everything is done")
    print("Thanks for the usage that script")
