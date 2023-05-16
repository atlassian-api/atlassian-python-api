# coding=utf-8
from atlassian import Jira

jira = Jira(url="http://localhost:8080", username="admin", password="admin")


def get_all_users(group, include_inactive=True):
    """
    Get all users for group. If their more, than 50 users in group:
    go through the pages and append other users to the list
    :param group:
    :param include_inactive:
    :return:
    """
    start = 0
    users = jira.get_all_users_from_group(group, include_inactive_users=include_inactive, start=start)
    processed_data = {
        "group_name": group,
        "total": users["total"],
        "users": [{"name": user["name"], "active": user["active"]} for user in users["values"]],
    }
    while "nextPage" in users:
        start += 50
        users = jira.get_all_users_from_group(group, include_inactive_users=include_inactive, start=start)
        user_list = [{"name": user["name"], "active": user["active"]} for user in users["values"]]
        processed_data["users"] += user_list

    return processed_data


def sort_users_in_group(group):
    """
    Take group, sort users by the name and return group with sorted users
    """
    group["users"] = [sorted_group for sorted_group in sorted(group["users"], key=lambda k: k["name"])]
    return group


def get_groups_data():
    """
    Get all groups, get all users for each group and sort groups by users
    :return:
    """
    groups = [group["name"] for group in jira.get_groups(limit=200)["groups"]]
    groups_and_users = [get_all_users(group) for group in groups]
    groups_and_users = [sort_users_in_group(group) for group in groups_and_users]
    return groups_and_users


def get_inactive_users(groups):
    """
    Take group list and return groups only with inactive users
    :param groups:
    :return:
    """
    inactive_users_list = []
    for group in groups:
        inactive_users = {
            "group_name": group["group_name"],
            "users": [
                {"name": user["name"], "active": user["active"]} for user in group["users"] if not user["active"]
            ],
        }
        inactive_users_list.append(inactive_users)

    return inactive_users_list


def exclude_inactive_users(groups):
    """
    Excluding inactive users from groups.
    :param groups:
    :return:
    """
    for group in groups:
        for user in group["users"]:
            print("Trying to delete {} from group {}".format(user["name"], group["group_name"]))
            jira.remove_user_from_group(user["name"], group["group_name"])
    return True


def filter_groups_by_members(groups, quantity=1):
    """
    Take groups list and return empty groups
    :param groups:
    :param quantity:
    :return:
    """
    return [x for x in groups if int(x["total"]) < quantity]


def find_group(groups, group_name):
    """
    Take groups list and find group by the group name
    :param groups:
    :param group_name:
    :return:
    """
    for group in groups:
        if group["group_name"] == group_name:
            return group
        else:
            return "Group {} not in list".format(group_name)
