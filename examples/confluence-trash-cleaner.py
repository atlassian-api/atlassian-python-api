# coding: utf8
from atlassian import Confluence

"""This example shows how to remove page by page from trash for all spaces"""

confluence = Confluence(
    url='http://localhost:8090',
    username='admin',
    password='admin')


def clean_pages_from_space(confluence, space_key):
    """
    Remove all pages from trash for related space
    :param confluence:
    :param space_key:
    :return:
    """
    limit = 500
    flag = True
    step = 0
    while flag:
        values = confluence.get_all_pages_from_space_trash(space=space_key, start=0, limit=limit)
        step += 1
        if len(values) == 0:
            flag = False
            print("For space {} trash is empty".format(space_key))
        else:
            for value in values:
                print(value['title'])
                confluence.remove_page_from_trash(value['id'])


def clean_all_trash_pages_from_all_spaces(confluence):
    """
    Main function for retrieve space keys and provide space for cleaner
    :param confluence:
    :return:
    """
    limit = 50
    flag = True
    i = 0
    while flag:
        space_lists = confluence.get_all_spaces(start=i * limit, limit=limit)
        if space_lists and len(space_lists) != 0:
            i += 1
            for space_list in space_lists:
                print("Start review the space with key = " + space_list['key'])
                clean_pages_from_space(confluence=confluence, space_key=space_list['key'])
        else:
            flag = False
    return 0


if __name__ == '__main__':
    clean_all_trash_pages_from_all_spaces(confluence=confluence)
