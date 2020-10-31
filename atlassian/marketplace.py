# coding=utf-8
import logging

from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class MarketPlace(AtlassianRestAPI):
    """Marketplace API wrapper."""

    def get_plugins_info(self, limit=10, offset=10):
        """
        Provide plugins info
        :param limit:
        :param offset:
        :return:
        """
        params = {}
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        url = "rest/1.0/plugins"
        return (self.get(url, params=params) or {}).get("plugins")

    def get_vendors_info(self, limit=10, offset=10):
        """
        Provide vendors info
        :param limit:
        :param offset:
        :return:
        """
        params = {}
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        url = "rest/1.0/vendors"
        return (self.get(url, params=params) or {}).get("vendors")

    def get_application_info(self, limit=10, offset=10):
        """
        Information about applications
        :param limit:
        :param offset:
        :return:
        """
        params = {}
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        url = "rest/2/applications"
        return self.get(url, params=params)

    def get_app_versions(self, add_on_key, application=None):
        """
        Get a list of versions for the specified app.
        :param add_on_key: The unique identifier for this app,
                            for example "com.atlassian.confluence.plugins.confluence-questions"
        :param application: Only returns apps compatible with this application
        :return:
        """
        params = {}
        if application:
            params["application"] = application
        url = "rest/2/addons/{addonKey}/versions".format(addonKey=add_on_key)
        return self.get(url, params=params)

    def get_app_reviews(self, add_on_key, sort=None):
        """
        Get a list of reviews for the specified app.
        :param add_on_key: The unique identifier for this app,
                            for example "com.atlassian.confluence.plugins.confluence-questions"
        :param sort: Specifies the review sort order
                     Valid values: helpful, recent
        :return:
        """
        url = "rest/2/addons/{addonKey}/reviews".format(addonKey=add_on_key)
        params = {}
        if sort:
            params["sort"] = sort
        return self.get(url, params=params)
