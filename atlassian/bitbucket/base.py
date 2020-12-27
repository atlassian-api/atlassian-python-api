# coding=utf-8

from datetime import datetime
from ..rest_client import AtlassianRestAPI


class BitbucketBase(AtlassianRestAPI):
    CONF_TIMEFORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
    bulk_headers = {"Content-Type": "application/vnd.atl.bitbucket.bulk+json"}

    def __init__(self, url, *args, **kwargs):
        """
        Init the rest api wrapper
        :param url:       The base url used for the rest api.
        :param *args:     The fixed arguments for the AtlassianRestApi.
        :param **kwargs:  The fixed arguments for the AtlassianRestApi.

        :return: nothing
        """
        self.timeformat_lambda = kwargs.pop("timeformat_lambda", lambda x: self._default_timeformat_lambda(x))
        self._check_timeformat_lambda()
        super(BitbucketBase, self).__init__(url, *args, **kwargs)

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

    def _check_timeformat_lambda(self):
        LAMBDA = lambda: 0  # noqa: E731
        if self.timeformat_lambda is None or (
            isinstance(self.timeformat_lambda, type(LAMBDA)) and self.timeformat_lambda.__name__ == LAMBDA.__name__
        ):
            return True
        else:
            ValueError("Expected [None] or [lambda function] for argument [timeformat_func]")

    @staticmethod
    def _default_timeformat_lambda(timestamp):
        return timestamp if isinstance(timestamp, datetime) else None

    def get_time(self, id):
        value_str = self.get_data(id)
        if self.timeformat_lambda is None:
            return value_str

        if isinstance(value_str, str):
            value = datetime.strptime(value_str, self.CONF_TIMEFORMAT)
        else:
            value = value_str

        return self.timeformat_lambda(value)

    @property
    def _new_session_args(self):
        return dict(
            session=self._session,
            cloud=self.cloud,
            api_root=self.api_root,
            api_version=self.api_version,
            timeformat_lambda=self.timeformat_lambda,
        )
