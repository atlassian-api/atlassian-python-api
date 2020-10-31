# coding=utf-8
from atlassian import Confluence

""" How to reindex the Confluence instance """

confluence = Confluence(url="http://localhost:8090", username="admin", password="admin")

if confluence.reindex_get_status().get("finished"):
    print("Start reindex")
    confluence.reindex()
