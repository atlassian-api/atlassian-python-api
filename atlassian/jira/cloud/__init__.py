"""
Jira Cloud API module for Jira API v3

This module provides a set of classes to interact with Jira Cloud API v3,
including the base classes, adapters, and endpoints.
"""

from atlassian.jira.cloud.cloud import CloudJira
from atlassian.jira.cloud.cloud import Jira
from atlassian.jira.cloud.adapter import JiraAdapter
from atlassian.jira.base import JiraEndpoints

from atlassian.jira.cloud.software import SoftwareJira
from atlassian.jira.cloud.software_adapter import SoftwareJiraAdapter
from atlassian.jira.cloud.permissions import PermissionsJira
from atlassian.jira.cloud.permissions_adapter import PermissionsJiraAdapter
from atlassian.jira.cloud.users import UsersJira
from atlassian.jira.cloud.users_adapter import UsersJiraAdapter
from atlassian.jira.cloud.richtext import RichTextJira
from atlassian.jira.cloud.richtext_adapter import RichTextJiraAdapter
from atlassian.jira.cloud.issuetypes import IssueTypesJira
from atlassian.jira.cloud.issuetypes_adapter import IssueTypesJiraAdapter
from atlassian.jira.cloud.projects import ProjectsJira
from atlassian.jira.cloud.projects_adapter import ProjectsJiraAdapter
from atlassian.jira.cloud.search import SearchJira
from atlassian.jira.cloud.search_adapter import SearchJiraAdapter

__all__ = [
    "CloudJira",
    "Jira",
    "JiraAdapter",
    "JiraEndpoints",
    "SoftwareJira",
    "SoftwareJiraAdapter",
    "PermissionsJira",
    "PermissionsJiraAdapter",
    "UsersJira",
    "UsersJiraAdapter",
    "RichTextJira",
    "RichTextJiraAdapter",
    "IssueTypesJira",
    "IssueTypesJiraAdapter",
    "ProjectsJira",
    "ProjectsJiraAdapter",
    "SearchJira",
    "SearchJiraAdapter",
]
