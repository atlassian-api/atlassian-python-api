# coding=utf-8
from atlassian import Jira

jira = Jira(
    url="http://localhost:8080/",
    username="jira-administrator",
    password="admin")
    
components = ["Data Base", "HTML", "JavaScript"]

"""That example show how to create components on all existing projects"""

for i in jira.get_all_projects(included_archived=None):
    for j in compo:
        data = {"project": i["key"], "name":j}
        jira.create_component(data)
        print("{} - component created ".format(component.get('name')))
        
