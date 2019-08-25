# coding=utf-8
from atlassian import Bamboo
import os

BAMBOO_URL = os.environ.get('BAMBOO_URL', 'http://localhost:8085')
ATLASSIAN_USER = os.environ.get('ATLASSIAN_USER', 'admin')
ATLASSIAN_PASSWORD = os.environ.get('ATLASSIAN_PASSWORD', 'admin')

bamboo = Bamboo(
    url=BAMBOO_URL,
    username=ATLASSIAN_USER,
    password=ATLASSIAN_PASSWORD)

# Delete entire plan
bamboo.delete_plan('PLAN-TODELETE')

# Delete single result
bamboo.delete_build_result('PLAN-TODELETE-7')
