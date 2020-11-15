# coding=utf-8
import logging

from atlassian import Bitbucket

logging.basicConfig(level=logging.DEBUG, format="[%(asctime).19s] [%(levelname)s] %(message)s")
logging.getLogger("requests").setLevel(logging.WARNING)
log = logging.getLogger("bitbucket-projects-administrators")

bitbucket = Bitbucket(url="http://localhost:7990", username="admin", password="admin")

html = "<table><tr><th>Project Key</th><th>Project Name</th><th>Administrator</th></tr>"

for data in bitbucket.all_project_administrators():
    html += "<tr><td>{project_key}</td><td>{project_name}</td><td><ul>".format(**data)
    for user in data["project_administrators"]:
        html += '<li><a href="mailto:{email}">{name}</a></li>'.format(**user)
    html += "</ul></td></tr>"

html += "</table><p></p><p></p>"

print(html)
