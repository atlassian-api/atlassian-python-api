# coding=utf-8
"""
Confluence API client package for Atlassian Python API.

This package provides both Cloud and Server implementations of the Confluence API.
"""

from urllib.parse import urlparse

from .cloud import Cloud as ConfluenceCloud
from .server import Server as ConfluenceServer

# Legacy import for backward compatibility
from .base import ConfluenceBase


# Legacy Confluence class for backward compatibility
class Confluence(ConfluenceBase):
    """Legacy Confluence class for backward compatibility."""

    def __init__(self, url, *args, **kwargs):
        # Detect which implementation to use
        # Priority: explicit cloud= kwarg > URL-based heuristic
        is_cloud = kwargs.get("cloud")
        if is_cloud is None:
            hostname = urlparse(url).hostname or ""
            is_cloud = (
                hostname == "atlassian.net"
                or hostname.endswith(".atlassian.net")
                or hostname == "jira.com"
                or hostname.endswith(".jira.com")
                or hostname == "api.atlassian.com"
                or hostname.endswith(".api.atlassian.com")
            )
        if is_cloud:
            impl = ConfluenceCloud(url, *args, **kwargs)
        else:
            impl = ConfluenceServer(url, *args, **kwargs)
        self._impl = impl

    def __getattr__(self, attr):
        # Delegate all unknown attributes to the true client
        return getattr(self._impl, attr)


__all__ = [
    "ConfluenceCloud",
    "ConfluenceServer",
    "ConfluenceBase",
]
