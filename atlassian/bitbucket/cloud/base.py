# coding=utf-8
import copy
from pprint import PrettyPrinter

from ..base import BitbucketBase


class BitbucketCloudBase(BitbucketBase):
    def __init__(self, url, link="self", *args, **kwargs):
        """
        Init the rest api wrapper
        :param url:       The base url used for the rest api.
        :param link:      Attribute to resolve a url based on input data. If None, no tries to receive an url from input data
        :param *args:     The fixed arguments for the AtlassianRestApi.
        :param **kwargs:  The keyword arguments for the AtlassianRestApi.

        :return: nothing
        """
        if "data" in kwargs:
            self.__data = kwargs.pop("data")
            expected_type = kwargs.pop("expected_type")
            if not self.get_data("type") == expected_type:
                raise ValueError(
                    "Expected type of data is [{}], got [{}].".format(expected_type, self.get_data("type"))
                )
        if url is None and link is not None:
            url = self.get_link(link)

        super(BitbucketCloudBase, self).__init__(url, *args, **kwargs)

    def __str__(self):
        return PrettyPrinter(indent=4).pformat(self.__data)

    def _get_paged(self, url, params=None, data=None, flags=None, trailing=None, absolute=False):
        """
        Used to get the paged data
        :param url:       The url to retrieve.
        :param params:    The parameters (optional).
        :param data:      The data (optional).
        :param flags:     The flags (optional).
        :param trailing:  If True, a trailing slash is added to the url (optional).
        :param absolute:  If True, the url is used absolute and not relative to the root (optional).

        :return: A generator for the project objects
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

    def update(self, **kwargs):
        """
        Fields not present in the request body are ignored.
        """
        self.__data = super(BitbucketBase, self).put(None, data=kwargs)
        return self

    @property
    def data(self):
        return copy.copy(self.__data)

    def get_data(self, id, default=None):
        return copy.copy(self.__data[id]) if id in self.__data else default

    def get_link(self, link):
        return self.__data["links"][link]["href"]
