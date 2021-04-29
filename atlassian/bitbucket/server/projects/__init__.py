# coding=utf-8

from requests import HTTPError
from .repos import Repositories
from ..base import BitbucketServerBase
from ..common.permissions import Groups, Users


class Projects(BitbucketServerBase):
    def __init__(self, url, *args, **kwargs):
        super(Projects, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
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

        :param name: string: The name of the project.
        :param key: string: The key of the project.
        :param description: string: The description of the project.
        :param avatar: string: The avatar of the project.

        :return: The created project object

        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp148
        """
        return self.__get_object(self.post(None, data={"name": name, "key": key, "description": description}))

    def each(self, name=None, permission=None):
        """
        Get all projects matching the criteria.

        :param name: string: Name to filter by.
        :param permission: string: Permission to filter by.

        :return: A generator for the project objects

        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp149
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
        :param by: string (default is "key"): How to interpret project, can be 'key' or 'name'.

        :return: The requested Project object

        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp153
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

    def exists(self, project, by="key"):
        """
        Check if project exist.

        :param project: string: The requested project.
        :param by: string (default is "key"): How to interpret project, can be 'key' or 'name'.

        :return: True if the project exists
        """
        exists = False
        try:
            self.get(project, by)
            exists = True
        except HTTPError as e:
            if e.response.status_code in (401, 404):
                pass
        except Exception as e:
            if not str(e) == "Unknown project {} '{}'".format(by, project):
                raise e
        return exists


class Project(BitbucketServerBase):
    def __init__(self, data, *args, **kwargs):
        super(Project, self).__init__(None, *args, data=data, **kwargs)
        self.__groups = Groups(self._sub_url("permissions/groups"), "PROJECT", **self._new_session_args)
        self.__users = Users(self._sub_url("permissions/users"), "PROJECT", **self._new_session_args)
        self.__repos = Repositories(self._sub_url("repos"), **self._new_session_args)

    def delete(self):
        """
        Delete the project.

        :return: The response on success

        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp151
        """
        return super(Project, self).delete(None)

    def update(self, **kwargs):
        """
        Update the project properties. Fields not present in the request body are ignored.

        :param kwargs: dict: The data to update.

        :return: The updated project

        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp152
        """
        return self._update_data(self.put(None, data=kwargs))

    @property
    def id(self):
        """The project identifier"""
        return self.get_data("id")

    @property
    def type(self):
        """The project type"""
        return self.get_data("type")

    @property
    def name(self):
        """The project name"""
        return self.get_data("name")

    @name.setter
    def name(self, name):
        """Setter for the project name"""
        return self.update(name=name)

    @property
    def key(self):
        """The project key"""
        return self.get_data("key")

    @key.setter
    def key(self, key):
        """Setter for the project key"""
        return self.update(key=key)

    @property
    def description(self):
        """The project description"""
        return self.get_data("description")

    @description.setter
    def description(self, description):
        """Setter for the project description"""
        return self.update(description=description)

    @property
    def public(self):
        """The project public flag"""
        return self.get_data("public")

    @public.setter
    def public(self, public):
        """Setter for the project public flag"""
        return self.update(public=public)

    def get_avatar(self, s=0):
        """
        Get the avatar.

        :param s: int (default 0): The desired size of the image. The server will return
                                   an image as close as possible to the specified size.

        :return: The response on success

        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp155
        """
        return self.get("avatar.png", params={"s": s})

    def set_avatar(self, avatar):
        """
        Set the avatar.

        :param avatar: See function create for examples.

        :return: The response on success

        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp156
        """
        return self.post("avatar.png", data={"avatar": avatar})

    @property
    def groups(self):
        """
        Property to access the project groups
        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp158
        """
        return self.__groups

    @property
    def users(self):
        """
        Property to access the project groups
        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp164
        """
        return self.__users

    @property
    def repos(self):
        """
        Property to access the repositories
        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp173
        """
        return self.__repos
