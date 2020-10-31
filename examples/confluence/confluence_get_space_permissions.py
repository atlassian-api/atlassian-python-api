# coding=utf-8
import logging
from pprint import pprint

from atlassian import Confluence

CONFLUENCE_URL = "http://conlfuence.example.com"
CONFLUENCE_LOGIN = "gonchik.tsymzhitov"
CONFLUENCE_PASSWORD = "************"

logging.basicConfig(level=logging.DEBUG)

confluence = Confluence(
    url=CONFLUENCE_URL,
    username=CONFLUENCE_LOGIN,
    password=CONFLUENCE_PASSWORD,
    timeout=180,
)

confluence.allow_redirects = False
pprint(confluence.get_space_permissions("DOC"))
