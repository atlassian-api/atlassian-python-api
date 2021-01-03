# coding=utf-8
from atlassian import Confluence
from pprint import pprint

"""This example shows how to get all users from group e.g. group_name """

confluence = Confluence(url="http://localhost:8090", username="admin", password="admin")


def get_all_members(group_name):
    flag = True
    i = 0
    limit = 50
    result = []

    while flag:
        response = confluence.get_group_members(group_name=group_name, start=i * limit, limit=limit)
        if response and len(response):
            i += 1
            result.append(response)
        else:
            flag = False
    return result


if __name__ == "__main__":
    group_name = "confluence-users"
    pprint(get_all_members(group_name=group_name))
