# coding=utf-8

import copy
import re
import sys

from datetime import datetime
from pprint import PrettyPrinter
from ..rest_client import AtlassianRestAPI

RE_TIMEZONE = re.compile(r"(\d{2}):(\d{2})$")


class BitbucketBase(AtlassianRestAPI):
    CONF_TIMEFORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
    bulk_headers = {"Content-Type": "application/vnd.atl.bitbucket.bulk+json"}

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
        self.timeformat_lambda = kwargs.pop("timeformat_lambda", lambda x: self._default_timeformat_lambda(x))
        self._check_timeformat_lambda()
        super(BitbucketBase, self).__init__(url, *args, **kwargs)

    def __str__(self):
        return PrettyPrinter(indent=4).pformat(self.__data if self.__data else self)

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
            response = self.get(
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

            if self.cloud:
                url = response.get("next")
                if url is None:
                    break
                # From now on we have absolute URLs with parameters
                absolute = True
                # Params are now provided by the url
                params = {}
                # Trailing should not be added as it is already part of the url
                trailing = False
            else:
                if response.get("nextPageStart") is None:
                    break
                params["start"] = response.get("nextPageStart")

        return

    @staticmethod
    def _default_timeformat_lambda(timestamp):
        """
        Default time format function.

        :param timestamp: datetime str: The datetime object of the parsed string or the raw value if parsing failed

        :return: timestamp if it was a datetime object, else None
        """
        return timestamp if isinstance(timestamp, datetime) else None

    def _check_timeformat_lambda(self):
        """
        Check the lambda for the time format. Raise an exception if the value is wrong
        """
        LAMBDA = lambda: 0  # noqa: E731
        if self.timeformat_lambda is None or (
            isinstance(self.timeformat_lambda, type(LAMBDA)) and self.timeformat_lambda.__name__ == LAMBDA.__name__
        ):
            return True
        else:
            ValueError("Expected [None] or [lambda function] for argument [timeformat_func]")

    def _sub_url(self, url):
        """
        Get the full url from a relative one.

        :param url: string: The sub url

        :return: The absolute url
        """
        return self.url_joiner(self.url, url)

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

    def get_time(self, id):
        """
        Return the time value with the expected format.

        :param id: string: The id for the time data

        :return: The time with the configured format, see timeformat_lambda.
        """
        value_str = self.get_data(id)
        if self.timeformat_lambda is None:
            return value_str

        if isinstance(value_str, str):
            # The format contains a : in the timezone which is supported from 3.7 on.
            if sys.version_info <= (3, 7):
                value_str = RE_TIMEZONE.sub(r"\1\2", value_str)
            value = datetime.strptime(value_str, self.CONF_TIMEFORMAT)
        else:
            value = value_str

        return self.timeformat_lambda(value)

    def _update_data(self, data):
        """
        Internal function to update the data.

        :param data: dict: The new data.

        :return: The updated object
        """
        self.__data = data

        return self

    @property
    def _new_session_args(self):
        """
        Get the kwargs for new objects (session, root, version,...).

        :return: A dict with the kwargs for new objects
        """
        return dict(
            session=self._session,
            cloud=self.cloud,
            api_root=self.api_root,
            api_version=self.api_version,
            timeformat_lambda=self.timeformat_lambda,
        )
