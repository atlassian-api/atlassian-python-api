# coding=utf-8

import logging

from ..base import ConfluenceBase

log = logging.getLogger(__name__)


class ConfluenceServerBase(ConfluenceBase):
    """
    Base class for Confluence Server API operations.
    """

    def __init__(self, url, *args, **kwargs):
        """
        Init the rest api wrapper

        :param url: string:    The base url used for the rest api.
        :param *args: list:    The fixed arguments for the AtlassianRestApi.
        :param **kwargs: dict: The keyword arguments for the AtlassianRestApi.

        :return: nothing
        """
        super(ConfluenceServerBase, self).__init__(url, *args, **kwargs)


