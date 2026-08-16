# coding=utf-8

from .base import BitbucketServerBase
from .globalPermissions import Groups, Users
from .projects import Projects
from .projects.repos import Repositories


class Server(BitbucketServerBase):
    """
    Class implementing parts of the REST API described in
    https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html
    """

    def __init__(self, url, *args, **kwargs):
        kwargs["cloud"] = False
        kwargs["api_root"] = "rest/api"
        kwargs["api_version"] = "1.0"
        url = url.strip("/") + f"/{kwargs['api_root']}/{kwargs['api_version']}"
        super(Server, self).__init__(url, *args, **kwargs)
        self.__projects = Projects(self._sub_url("projects"), **self._new_session_args)
        self.__groups = Groups(self._sub_url("admin/permissions/groups"), **self._new_session_args)
        self.__users = Users(self._sub_url("admin/permissions/users"), **self._new_session_args)

    @property
    def groups(self):
        """
        Property to access the global groups
        Reference: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp62
        """
        return self.__groups

    @property
    def users(self):
        """
        Property to access the global users
        Reference: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp68
        """
        return self.__users

    @property
    def projects(self):
        """
        Property to access the projects
        Reference: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp147
        """
        return self.__projects

    def personal_repositories(self, username):
        """Return repositories owned by a Bitbucket Server/Data Center user.

        ``username`` may be supplied with or without the leading ``~``. The
        returned collection has the same API as ``project.repos`` and uses
        Bitbucket's user-centric ``/users/{userSlug}/repos`` endpoint.
        """
        user_slug = username if username.startswith("~") else f"~{username}"
        return Repositories(self._sub_url(f"users/{user_slug}/repos"), **self._new_session_args)
