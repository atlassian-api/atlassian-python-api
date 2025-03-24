# coding=utf-8
from atlassian import Jira

jira = Jira(url="https://jira.example.com", username="mskymoore", password="admin")

alive_node_ids = [_["nodeId"] for _ in jira.get_cluster_alive_nodes()]

zips_creation_task_id = jira.generate_support_zip_on_nodes(alive_node_ids)["clusterTaskId"]

in_progress_zips = list()

while True:
    for task in jira.check_support_zip_status(zips_creation_task_id)["tasks"]:
        if task["status"] == "IN_PROGRESS":
            print(f"file {task['fileName']} {task['progressMessage']}")
            if task["fileName"] not in in_progress_zips:
                in_progress_zips.append(task["fileName"])
        else:
            support_zip = jira.download_support_zip(task["fileName"])
            with open(task["fileName"], "wb") as fp:
                fp.write(support_zip)
            print(f"{task['fileName']} written.")
            if task["fileName"] in in_progress_zips:
                in_progress_zips.remove(task["fileName"])

    if len(in_progress_zips) == 0:
        break
