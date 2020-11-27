# coding=utf-8

from ..base import BitbucketCloudBase

from .projects import Projects
from ..repositories import WorkspaceRepositories


class Workspaces(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(Workspaces, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        if "errors" in data:
            return
        return Workspace(data, **self._new_session_args)

    def each(self, role=None, q=None, sort=None):
        """
        Get all workspaces matching the criteria.

        :param role: string: Filters the workspaces based on the authenticated user"s role on each workspace.
                             * member: returns a list of all the workspaces which the caller is a member of
                               at least one workspace group or repository
                             * collaborator: returns a list of workspaces which the caller has write access
                               to at least one repository in the workspace
                             * owner: returns a list of workspaces which the caller has administrator access
        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the Workspace objects
        """
        params = {}
        if role is not None:
            params["role"] = role
        if q is not None:
            params["q"] = q
        if sort is not None:
            params["sort"] = sort
        for workspace in self._get_paged(None, params):
            yield self.__get_object(workspace)

        return

    def get(self, workspace):
        """
        Returns the requested workspace

        :param workspace: string: This can either be the workspace ID (slug) or the workspace UUID
                                  surrounded by curly-braces, for example: {workspace UUID}.

        :return: The requested Workspace objects
        """
        return self.__get_object(super(Workspaces, self).get(workspace))


class Workspace(BitbucketCloudBase):
    def __init__(self, data, *args, **kwargs):
        super(Workspace, self).__init__(None, *args, data=data, expected_type="workspace", **kwargs)
        self.__projects = Projects(self.get_link("projects"), **self._new_session_args)
        self.__repositories = WorkspaceRepositories(self.get_link("repositories"), **self._new_session_args)

    @property
    def projects(self):
        return self.__projects

    @property
    def repositories(self):
        return self.__repositories

    @property
    def name(self):
        return self.get_data("name")

    @property
    def slug(self):
        return self.get_data("slug")

    def uuid(self):
        return self.get_data("uuid")

    @property
    def is_private(self):
        return self.get_data("is_private")

    @property
    def created_on(self):
        return self.get_data("created_on")

    @property
    def updated_on(self):
        return self.get_data("updated_on", "never updated")

    def get_avatar(self):
        return self.get(self.get_link("avatar"), absolute=True)
