"""Shared Requirement Yogi client infrastructure."""

from ..rest_client import AtlassianRestAPI


class YogiBase(AtlassianRestAPI):
    """Base client for Requirement Yogi REST APIs."""

    def __init__(self, url, *args, **kwargs):
        """Create a client using ``url`` as the Requirement Yogi API base URL."""
        super(YogiBase, self).__init__(url.rstrip("/"), *args, **kwargs)
