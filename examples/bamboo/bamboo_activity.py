# coding=utf-8
import os

from atlassian import Bamboo

"""
    Example for check exist activity and agent status
"""
BAMBOO_URL = os.environ.get("BAMBOO_URL", "http://localhost:8085")
ATLASSIAN_USER = os.environ.get("ATLASSIAN_USER", "admin")
ATLASSIAN_PASSWORD = os.environ.get("ATLASSIAN_PASSWORD", "admin")

bamboo = Bamboo(url=BAMBOO_URL, username=ATLASSIAN_USER, password=ATLASSIAN_PASSWORD)

agent_status = bamboo.agent_status()
print(agent_status)

activity = bamboo.activity()
print(activity)
