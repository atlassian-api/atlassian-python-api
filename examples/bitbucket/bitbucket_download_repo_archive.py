# coding=utf-8
from atlassian import Bitbucket

bitbucket = Bitbucket(url="http://localhost:7990", username="admin", password="admin")

with open("archive.tgz", mode="wb") as dest_fd:
    bitbucket.download_repo_archive(
        project_key="DEMO",
        repository_slug="example-repository",
        dest_fd="file_name",
        at="master",
        format="tar.gz",
    )
