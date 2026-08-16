# coding=utf-8
"""
Confluence API client package for Atlassian Python API.

This package provides both Cloud and Server implementations of the Confluence API.
"""

from urllib.parse import urlparse
import warnings

from ..confluence_base import ConfluenceBase
from .cloud import Cloud as LegacyConfluenceCloud
from .server import Server as ConfluenceServer
from .base import ConfluenceBase as LegacyConfluenceBase


# Legacy Confluence class for backward compatibility
class Confluence(LegacyConfluenceBase):
    """Legacy Confluence class for backward compatibility."""

    def __new__(cls, url, *args, **kwargs):
        api_version = kwargs.get("api_version")
        # Scoped API tokens use the Atlassian API gateway and only support the
        # Cloud v2 endpoints. Route gateway URLs there automatically so callers
        # do not have to know the internal client split.
        if api_version in (1, 2) or ConfluenceBase._is_api_gateway_url(url):
            from .cloud.cloud import ConfluenceCloud as VersionedConfluenceCloud

            return VersionedConfluenceCloud(url, *args, **kwargs)
        return super().__new__(cls)

    def __init__(self, url, *args, **kwargs):
        if type(self) is not Confluence:
            return
        if kwargs.get("api_version") == "cloud":
            warnings.warn(
                "api_version='cloud' is deprecated; use cloud=True, or " "ConfluenceV2 for the Cloud V2 API.",
                DeprecationWarning,
                stacklevel=2,
            )
            kwargs.pop("api_version")
            kwargs["cloud"] = True
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
            impl = LegacyConfluenceCloud(url, *args, **kwargs)
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

# ``ConfluenceCloud`` is the established Cloud REST client.  The separate v2
# implementation is intentionally exported as ``atlassian.ConfluenceV2``.
ConfluenceCloud = LegacyConfluenceCloud
