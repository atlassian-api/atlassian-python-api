# coding=utf-8
from pprint import pprint

from atlassian import Bitbucket

bitbucket = Bitbucket(url="http://localhost:7990", username="admin", password="admin")

# project_list() is a generator so that later API pages are fetched only when
# needed. Iterate it directly, or use list(...) when the whole result fits in
# memory.
for project in bitbucket.project_list():
    pprint(project)
