"""
Module for Confluence Server API implementation
"""

import logging
from typing import Any, Dict, List, Optional, Union

from ..base import ConfluenceBase

log = logging.getLogger(__name__)


class ConfluenceServer(ConfluenceBase):
    """
    Confluence Server API implementation class
    """

    def __init__(self, url: str, *args, **kwargs):
        """
        Initialize the ConfluenceServer instance

        Args:
            url: Confluence Server base URL
            *args: Variable length argument list passed to ConfluenceBase
            **kwargs: Keyword arguments passed to ConfluenceBase
        """
        # Server only supports v1
        kwargs.setdefault("api_version", 1)
        super(ConfluenceServer, self).__init__(url, *args, **kwargs)
