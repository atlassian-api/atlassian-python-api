# coding=utf-8
import logging

from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)

ADMIN_URL = "https://api.atlassian.com"


class CloudAdmin(AtlassianRestAPI):
    """Client for Atlassian Administration's organization APIs.

    This client is separate from product clients because it uses organization
    admin API keys and the ``api.atlassian.com/admin`` API surface.  API keys
    need the scopes required by each operation, such as ``read:orgs:admin``.
    """

    def __init__(self, admin_api_key, *args, **kwargs):
        kwargs["token"] = admin_api_key
        kwargs["api_root"] = "admin"
        kwargs["api_version"] = "v2"
        super(CloudAdmin, self).__init__(url=ADMIN_URL, *args, **kwargs)

    @staticmethod
    def _params(**kwargs):
        return {key: value for key, value in kwargs.items() if value is not None}

    def get_organizations(self, cursor=None):
        """Return organizations accessible to the admin API key."""
        return self.get("admin/v1/orgs", params=self._params(cursor=cursor))

    def get_organization(self, org_id):
        """Return one organization (requires ``read:orgs:admin``)."""
        return self.get(f"admin/v1/orgs/{org_id}")

    def get_directories(self, org_id, account_id=None, directory_ids=None, search_term=None, cursor=None, limit=None):
        """Return organization directories, optionally filtered or cursor-paged."""
        return self.get(
            f"admin/v2/orgs/{org_id}/directories",
            params=self._params(
                accountId=account_id, directoryIds=directory_ids, searchTerm=search_term, cursor=cursor, limit=limit
            ),
        )

    def search_directory_users(self, org_id, directory_id, data=None):
        """Search directory users with the V2 request body (for example ``searchTerm`` or ``emails``)."""
        return self.post(f"admin/v2/orgs/{org_id}/directories/{directory_id}/users/search", data=data or {})

    def get_directory_user(self, org_id, directory_id, user_id):
        """Return details for one directory user."""
        return self.get(f"admin/v2/orgs/{org_id}/directories/{directory_id}/users/{user_id}")

    def get_directory_users_count(self, org_id, directory_id):
        """Return the number of users in a directory."""
        return self.get(f"admin/v2/orgs/{org_id}/directories/{directory_id}/users/count")

    def get_groups(self, org_id, directory_id, cursor=None, limit=None, search_term=None):
        """Return groups in a directory."""
        return self.get(
            f"admin/v2/orgs/{org_id}/directories/{directory_id}/groups",
            params=self._params(cursor=cursor, limit=limit, searchTerm=search_term),
        )

    def search_directory_groups(self, org_id, directory_id, data=None):
        """Search groups in a directory using the V2 request-body filters."""
        return self.post(f"admin/v2/orgs/{org_id}/directories/{directory_id}/groups/search", data=data or {})

    def get_group(self, org_id, directory_id, group_id):
        """Return one directory group."""
        return self.get(f"admin/v2/orgs/{org_id}/directories/{directory_id}/groups/{group_id}")

    def get_domains(self, org_id, cursor=None, limit=None):
        """Return verified domains for an organization."""
        return self.get(f"admin/v2/orgs/{org_id}/domains", params=self._params(cursor=cursor, limit=limit))

    def get_domain(self, org_id, domain_id):
        """Return one verified domain."""
        return self.get(f"admin/v2/orgs/{org_id}/domains/{domain_id}")

    def get_events(self, org_id, cursor=None, limit=None):
        """Return organization audit events."""
        return self.get(f"admin/v2/orgs/{org_id}/events", params=self._params(cursor=cursor, limit=limit))

    def get_event(self, org_id, event_id):
        """Return one organization audit event."""
        return self.get(f"admin/v2/orgs/{org_id}/events/{event_id}")

    @staticmethod
    def _user_management_url(account_id, suffix=""):
        return f"{ADMIN_URL}/users/{account_id}/manage{suffix}"

    def get_user_management_permissions(self, account_id, privileges=None):
        """Return privileges the API key has for managing an account."""
        return self.get(
            self._user_management_url(account_id), absolute=True, params=self._params(privileges=privileges)
        )

    def get_user_profile(self, account_id):
        """Return an account profile through the User Management API."""
        return self.get(self._user_management_url(account_id, "/profile"), absolute=True)

    def update_user_profile(self, account_id, data):
        """Patch profile fields permitted by the account's ``profile.write`` privilege."""
        return self.patch(self._user_management_url(account_id, "/profile"), data=data, absolute=True)

    def set_user_email(self, account_id, email):
        """Set a managed user's verified email address and invalidate active sessions."""
        return self.put(self._user_management_url(account_id, "/email"), data={"email": email}, absolute=True)

    def get_user_api_tokens(self, account_id):
        """Return API tokens for a user when the API key has the required privilege."""
        return self.get(self._user_management_url(account_id, "/api-tokens"), absolute=True)

    def delete_user_api_token(self, account_id, token_id):
        """Revoke one user API token."""
        return self.delete(self._user_management_url(account_id, f"/api-tokens/{token_id}"), absolute=True)

    def deactivate_user(self, account_id, message=None):
        """Deactivate a managed account; an optional message is shown to the user."""
        data = self._params(message=message)
        return self.post(self._user_management_url(account_id, "/lifecycle/disable"), data=data, absolute=True)

    def activate_user(self, account_id):
        """Reactivate a deactivated managed account."""
        return self.post(self._user_management_url(account_id, "/lifecycle/enable"), data={}, absolute=True)

    def delete_user(self, account_id):
        """Schedule permanent deletion of a managed account after its grace period."""
        return self.post(self._user_management_url(account_id, "/lifecycle/delete"), data={}, absolute=True)

    def cancel_user_deletion(self, account_id):
        """Cancel deletion during its grace period and reactivate the account."""
        return self.post(self._user_management_url(account_id, "/lifecycle/cancel-delete"), data={}, absolute=True)

    @staticmethod
    def _scim_url(directory_id, resource=""):
        return f"{ADMIN_URL}/scim/directory/{directory_id}{resource}"

    def get_scim_users(self, directory_id, **params):
        """List SCIM users; pass SCIM filters such as ``filter`` or ``startIndex`` as keywords."""
        return self.get(self._scim_url(directory_id, "/Users"), absolute=True, params=self._params(**params))

    def get_scim_user(self, directory_id, user_id):
        """Return one SCIM user."""
        return self.get(self._scim_url(directory_id, f"/Users/{user_id}"), absolute=True)

    def create_scim_user(self, directory_id, data):
        """Create a SCIM user from a SCIM 2.0 User resource."""
        return self.post(self._scim_url(directory_id, "/Users"), data=data, absolute=True)

    def replace_scim_user(self, directory_id, user_id, data):
        """Replace a SCIM user with a complete User resource."""
        return self.put(self._scim_url(directory_id, f"/Users/{user_id}"), data=data, absolute=True)

    def patch_scim_user(self, directory_id, user_id, operations):
        """Apply SCIM PATCH operations to a user."""
        return self.patch(
            self._scim_url(directory_id, f"/Users/{user_id}"), data={"Operations": operations}, absolute=True
        )

    def delete_scim_user(self, directory_id, user_id):
        """Delete a user from the SCIM directory."""
        return self.delete(self._scim_url(directory_id, f"/Users/{user_id}"), absolute=True)

    def get_scim_groups(self, directory_id, **params):
        """List SCIM groups; pass SCIM filters as keyword arguments."""
        return self.get(self._scim_url(directory_id, "/Groups"), absolute=True, params=self._params(**params))

    def get_scim_group(self, directory_id, group_id):
        """Return one SCIM group."""
        return self.get(self._scim_url(directory_id, f"/Groups/{group_id}"), absolute=True)

    def create_scim_group(self, directory_id, data):
        """Create a SCIM group resource."""
        return self.post(self._scim_url(directory_id, "/Groups"), data=data, absolute=True)

    def replace_scim_group(self, directory_id, group_id, data):
        """Replace a SCIM group with a complete Group resource."""
        return self.put(self._scim_url(directory_id, f"/Groups/{group_id}"), data=data, absolute=True)

    def patch_scim_group(self, directory_id, group_id, operations):
        """Apply SCIM PATCH operations to a group, including membership changes."""
        return self.patch(
            self._scim_url(directory_id, f"/Groups/{group_id}"), data={"Operations": operations}, absolute=True
        )

    def delete_scim_group(self, directory_id, group_id):
        """Delete a SCIM group."""
        return self.delete(self._scim_url(directory_id, f"/Groups/{group_id}"), absolute=True)

    def get_scim_schemas(self, directory_id, schema_id=None):
        """Return all SCIM schemas or one schema by URN."""
        suffix = "/Schemas" if schema_id is None else f"/Schemas/{schema_id}"
        return self.get(self._scim_url(directory_id, suffix), absolute=True)

    def get_scim_service_provider_config(self, directory_id):
        """Return supported SCIM features for a directory."""
        return self.get(self._scim_url(directory_id, "/ServiceProviderConfig"), absolute=True)

    def get_scim_resource_types(self, directory_id, resource_type=None):
        """Return SCIM resource types, or a single User/Group resource type."""
        suffix = "/ResourceTypes" if resource_type is None else f"/ResourceTypes/{resource_type}"
        return self.get(self._scim_url(directory_id, suffix), absolute=True)

    def get_scim_links(self, org_id, account_id):
        """Return SCIM links for an Atlassian account."""
        return self.get(
            f"{ADMIN_URL}/admin/user-provisioning/v1/org/{org_id}/user/{account_id}/get-scim-links", absolute=True
        )

    def get_scim_links_for_email(self, org_id, email):
        """Return SCIM links associated with an email address."""
        return self.post(
            f"{ADMIN_URL}/admin/user-provisioning/v1/org/{org_id}/get-scim-links-for-email",
            data={"email": email},
            absolute=True,
        )

    def unlink_scim_user(self, org_id, directory_id, user_id):
        """Unlink a SCIM user from an Atlassian account without deleting either resource."""
        return self.patch(
            f"{ADMIN_URL}/admin/user-provisioning/v1/org/{org_id}/scimDirectoryId/{directory_id}/scimUserId/{user_id}/unlink",
            data={},
            absolute=True,
        )

    def delete_scim_user_from_database(self, org_id, account_id):
        """Delete only the SCIM database record; use only for repair workflows."""
        return self.delete(
            f"{ADMIN_URL}/admin/user-provisioning/v1/org/{org_id}/user/{account_id}/onlyDeleteUserInDB", absolute=True
        )

    @staticmethod
    def _dlp_url(org_id, suffix=""):
        return f"{ADMIN_URL}/admin/dlp/v1/orgs/{org_id}/classification-levels{suffix}"

    def get_classification_levels(self, org_id):
        """List DLP classification levels (``read:classification-levels:admin``)."""
        return self.get(self._dlp_url(org_id), absolute=True)

    def get_classification_level(self, org_id, level_id):
        """Return one DLP classification level."""
        return self.get(self._dlp_url(org_id, f"/{level_id}"), absolute=True)

    def create_classification_level(self, org_id, data):
        """Create a draft DLP classification level."""
        return self.post(self._dlp_url(org_id), data=data, absolute=True)

    def update_classification_level(self, org_id, level_id, data):
        """Replace/edit a DLP classification level."""
        return self.put(self._dlp_url(org_id, f"/{level_id}"), data=data, absolute=True)

    def publish_classification_levels(self, org_id, level_ids):
        """Publish one or more draft classification levels."""
        return self.post(self._dlp_url(org_id, "/publish"), data={"levelIds": level_ids}, absolute=True)

    def archive_classification_level(self, org_id, level_id):
        """Archive one classification level; published content becomes unclassified."""
        return self.post(self._dlp_url(org_id, "/archive"), data={"levelId": level_id}, absolute=True)

    def restore_classification_level(self, org_id, level_id):
        """Restore an archived classification level as a draft."""
        return self.post(self._dlp_url(org_id, "/restore"), data={"levelId": level_id}, absolute=True)

    def reorder_classification_levels(self, org_id, level_ids):
        """Set classification-level order; the most sensitive level ranks first."""
        return self.post(self._dlp_url(org_id, "/reorder"), data={"levelIds": level_ids}, absolute=True)

    @staticmethod
    def _control_url(org_id, suffix="", version="v2"):
        if version not in {"v1", "v2"}:
            raise ValueError("Control API version must be 'v1' or 'v2'")
        return f"{ADMIN_URL}/admin/control/{version}/orgs/{org_id}{suffix}"

    def get_control_policies(self, org_id, version="v2", **params):
        """List Admin Control policies (V2 by default)."""
        return self.get(self._control_url(org_id, "/policies", version), absolute=True, params=self._params(**params))

    def get_control_policy(self, org_id, policy_id, version="v2"):
        """Return one Admin Control policy."""
        return self.get(self._control_url(org_id, f"/policies/{policy_id}", version), absolute=True)

    def create_control_policy(self, org_id, data, version="v2"):
        """Create an Admin Control policy."""
        return self.post(self._control_url(org_id, "/policies", version), data=data, absolute=True)

    def update_control_policy(self, org_id, policy_id, data, version="v2"):
        """Replace an Admin Control policy."""
        return self.put(self._control_url(org_id, f"/policies/{policy_id}", version), data=data, absolute=True)

    def delete_control_policy(self, org_id, policy_id, version="v2"):
        """Delete an Admin Control policy."""
        return self.delete(self._control_url(org_id, f"/policies/{policy_id}", version), absolute=True)

    def publish_control_draft_policies(self, org_id, data=None):
        """Publish V2 draft policies; this applies pending organization controls."""
        return self.post(self._control_url(org_id, "/policies/publishDraftPolicies"), data=data or {}, absolute=True)

    def validate_control_policy(self, org_id, policy_id):
        """Validate a V1 policy without changing it."""
        return self.get(self._control_url(org_id, f"/policies/{policy_id}/validate", "v1"), absolute=True)

    def get_control_policy_resources(self, org_id, policy_id, version="v2"):
        """List resources associated with a policy."""
        return self.get(self._control_url(org_id, f"/policies/{policy_id}/resources", version), absolute=True)

    def add_control_policy_resource(self, org_id, policy_id, data, version="v2"):
        """Associate a resource with a policy."""
        return self.post(
            self._control_url(org_id, f"/policies/{policy_id}/resources", version), data=data, absolute=True
        )

    def delete_control_policy_resources(self, org_id, policy_id, version="v2"):
        """Remove all resources associated with a policy."""
        return self.delete(self._control_url(org_id, f"/policies/{policy_id}/resources", version), absolute=True)

    def update_control_policy_resource(self, org_id, policy_id, resource_id, data):
        """Update one V1 policy resource."""
        return self.put(
            self._control_url(org_id, f"/policies/{policy_id}/resources/{resource_id}", "v1"), data=data, absolute=True
        )

    def delete_control_policy_resource(self, org_id, policy_id, resource_id):
        """Remove one V1 policy resource."""
        return self.delete(
            self._control_url(org_id, f"/policies/{policy_id}/resources/{resource_id}", "v1"), absolute=True
        )

    def add_users_to_auth_policy(self, org_id, policy_id, data):
        """Start a V1 task assigning users to an authentication policy."""
        return self.post(
            self._control_url(org_id, f"/auth-policy/{policy_id}/add-users", "v1"), data=data, absolute=True
        )

    def get_auth_policy_task(self, org_id, task_id):
        """Return status for an asynchronous authentication-policy task."""
        return self.get(self._control_url(org_id, f"/auth-policy/task/{task_id}", "v1"), absolute=True)

    def get_users_auth_policies(self, org_id, data):
        """Return authentication-policy information for managed users in bulk."""
        return self.post(self._control_url(org_id, "/users/auth-policies/bulk-fetch", "v1"), data=data, absolute=True)

    @staticmethod
    def _api_access_url(org_id, suffix=""):
        return f"{ADMIN_URL}/admin/api-access/v1/orgs/{org_id}{suffix}"

    def get_org_api_tokens(self, org_id, **params):
        """List organization API tokens."""
        return self.get(self._api_access_url(org_id, "/api-tokens"), absolute=True, params=self._params(**params))

    def delete_org_api_tokens(self, org_id, data):
        """Delete organization API tokens selected by the API Access request body."""
        return self.delete(self._api_access_url(org_id, "/api-tokens"), data=data, absolute=True)

    def get_org_api_token_count(self, org_id):
        """Return API-token count for an organization."""
        return self.get(self._api_access_url(org_id, "/api-tokens/count"), absolute=True)

    def get_service_account_api_token_count(self, org_id, data):
        """Return service-account API-token count using the supplied filter body."""
        return self.post(self._api_access_url(org_id, "/service-accounts/count"), data=data, absolute=True)

    def get_service_account_api_tokens(self, org_id, account_id, **params):
        """List API tokens belonging to a service account."""
        return self.get(
            self._api_access_url(org_id, f"/service-accounts/{account_id}/api-tokens"),
            absolute=True,
            params=self._params(**params),
        )

    def delete_service_account_api_tokens(self, org_id, account_id, data):
        """Delete selected service-account API tokens."""
        return self.delete(
            self._api_access_url(org_id, f"/service-accounts/{account_id}/api-tokens"), data=data, absolute=True
        )

    def get_org_api_key_count(self, org_id):
        """Return API-key count for an organization."""
        return self.get(self._api_access_url(org_id, "/api-keys/count"), absolute=True)

    def get_org_api_keys(self, org_id, **params):
        """List API keys in an organization."""
        return self.get(self._api_access_url(org_id, "/api-keys"), absolute=True, params=self._params(**params))

    def revoke_org_api_key(self, org_id, api_key_id, data=None):
        """Revoke an organization API key."""
        return self.patch(
            self._api_access_url(org_id, f"/api-keys/revoke/{api_key_id}"), data=data or {}, absolute=True
        )

    def get_oauth_clients(self, org_id, **params):
        """List organization OAuth clients."""
        return self.get(self._api_access_url(org_id, "/oauth-clients"), absolute=True, params=self._params(**params))

    def create_oauth_client(self, org_id, data):
        """Create an OAuth client."""
        return self.post(self._api_access_url(org_id, "/oauth-clients"), data=data, absolute=True)

    def get_oauth_client_count(self, org_id, data=None):
        """Return OAuth-client count, optionally using API Access filters."""
        return self.post(self._api_access_url(org_id, "/oauth-clients/count"), data=data or {}, absolute=True)

    def get_oauth_client(self, org_id, client_id):
        """Return one OAuth client."""
        return self.get(self._api_access_url(org_id, f"/oauth-clients/{client_id}"), absolute=True)

    def delete_oauth_client(self, org_id, client_id):
        """Delete an OAuth client."""
        return self.delete(self._api_access_url(org_id, f"/oauth-clients/{client_id}"), absolute=True)

    def get_service_accounts(self, org_id, **params):
        """List organization service accounts."""
        return self.get(self._api_access_url(org_id, "/service-accounts"), absolute=True, params=self._params(**params))

    def create_service_account(self, org_id, data):
        """Create a service account."""
        return self.post(self._api_access_url(org_id, "/service-accounts"), data=data, absolute=True)

    def update_service_account(self, org_id, data):
        """Patch a service account using the API Access request body."""
        return self.patch(self._api_access_url(org_id, "/service-accounts"), data=data, absolute=True)

    def delete_service_account(self, org_id, service_account_id):
        """Delete a service account."""
        return self.delete(self._api_access_url(org_id, f"/service-accounts/{service_account_id}"), absolute=True)


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
