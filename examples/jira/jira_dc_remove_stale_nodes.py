# coding=utf-8
from atlassian import Jira

"""Remove stale nodes from cluster before version 8.10
See https://confluence.atlassian.com/jirakb/remove-abandoned-or-offline-nodes-in-jira-data-center-946616137.html
"""
jira = Jira(url="http://localhost:8080", username="admin", password="admin")
stale_node_ids = [_["nodeId"] for _ in jira.get_cluster_all_nodes() if not _["alive"] and _["state"] == "OFFLINE"]
for _ in stale_node_ids:
    jira.delete_cluster_node(_)
