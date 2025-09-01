# coding=utf-8

import copy
import logging
from requests import HTTPError
from ..rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class ConfluenceBase(AtlassianRestAPI):
    """
    Base class for Confluence API operations.
    """

    def __init__(self, url, *args, **kwargs):
        """
        Init the rest api wrapper

        :param url: string:    The base url used for the rest api.
        :param *args: list:    The fixed arguments for the AtlassianRestApi.
        :param **kwargs: dict: The keyword arguments for the AtlassianRestApi.

        :return: nothing
        """
        self._update_data(kwargs.pop("data", {}))
        if url is None:
            url = self.get_link("self")
            if isinstance(url, list):  # Server has a list of links
                url = url[0]
        super().__init__(url, *args, **kwargs)

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

    def _update_data(self, data):
        """
        Internal function to update the data.

        :param data: dict: The new data.
        :return: The updated object
        """
        self.__data = data
        return self

    @property
    def data(self):
        """
        Get the internal cached data. For data integrity a deep copy is returned.

        :return: A copy of the data cache
        """
        return copy.copy(self.__data)

    def get_data(self, id, default=None):
        """
        Get a data element from the internal data cache. For data integrity a deep copy is returned.
        If data isn't present, the default value is returned.

        :param id: string:                     The data element to return
        :param default: any (default is None): The value to return if id is not present

        :return: The requested data element
        """
        return copy.copy(self.__data[id]) if id in self.__data else default

    def get_link(self, link):
        """
        Get a link from the data.

        :param link: string: The link identifier
        :return: The requested link or None if it isn't present
        """
        links = self.get_data("links")
        if links is None or link not in links:
            return None
        return links[link]["href"]

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
        Used to get the paged data

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

            if self.cloud:
                url = response.get("_links", {}).get("next", {}).get("href")
                if url is None:
                    break
                # From now on we have absolute URLs with parameters
                absolute = True
                # Params are now provided by the url
                params = {}
                # Trailing should not be added as it is already part of the url
                trailing = False
            else:
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

    def raise_for_status(self, response):
        """
        Checks the response for errors and throws an exception if return code >= 400

        Implementation for Confluence Server according to
            https://developer.atlassian.com/server/confluence/rest/v1002/intro/#about
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
