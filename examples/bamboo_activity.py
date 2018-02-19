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


agent_status = bamboo.agent_status()
pprint(agent_status)

activity = bamboo.activity()
pprint(activity)
