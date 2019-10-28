# coding=utf-8
import logging

from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class MarketPlace(AtlassianRestAPI):
    """Marketplace API wrapper.
    """

    def get_plugins_info(self, limit=10, offset=10):
        """
        Provide plugins info
        :param limit:
        :param offset:
        :return:
        """
        params = {}
        if offset:
            params['offset'] = offset
        if limit:
            params['limit'] = limit
        url = 'rest/1.0/plugins'
        return (self.get(url, params=params) or {}).get('plugins')

    def get_vendors_info(self, limit=10, offset=10):
        """
        Provide vendors info
        :param limit:
        :param offset:
        :return:
        """
        params = {}
        if offset:
            params['offset'] = offset
        if limit:
            params['limit'] = limit
        url = 'rest/1.0/vendors'
        return (self.get(url, params=params) or {}).get('vendors')

    def get_application_info(self, limit=10, offset=10):
        """
        Information about applications
        :param limit:
        :param offset:
        :return:
        """
        params = {}
        if offset:
            params['offset'] = offset
        if limit:
            params['limit'] = limit
        url = 'rest/2/applications'
        return self.get(url, params=params)
