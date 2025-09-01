# coding=utf-8

import logging

from ..base import ConfluenceBase

log = logging.getLogger(__name__)


class ConfluenceServerBase(ConfluenceBase):
    """
    Base class for Confluence Server API operations.
    """

    def __init__(self, url, *args, **kwargs):
        """
        Init the rest api wrapper

        :param url: string:    The base url used for the rest api.
        :param *args: list:    The fixed arguments for the AtlassianRestApi.
        :param **kwargs: dict: The keyword arguments for the AtlassianRestApi.

        :return: nothing
        """
        super(ConfluenceServerBase, self).__init__(url, *args, **kwargs)

    def _get_paged(
        self,
        url,
        params=None,
        data=None,
        flags=None,
        trailing=False,
        absolute=False,
    ):
        """
        Used to get the paged data for Confluence Server

        :param url: string:                        The url to retrieve
        :param params: dict (default is None):     The parameter's
        :param data: dict (default is None):       The data
        :param flags: string[] (default is None):  The flags
        :param trailing: bool (default is None):   If True, a trailing slash is added to the url
        :param absolute: bool (default is False):  If True, the url is used absolute and not relative to the root

        :return: A generator object for the data elements
        """
        if params is None:
            params = {}

        while True:
            response = self.get(
                url,
                trailing=trailing,
                params=params,
                data=data,
                flags=flags,
                absolute=absolute,
            )
            if "results" not in response:
                return

            yield from response.get("results", [])

            # Confluence Server uses _links.next.href for pagination
            if response.get("_links", {}).get("next") is None:
                break
            # For server, we need to extract the next page URL from the _links.next.href
            next_url = response.get("_links", {}).get("next", {}).get("href")
            if next_url is None:
                break
            url = next_url
            absolute = True
            params = {}
            trailing = False

        return
