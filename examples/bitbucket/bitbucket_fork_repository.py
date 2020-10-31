# coding=utf-8
from atlassian import Bitbucket

bitbucket = Bitbucket(url="http://localhost:7990", username="admin", password="admin")

data = bitbucket.fork_repository(
    project_key="DEMO",
    repository_slug="example-repository",
    new_repository_slug="forked-repository",
)

print(data)
