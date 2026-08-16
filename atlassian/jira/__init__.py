# coding=utf-8
"""Jira API clients split by deployment target.

``Jira`` remains the legacy-compatible Server/Data Center client.  Use
``JiraCloud`` for Jira Cloud Core REST v2/v3.
"""

from .jira_cloud import JiraCloud, JiraServiceManagement, JiraSoftware, create_jira_cloud
from .jira_server import Jira as JiraServer

# Preserve ``from atlassian.jira import Jira`` and ``from atlassian import Jira``.
Jira = JiraServer

__all__ = [
    "Jira",
    "JiraServer",
    "JiraCloud",
    "JiraSoftware",
    "JiraServiceManagement",
    "create_jira_cloud",
]
