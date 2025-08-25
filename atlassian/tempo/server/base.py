# coding=utf-8
"""
Tempo Server API base class.
"""

from ...rest_client import AtlassianRestAPI


class TempoServerBase(AtlassianRestAPI):
    """
    Base class for Tempo Server API operations.
    """

    def __init__(self, url, *args, **kwargs):
        super(TempoServerBase, self).__init__(url, *args, **kwargs)

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

    def _call_parent_method(self, method_name, *args, **kwargs):
        """
        Call a method on the parent class.

        :param method_name: The name of the method to call
        :param args: Arguments to pass to the method
        :param kwargs: Keyword arguments to pass to the method
        :return: The result of the method call
        """
        method = getattr(super(), method_name)
        return method(*args, **kwargs)
