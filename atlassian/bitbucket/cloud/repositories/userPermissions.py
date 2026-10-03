# coding=utf-8

from ..base import BitbucketCloudBase
from ..common.users import User


class UserPermissions(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(UserPermissions, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        return UserPermission(self.url, data, **self._new_session_args)  # fmt: skip

    def each(self, q=None, sort=None):
        """
        Returns the list of explicit user permissions in this repository.

        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the UserPermission objects

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-repositories/#api-repositories-workspace-repo-slug-permissions-config-users-get
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        for user_permission in self._get_paged(
            None,
            trailing=True,
            params=params,
        ):
            yield self.__get_object(user_permission)

        return

    def get(self, user_id):
        """
        Returns the explicit user permission for the given user in this repository.

        :param user_id: string: The UUID of the account surrounded by curly-braces
                                (for example ``{account UUID}``) or an Atlassian
                                Account ID (for example ``557058:ba8948b2-...``).

        :return: The requested UserPermission object

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-repositories/#api-repositories-workspace-repo-slug-permissions-config-users-selected-user-id-get
        """
        return self.__get_object(super(UserPermissions, self).get(user_id))

    def grant(self, user_id, permission):
        """
        Grant (or update) an explicit permission for the given user on this repository.

        The user must be a member of the workspace and cannot be the workspace
        owner. Only users with admin permission for the repository may call
        this resource, and only app password authentication is accepted.

        :param user_id: string: The UUID of the account surrounded by curly-braces
                                (for example ``{account UUID}``) or an Atlassian
                                Account ID (for example ``557058:ba8948b2-...``).
        :param permission: string: One of 'read', 'write' or 'admin'.

        :return: The updated UserPermission object

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-repositories/#api-repositories-workspace-repo-slug-permissions-config-users-selected-user-id-put
        """
        if permission not in ("read", "write", "admin"):
            raise ValueError(f"Invalid permission '{permission}', expected 'read', 'write' or 'admin'")
        return self.__get_object(self.put(user_id, data={"permission": permission}))

    def revoke(self, user_id):
        """
        Remove the explicit user permission for the given user on this repository,
        if one exists.

        :param user_id: string: The UUID of the account surrounded by curly-braces
                                (for example ``{account UUID}``) or an Atlassian
                                Account ID (for example ``557058:ba8948b2-...``).

        :return: The response on success

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-repositories/#api-repositories-workspace-repo-slug-permissions-config-users-selected-user-id-delete
        """
        return self.delete(user_id)


class UserPermission(BitbucketCloudBase):
    def __init__(self, url, data, *args, **kwargs):
        super(UserPermission, self).__init__(
            url, *args, data=data, expected_type="repository_user_permission", **kwargs
        )

    def update(self, permission):
        """
        Update the permission level.

        :param permission: string: One of 'read', 'write' or 'admin'.

        :return: The updated UserPermission object

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-repositories/#api-repositories-workspace-repo-slug-permissions-config-users-selected-user-id-put
        """
        if permission not in ("read", "write", "admin"):
            raise ValueError(f"Invalid permission '{permission}', expected 'read', 'write' or 'admin'")
        return self._update_data(self.put(None, data={"permission": permission}))

    def delete(self):
        """
        Remove the explicit user permission.

        :return: The response on success

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-repositories/#api-repositories-workspace-repo-slug-permissions-config-users-selected-user-id-delete
        """
        return super(UserPermission, self).delete(None)

    @property
    def type(self):
        """The user permission type"""
        return self.get_data("type")

    @property
    def permission(self):
        """The user permission level ('read', 'write', 'admin' or 'none')"""
        return self.get_data("permission")

    @property
    def user(self):
        """The user the permission is granted to"""
        data = self.get_data("user")
        return User(None, data) if data is not None else None

    @property
    def links(self):
        """The user permission links"""
        return self.get_data("links")
