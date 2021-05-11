# coding=utf-8

from .base import BitbucketServerBase


class GlobalPermissions(BitbucketServerBase):
    LICENSED_USER = "LICENSED_USER"
    PROJECT_CREATE = "PROJECT_CREATE"
    ADMIN = "ADMIN"
    SYS_ADMIN = "SYS_ADMIN"

    def __init__(self, url, *args, **kwargs):
        super(GlobalPermissions, self).__init__(url, *args, **kwargs)

    def licensed_user(self, name):
        """
        Add the licensed user permission for a group/user.
        """
        return self.add(name, self.__permission(self.LICENSED_USER))

    def project_create(self, name):
        """
        Add the project create permission for a group/user.
        """
        return self.add(name, self.__permission(self.PROJECT_CREATE))

    def admin(self, name):
        """
        Add the admin permission for a group/user.
        """
        return self.add(name, self.__permission(self.ADMIN))

    def sys_admin(self, name):
        """
        Add the sys admin permission for a group/user.
        """
        return self.add(name, self.__permission(self.SYS_ADMIN))

    def add(self, name, permission):
        """
        Add the permission for a group/user.

        :param name: string: The names of the groups/users
        :param permission: string: The permission to grant.

        API docs:
        - For groups see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp64
        - For users see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp70
        """
        self.put(name, permission)
        return

    def each(self, filter=None):
        """
        Get all groups/users.

        :params filter: string: If specified only group/user names containing the supplied string will be returned

        :return: A generator for the group/user permission objects

        API docs:
        - For groups see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp63
        - For users see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp69
        """
        params = {}
        if filter is not None:
            params["filter"] = filter
        for entry in self._get_paged(None, params=params):
            entry = self._get_object(entry)
            entry.url = self.url
            yield entry

    def each_none(self, filter=None):
        """
        Get all not granted groups/users.

        :params filter: string: If specified only group/user names containing the supplied string will be returned

        :return: A generator for the group/user permission objects

        API docs:
        - For groups see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp67
        - For users see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp73
        """
        params = {}
        if filter is not None:
            params["filter"] = filter
        for entry in self._get_paged("none", params=params):
            yield self._get_object(entry)

    def get(self, name):
        """
        Returns the requested group/user

        :param name: string: The requested element name.

        :return: The requested group/user object
        """
        for entry in self.each(filter=name):
            if entry.name == name:
                return entry

        raise Exception("Unknown group/user '{}'".format(name))


class Groups(GlobalPermissions):
    def __init__(self, url, *args, **kwargs):
        super(Groups, self).__init__(url, *args, **kwargs)

    def _get_object(self, data):
        return Group(data, **self._new_session_args)


class Users(GlobalPermissions):
    def __init__(self, url, *args, **kwargs):
        super(Users, self).__init__(url, *args, **kwargs)

    def _get_object(self, data):
        return User(data, **self._new_session_args)


class PermissionBase(BitbucketServerBase):
    @property
    def permission(self):
        if self.url is None:
            raise NotImplementedError("Permission not implemented for this object type.")
        return self.get_data("permission")

    @property
    def is_licensed_user(self):
        return True if self.permission == GlobalPermissions.LICENSED_USER else False

    @property
    def is_project_create(self):
        return True if self.permission == GlobalPermissions.PROJECT_CREATE else False

    @property
    def is_admin(self):
        return True if self.permission == GlobalPermissions.ADMIN else False

    @property
    def is_sys_admin(self):
        return True if self.permission == GlobalPermissions.SYS_ADMIN else False

    def delete(self):
        """
        Delete the permission.

        :return: The response on success
        """
        if self.url is None:
            raise NotImplementedError("Delete not implemented for this object type.")
        return super(PermissionBase, self).delete(None, params={"name": self.name})


class Group(PermissionBase):
    def __init__(self, data, *args, **kwargs):
        super(Group, self).__init__(None, *args, data=data, **kwargs)

    @property
    def name(self):
        if self.url is None:
            return self.get_data("name")
        return self.get_data("group")["name"]


class User(PermissionBase):
    def __init__(self, data, *args, **kwargs):
        super(User, self).__init__(None, *args, data=data, **kwargs)

    def __userdata(self, key):
        if self.url is None:
            return self.get_data(key)
        return self.get_data("user")[key]

    @property
    def name(self):
        return self.__userdata("name")

    @property
    def email(self):
        return self.__userdata("emailAddress")

    @property
    def displayname(self):
        return self.__userdata("displayName")

    @property
    def active(self):
        return self.__userdata("active")

    @property
    def slug(self):
        return self.__userdata("slug")

    @property
    def id(self):
        return self.__userdata("id")
