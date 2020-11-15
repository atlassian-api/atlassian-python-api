# coding=utf-8
from atlassian import Confluence

"""
This example shows how to clean page versions for subtree of pages
"""

CONFLUENCE_URL = "confluence.example.com"
CONFLUENCE_LOGIN = "gonchik.tsymzhitov"
CONFLUENCE_PASSWORD = "passwordpassword"

if __name__ == "__main__":
    confluence = Confluence(
        url=CONFLUENCE_URL,
        username=CONFLUENCE_LOGIN,
        password=CONFLUENCE_PASSWORD,
        timeout=190,
    )
    remained_count = 1

    subtree = confluence.get_subtree_of_content_ids("123123")
    for page_id in subtree:
        confluence.remove_page_history_keep_version(page_id=page_id, keep_last_versions=remained_count)
