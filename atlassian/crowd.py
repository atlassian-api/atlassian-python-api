# coding=utf-8
import logging

from bs4 import BeautifulSoup
from jmespath import search

from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Crowd(AtlassianRestAPI):
    """Crowd API wrapper.
    Important to note that you will have to use an application credentials,
    not user credentials, in order to access Crowd APIs"""

    def __init__(
        self,
        url,
        username,
        password,
        timeout=60,
        api_root="rest",
        api_version="latest",
    ):
        super(Crowd, self).__init__(url, username, password, timeout, api_root, api_version)

    def _crowd_api_url(self, api, resource, api_version=None):
        version = api_version or self.api_version
        return f"/{self.api_root}/{api}/{version}/{resource}"

    def _admin_api_url(self, resource):
        return f"/{self.api_root}/admin/1.0/{resource}"

    def _user_change_status(self, username, active):
        """
        Change user status.
        :param username: str - username
        :param active: bool - True/False
        :return:
        """

        user = self.user(username)

        user_object = {
            "name": username,
            "active": active,
            "display-name": user.get("display-name"),
            "first-name": user.get("first-name"),
            "last-name": user.get("last-name"),
            "email": user.get("email"),
        }

        params = {"username": username}

        return self.put(
            self._crowd_api_url("usermanagement", "user"),
            params=params,
            data=user_object,
        )

    def user(self, username):
        """
        Get user information
        :param username:
        :return:
        """
        params = {"username": username}
        return self.get(self._crowd_api_url("usermanagement", "user"), params=params)

    def user_activate(self, username):
        """
        Activate user
        :param username: str - username
        """

        return self._user_change_status(username, True)

    def user_create(
        self,
        username,
        active,
        first_name,
        last_name,
        display_name,
        email,
        password,
    ):
        """
        Create new user method
        :param  active: bool:
        :param  username: string: username
        :param  active: bool:
        :param  first_name: string:
        :param  last_name: string:
        :param  display_name:  string:
        :param  email: string:
        :param  password: string:
        :return:
        """

        user_object = {
            "name": username,
            "password": {"value": password},
            "active": active,
            "first-name": first_name,
            "last-name": last_name,
            "display-name": display_name,
            "email": email,
        }

        return self.post(self._crowd_api_url("usermanagement", "user"), data=user_object)

    def user_deactivate(self, username):
        """
        Deactivate user

        :return:
        """

        return self._user_change_status(username, False)

    def user_delete(self, username):
        """
        Delete user
        :param username: str - username
        :return:
        """

        params = {"username": username}

        return self.delete(self._crowd_api_url("usermanagement", "user"), params=params)

    def user_groups(self, username, kind="direct"):
        """
        Get user's all group info
        :param username: str - username
        :param kind: str - group type
        :return: The specify user's group info
        """
        path = self._crowd_api_url("usermanagement", f"user/group/{kind}")
        response = self.get(path, params={"username": username})
        return search("groups[*].name", response)

    def group_members(self, group, kind="direct", max_results=99999):
        """
        Get group's all direct members
        :param group: str - group name
        :param kind: str - group type
        :param max_results: int - maximum number of results
        :return: The specify group's direct members info
        """
        path = self._crowd_api_url("usermanagement", f"group/user/{kind}")
        params = {"groupname": group, "max-results": max_results}
        response = self.get(path, params=params)
        return search("users[*].name", response)

    def is_user_in_group(self, username, group, kind="direct"):
        """
        Check if the user is a member of the group
        :param username: str - username
        :param group: str - group name
        :param kind: str - group type
        :return: bool - Return `True` or `False`
        """
        path = self._crowd_api_url("usermanagement", f"group/user/{kind}")
        params = {"username": username, "groupname": group}
        response = self.get(path, params=params, advanced_mode=True)
        return response.status_code == 200

    def group_add_user(self, username, groupname):
        """
        Add user to group
        :param username: str - username
        :param groupname: str - group name
        :return:
        """

        params = {"groupname": groupname}
        data = {"name": username}

        return self.post(
            self._crowd_api_url("usermanagement", "user/group/direct"),
            params=params,
            data=data,
        )

    def group_remove_user(self, username, groupname):
        """Remove a direct user-to-group membership."""
        return self.delete(
            self._crowd_api_url("usermanagement", "user/group/direct"),
            params={"username": username, "groupname": groupname},
        )

    def user_update(self, username, data):
        """Update a user with a Crowd user representation."""
        return self.put(self._crowd_api_url("usermanagement", "user"), params={"username": username}, data=data)

    def user_update_password(self, username, password):
        """Update a user's password."""
        return self.put(
            self._crowd_api_url("usermanagement", "user/password"),
            params={"username": username},
            data={"value": password},
        )

    def user_attributes(self, username):
        """Return all attributes for a user."""
        return self.get(self._crowd_api_url("usermanagement", "user/attribute"), params={"username": username})

    def user_store_attributes(self, username, attributes):
        """Store user attributes using Crowd's attribute request body."""
        return self.put(
            self._crowd_api_url("usermanagement", "user/attribute"), params={"username": username}, data=attributes
        )

    def user_remove_attribute(self, username, attribute_name):
        """Delete one user attribute."""
        return self.delete(
            self._crowd_api_url("usermanagement", "user/attribute"),
            params={"username": username, "attributename": attribute_name},
        )

    def group(self, groupname):
        """Return a group by name."""
        return self.get(self._crowd_api_url("usermanagement", "group"), params={"groupname": groupname})

    def group_update(self, groupname, data):
        """Update a group with a Crowd group representation."""
        return self.put(self._crowd_api_url("usermanagement", "group"), params={"groupname": groupname}, data=data)

    def group_delete(self, groupname):
        """Delete a group by name."""
        return self.delete(self._crowd_api_url("usermanagement", "group"), params={"groupname": groupname})

    def group_attributes(self, groupname):
        """Return all attributes for a group."""
        return self.get(self._crowd_api_url("usermanagement", "group/attribute"), params={"groupname": groupname})

    def group_store_attributes(self, groupname, attributes):
        """Store group attributes using Crowd's attribute request body."""
        return self.put(
            self._crowd_api_url("usermanagement", "group/attribute"), params={"groupname": groupname}, data=attributes
        )

    def group_remove_attribute(self, groupname, attribute_name):
        """Delete one group attribute."""
        return self.delete(
            self._crowd_api_url("usermanagement", "group/attribute"),
            params={"groupname": groupname, "attributename": attribute_name},
        )

    def nested_group_members(self, groupname, max_results=99999):
        """Return users who are direct or nested members of a group."""
        response = self.get(
            self._crowd_api_url("usermanagement", "group/user/nested"),
            params={"groupname": groupname, "max-results": max_results},
        )
        return search("users[*].name", response)

    def nested_user_groups(self, username):
        """Return direct and nested groups for a user."""
        response = self.get(self._crowd_api_url("usermanagement", "user/group/nested"), params={"username": username})
        return search("groups[*].name", response)

    def group_child_groups(self, groupname, child_groupname=None, start_index=0, max_results=99999):
        """
        Get direct child groups of a group.
        :param groupname: str - parent group name
        :param child_groupname: str - optional single child group name to retrieve
        :param start_index: int - start index for paging
        :param max_results: int - maximum number of results
        :return: list of group names
        """
        path = self._crowd_api_url("usermanagement", "group/child-group/direct")
        params = {"groupname": groupname, "start-index": start_index, "max-results": max_results}
        if child_groupname:
            params["child-groupname"] = child_groupname
        response = self.get(path, params=params)
        return search("groups[*].name", response)

    def nested_group_child_groups(self, groupname, child_groupname=None, start_index=0, max_results=99999):
        """
        Get nested child groups of a group.
        :param groupname: str - parent group name
        :param child_groupname: str - optional single nested child group name to retrieve
        :param start_index: int - start index for paging
        :param max_results: int - maximum number of results
        :return: list of group names
        """
        path = self._crowd_api_url("usermanagement", "group/child-group/nested")
        params = {"groupname": groupname, "start-index": start_index, "max-results": max_results}
        if child_groupname:
            params["child-groupname"] = child_groupname
        response = self.get(path, params=params)
        return search("groups[*].name", response)

    def group_add_child_group(self, groupname, child_groupname):
        """
        Add a direct child group membership to a group.
        :param groupname: str - parent group name
        :param child_groupname: str - child group name to add
        :return:
        """
        params = {"groupname": groupname}
        data = {"name": child_groupname}
        return self.post(self._crowd_api_url("usermanagement", "group/child-group/direct"), params=params, data=data)

    def group_remove_child_group(self, groupname, child_groupname):
        """
        Remove a direct child group membership from a group.
        :param groupname: str - parent group name
        :param child_groupname: str - child group name to remove
        :return:
        """
        params = {"groupname": groupname, "child-groupname": child_groupname}
        return self.delete(self._crowd_api_url("usermanagement", "group/child-group/direct"), params=params)

    def group_parent_groups(self, groupname, child_groupname=None, start_index=0, max_results=99999):
        """
        Get direct parent groups of a group.
        :param groupname: str - group name
        :param child_groupname: str - optional child group name
        :param start_index: int - start index for paging
        :param max_results: int - maximum number of results
        :return: list of group names
        """
        path = self._crowd_api_url("usermanagement", "group/parent-group/direct")
        params = {"groupname": groupname, "start-index": start_index, "max-results": max_results}
        if child_groupname:
            params["child-groupname"] = child_groupname
        response = self.get(path, params=params)
        return search("groups[*].name", response)

    def nested_group_parent_groups(self, groupname, parent_groupname=None, start_index=0, max_results=99999):
        """
        Get nested parent groups of a group.
        :param groupname: str - group name
        :param parent_groupname: str - optional single parent group name to retrieve
        :param start_index: int - start index for paging
        :param max_results: int - maximum number of results
        :return: list of group names
        """
        path = self._crowd_api_url("usermanagement", "group/parent-group/nested")
        params = {"groupname": groupname, "start-index": start_index, "max-results": max_results}
        if parent_groupname:
            params["parent-groupname"] = parent_groupname
        response = self.get(path, params=params)
        return search("groups[*].name", response)

    def group_add_parent_group(self, groupname, parent_groupname):
        """
        Add a direct parent group membership to a group.
        :param groupname: str - child group name
        :param parent_groupname: str - parent group name to add
        :return:
        """
        params = {"groupname": groupname}
        data = {"name": parent_groupname}
        return self.post(self._crowd_api_url("usermanagement", "group/parent-group/direct"), params=params, data=data)

    def session_create(self, username, password, validate_password=True, duration=None):
        """
        Authenticate a user and create a Crowd SSO session.
        :param username: str - username
        :param password: str - password
        :param validate_password: bool - whether to validate the password
        :param duration: int - requested token duration in seconds
        :return: session info
        """
        params = {"validate-password": str(validate_password).lower()}
        if duration:
            params["duration"] = duration
        data = {"userName": username, "password": password}
        return self.post(self._crowd_api_url("usermanagement", "session"), params=params, data=data)

    def session_validate(self, token, validation_factors=None):
        """
        Validate a Crowd SSO session token.
        :param token: str - SSO token
        :param validation_factors: dict - validation factors request body
        :return: session info
        """
        data = validation_factors or {}
        return self.post(self._crowd_api_url("usermanagement", f"session/{token}"), data=data)

    def session_get(self, token):
        """
        Get session information by token.
        :param token: str - SSO token
        :return: session info
        """
        return self.get(self._crowd_api_url("usermanagement", f"session/{token}"))

    def session_delete(self, token):
        """
        Invalidate a Crowd SSO session token.
        :param token: str - SSO token
        :return:
        """
        return self.delete(self._crowd_api_url("usermanagement", f"session/{token}"))

    def session_delete_user_tokens(self, username, exclude=None):
        """
        Delete all tokens for a user, optionally excluding one token.
        :param username: str - username
        :param exclude: str - token to exclude from invalidation
        :return:
        """
        params = {"username": username}
        if exclude:
            params["exclude"] = exclude
        return self.delete(self._crowd_api_url("usermanagement", "session"), params=params)

    def search_cql(self, entity_type, restriction=None, start_index=0, max_results=99999):
        """
        Search entities using Crowd Query Language (GET).
        :param entity_type: str - type of entity to search
        :param restriction: str - CQL restriction
        :param start_index: int - start index for paging
        :param max_results: int - maximum number of results
        :return: search results
        """
        params = {"entity-type": entity_type, "start-index": start_index, "max-results": max_results}
        if restriction:
            params["restriction"] = restriction
        return self.get(self._crowd_api_url("usermanagement", "search"), params=params)

    def search(self, entity_type, restriction=None, start_index=0, max_results=99999):
        """
        Search entities using a search restriction body (POST).
        :param entity_type: str - type of entity to search
        :param restriction: dict - search restriction request body
        :param start_index: int - start index for paging
        :param max_results: int - maximum number of results
        :return: search results
        """
        params = {"entity-type": entity_type, "start-index": start_index, "max-results": max_results}
        data = restriction or {}
        return self.post(self._crowd_api_url("usermanagement", "search"), params=params, data=data)

    def user_authenticate(self, username, password):
        """
        Authenticate a user and return user information.
        :param username: str - username
        :param password: str - password
        :return: user info
        """
        params = {"username": username}
        data = {"value": password}
        return self.post(self._crowd_api_url("usermanagement", "authentication"), params=params, data=data)

    def user_authentication_notify(self, username):
        """
        Notify Crowd that a user has been authenticated by a trusted application.
        :param username: str - username
        :return:
        """
        params = {"username": username}
        return self.post(self._crowd_api_url("usermanagement", "authentication/notify"), params=params)

    def user_delete_password(self, username):
        """
        Delete a user's password.
        :param username: str - username
        :return:
        """
        params = {"username": username}
        return self.delete(self._crowd_api_url("usermanagement", "user/password"), params=params)

    def user_request_password_reset(self, username):
        """
        Request a password reset email for a user.
        :param username: str - username
        :return:
        """
        params = {"username": username}
        return self.post(self._crowd_api_url("usermanagement", "user/mail/password"), params=params)

    def user_request_usernames_reminder(self, email):
        """
        Request a username reminder email.
        :param email: str - email address
        :return:
        """
        params = {"email": email}
        return self.post(self._crowd_api_url("usermanagement", "user/mail/usernames"), params=params)

    def user_rename(self, username, new_name):
        """
        Rename a user.
        :param username: str - current username
        :param new_name: str - new username
        :return:
        """
        params = {"username": username}
        data = {"newName": new_name}
        return self.post(self._crowd_api_url("usermanagement", "user/rename"), params=params, data=data)

    def user_expire_all_passwords(self, confirm=True):
        """
        Expire all user passwords.
        :param confirm: bool - must be True to perform the action
        :return:
        """
        params = {"confirm": str(confirm).lower()}
        return self.post(self._crowd_api_url("usermanagement", "user/expire-all-passwords"), params=params)

    def user_avatar(self, username, size=None):
        """
        Get a user's avatar.
        :param username: str - username
        :param size: int - requested avatar size in pixels
        :return: avatar content
        """
        params = {"username": username}
        if size:
            params["s"] = size
        return self.get(self._crowd_api_url("usermanagement", "user/avatar"), params=params)

    def get_cookie_config(self):
        """Get the Crowd cookie configuration."""
        return self.get(self._crowd_api_url("usermanagement", "config/cookie"))

    def account_change_password(self, username, old_password, new_password):
        """
        Change the current user's password.
        :param username: str - username
        :param old_password: str - current password
        :param new_password: str - new password
        :return:
        """
        data = {"username": username, "oldPassword": old_password, "newPassword": new_password}
        return self.post(self._crowd_api_url("account", "change-password", api_version="1"), data=data)

    def account_forgotten_password(self, username):
        """
        Start the forgotten password procedure.
        :param username: str - username
        :return:
        """
        return self.post(
            self._crowd_api_url("account", "forgotten-password", api_version="1"),
            params={"username": username},
        )

    def account_forgotten_username(self, email):
        """
        Start the forgotten username procedure.
        :param email: str - email address
        :return:
        """
        return self.post(
            self._crowd_api_url("account", "forgotten-username", api_version="1"),
            params={"email": email},
        )

    def account_reset_password(self, username, token, password, directory_id=None):
        """
        Reset a forgotten password.
        :param username: str - username
        :param token: str - reset token
        :param password: str - new password
        :param directory_id: int - directory id
        :return:
        """
        data = {"username": username, "token": token, "password": password}
        if directory_id:
            data["directoryId"] = directory_id
        return self.post(self._crowd_api_url("account", "reset-password", api_version="1"), data=data)

    def account_validate_token(self, username, token, directory_id=None):
        """
        Check whether a user's reset token is still valid.
        :param username: str - username
        :param token: str - reset token
        :param directory_id: int - directory id
        :return:
        """
        data = {"username": username, "token": token}
        if directory_id:
            data["directoryId"] = directory_id
        return self.post(self._crowd_api_url("account", "token-status", api_version="1"), data=data)

    def directory_test_azure_ad(self, config, directory_id=None):
        """
        Test Microsoft Entra ID (Azure AD) directory connection.
        :param config: dict - Azure AD connection test data
        :param directory_id: int - optional directory id to test against
        :return: connection test result
        """
        path = "directorymanagement/1/directory/testazuread"
        if directory_id:
            path = f"{path}/{directory_id}"
        return self.post(self.url_joiner(self.api_root, path), data=config)

    def directory_test_crowd(self, config, directory_id=None):
        """
        Test Crowd directory connection.
        :param config: dict - Crowd connection test data
        :param directory_id: int - optional directory id to test against
        :return: connection test result
        """
        path = "directorymanagement/1/directory/testcrowd"
        if directory_id:
            path = f"{path}/{directory_id}"
        return self.post(self.url_joiner(self.api_root, path), data=config)

    def directory_test_ldap(self, config, directory_id=None):
        """
        Test LDAP directory connection.
        :param config: dict - LDAP connection test data
        :param directory_id: int - optional directory id to test against
        :return: connection test result
        """
        path = "directorymanagement/1/directory/testldap"
        if directory_id:
            path = f"{path}/{directory_id}"
        return self.post(self.url_joiner(self.api_root, path), data=config)

    def directory_test_ldap_search(self, config, directory_id=None):
        """
        Test LDAP directory search.
        :param config: dict - LDAP search test data
        :param directory_id: int - optional directory id to test against
        :return: search test result
        """
        path = "directorymanagement/1/directory/testsearch"
        if directory_id:
            path = f"{path}/{directory_id}"
        return self.post(self.url_joiner(self.api_root, path), data=config)

    def user_aliases(self, username):
        """
        Get all aliases for a user across alias-enabled applications.
        :param username: str - username in Crowd
        :return: aliases
        """
        return self.get(self._crowd_api_url("appmanagement", "aliases", api_version="1"), params={"user": username})

    def set_user_aliases(self, username, aliases):
        """
        Set aliases for a user across applications.
        :param username: str - username in Crowd
        :param aliases: dict - mapping of application id to alias
        :return:
        """
        return self.put(
            self._crowd_api_url("appmanagement", "aliases", api_version="1"),
            params={"user": username},
            data=aliases,
        )

    def delete_user_aliases(self, username):
        """
        Delete all aliases for a user.
        :param username: str - username in Crowd
        :return:
        """
        return self.delete(
            self._crowd_api_url("appmanagement", "aliases", api_version="1"),
            params={"user": username},
        )

    def get_alias(self, application_id, username):
        """
        Get a user's alias in a specific application.
        :param application_id: str - application id
        :param username: str - username
        :return: alias
        """
        return self.get(
            self._crowd_api_url("appmanagement", f"aliases/{application_id}/alias", api_version="1"),
            params={"user": username},
        )

    def set_alias(self, application_id, username, alias):
        """
        Set a user's alias in a specific application.
        :param application_id: str - application id
        :param username: str - username
        :param alias: str - alias value
        :return:
        """
        headers = {"Content-Type": "text/plain"}
        return self.put(
            self._crowd_api_url("appmanagement", f"aliases/{application_id}/alias", api_version="1"),
            params={"user": username},
            data=alias,
            headers=headers,
        )

    def delete_alias(self, application_id, username):
        """
        Delete a user's alias in a specific application.
        :param application_id: str - application id
        :param username: str - username
        :return:
        """
        return self.delete(
            self._crowd_api_url("appmanagement", f"aliases/{application_id}/alias", api_version="1"),
            params={"user": username},
        )

    def get_username_for_alias(self, application_id, alias):
        """
        Get the username for an alias in a specific application.
        :param application_id: str - application id
        :param alias: str - alias
        :return: username
        """
        return self.get(
            self._crowd_api_url("appmanagement", f"aliases/{application_id}/username", api_version="1"),
            params={"alias": alias},
        )

    def get_applications(self, name=None):
        """
        Get all applications or a specific application by name.
        :param name: str - optional application name to filter by
        :return: applications
        """
        params = {"name": name} if name else {}
        return self.get(self._crowd_api_url("appmanagement", "application", api_version="1"), params=params)

    def create_application(self, data, include_request_address=None):
        """
        Add a new application.
        :param data: dict - application representation
        :param include_request_address: bool - include request address in response
        :return:
        """
        params = {}
        if include_request_address is not None:
            params["include-request-address"] = include_request_address
        return self.post(
            self._crowd_api_url("appmanagement", "application", api_version="1"),
            params=params,
            data=data,
        )

    def get_application(self, application_id):
        """
        Get an application by id.
        :param application_id: str - application id
        :return: application
        """
        return self.get(self._crowd_api_url("appmanagement", f"application/{application_id}", api_version="1"))

    def update_application(self, application_id, data):
        """
        Update an application.
        :param application_id: str - application id
        :param data: dict - application representation
        :return:
        """
        return self.put(
            self._crowd_api_url("appmanagement", f"application/{application_id}", api_version="1"),
            data=data,
        )

    def delete_application(self, application_id):
        """
        Delete an application.
        :param application_id: str - application id
        :return:
        """
        return self.delete(self._crowd_api_url("appmanagement", f"application/{application_id}", api_version="1"))

    def get_remote_addresses(self, application_id):
        """
        Get remote addresses for an application.
        :param application_id: str - application id
        :return: remote addresses
        """
        return self.get(
            self._crowd_api_url("appmanagement", f"application/{application_id}/remote_address", api_version="1")
        )

    def add_remote_address(self, application_id, address):
        """
        Add a remote address to an application.
        :param application_id: str - application id
        :param address: dict - remote address representation or string value
        :return:
        """
        data = {"value": address} if isinstance(address, str) else address
        return self.post(
            self._crowd_api_url("appmanagement", f"application/{application_id}/remote_address", api_version="1"),
            data=data,
        )

    def remove_remote_address(self, application_id, address):
        """
        Remove a remote address from an application.
        :param application_id: str - application id
        :param address: str - remote address to remove
        :return:
        """
        return self.delete(
            self._crowd_api_url("appmanagement", f"application/{application_id}/remote_address", api_version="1"),
            params={"address": address},
        )

    def get_admin_applications(self, name=None, active=None, start=0, limit=99999):
        """
        Get all applications or filter by name and active status.
        :param name: str - optional application name filter
        :param active: bool - optional active status filter
        :param start: int - start index for paging
        :param limit: int - maximum number of results
        :return: applications
        """
        params = {"start": start, "limit": limit}
        if name:
            params["name"] = name
        if active is not None:
            params["active"] = active
        return self.get(self._admin_api_url("application"), params=params)

    def get_admin_application(self, application_id):
        """
        Get an application by id.
        :param application_id: str - application id
        :return: application
        """
        return self.get(self._admin_api_url(f"application/{application_id}"))

    def update_admin_application(self, application_id, data):
        """
        Update an application.
        :param application_id: str - application id
        :param data: dict - application representation
        :return:
        """
        return self.put(self._admin_api_url(f"application/{application_id}"), data=data)

    def get_access_based_synchronization(self, application_id):
        """
        Get access-based synchronization settings for an application.
        :param application_id: str - application id
        :return: synchronization settings
        """
        return self.get(self._admin_api_url(f"application/{application_id}/access-based-synchronization"))

    def update_access_based_synchronization(self, application_id, data):
        """
        Update access-based synchronization settings for an application.
        :param application_id: str - application id
        :param data: dict - synchronization settings
        :return:
        """
        return self.put(self._admin_api_url(f"application/{application_id}/access-based-synchronization"), data=data)

    def get_directory_mappings(self, application_id, start=0, limit=99999):
        """
        Get directory mappings for an application.
        :param application_id: str - application id
        :param start: int - start index for paging
        :param limit: int - maximum number of results
        :return: directory mappings
        """
        params = {"start": start, "limit": limit}
        return self.get(self._admin_api_url(f"application/{application_id}/directory-mapping"), params=params)

    def add_directory_mapping(self, application_id, data):
        """
        Add a directory mapping to an application.
        :param application_id: str - application id
        :param data: dict - directory mapping representation
        :return:
        """
        return self.post(self._admin_api_url(f"application/{application_id}/directory-mapping"), data=data)

    def get_directory_mapping(self, application_id, directory_id):
        """
        Get a directory mapping for an application.
        :param application_id: str - application id
        :param directory_id: str - directory id
        :return: directory mapping
        """
        return self.get(self._admin_api_url(f"application/{application_id}/directory-mapping/{directory_id}"))

    def update_directory_mapping(self, application_id, directory_id, data):
        """
        Update a directory mapping for an application.
        :param application_id: str - application id
        :param directory_id: str - directory id
        :param data: dict - directory mapping representation
        :return:
        """
        return self.put(
            self._admin_api_url(f"application/{application_id}/directory-mapping/{directory_id}"),
            data=data,
        )

    def delete_directory_mapping(self, application_id, directory_id):
        """
        Delete a directory mapping from an application.
        :param application_id: str - application id
        :param directory_id: str - directory id
        :return:
        """
        return self.delete(self._admin_api_url(f"application/{application_id}/directory-mapping/{directory_id}"))

    def move_directory_mapping(self, application_id, directory_id, data):
        """
        Reorder directory mappings for an application.
        :param application_id: str - application id
        :param directory_id: str - directory id
        :param data: dict - move request body
        :return:
        """
        return self.post(
            self._admin_api_url(f"application/{application_id}/directory-mapping/{directory_id}/move"),
            data=data,
        )

    def get_detailed_directories(self, search=None, active=None, start=0, limit=99999):
        """
        Get detailed directory data list.
        :param search: str - optional search query
        :param active: bool - optional active status filter
        :param start: int - start index for paging
        :param limit: int - maximum number of results
        :return: directories
        """
        params = {"start": start, "limit": limit}
        if search:
            params["search"] = search
        if active is not None:
            params["active"] = active
        return self.get(self._admin_api_url("directory/detailed"), params=params)

    def get_detailed_directory(self, directory_id):
        """
        Get detailed directory data.
        :param directory_id: str - directory id
        :return: directory
        """
        return self.get(self._admin_api_url(f"directory/detailed/{directory_id}"))

    def synchronize_directory(self, directory_id):
        """
        Schedule synchronisation for a directory.
        :param directory_id: str - directory id
        :return:
        """
        return self.post(self._admin_api_url(f"directory/detailed/{directory_id}/synchronize"))

    def get_managed_directories(self, start=0, limit=99999):
        """
        Get managed directories.
        :param start: int - start index for paging
        :param limit: int - maximum number of results
        :return: directories
        """
        return self.get(self._admin_api_url("directory/managed"), params={"start": start, "limit": limit})

    def search_directory_groups(self, directory_id, term, active=None, start=0, limit=99999):
        """
        Search groups in a directory.
        :param directory_id: str - directory id
        :param term: str - search term
        :param active: bool - optional active status filter
        :param start: int - start index for paging
        :param limit: int - maximum number of results
        :return: groups
        """
        params = {"term": term, "start": start, "limit": limit}
        if active is not None:
            params["active"] = active
        return self.get(self._admin_api_url(f"group/search/{directory_id}"), params=params)

    def get_admin_group_nested_groups(self, group_id, start=0, limit=99999):
        """
        Get nested groups for a group.
        :param group_id: str - group id
        :param start: int - start index for paging
        :param limit: int - maximum number of results
        :return: groups
        """
        return self.get(
            self._admin_api_url(f"group/{group_id}/groups"),
            params={"start": start, "limit": limit},
        )

    def add_admin_group_nested_groups(self, group_id, data):
        """
        Add nested groups to a group.
        :param group_id: str - group id
        :param data: dict - group membership request body
        :return:
        """
        return self.post(self._admin_api_url(f"group/{group_id}/groups"), data=data)

    def get_group_administrators(self, group_id, start=0, limit=99999):
        """
        Get administrators of a group.
        :param group_id: str - group id
        :param start: int - start index for paging
        :param limit: int - maximum number of results
        :return: administrators
        """
        return self.get(
            self._admin_api_url(f"group-level-admin/{group_id}/admins"),
            params={"start": start, "limit": limit},
        )

    def add_group_administrators(self, group_id, data):
        """
        Add administrators to a group.
        :param group_id: str - group id
        :param data: dict - administrator request body
        :return:
        """
        return self.post(self._admin_api_url(f"group-level-admin/{group_id}/admins"), data=data)

    def get_group_admin_candidates(self, group_id, search=None, limit=99999):
        """
        Get group administrator candidates.
        :param group_id: str - group id
        :param search: str - optional search string
        :param limit: int - maximum number of results
        :return: candidates
        """
        params = {"limit": limit}
        if search:
            params["search"] = search
        return self.get(self._admin_api_url(f"group-level-admin/{group_id}/admins/suggestions"), params=params)

    def remove_group_admin_user(self, group_id, admin_user_id):
        """
        Revoke group administrator rights from a user.
        :param group_id: str - group id
        :param admin_user_id: str - admin user id
        :return:
        """
        return self.delete(self._admin_api_url(f"group-level-admin/{group_id}/admins/users/{admin_user_id}"))

    def remove_group_admin_group(self, group_id, admin_group_id):
        """
        Revoke group administrator rights from a group.
        :param group_id: str - group id
        :param admin_group_id: str - admin group id
        :return:
        """
        return self.delete(self._admin_api_url(f"group-level-admin/{group_id}/admins/groups/{admin_group_id}"))

    def search_administered_groups(self, query=None, start=0, limit=99999):
        """
        Search administered groups.
        :param query: dict - search request body
        :param start: int - start index for paging
        :param limit: int - maximum number of results
        :return: groups
        """
        params = {"start": start, "limit": limit}
        return self.post(self._admin_api_url("groups/query"), params=params, data=query or {})

    def get_admin_group_details(self, group_id):
        """
        Get group details.
        :param group_id: str - group id
        :return: group details
        """
        return self.get(self._admin_api_url(f"groups/{group_id}"))

    def get_admin_group_members(self, group_id, start=0, limit=99999):
        """
        Get members of a group.
        :param group_id: str - group id
        :param start: int - start index for paging
        :param limit: int - maximum number of results
        :return: members
        """
        return self.get(self._admin_api_url(f"groups/{group_id}/users"), params={"start": start, "limit": limit})

    def add_users_to_admin_group(self, group_id, data):
        """
        Add users to a group.
        :param group_id: str - group id
        :param data: dict - users to add
        :return:
        """
        return self.post(self._admin_api_url(f"groups/{group_id}/users"), data=data)

    def remove_users_from_admin_group(self, group_id, data):
        """
        Remove users from a group.
        :param group_id: str - group id
        :param data: dict - users to remove
        :return:
        """
        return self.delete(self._admin_api_url(f"groups/{group_id}/users"), data=data)

    def search_admin_group_user_suggestions(self, group_id, search=None, limit=99999):
        """
        Search users to add to a group.
        :param group_id: str - group id
        :param search: str - optional search string
        :param limit: int - maximum number of results
        :return: user suggestions
        """
        params = {"limit": limit}
        if search:
            params["search"] = search
        return self.get(self._admin_api_url(f"groups/{group_id}/users/suggestions"), params=params)

    def search_admin_users(self, query=None, start=0, limit=99999):
        """
        Search users.
        :param query: dict - search request body
        :param start: int - start index for paging
        :param limit: int - maximum number of results
        :return: users
        """
        params = {"start": start, "limit": limit}
        return self.post(self._admin_api_url("users/search"), params=params, data=query or {})

    def add_user_to_admin_group(self, user_id, data):
        """
        Add a user to groups.
        :param user_id: str - user id
        :param data: dict - groups to add
        :return:
        """
        return self.post(self._admin_api_url(f"users/{user_id}/groups"), data=data)

    def remove_user_from_admin_group(self, user_id, data):
        """
        Remove a user from groups.
        :param user_id: str - user id
        :param data: dict - groups to remove
        :return:
        """
        return self.delete(self._admin_api_url(f"users/{user_id}/groups"), data=data)

    def get_server_info(self):
        """Get Crowd server information."""
        return self.get(self._admin_api_url("server-info"))

    def get_application_sessions(self, search=None, start=0, limit=99999):
        """
        Get application sessions.
        :param search: str - optional search keyword
        :param start: int - start index for paging
        :param limit: int - maximum number of results
        :return: sessions
        """
        params = {"start": start, "limit": limit}
        if search:
            params["search"] = search
        return self.get(self._admin_api_url("sessions/application"), params=params)

    def get_user_sessions(self, search=None, directory_id=None, start=0, limit=99999):
        """
        Get user sessions.
        :param search: str - optional search keyword
        :param directory_id: str - optional directory id filter
        :param start: int - start index for paging
        :param limit: int - maximum number of results
        :return: sessions
        """
        params = {"start": start, "limit": limit}
        if search:
            params["search"] = search
        if directory_id:
            params["directoryId"] = directory_id
        return self.get(self._admin_api_url("sessions/user"), params=params)

    def expire_session(self, random_hash):
        """
        Expire a session by random hash.
        :param random_hash: str - session random hash
        :return:
        """
        return self.delete(self._admin_api_url(f"sessions/{random_hash}"))

    def get_licensing_summary(self, application_id, version=None, jira_type=None):
        """
        Get licensing summary for an application.
        :param application_id: str - application id
        :param version: str - optional licensing data version
        :param jira_type: str - optional Jira subtype
        :return: licensing summary
        """
        params = {}
        if version:
            params["version"] = version
        if jira_type:
            params["jiraType"] = jira_type
        return self.get(self._admin_api_url(f"licensing/{application_id}/summary"), params=params)

    def get_licensed_directories(self, application_id, version=None, jira_type=None, start=0, limit=99999):
        """
        Get licensed directories for an application.
        :param application_id: str - application id
        :param version: str - optional licensing data version
        :param jira_type: str - optional Jira subtype
        :param start: int - start index for paging
        :param limit: int - maximum number of results
        :return: directories
        """
        params = {"start": start, "limit": limit}
        if version:
            params["version"] = version
        if jira_type:
            params["jiraType"] = jira_type
        return self.get(self._admin_api_url(f"licensing/{application_id}/directories"), params=params)

    def get_licensed_jira_types(self, application_id, version=None):
        """
        Get Jira types for licensing.
        :param application_id: str - application id
        :param version: str - optional licensing data version
        :return: Jira types
        """
        params = {"version": version} if version else {}
        return self.get(self._admin_api_url(f"licensing/{application_id}/jira-types"), params=params)

    def search_licensed_users(self, application_id, query=None, start=0, limit=99999):
        """
        Search licensed users for an application.
        :param application_id: str - application id
        :param query: dict - search request body
        :param start: int - start index for paging
        :param limit: int - maximum number of results
        :return: users
        """
        params = {"start": start, "limit": limit}
        return self.post(
            self._admin_api_url(f"licensing/{application_id}/licensed-users/search"),
            params=params,
            data=query or {},
        )

    def export_licensed_users(
        self,
        application_id,
        search=None,
        directory_id=None,
        jira_type=None,
        last_login_before=None,
        search_version=None,
    ):
        """
        Export licensed users for an application.
        :param application_id: str - application id
        :param search: str - optional search text
        :param directory_id: str - optional directory id filter
        :param jira_type: str - optional Jira subtype
        :param last_login_before: str - optional last logged in date filter
        :param search_version: str - optional licensing data version
        :return: exported users
        """
        params = {}
        if search:
            params["search"] = search
        if directory_id:
            params["directoryId"] = directory_id
        if jira_type:
            params["jiraType"] = jira_type
        if last_login_before:
            params["lastLoginBefore"] = last_login_before
        if search_version:
            params["searchVersion"] = search_version
        return self.get(self._admin_api_url(f"licensing/{application_id}/licensed-users/download"), params=params)

    def create_backup(self, data=None):
        """
        Create a backup.
        :param data: dict - optional backup request body
        :return:
        """
        return self.post(self._admin_api_url("backup"), data=data or {})

    def get_backup_summary(self):
        """Get backup summary."""
        return self.get(self._admin_api_url("backup/summary"))

    def get_backup_configuration(self):
        """Get backup configuration."""
        return self.get(self._admin_api_url("backup/configuration"))

    def save_backup_configuration(self, data):
        """
        Save backup configuration.
        :param data: dict - backup configuration
        :return:
        """
        return self.post(self._admin_api_url("backup/configuration"), data=data)

    def add_audit_log_changeset(self, data):
        """
        Add an audit log changeset.
        :param data: dict - changeset data
        :return:
        """
        return self.post(self._admin_api_url("auditlog"), data=data)

    def get_audit_log_configuration(self):
        """Get audit log configuration."""
        return self.get(self._admin_api_url("auditlog/configuration"))

    def set_audit_log_configuration(self, data):
        """
        Set audit log configuration.
        :param data: dict - audit log configuration
        :return:
        """
        return self.put(self._admin_api_url("auditlog/configuration"), data=data)

    def search_audit_log(self, query=None, start=0, limit=99999):
        """
        Search audit log.
        :param query: dict - search request body
        :param start: int - start index for paging
        :param limit: int - maximum number of results
        :return: audit log entries
        """
        params = {"start": start, "limit": limit}
        return self.post(self._admin_api_url("auditlog/query"), params=params, data=query or {})

    def get_audit_log_filter_values(self, projection=None, search=None, start=0, limit=99999):
        """
        Get audit log filter values.
        :param projection: str - item type requested
        :param search: str - optional search string
        :param start: int - start index for paging
        :param limit: int - maximum number of results
        :return: filter values
        """
        params = {"start": start, "limit": limit}
        if projection:
            params["projection"] = projection
        if search:
            params["search"] = search
        return self.post(self._admin_api_url("auditlog/query/filter"), params=params)

    def get_look_and_feel_config(self):
        """Get look and feel configuration."""
        return self.get(self._admin_api_url("look-and-feel/config"))

    def update_look_and_feel_config(self, data):
        """
        Update look and feel configuration.
        :param data: dict - look and feel configuration
        :return:
        """
        return self.put(self._admin_api_url("look-and-feel/config"), data=data)

    def reset_look_and_feel_config(self):
        """Reset look and feel configuration to default."""
        return self.post(self._admin_api_url("look-and-feel/reset-config"))

    def get_remember_me_config(self):
        """Get remember me configuration."""
        return self.get(self._admin_api_url("remember-me/config"))

    def update_remember_me_config(self, data):
        """
        Update remember me configuration.
        :param data: dict - remember me configuration
        :return:
        """
        return self.put(self._admin_api_url("remember-me/config"), data=data)

    def expire_all_remember_me_tokens(self):
        """Expire all remember me tokens."""
        return self.post(self._admin_api_url("remember-me/expire-all"))

    def get_saml_config(self):
        """Get SAML configuration."""
        return self.get(self._admin_api_url("samlconfig"))

    def get_saml_application_config(self, application_id):
        """
        Get SAML configuration for an application.
        :param application_id: str - application id
        :return: SAML application configuration
        """
        return self.get(self._admin_api_url(f"samlconfig/application/{application_id}"))

    def update_saml_application_config(self, application_id, data):
        """
        Update SAML configuration for an application.
        :param application_id: str - application id
        :param data: dict - SAML configuration
        :return:
        """
        return self.post(self._admin_api_url(f"samlconfig/application/{application_id}"), data=data)

    def parse_saml_metadata(self, data):
        """
        Parse SAML metadata.
        :param data: bytes or str - SAML metadata content
        :return: parsed metadata
        """
        headers = {"Content-Type": "application/octet-stream"}
        return self.post(self._admin_api_url("samlconfig/application/parse_metadata"), data=data, headers=headers)

    def parse_saml_metadata_file(self, file_path):
        """
        Parse SAML metadata from a file.
        :param file_path: str - path to SAML metadata file
        :return: parsed metadata
        """
        with open(file_path, "rb") as f:
            return self.post(
                self._admin_api_url("samlconfig/application/parse_metadata_multipart"),
                files={"file": f},
            )

    def reset_saml_certificates(self):
        """Reset SAML certificates."""
        return self.post(self._admin_api_url("samlconfig/reset-certificates"))

    def get_saml_idp_metadata(self):
        """Get SAML identity provider metadata."""
        return self.get(self._admin_api_url("samlconfig/idp/metadata"))

    def find_saml_directory_mapping_mismatch(self, application_id):
        """
        Find directory mappings mismatch for SAML application.
        :param application_id: str - application id
        :return: mismatch info
        """
        return self.get(self._admin_api_url(f"samlconfig/application/{application_id}/directory-mapping-mismatch"))

    def get_dynamic_ldap_pool_statistics(self):
        """Get dynamic LDAP pool statistics."""
        return self.get(self._admin_api_url("dynamic-ldap-pool-statistics"))

    def save_mail_configuration(self, data):
        """
        Save mail server configuration.
        :param data: dict - mail configuration
        :return:
        """
        return self.post(self._admin_api_url("mail/configuration"), data=data)

    def test_mail_configuration(self, data):
        """
        Test mail server connection.
        :param data: dict - mail configuration
        :return:
        """
        return self.post(self._admin_api_url("mail/configuration/test"), data=data)

    def validate_mail_configuration(self, data):
        """
        Validate mail server configuration fields.
        :param data: dict - mail configuration
        :return:
        """
        return self.post(self._admin_api_url("mail/configuration/validate"), data=data)

    def health_check(self):
        """
        Get health status
        https://confluence.atlassian.com/jirakb/how-to-retrieve-health-check-results-using-rest-api-867195158.html
        :return:
        """
        # check as Troubleshooting & Support Tools Plugin
        response = self.get("rest/troubleshooting/1.0/check/")
        if not response:
            # check as support tools
            response = self.get("rest/supportHealthCheck/1.0/check/")
        return response

    def get_plugins_info(self):
        """
        Provide plugins info
        :return a json of installed plugins
        """
        url = "rest/plugins/1.0/"
        return self.get(url, headers=self.no_check_headers, trailing=True)

    def get_plugin_info(self, plugin_key):
        """
        Provide plugin info
        :return a json of installed plugins
        """
        url = f"rest/plugins/1.0/{plugin_key}-key"
        return self.get(url, headers=self.no_check_headers, trailing=True)

    def get_plugin_license_info(self, plugin_key):
        """
        Provide plugin license info
        :return a json specific License query
        """
        url = f"rest/plugins/1.0/{plugin_key}-key/license"
        return self.get(url, headers=self.no_check_headers, trailing=True)

    def upload_plugin(self, plugin_path):
        """
        Provide plugin path for upload into Jira e.g. useful for auto deploy
        :param plugin_path:
        :return:
        """
        files = {"plugin": open(plugin_path, "rb")}
        upm_token = self.request(
            method="GET",
            path="rest/plugins/1.0/",
            headers=self.no_check_headers,
            trailing=True,
        ).headers["upm-token"]
        url = f"rest/plugins/1.0/?token={upm_token}"
        return self.post(url, files=files, headers=self.no_check_headers)

    def delete_plugin(self, plugin_key):
        """
        Delete plugin
        :param plugin_key:
        :return:
        """
        url = f"rest/plugins/1.0/{plugin_key}-key"
        return self.delete(url)

    def check_plugin_manager_status(self):
        url = "rest/plugins/latest/safe-mode"
        return self.request(method="GET", path=url, headers=self.safe_mode_headers)

    def update_plugin_license(self, plugin_key, raw_license):
        """
        Update license for plugin
        :param plugin_key:
        :param raw_license:
        :return:
        """
        app_headers = {
            "X-Atlassian-Token": "no-check",
            "Content-Type": "application/vnd.atl.plugins+json",
        }
        url = f"/plugins/1.0/{plugin_key}/license"
        data = {"rawLicense": raw_license}
        return self.put(url, data=data, headers=app_headers)

    @property
    def memberships(self):
        """
        Retrieves full details of all group memberships, with users and nested groups.
        See: https://docs.atlassian.com/atlassian-crowd/5.3.1/REST/#usermanagement/1/group-getAllMemberships
        :return: All membership mapping dict
        """
        path = self._crowd_api_url("usermanagement", "group/membership")
        headers = {"Accept": "application/xml"}
        response = self.get(path, headers=headers)
        soup = BeautifulSoup(response, "xml")
        memberships = {}
        for membership in soup.find_all("membership"):
            group = membership["group"]
            users = [user["name"] for user in membership.find_all("user")]
            memberships[group] = users
        return memberships

    def group_create(self, groupname, description=None, active=True):
        """
        Create new group method
        :param groupname: string: The name of new group
        :param description: string: The description of new group, default is None
        :param active: bool: Weather the group is active, default is True
        :return: Create result
        """
        group = {
            "name": groupname,
            "active": active,
            "description": description,
            "type": "GROUP",
        }

        return self.post(self._crowd_api_url("usermanagement", "group"), data=group)
