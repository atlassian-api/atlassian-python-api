# coding=utf-8
from atlassian import Bitbucket

bitbucket = Bitbucket(url="http://localhost:7990", username="admin", password="admin")
pr_id = 12345

pr = bitbucket.get_pullrequest("project_name", "repository_name", pr_id)
ver = pr.json().get("version")
print("PR version: {}".format(ver))

response = bitbucket.decline_pull_request("project_name", "repository_name", pr_id, ver)
print("Declined: {}".format(response))
ver = response.json().get("version")
print("PR version: {}".format(ver))

response = bitbucket.reopen_pull_request("project_name", "repository_name", pr_id, ver)
print("Reopen: {}".format(response))
ver = response.json().get("version")
print("PR version: {}".format(ver))

response = bitbucket.is_pull_request_can_be_merged("project_name", "repository_name", pr_id)
print("Reopen: {}".format(response))
print("PR version: {}".format(ver))

response = bitbucket.merge_pull_request("project_name", "repository_name", pr_id, ver)
print("Merged: {}".format(response))
