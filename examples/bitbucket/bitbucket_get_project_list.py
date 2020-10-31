# coding=utf-8
from pprint import pprint

from atlassian import Bitbucket

bitbucket = Bitbucket(url="http://localhost:7990", username="admin", password="admin")

pprint(bitbucket.project_list())
