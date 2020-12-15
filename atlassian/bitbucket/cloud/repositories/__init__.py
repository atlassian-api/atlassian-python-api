# coding=utf-8

from ..base import BitbucketCloudBase
from .issues import Issues
from .branchRestrictions import BranchRestrictions
from .defaultReviewers import DefaultReviewers
from .pipelines import Pipelines


class RepositoriesBase(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(RepositoriesBase, self).__init__(url, *args, **kwargs)

    def _get_object(self, data):
        if "errors" in data:
            return
        return Repository(data, **self._new_session_args)


class Repositories(RepositoriesBase):
    def __init__(self, url, *args, **kwargs):
        super(Repositories, self).__init__(url, *args, **kwargs)

    def each(self, after=None, role=None, q=None, sort=None):
        """
        Get all repositories matching the criteria.

        The result can be narrowed down based on the authenticated user"s role.
        E.g. with ?role=contributor, only those repositories that the authenticated user has write access to
        are returned (this includes any repo the user is an admin on, as that implies write access).

        :param after: string: Filter the results to include only repositories created on or after this ISO-8601
                              timestamp. Example: YYYY-MM-DDTHH:mm:ss.sssZ
        :param role: string: Filters the workspaces based on the authenticated user"s role on each workspace.
                             * member: returns a list of all the workspaces which the caller is a member of
                               at least one workspace group or repository
                             * collaborator: returns a list of workspaces which the caller has write access
                               to at least one repository in the workspace
                             * owner: returns a list of workspaces which the caller has administrator access
        :param q: string: Query string to narrow down the response. role parameter must also be specified.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the Rorkspace objects
        """
        if q is not None and role is None:
            raise ValueError("Argument [q] requires argument [role].")

        params = {}
        if after is not None:
            params["after"] = after
        if role is not None:
            params["role"] = role
        if q is not None:
            params["q"] = q
        if sort is not None:
            params["sort"] = sort
        for repository in self._get_paged(None, params):
            yield self._get_repository_object(repository)


class WorkspaceRepositories(RepositoriesBase):
    def __init__(self, url, *args, **kwargs):
        super(WorkspaceRepositories, self).__init__(url, *args, **kwargs)

    def each(self, role=None, q=None, sort=None):
        """
        Get all repositories in the workspace matching the criteria.

        :param role: string: Filters the workspaces based on the authenticated user"s role on each workspace.
                             * member: returns a list of all the workspaces which the caller is a member of
                               at least one workspace group or repository
                             * collaborator: returns a list of workspaces which the caller has write access
                               to at least one repository in the workspace
                             * owner: returns a list of workspaces which the caller has administrator access
        :param q: string: Query string to narrow down the response. role parameter must also be specified.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the Rorkspace objects
        """
        params = {}
        if role is not None:
            params["role"] = role
        if q is not None:
            params["q"] = q
        if sort is not None:
            params["sort"] = sort
        for repository in self._get_paged(None, params):
            yield self._get_object(repository)

    def get(self, repository, by="slug"):
        """
        Returns the requested repository

        :param repository: string: The requested repository.
        :param by: string: How to interprate repository, can be 'slug' or 'name'.

        :return: The requested Repository object
        """
        if by == "slug":
            return self._get_object(super(WorkspaceRepositories, self).get(repository))
        elif by == "name":
            for r in self.each():
                if r.name == repository:
                    return r
        else:
            ValueError("Unknown value '{}' for argument [by], expected 'key' or 'name'".format(by))

        raise Exception("Unknown repository {} '{}'".format(by, repository))


class ProjectRepositories(RepositoriesBase):
    def __init__(self, url, *args, **kwargs):
        super(ProjectRepositories, self).__init__(url, *args, **kwargs)

    def each(self, sort=None):
        """
        Get all repositories in the project matching the criteria.

        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the Rorkspace objects
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        for repository in self._get_paged(None, params):
            yield self._get_object(repository)

    def get(self, repository, by="slug"):
        """
        Returns the requested repository

        :param repository: string: The requested repository.
        :param by: string: How to interprate repository, can be 'slug' or 'name'.

        :return: The requested Repository object
        """
        if by not in ("slug", "name"):
            ValueError("Unknown value '{}' for argument [by], expected 'slug' or 'name'".format(by))

        for r in self.each():
            if ((by == "slug") and (r.slug == repository)) or ((by == "name") and (r.name == repository)):
                return r

        raise Exception("Unknown repository {} '{}'".format(by, repository))


class Repository(BitbucketCloudBase):
    def __init__(self, data, *args, **kwargs):
        super(Repository, self).__init__(None, *args, data=data, expected_type="repository", **kwargs)
        self.__branch_restrictions = BranchRestrictions(
            "{}/branch-restrictions".format(self.url), **self._new_session_args
        )
        self.__default_reviewers = DefaultReviewers("{}/default-reviewers".format(self.url), **self._new_session_args)
        self.__issues = Issues("{}/issues".format(self.url), **self._new_session_args)
        self.__pipelines = Pipelines("{}/pipelines".format(self.url), **self._new_session_args)

    @property
    def branch_restrictions(self):
        return self.__branch_restrictions

    @property
    def default_reviewers(self):
        return self.__default_reviewers

    @property
    def issues(self):
        return self.__issues

    @property
    def pipelines(self):
        return self.__pipelines

    @property
    def name(self):
        return self.get_data("name")

    @property
    def slug(self):
        return self.get_data("slug")

    @property
    def description(self):
        return self.get_data("description")

    @property
    def is_private(self):
        return self.get_data("is_private")

    @property
    def uuid(self):
        return self.get_data("uuid")

    @property
    def size(self):
        return self.get_data("size")

    @property
    def created_on(self):
        return self.get_data("created_on")

    @property
    def updated_on(self):
        return self.get_data("updated_on", "never updated")

    def get_avatar(self):
        return self.get(self.get_link("avatar"), absolute=True)
