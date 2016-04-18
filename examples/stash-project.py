from pprint import pprint
from atlassian import Stash


def html(project):
    html = '<tr><td>{project_key}</td><td>{project_name}</td><td><ul>'.format(**project)
    for user in project['project_administrators']:
        html += '\n\t<li><a href="mailto:{email}">{name}</a></li>'.format(**user)
    return html + '</ul></td></tr>\n'

stash = Stash(
    url='http://localhost:7990',
    username='admin',
    password='admin')

data = stash.project('DEMO')
pprint(html(data))
