# coding=utf-8
"""
Tempo Cloud API base class.
"""

from ...rest_client import AtlassianRestAPI


class TempoCloudBase(AtlassianRestAPI):
    """
    Base class for Tempo Cloud API operations.
    """

    def __init__(self, url, *args, **kwargs):
        super(TempoCloudBase, self).__init__(url, *args, **kwargs)

    def _sub_url(self, url):
        """
        Get the full url from a relative one.

        :param url: string: The sub url
        :return: The absolute url
        """
        return self.url_joiner(self.url, url)

    @property
    def _new_session_args(self):
        """
        Get the kwargs for new objects (session, root, version,...).

        :return: A dict with the kwargs for new objects
        """
        return {
            "session": self._session,
            "cloud": self.cloud,
            "api_root": self.api_root,
            "api_version": self.api_version,
        }
