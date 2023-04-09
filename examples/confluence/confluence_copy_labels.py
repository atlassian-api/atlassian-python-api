import argparse
import logging
from os import environ

from atlassian import Confluence

"""
This example related to the syncing labels between 2 spaces
"""

CONFLUENCE_URL = environ.get("CONFLUENCE_URL")
CONFLUENCE_LOGIN = environ.get("CONFLUENCE_LOGIN")
CONFLUENCE_PASSWORD = environ.get("CONFLUENCE_PASSWORD")
confluence = Confluence(
    url=CONFLUENCE_URL,
    username=CONFLUENCE_LOGIN,
    password=CONFLUENCE_PASSWORD,
    timeout=185,
)


def sync_labels_pages(pages, destination_space):
    """
    Sync labels between to 2 spaces
    :param destination_space:
    :param pages:
    :return:
    """
    for page in pages:
        page_id = page.get("id")
        page_title = page.get("title")
        labels_response = confluence.get_page_labels(page_id)
        if labels_response.get("size") > 0:
            labels = labels_response.get("results")
            response = confluence.get_page_by_title(destination_space, page_title)
            if response:
                destination_page_id = response.get("id")
                for label in labels:
                    if label.get("prefix") == "global":
                        label_name = label.get("name")
                        if not DRY_RUN:
                            confluence.set_page_label(destination_page_id, label_name)
                        print(label_name + " copied to " + page_title)
    return


if __name__ == "__main__":
    # Setting the logging level. INFO|ERROR|DEBUG are the most common.
    logging.basicConfig(level=logging.INFO)
    # Initialize argparse module with some program name and additional information
    parser = argparse.ArgumentParser(
        prog="confluence_copy_lables_between_spaces",
        description="Simple execution for sync labels between 2 spaces",
    )
    parser.add_argument("--source", dest="source", default="SOURCESPACE", help="Just Source Space")
    parser.add_argument(
        "--destination",
        dest="destination",
        default="DESTINATIONSPACE",
        help="Just Destination Space",
    )
    parser.add_argument("--dry-run", dest="dry_run", action="store_true")
    args = parser.parse_args()
    SOURCE_SPACE = args.source
    DESTINATION_SPACE = args.destination
    DRY_RUN = False
    if args.dry_run:
        DRY_RUN = True
    limit = 50
    flag = True
    step = 0
    while flag:
        values = confluence.get_all_pages_from_space(
            SOURCE_SPACE,
            step * limit,
            limit=limit,
            status="current",
            content_type="page",
        )
        step += 1
        if len(values) == 0:
            flag = False
            break
        sync_labels_pages(values, DESTINATION_SPACE)
