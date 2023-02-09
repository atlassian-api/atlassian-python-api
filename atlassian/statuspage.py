# coding=utf-8
import logging
from enum import Enum
from typing import TypedDict

from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Branding(Enum):
    """The main template your statuspage will use"""
    PREMIUM = "premium"
    BASIC = "basic"


class StatusPage(AtlassianRestAPI):
    """StatusPage API wrapper."""

    def __init__(self, *args, **kwargs):
        super(StatusPage, self).__init__(*args, **kwargs)

    def list_pages(self):
        """
        Get a list of pages

        Notes
        -----
        Available fields: https://developer.statuspage.io/#operation/getPages

        Returns
        -------
        any
        """
        url = "v1/pages"
        return self.get(url)

    def get_page(self, page_id: str):
        """
        Get page information

        Parameters
        ----------
        page_id : str
            Your page unique ID

        Notes
        -----
        Available fields: https://developer.statuspage.io/#operation/getPagesPageId

        Returns
        -------
        any
        """
        url = "v1/pages/{}".format(page_id)
        return self.get(url)

    def update_page(self,
                    page_id: str,
                    page: dict[str, any]):
        """
        Update a page

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page : dict[str,any]
            Your page values that you want to change

        Notes
        -----
        Available fields: https://developer.statuspage.io/#operation/patchPagesPageId

        Returns
        -------
        any
        """
        url = "v1/pages/{}".format(page_id)
        return self.put(url, data={'page': page})
