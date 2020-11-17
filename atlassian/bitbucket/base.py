# coding=utf-8
import copy

from pprint import PrettyPrinter

from ..rest_client import AtlassianRestAPI


class BitbucketBase(AtlassianRestAPI):
    def __init__(self, url, *args, **kwargs):
        """
        Init the rest api wrapper
        :param url:       The base url used for the rest api.
        :param *args:     The fixed arguments for the AtlassianRestApi.
        :param **kwargs:  The fixed arguments for the AtlassianRestApi.

        :return: nothing
        """
        if "data" in kwargs:
            self.__data = kwargs.pop("data")
            expected_type = kwargs.pop("expected_type")
            if not self.get_data("type") == expected_type:
                raise ValueError(
                    "Expected type of data is [{}], got [{}].".format(expected_type, self.get_data("type"))
                )
        if url is None:
            url = self.get_link("self")
        super(BitbucketBase, self).__init__(url, *args, **kwargs)

    def __str__(self):
        return PrettyPrinter(indent=4).pformat(self.__data)

    def _get_paged(self, url, params={}, data=None, flags=None, trailing=None, absolute=False):
        """
        Used to get the paged data
        :param url:       The url to retrieve.
        :param params:    The parameters (optional).
        :param data:      The data (optional).

        :return: nothing
        """

        while True:
            response = self.get(url, trailing=trailing, params=params, data=data, flags=flags, absolute=absolute)
            if "values" not in response:
                return

            for value in response.get("values", []):
                yield value

            if self.cloud:
                url = response.get("next")
                if url is None:
                    break
                # From now on we have absolute URLs
                absolute = True
            else:
                if response.get("nextPageStart") is None:
                    break
                params["start"] = response.get("nextPageStart")

        return

    @property
    def _new_session_args(self):
        return dict(
            session=self._session,
            cloud=self.cloud,
            api_root=self.api_root,
            api_version=self.api_version,
        )

    @property
    def data(self):
        return copy.copy(self.__data)

    def get_data(self, id):
        return copy.copy(self.__data[id])

    def get_link(self, link):
        return self.__data["links"][link]["href"]
