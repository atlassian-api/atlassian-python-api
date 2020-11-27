# coding=utf-8

from ..base import BitbucketServerBase


class Permissions(BitbucketServerBase):
    ADMIN = "ADMIN"
    WRITE = "WRITE"
    READ = "READ"

    def __init__(self, url, permission_prefix, *args, **kwargs):
        self.__permission_prefix = permission_prefix
        super(Permissions, self).__init__(url, *args, can_delete=True, **kwargs)

    def __permission(self, permission):
        return "{}_{}".format(self.__permission_prefix, permission)

    def admin(self, name):
        """
        Add the admin permission for a group/user.
        """
        return self.add(name, self.__permission(self.ADMIN))

    def write(self, name):
        """
        Add the write permission for a group/user.
        """
        return self.add(name, self.__permission(self.WRITE))

    def read(self, name):
        """
        Add the read permission for a group/user.
        """
        return self.add(name, self.__permission(self.READ))

    def add(self, name, permission):
        """
        Add the permission for a group/user.

        For project groups see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp160
        For project users see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp166
        For repository groups see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp282
        For repository users see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp288

        :param name: string: The names of the groups/users
        :param permission: string: The permission to grant.

        :return: True on success
        """
        data = self.put(name, permission)
        if "errors" in data:
            return
        return True

    def each(self, filter=None):
        """
        Get all groups/users.

        For project groups see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp159
        For project users see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp165
        For repository groupss see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp280
        For repository users see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp286

        :params filter: string: If specified only group/user names containing the supplied string will be returned

        :return: A generator for the group/user permission objects
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

        For project groups see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp163
        For project users see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp169
        For repository groups see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp284
        For repository users see https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp290

        :params filter: string: If specified only group/user names containing the supplied string will be returned

        :return: A generator for the group/user permission objects
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


class Groups(Permissions):
    def __init__(self, url, permission_prefix, *args, **kwargs):
        super(Groups, self).__init__(url, permission_prefix, *args, **kwargs)

    def _get_object(self, data):
        if "errors" in data:
            return
        return Group(data, **self._new_session_args)


class Users(Permissions):
    def __init__(self, url, permission_prefix, *args, **kwargs):
        super(Users, self).__init__(url, permission_prefix, *args, **kwargs)

    def _get_object(self, data):
        if "errors" in data:
            return
        return User(data, **self._new_session_args)


class PermissionBase(BitbucketServerBase):
    @property
    def permission(self):
        if self.url is None:
            raise NotImplementedError("Pemission not implemented for this object type.")
        return self.get_data("permission")

    @property
    def is_admin(self):
        return True if self.permission == Permissions.ADMIN else False

    @property
    def is_write(self):
        return True if self.permission == Permissions.WRITE else False

    @property
    def is_read(self):
        return True if self.permission == Permissions.READ else False

    @property
    def can_write(self):
        return True if self.permission in (Permissions.ADMIN, Permissions.WRITE) else False

    def delete(self):
        """
        Delete the element.

        :return: True if the permission was deleted
        """
        if self.url is None:
            raise NotImplementedError("Delete not implemented for this object type.")
        data = super(BitbucketServerBase, self).delete(None, params={"name": self.name})
        if "errors" in data:
            return
        return True


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
        print(self.__dict__)
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
