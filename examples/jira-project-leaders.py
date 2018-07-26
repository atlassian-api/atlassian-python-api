# coding: utf8
from urllib.parse import quote
from atlassian import Jira

jira = Jira(
    url='http://localhost:8080',
    username='admin',
    password='admin')

EMAIL_SUBJECT = quote('Jira access to project {project_key}')
EMAIL_BODY = quote('''Proszę o dostęp do projektu {project_key} w Jirze.

Aby nadać mi odpowiednie uprawnienia przypisz mnie do roli na stronie:
http://localhost:8080/plugins/servlet/project-config/{project_key}/roles

Role:
Users - dostęp tylko do odczytu + komentowanie
Developers - praca na zadaniach, edycja itp.
Admin - Zmiana konfiguracji oraz możliwość startowania sprintów''')

MAILTO = '<a href="mailto:{lead_email}?subject={email_subject}&body={email_body}">{lead_name}</a>'

print('|| Project Key || Project Name || Ask for Access ||')

for project in jira.project_leaders():
    print('| {project_key} | {project_name} | {lead_name} <{lead_email}> |'.format(project_key=project['project_key'],
                                                                                   project_name=project['project_name'],
                                                                                   email_subject=EMAIL_SUBJECT,
                                                                                   email_body=EMAIL_BODY,
                                                                                   lead_name=project['lead_name'],
                                                                                   lead_email=project['lead_email']))
