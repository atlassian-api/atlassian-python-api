"""
Confluence module for both Cloud and Server implementations
"""

from typing import Union

from .base import ConfluenceBase
from .cloud import ConfluenceCloud
from .server import ConfluenceServer


def Confluence(url: str, *args, **kwargs) -> Union[ConfluenceCloud, ConfluenceServer]:
    """
    Factory function to create appropriate Confluence instance based on URL

    Args:
        url: The Confluence instance URL
        *args: Arguments to pass to the implementation
        **kwargs: Keyword arguments to pass to the implementation

    Returns:
        Either ConfluenceCloud or ConfluenceServer instance
    """
    if ConfluenceBase._is_cloud_url(url):
        return ConfluenceCloud(url, *args, **kwargs)
    return ConfluenceServer(url, *args, **kwargs)


__all__ = ["Confluence", "ConfluenceBase", "ConfluenceCloud", "ConfluenceServer"]
