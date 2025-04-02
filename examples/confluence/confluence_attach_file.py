# coding=utf-8
"""
This is example to attach file with mimetype

"""
import logging

# https://pypi.org/project/python-magic/
import magic

from atlassian import Confluence

logging.basicConfig(level=logging.DEBUG)

confluence = Confluence(
    url="http://localhost:8090",
    username="admin",
    password="admin",
)


def attach_file(page_title, file_location, file_name, mime_type, space):
    page_id = confluence.get_page_by_title(space=space, title=page_title).get("id") or None
    if page_id is None:
        return 1
    try:
        confluence.attach_file(
            filename=file_location, name=file_name, content_type=mime_type, page_id=page_id, space=space
        )
    except Exception:
        return 1
    return 0


mime_type = magic.Magic(mime=True)

file_location_with_page = "~/test/test_file.pdf"
file_name = "So excited overview of report.pdf"
title = "The page with attachments"
space = "TST"

content_type = magic.from_file(file_name, mime=True)
attach_file(
    file_location=file_location_with_page, file_name=file_name, mime_type=content_type, page_title=title, space=space
)
