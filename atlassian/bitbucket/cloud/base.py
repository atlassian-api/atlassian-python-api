# coding=utf-8

from ..base import BitbucketBase


class BitbucketCloudBase(BitbucketBase):
    def __init__(self, url, *args, **kwargs):
        """
        Init the rest api wrapper
        :param url:       The base url used for the rest api.
        :param *args:     The fixed arguments for the AtlassianRestApi.
        :param **kwargs:  The fixed arguments for the AtlassianRestApi.

        :return: nothing
        """
        super(BitbucketCloudBase, self).__init__(url, *args, **kwargs)

    def _get_paged(self, url, params={}, data=None, flags=None, trailing=None, absolute=False):
        """
        Used to get the paged data
        :param url:       The url to retrieve.
        :param params:    The parameters (optional).
        :param data:      The data (optional).

        :return: nothing
        """

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
