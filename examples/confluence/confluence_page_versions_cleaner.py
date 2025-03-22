# coding=utf-8
from atlassian import Confluence

CONFLUENCE_URL = "confluence.example.com"
CONFLUENCE_LOGIN = "gonchik.tsymzhitov"
CONFLUENCE_PASSWORD = "passwordpassword"
REMAINED_PAGE_HISTORY_COUNT = 1


def page_version_remover(content_id, remained_page_numbers):
    response = confluence.get_content_history(content_id)
    if not response or not response.get("latest"):
        return
    latest_version_count = int(response.get("lastUpdated").get("number"))
    if len(response) > 0 and latest_version_count > remained_page_numbers:
        print(
            (
                f"Number of {confluence.url_joiner(confluence.url, '/pages/viewpage.action?pageId=' + content_id)} latest version {latest_version_count}"
            )
        )
        for version_page_counter in range(1, (latest_version_count - remained_page_numbers + 1), 1):
            confluence.remove_content_history(content_id, 1)
    else:
        print("Number of page history smaller than remained")


def get_all_page_ids_from_space(space):
    """
    :param space:
    :return:
    """
    limit = 500
    flag = True
    step = 0
    content_ids = []

    while flag:
        values = confluence.get_all_pages_from_space(space=space, start=limit * step, limit=limit)
        step += 1
        if len(values) == 0:
            flag = False
            print("Did not find any pages, please, check permissions")
        else:
            for value in values:
                print(("Retrieve page with title: " + value["title"]))
                content_ids.append((value["id"]))
    print(f"Found in space {space} pages {len(content_ids)}")
    return content_ids


def get_all_spaces():
    limit = 50
    flag = True
    i = 0
    space_key_list = []
    while flag:
        space_lists = confluence.get_all_spaces(start=i * limit, limit=limit)
        if space_lists and len(space_lists) != 0:
            i += 1
            for space_list in space_lists:
                print(("Start review the space with key = " + space_list["key"]))
                space_key_list.append(space_list["key"])
        else:
            flag = False

    return space_key_list


def reduce_page_numbers(page_id, remained_page_history_count):
    page_version_remover(page_id, remained_page_history_count)
    return


if __name__ == "__main__":
    confluence = Confluence(
        url=CONFLUENCE_URL,
        username=CONFLUENCE_LOGIN,
        password=CONFLUENCE_PASSWORD,
        timeout=190,
    )
    space_keys = get_all_spaces()
    counter = 0
    for space_key in space_keys:
        print(f"Starting review space with key {space_key}")
        page_ids = get_all_page_ids_from_space(space_key)
        for page_id in page_ids:
            reduce_page_numbers(page_id=page_id, remained_page_history_count=REMAINED_PAGE_HISTORY_COUNT)
