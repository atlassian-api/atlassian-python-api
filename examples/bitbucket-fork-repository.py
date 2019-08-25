# coding=utf-8
from atlassian import Bitbucket

bitbucket = Bitbucket(
    url='http://localhost:7990',
    username='admin',
    password='admin')

data = bitbucket.fork_repository(
    project='DEMO',
    repository='example-repository',
    new_repository='forked-repository')

print(data)
