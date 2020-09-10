# coding=utf-8
from atlassian import Bitbucket
from pprint import pprint

bitbucket = Bitbucket(
    url='http://localhost:7990',
    username='admin',
    password='admin')

pprint(bitbucket.project_list())
