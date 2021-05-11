# coding=utf-8
from atlassian import Bitbucket

"""This example shows how to create, get and delete tags"""

bitbucket = Bitbucket(url="http://localhost:7990", username="admin", password="admin")

if __name__ == "__main__":
    response = bitbucket.set_tag(
        project_key="gonchik.tsymzhitov",
        repository_slug="gonchik",
        tag_name="test1",
        commit_revision="ebcf5fdffa0",
        description="Stable release",
    )
    print("Response after set_tag method")
    print(response)

    response = bitbucket.get_project_tags(project_key="INT", repository_slug="jira-plugins", tag_name="test1")
    print("Retrieve tag")
    print(response)
    print("Remove tag")
    bitbucket.delete_tag(project_key="INT", repository_slug="jira-plugins", tag_name="test1")
