# coding=utf-8
import logging
from ..rest_client import AtlassianRestAPI


log = logging.getLogger(__name__)

class ConfluenceBase(AtlassianRestAPI):
    content_types = {
        ".gif": "image/gif",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".pdf": "application/pdf",
        ".doc": "application/msword",
        ".xls": "application/vnd.ms-excel",
        ".svg": "image/svg+xml",
    }

    def __init__(self, url, *args, **kwargs):
        if ("atlassian.net" in url or "jira.com" in url) and ("/wiki" not in url):
            url = AtlassianRestAPI.url_joiner(url, "/wiki")
            if "cloud" not in kwargs:
                kwargs["cloud"] = True
        super(ConfluenceBase, self).__init__(url, *args, **kwargs)

  