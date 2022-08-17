# coding=utf-8
import logging

from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)

ADMIN_URL = "https://api.atlassian.com"


class CloudAdminOrgs(AtlassianRestAPI):
    def __init__(self, admin_api_key, *args, **kwargs):
        kwargs["token"] = admin_api_key
        kwargs["api_root"] = "admin"
        kwargs["api_version"] = "v1"
        super(CloudAdminOrgs, self).__init__(url=ADMIN_URL, *args, **kwargs)

    def get_organizations(self):
        url = self.resource_url("orgs")
        return self.get(url)


class CloudAdminUsers(AtlassianRestAPI):
    def __init__(self, admin_api_key, *args, **kwargs):
        kwargs["token"] = admin_api_key
        kwargs["api_root"] = "users"
        kwargs["api_version"] = None
        super(CloudAdminUsers, self).__init__(ADMIN_URL, *args, **kwargs)

    def get_profile(self, account_id):
        url = self.resource_url("{}/manage/profile".format(account_id))
        return self.get(url)
