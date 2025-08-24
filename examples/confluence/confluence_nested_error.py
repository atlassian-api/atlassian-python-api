# coding=utf-8
from atlassian import Confluence
from atlassian.confluence_old import ApiError

""" This example shows a way to get the real reason for an exception"""
try:
    confluence = Confluence(
        url="http://some_site_without_permission.com",
        username="admin",
        password="admin",
    )
    result = confluence.get_user_details_by_username(username="gonchik.tsymzhitov", expand="status")
except ApiError as e:
    print(f"FAILURE: {e}, caused by {e.reason if e.reason is not None else 'unknown reason'}")
else:
    print(result)
