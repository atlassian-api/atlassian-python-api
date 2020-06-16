# coding=utf-8
from atlassian import Confluence
#from var import config
import logging
from pprint import pprint

CONFLUENCE_URL = config.CONFLUENCE_URL
CONFLUENCE_LOGIN = config.CONFLUENCE_LOGIN
CONFLUENCE_PASSWORD = config.CONFLUENCE_PASSWORD

logging.basicConfig(level=logging.DEBUG)

confluence = Confluence(
    url=CONFLUENCE_URL,
    username=CONFLUENCE_LOGIN,
    password=CONFLUENCE_PASSWORD,
    timeout=180)

confluence.allow_redirects = False
pprint(confluence.get_space_permissions("DOC"))
