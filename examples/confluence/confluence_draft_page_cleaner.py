# coding=utf-8
import datetime

from atlassian import Confluence

"""This example shows how to remove old draft pages (it is configure by DRAFT_DAYS variable) for all spaces"""

confluence = Confluence(url="http://localhost:8090", username="admin", password="admin")


def clean_draft_pages_from_space(space_key, count, date_now):
    """
    Remove draft pages from space using datetime.now()
    :param space_key:
    :param count:
    :param date_now:
    :return: int counter
    """
    pages = confluence.get_all_draft_pages_from_space(space=space_key, start=0, limit=500)
    for page in pages:
        page_id = page["id"]
        draft_page = confluence.get_draft_page_by_id(page_id=page_id)
        last_date_string = draft_page["version"]["when"]
        last_date = datetime.datetime.strptime(last_date_string.replace(".000", "")[:-6], "%Y-%m-%dT%H:%M:%S")
        if (date_now - last_date) > datetime.timedelta(days=DRAFT_DAYS):
            count += 1
            print("Removing page with page id: " + page_id)
            confluence.remove_page_as_draft(page_id=page_id)
            print("Removed page with date " + last_date_string)
    return count


def clean_all_draft_pages_from_all_spaces(days=30):
    """
    Remove all draft pages for all spaces older than DRAFT_DAYS
    :param days: int
    :return:
    """
    date_now = datetime.datetime.now()
    count = 0
    limit = 50
    flag = True
    i = 0
    while flag:
        space_lists = confluence.get_all_spaces(start=i * limit, limit=limit)
        if space_lists and len(space_lists) != 0:
            i += 1
            for space_list in space_lists:
                print("Start review the space {}".format(space_list["key"]))
                count = clean_draft_pages_from_space(space_key=space_list["key"], count=count, date_now=date_now)
        else:
            flag = False
    print("Script has removed {count} draft pages older than {days} days".format(count=count, days=days))


if __name__ == "__main__":
    DRAFT_DAYS = 30
    clean_all_draft_pages_from_all_spaces(days=DRAFT_DAYS)
