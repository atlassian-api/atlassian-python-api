# coding=utf-8
"""
Confluence API client package for Atlassian Python API.

This package provides both Cloud and Server implementations of the Confluence API.
"""

from .cloud import Cloud as ConfluenceCloud
from .server import Server as ConfluenceServer

# Legacy import for backward compatibility
from .base import ConfluenceBase


# Legacy Confluence class for backward compatibility
class Confluence(ConfluenceBase):
    """Legacy Confluence class for backward compatibility."""

    def __init__(self, url, *args, **kwargs):
        # Auto-detect if it's cloud or server based on URL
        if ("atlassian.net" in url or "jira.com" in url) and ("/wiki" not in url):
            if "cloud" not in kwargs:
                kwargs["cloud"] = True
        super().__init__(url, *args, **kwargs)


__all__ = [
    "ConfluenceCloud",
    "ConfluenceServer",
    "ConfluenceBase",
]
