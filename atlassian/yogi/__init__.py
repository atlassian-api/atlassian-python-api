"""Requirement Yogi clients for Jira and Confluence."""

from .yogi_confluence_cloud import ConfluenceCloud, YogiConfluenceCloud
from .yogi_confluence_dc import ConfluenceDC, YogiConfluenceDC
from .yogi_jira_cloud import JiraCloud, YogiJiraCloud
from .yogi_jira_dc import JiraDC, YogiJiraDC

__all__ = [
    "YogiJiraCloud",
    "YogiJiraDC",
    "YogiConfluenceCloud",
    "YogiConfluenceDC",
    "JiraCloud",
    "JiraDC",
    "ConfluenceCloud",
    "ConfluenceDC",
]
