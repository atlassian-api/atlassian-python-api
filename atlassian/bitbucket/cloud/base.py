# coding=utf-8

from ..base import BitbucketBase


class BitbucketCloudBase(BitbucketBase):
    def __init__(self, url, *args, **kwargs):
        """
        Init the rest api wrapper

        :param url: string:    The base url used for the rest api.
        :param *args: list:    The fixed arguments for the AtlassianRestApi.
        :param **kwargs: dict: The keyword arguments for the AtlassianRestApi.

        :return: nothing
        """
        expected_type = kwargs.pop("expected_type", None)
        super(BitbucketCloudBase, self).__init__(url, *args, **kwargs)
        if expected_type is not None and not expected_type == self.get_data("type"):
            raise ValueError("Expected type of data is [{}], got [{}].".format(expected_type, self.get_data("type")))

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

    def _get_paged(self, url, params=None, data=None, flags=None, trailing=None, absolute=False):
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
            response = super(BitbucketCloudBase, self).get(
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

            url = response.get("next")
            if url is None:
                break
            # From now on we have absolute URLs
            absolute = True

        return
