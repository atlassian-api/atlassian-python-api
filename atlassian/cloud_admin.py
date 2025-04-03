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
        """
        Returns a list of your organizations (based on your API key).
        :return:
        """
        url = self.resource_url("orgs")
        return self.get(url)

    def get_organization(self, org_id):
        """
        Returns information about a single organization by ID
        :param org_id:
        :return:
        """
        url = self.resource_url(f"orgs/{org_id}")
        return self.get(url)

    def get_managed_accounts_in_organization(self, org_id, cursor=None):
        """
        Returns a list of accounts managed by the organization
        :param org_id:
        :param cursor:
        :return:
        """
        url = self.resource_url(f"orgs/{org_id}/users")
        params = {}
        if cursor:
            params["cursor"] = cursor
        return self.get(url, params=params)

    def search_users_in_organization(
        self,
        org_id,
        account_ids=None,
        account_types=None,
        account_statuses=None,
        name_or_nicknames=None,
        email_usernames=None,
        email_domains=None,
        is_suspended=None,
        cursor=None,
        limit=10000,
        expand=None,
    ):
        """
        Returns a list of accounts in the organization that match the search criteria.
        The API is available for customers using the new user management experience only.
        How the new user management experience works
        Returns a list of users within an organization,
        offering search functionality through multiple parameters for more precise results.
        :param org_id:
        :param account_ids: Unique ID of the users account. The format is [a-zA-Z0-9_|-:]{1,128}
        :param account_types: The type of account Valid values: atlassian, customer, app
        :param account_statuses: The lifecycle status of the account
        :param name_or_nicknames:
        :param email_usernames:
        :param email_domains:
        :param is_suspended: Suspended users with no access. This is independent of the user account status
        :param cursor: Starting point marker for page result retrieval
        :param limit: The number of items to return. Default = max = 10000
        :param expand: Valid values: NAME, EMAIL, EMAIL_VERIFIED, PRODUCT_LAST_ACCESS, GROUPS
        :return:
        """

        url = self.resource_url(f"orgs/{org_id}/users/search")
        params = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        if account_ids:
            params["accountIds"] = account_ids
        if account_types:
            params["accountTypes"] = account_types
        if account_statuses:
            params["accountStatuses"] = account_statuses
        if name_or_nicknames:
            params["nameOrNicknames"] = name_or_nicknames
        if email_usernames:
            params["emailUsernames"] = email_usernames
        if email_domains:
            params["emailDomains"] = email_domains
        if is_suspended:
            params["isSuspended"] = is_suspended
        if expand:
            params["expand"] = expand

        return self.get(url, params=params)


class CloudAdminUsers(AtlassianRestAPI):
    def __init__(self, admin_api_key, *args, **kwargs):
        kwargs["token"] = admin_api_key
        kwargs["api_root"] = "users"
        kwargs["api_version"] = None
        super(CloudAdminUsers, self).__init__(ADMIN_URL, *args, **kwargs)

    def get_profile(self, account_id):
        url = self.resource_url(f"{account_id}/manage/profile")
        return self.get(url)
