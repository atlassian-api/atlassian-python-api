"""
Atlassian Python API
"""

from .bamboo import Bamboo
from .bitbucket import Bitbucket
from .bitbucket import Bitbucket as Stash
from .cloud_admin import CloudAdminOrgs, CloudAdminUsers
from .confluence import Confluence
from .crowd import Crowd
from .insight import Insight
from .insight import Insight as Assets  # used for Insight on-premise
from .assets import AssetsCloud  # used for Insight Cloud
from .jira import Jira
from .marketplace import MarketPlace
from .portfolio import Portfolio
from .service_desk import ServiceDesk
from .service_desk import ServiceDesk as ServiceManagement
from .xray import Xray

__all__ = [
    "Confluence",
    "Jira",
    "Bitbucket",
    "CloudAdminOrgs",
    "CloudAdminUsers",
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
]
