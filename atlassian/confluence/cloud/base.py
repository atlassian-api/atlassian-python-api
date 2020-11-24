# coding=utf-8

from ..base import ConfluenceBase


class ConfluenceCloudBase(ConfluenceBase):
    def __init__(self, url, *args, **kwargs):
        """
        Init the rest api wrapper
        :param url:       The base url used for the rest api.
        :param *args:     The fixed arguments for the AtlassianRestApi.
        :param **kwargs:  The fixed arguments for the AtlassianRestApi.

        :return: nothing
        """
        super(ConfluenceCloudBase, self).__init__(url, *args, **kwargs)
