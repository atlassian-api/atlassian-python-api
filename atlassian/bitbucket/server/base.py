# coding=utf-8
import copy

from pprint import PrettyPrinter

from ..base import BitbucketBase


class BitbucketServerBase(BitbucketBase):
    def __init__(self, url, *args, **kwargs):
        """
        Init the rest api wrapper
        :param url:       The base url used for the rest api.
        :param *args:     The fixed arguments for the AtlassianRestApi.
        :param **kwargs:  The keyword arguments for the AtlassianRestApi.

        :return: nothing
        """
        self.__can_delete = kwargs.pop("can_delete", False)
        self.__can_update = kwargs.pop("can_update", False)
        if "data" in kwargs:
            self.__data = kwargs.pop("data")
        if url is None and "links" in self.__data:
            url = self.get_link("self")[0]
        super(BitbucketServerBase, self).__init__(url, *args, **kwargs)

    def __str__(self):
        return PrettyPrinter(indent=4).pformat(self.__data)

    def _sub_url(self, url):
        return self.url_joiner(self.url, url)

    def _get_paged(self, url, params=None, data=None, flags=None, trailing=False, absolute=False):
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

            values = response.get("values", [])
            if not response.get("size", -1) == len(values):
                raise AssertionError(
                    "Wrong response for url [{}], the size attribute doesn't match the number of recieved values:\n{}".format(
                        self.url, response
                    )
                )

            for value in values:
                yield value

            if response.get("nextPageStart") is None:
                break
            params["start"] = response.get("nextPageStart")

        return

    def update(self, **kwargs):
        """
        Update the data. Fields not present in the request body are ignored.

        :return: True if the update was successful
        """
        if self.__can_update == False:
            raise NotImplementedError("Update not implemented for this object type.")
        data = self.put(None, data=kwargs)
        if "errors" in data:
            return
        self.__data = data

        return True

    def delete(self):
        """
        Delete the element.

        :return: True if delete was successful
        """
        if self.__can_delete == False:
            raise NotImplementedError("Delete not implemented for this object type.")
        data = super(BitbucketServerBase, self).delete(None)
        if "errors" in data:
            return
        return True

    @property
    def data(self):
        return copy.copy(self.__data)

    def get_data(self, id):
        return copy.copy(self.__data[id])

    def get_link(self, link):
        return [x["href"] for x in self.__data["links"][link]]
