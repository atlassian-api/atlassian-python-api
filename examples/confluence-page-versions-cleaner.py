from atlassian import Confluence

CONFLUENCE_URL = "confluence.example.com"
CONFLUENCE_LOGIN = "gonchik.tsymzhitov"
CONFLUENCE_PASSWORD = "passwordpassword"


def page_version_remover(server, content_id, remained_page_numbers):
    response = server.get_content_history(content_id)
    if not response.get('latest'):
        return
    latest_version_count = int(response.get('lastUpdated').get('number'))
    if len(response) > 0 and latest_version_count > remained_page_numbers:
        print("Number of {} latest version {}".format(
            confluence.url_joiner(confluence.url, "/pages/viewpage.action?pageId=" + content_id), latest_version_count))
        for version_page_counter in range(1, (latest_version_count - remained_page_numbers + 1), 1):
            server.remove_content_history(content_id, 1)
    else:
        print('Number of page history smaller than remained')


def get_all_page_ids_from_space(confluence, space_key):
    """
    :param confluence:
    :param space_key:
    :return:
    """
    limit = 500
    flag = True
    step = 0
    page_ids = []

    while flag:
        values = confluence.get_all_pages_from_space(space=space_key, start=limit * step, limit=limit)
        step += 1
        if len(values) == 0:
            flag = False
            print("Did not find any pages, please, check permissions")
        else:
            for value in values:
                print("Retrieve page with title: " + value['title'])
                page_ids.append((value['id']))
    print("Found in space {} pages {}".format(space_key, len(page_ids)))
    return page_ids


def get_all_spaces(confluence):
    limit = 50
    flag = True
    i = 0
    space_key_list = []
    while flag:
        space_lists = confluence.get_all_spaces(start=i * limit, limit=limit)
        if space_lists and len(space_lists) != 0:
            i += 1
            for space_list in space_lists:
                print("Start review the space with key = " + space_list['key'])
                space_key_list.append(space_list['key'])
        else:
            flag = False

    return space_key_list


def reduce_page_numbers(confluence, page_id, remained_page_history_count):
    page_version_remover(confluence, page_id, remained_page_history_count)
    return


if __name__ == '__main__':
    confluence = Confluence(
        url=CONFLUENCE_URL,
        username=CONFLUENCE_LOGIN,
        password=CONFLUENCE_PASSWORD,
        timeout=190
    )
    remained_count = 1
    space_keys = get_all_spaces(confluence)
    counter = 0
    for space_key in space_keys:
        print("Starting review space with key {}".format(space_key))
        page_ids = get_all_page_ids_from_space(confluence, space_key)
        for page_id in page_ids:
            reduce_page_numbers(confluence, page_id=page_id, remained_page_history_count=remained_count)