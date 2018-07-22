from atlassian import Confluence
from atlassian import Jira
from pprint import pprint

jira = Jira(
    url='http://localhost:8080',
    username='admin',
    password='admin')

html = """<table>
                <tr>
                    <th>Project Key</th>
                    <th>Project Name</th>
                    <th>Leader</th>
                    <th>Email</th>
                </tr>"""

for data in jira.project_leaders():
    html += """<tr>
                    <td>{project_key}</td>
                    <td>{project_name}</td>
                    <td>{lead_name}</td>
                    <td><a href="mailto:{lead_email}">{lead_email}</a></td>
                </tr>""".format(**data)

html += '</table>'

pprint(html)
