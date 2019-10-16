# coding=utf-8
from atlassian import Bitbucket

bitbucket = Bitbucket(
    url='http://localhost:7990',
    username='admin',
    password='admin')

changelog = bitbucket.get_changelog(
    project='DEMO',
    repository='example-repository',
    ref_from='develop',
    ref_to='master')

print(changelog)
