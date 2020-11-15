# coding=utf-8
from atlassian import Jira

jira = Jira(url="http://localhost:8080/", username="jira-administrator", password="admin")

components = ["Data Base", "HTML", "JavaScript"]

"""That example show how to create components on all existing projects, only skipping the one in a provided list"""

project_to_skip = ["SI", "SA", "ETA"]

for i in jira.get_all_projects(included_archived=None):
    if i["key"] in project_to_skip:
        print("Skipping project {} ".format(i["key"]))
    else:
        for j in components:
            print("Creating in project {} ".format(i["key"]))
            comp = {"project": i["key"], "name": j}
            jira.create_component(comp)
            print("{} - component created ".format(comp.get("name")))
