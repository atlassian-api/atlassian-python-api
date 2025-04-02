"""
Confluence module for both Cloud and Server implementations
"""
from atlassian.confluence.base import ConfluenceBase
from atlassian.confluence.cloud import ConfluenceCloud
from atlassian.confluence.server import ConfluenceServer

__all__ = ['ConfluenceBase', 'ConfluenceCloud', 'ConfluenceServer'] 