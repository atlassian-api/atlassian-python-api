# coding=utf-8

from .repos import Repositories
from ..base import BitbucketServerBase
from ..common import Groups, Users


class Projects(BitbucketServerBase):
    def __init__(self, url, *args, **kwargs):
        super(Projects, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        if "errors" in data:
            return
        return Project(data, **self._new_session_args)

    def create(self, name, key, description, avatar=None):
        """
        Creates a new project with the given values.

        Note that the avatar has to be embedded as either a data-url or a URL to an external image as shown in
        the examples below:

            w.projects.create( "Mars Project", "MARS", "Software for colonizing mars.",
                avatar="data:image/gif;base64,R0lGODlhEAAQAMQAAORHHOVSKudfOulrSOp3WOyDZu6QdvCchPGolfO0o/..."
            )

            w.projects.create( "Mars Project", "MARS", "Software for colonizing mars.",
                avatar="http://i.imgur.com/72tRx4w.gif"
            )

        See https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp148

        :param name: string: The name of the project.
        :param key: string: The key of the project.
        :param description: string: The description of the project.
        :param avatar: string: The avatar of the project.

        :return: The created project object
        """
        return self.__get_object(self.post(None, data={"name": name, "key": key, "description": description}))

    def each(self, name=None, permission=None):
        """
        Get all projects matching the criteria.

        See https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp149

        :param name: string: Name to filter by.
        :param permission: string: Permission to filter by.

        :return: A generator for the project objects
        """
        params = {}
        if name is not None:
            params["name"] = name
        if permission is not None:
            params["permission"] = permission
        for project in self._get_paged(None, params=params):
            yield self.__get_object(project)

        return

    def get(self, project, by="key"):
        """
        Returns the requested project

        :param project: string: The requested project.
        :param by: string: How to interprate project, can be 'key' or 'name'.

        :return: The requested Project object
        """
        if by == "key":
            return self.__get_object(super(Projects, self).get(project))
        elif by == "name":
            for p in self.each(name=project):
                if p.name == project:
                    return p
        else:
            ValueError("Unknown value '{}' for argument [by], expected 'key' or 'name'".format(by))

        raise Exception("Unknown project {} '{}'".format(by, project))


class Project(BitbucketServerBase):
    def __init__(self, data, *args, **kwargs):
        super(Project, self).__init__(None, *args, data=data, can_update=True, can_delete=True, **kwargs)
        self.__groups = Groups(self._sub_url("permissions/groups"), "PROJECT", **self._new_session_args)
        self.__users = Users(self._sub_url("permissions/users"), "PROJECT", **self._new_session_args)
        self.__repos = Repositories(self._sub_url("repos"), **self._new_session_args)

    @property
    def name(self):
        return self.get_data("name")

    @name.setter
    def name(self, name):
        return self.update(data={"name": name})

    @property
    def key(self):
        return self.get_data("key")

    @key.setter
    def key(self, key):
        return self.update(data={"key": key})

    @property
    def description(self):
        return self.get_data("description")

    @description.setter
    def description(self, description):
        return self.update(data={"description": description})

    @property
    def public(self):
        return self.get_data("public")

    @public.setter
    def public(self, public):
        return self.update(data={"public": public})

    @property
    def id(self):
        return self.get_data("id")

    @property
    def type(self):
        return self.get_data("type")

    def get_avatar(self, s=0):
        """
        :param s: int (default 0): The desired size of the image. The server will return
                                   an image as close as possible to the specified size.
        """
        return self.get("avatar.png", params={"s": s})

    def set_avatar(self, avatar):
        """
        :param avatar: See function create for examples.
        """
        return self.post("avatar.png", data={"avatar": avatar})

    @property
    def groups(self):
        """
        Property to access the project groups (https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp158)
        """
        return self.__groups

    @property
    def users(self):
        """
        Property to access the project groups (https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp164)
        """
        return self.__users

    @property
    def repos(self):
        """
        Property to access the repositories (https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp173)
        """
        return self.__repos
