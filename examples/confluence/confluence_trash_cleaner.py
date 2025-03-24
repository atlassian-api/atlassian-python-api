# coding=utf-8
from atlassian import Confluence

"""This example shows how to remove page by page from trash for all spaces"""

confluence = Confluence(url="http://localhost:8090", username="admin", password="admin")


def clean_pages_from_space(space_key, limit=500):
    """
    Remove all pages from trash for related space
    :param limit:
    :param space_key:
    :return:
    """
    flag = True
    while flag:
        values = confluence.get_all_pages_from_space_trash(space=space_key, start=0, limit=limit, content_type="page")
        if not values or len(values) == 0:
            flag = False
            print(f"For space {space_key} trash is empty")
        else:
            print(f"Found in space {space_key} pages as trashed {len(values)}")
            for value in values:
                print(("Removing page with title: " + value["title"]))
                confluence.remove_page_from_trash(value["id"])


def clean_blog_posts_from_space(space_key, limit=500):
    """
    Remove all pages from trash for related space
    :param limit:
    :param space_key:
    :return:
    """
    flag = True
    while flag:
        values = confluence.get_all_pages_from_space_trash(
            space=space_key, start=0, limit=limit, content_type="blogpost"
        )
        if values and len(values) > 0:
            print(f"Found in space {space_key} pages as trashed {len(values)}")
            for value in values:
                print(("Removing page with title: " + value["title"]))
                confluence.remove_page_from_trash(value["id"])
        else:
            flag = False
            print(f"For space {space_key} trash is empty")


def clean_all_trash_pages_from_all_spaces():
    """
    Main function for retrieve space keys and provide space for cleaner
    :return:
    """
    limit = 50
    flag = True
    i = 0
    while flag:
        space_lists = confluence.get_all_spaces(start=i * limit, limit=limit)
        if space_lists and len(space_lists) != 0:
            i += 1
            for space_list in space_lists["results"]:
                print(("Start review the space with key = " + space_list["key"]))
                clean_pages_from_space(space_key=space_list["key"])
                clean_blog_posts_from_space(space_key=space_list["key"])
        else:
            flag = False
    return 0


if __name__ == "__main__":
    clean_all_trash_pages_from_all_spaces()
