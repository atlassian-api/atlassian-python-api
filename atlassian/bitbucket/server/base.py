# coding=utf-8

from ..base import BitbucketBase


class BitbucketServerBase(BitbucketBase):
    def get_link(self, link):
        """
        Get a link from the data.

        :param link: string: The link identifier

        :return: The requested list of links or None if it isn't present
        """
        links = self.get_data("links")
        if links is None or link not in links:
            return None
        return [x["href"] for x in links[link]]

    def _get_paged(self, url, params=None, data=None, flags=None, trailing=False, absolute=False):
        """
        Used to get the paged data

        :param url: string:                        The url to retrieve
        :param params: dict (default is None):     The parameters
        :param data: dict (default is None):       The data
        :param flags: string[] (default is None):  The flags
        :param trailing: bool (default is None):   If True, a trailing slash is added to the url
        :param absolute: bool (default is False):  If True, the url is used absolute and not relative to the root

        :return: A generator object for the data elements
        """
        if params is None:
            params = {}

        while True:
            response = super(BitbucketServerBase, self).get(
                url,
                trailing=trailing,
                params=params,
                data=data,
                flags=flags,
                absolute=absolute,
            )
            if "values" not in response:
                return

            for value in response.get("values", []):
                yield value

            if response.get("nextPageStart") is None:
                break
            params["start"] = response.get("nextPageStart")

        return
