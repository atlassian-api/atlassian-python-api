# coding=utf-8

from ..rest_client import AtlassianRestAPI


class BitbucketBase(AtlassianRestAPI):
    bulk_headers = {"Content-Type": "application/vnd.atl.bitbucket.bulk+json"}

    def __init__(self, url, *args, **kwargs):
        """
        Init the rest api wrapper
        :param url:       The base url used for the rest api.
        :param *args:     The fixed arguments for the AtlassianRestApi.
        :param **kwargs:  The fixed arguments for the AtlassianRestApi.

        :return: nothing
        """
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

            values = response.get("values", [])
            if not response.get("size", -1) == len(values):
                raise AssertionError(
                    "Wrong response for url [{}], the size attribute doesn't match the number of recieved values:\n{}".format(
                        self.url, response
                    )
                )

            for value in values:
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
