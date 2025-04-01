from .bamboo import Bamboo
from .bitbucket import Bitbucket
from .bitbucket import Bitbucket as Stash
from .cloud_admin import CloudAdminOrgs, CloudAdminUsers
from .confluence import Confluence
from .confluence_base import ConfluenceBase
from .confluence_v2 import ConfluenceV2
from .crowd import Crowd
from .insight import Insight
from .insight import Insight as Assets
from .jira import Jira
from .marketplace import MarketPlace
from .portfolio import Portfolio
from .service_desk import ServiceDesk
from .service_desk import ServiceDesk as ServiceManagement
from .xray import Xray


# Factory function for Confluence client
def create_confluence(url, *args, api_version=1, **kwargs):
    """
    Create a Confluence client with the specified API version.
    
    Args:
        url: The Confluence instance URL
        api_version: API version, 1 or 2, defaults to 1
        args: Arguments to pass to Confluence constructor
        kwargs: Keyword arguments to pass to Confluence constructor
        
    Returns:
        A Confluence client configured for the specified API version
    """
    return ConfluenceBase.factory(url, *args, api_version=api_version, **kwargs)


__all__ = [
    "Confluence",
    "ConfluenceBase",
    "ConfluenceV2",
    "create_confluence",
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
]
