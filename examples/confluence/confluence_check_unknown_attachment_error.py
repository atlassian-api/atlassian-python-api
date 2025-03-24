# coding=utf-8
from atlassian import Confluence

"""This example how to detect unknown-attachments errors"""

confluence = Confluence(url="http://localhost:8090", username="admin", password="admin", timeout=185)


def get_all_pages_ids(space_key):
    page_ids = []

    limit = 50
    flag = True
    step = 0
    while flag:
        values = confluence.get_all_pages_from_space(space=space_key, start=step * limit, limit=limit)
        step += 1

        if len(values) == 0:
            flag = False
            print("Extracted all pages excluding restricts")
        else:
            for value in values:
                page_ids.append(value.get("id"))

    return page_ids


def check_unknown_attachment_in_space(space_key):
    """
    Detect errors in space
    :param space_key:
    :return:
    """
    page_ids = get_all_pages_ids(space_key)
    print(f"Start review pages {len(page_ids)} in {space_key}")
    for page_id in page_ids:
        link = confluence.has_unknown_attachment_error(page_id)
        if len(link) > 0:
            print(link)


if __name__ == "__main__":
    space_list = confluence.get_all_spaces()
    for space in space_list:
        print(f"Start review {space['key']} space")
        check_unknown_attachment_in_space(space["key"])
