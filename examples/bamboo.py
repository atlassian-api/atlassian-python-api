from pprint import pprint
from atlassian import Bamboo
import os

BAMBOO_URL = os.environ.get('BAMBOO_URL', 'http://localhost:8085')
ATLASSIAN_USER = os.environ.get('ATLASSIAN_USER', 'admin')
ATLASSIAN_PASSWORD = os.environ.get('ATLASSIAN_PASSWORD', 'admin')

bamboo = Bamboo(
    url=BAMBOO_URL,
    username=ATLASSIAN_USER,
    password=ATLASSIAN_PASSWORD)


# Methods in plural (projects, plans, results...) return a generator that iterates through
# all results without the need of dealing need with pagination

# for project in bamboo.projects():
#    pprint(project)


for branch in bamboo.plan_branches('PROJ-SP2'):
    pprint(branch)

# for result in bamboo.latest_results():
#    pprint(result)

# for result in bamboo.plan_results(project_key='FOO', plan_key='BAR'):
#    pprint(result)

# for report in bamboo.reports():
#     pprint(report)


# Methods in singular (project, plan, result...) return a single dictionary

pprint(bamboo.project('FOO'))

pprint(bamboo.build_result('FOO-BAR-1'))







