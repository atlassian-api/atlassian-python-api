# coding=utf-8
from atlassian import Bitbucket


def html(project):
    html_data = "<table>\n"
    html_data += "\t<tr><th>ITEM</th><th>VALUE</th></tr>\n"
    html_data += "\t<tr><td>key</td><td>{key}</td></tr>\n".format(**project)
    html_data += "\t<tr><td>name</td><td>{name}</td></tr>\n".format(**project)
    html_data += "\t<tr><td>description</td><td>{description}</td></tr>\n".format(**project)
    html_data += "\t<tr><td>id</td><td>{id}</td></tr>\n".format(**project)
    return html_data + "</table>\n"


bitbucket = Bitbucket(url="http://localhost:7990", username="admin", password="admin")

data = bitbucket.project("DEMO")
print((html(data)))
