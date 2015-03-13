import logging
from atlassian import Confluence
from atlassian import Jira


logging.basicConfig(level=logging.DEBUG, format='[%(asctime).19s] [%(levelname)s] %(message)s')
logging.getLogger('requests').setLevel(logging.WARNING)
log = logging.getLogger('jira-projects-administrators')


jira = Jira(
    url='http://localhost:8080',
    username='admin',
    password='admin')

html = '<table><tr><th>Project Key</th><th>Project Name</th><th>Leader</th><th>Email</th></tr>'

for data in jira.project_leaders():
    log.info('{project_key} leader is {lead_name} <{lead_email}>'.format(**data))
    html += '<tr><td>{project_key}</td><td>{project_name}<td></td>{lead_name}<td></td><a href="mailto:{lead_email}">{lead_email}</a></td></tr>'.format(**data)

html += '</table><p></p><p></p>'

print(html)
