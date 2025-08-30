# coding=utf-8

import logging
from requests import HTTPError

from ..base import ConfluenceBase

log = logging.getLogger(__name__)


class ConfluenceCloudBase(ConfluenceBase):
    """
    Base class for Confluence Cloud API operations.
    """

    def __init__(self, url, *args, **kwargs):
        """
        Init the rest api wrapper

        :param url: string:    The base url used for the rest api.
        :param *args: list:    The fixed arguments for the AtlassianRestApi.
        :param **kwargs: dict: The keyword arguments for the AtlassianRestApi.

        :return: nothing
        """
        super(ConfluenceCloudBase, self).__init__(url, *args, **kwargs)

    def raise_for_status(self, response):
        """
        Checks the response for errors and throws an exception if return code >= 400

        Implementation for Confluence Cloud according to
        https://developer.atlassian.com/cloud/confluence/rest/v2/intro/#about

        :param response:
        :return:
        """
        if 400 <= response.status_code < 600:
            try:
                j = response.json()
                if "message" in j:
                    error_msg = j["message"]
                    if "detail" in j:
                        error_msg = f"{error_msg}\n{str(j['detail'])}"
                else:
                    error_msg = f"HTTP {response.status_code}: {response.reason}"
            except Exception as e:
                log.error(e)
                response.raise_for_status()
            else:
                raise HTTPError(error_msg, response=response)
        else:
            response.raise_for_status()

    def _get_paged(
        self,
        url,
        params=None,
        data=None,
        flags=None,
        trailing=None,
        absolute=False,
    ):
        """
        Used to get the paged data for Confluence Cloud

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

            # Confluence Cloud uses _links.next.href for pagination
            url = response.get("_links", {}).get("next", {}).get("href")
            if url is None:
                break
            # From now on we have absolute URLs with parameters
            absolute = True
            # Params are now provided by the url
            params = {}
            # Trailing should not be added as it is already part of the url
            trailing = False

        return
