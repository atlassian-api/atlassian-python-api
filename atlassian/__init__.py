"""
Atlassian Python API
"""

from .bamboo import Bamboo
from .bitbucket import Bitbucket
from .bitbucket import Bitbucket as Stash
from .cloud_admin import CloudAdmin, CloudAdminOrgs, CloudAdminUsers
from .confluence import Confluence, ConfluenceBase, ConfluenceCloud, ConfluenceServer
from .confluence.cloud.cloud import ConfluenceCloud as ConfluenceV2
from .crowd import Crowd
from .insight import Insight
from .insight import Insight as Assets  # used for Insight on-premise
from .assets import AssetsCloud  # used for Insight Cloud
from .jira import Jira, JiraCloud, JiraServer, JiraServiceManagement, JiraSoftware, create_jira_cloud
from .marketplace import MarketPlace
from .portfolio import Portfolio
from .service_desk import ServiceDesk
from .service_desk import ServiceDesk as ServiceManagement
from .tempo import TempoCloud, TempoServer
from .xray import Xray
from .yogi import YogiConfluenceCloud, YogiConfluenceDC, YogiJiraCloud, YogiJiraDC


# Confluence REST API v2 client.  The existing ``Confluence`` class remains
# the backwards-compatible v1/v2 URL-dispatching client.
def create_confluence(url, *args, api_version=1, **kwargs):
    """Create a version-aware Confluence client."""
    return ConfluenceBase.factory(url, *args, api_version=api_version, **kwargs)


__all__ = [
    "Confluence",
    "ConfluenceBase",
    "ConfluenceCloud",
    "ConfluenceServer",
    "ConfluenceV2",
    "create_confluence",
    "Jira",
    "JiraServer",
    "JiraCloud",
    "JiraSoftware",
    "JiraServiceManagement",
    "create_jira_cloud",
    "Bitbucket",
    "CloudAdminOrgs",
    "CloudAdminUsers",
    "CloudAdmin",
    "Portfolio",
    "Bamboo",
    "Stash",
    "Crowd",
    "ServiceDesk",
    "ServiceManagement",
    "MarketPlace",
    "Xray",
    "Insight",
    "Assets",
    "AssetsCloud",
    "TempoCloud",
    "TempoServer",
    "YogiJiraCloud",
    "YogiJiraDC",
    "YogiConfluenceCloud",
    "YogiConfluenceDC",
]
