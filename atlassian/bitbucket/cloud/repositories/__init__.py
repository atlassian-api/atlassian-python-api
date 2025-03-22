# coding=utf-8

from requests import HTTPError
from ..base import BitbucketCloudBase
from .issues import Issues
from .branchRestrictions import BranchRestrictions
from .commits import Commits
from .hooks import Hooks
from .defaultReviewers import DefaultReviewers
from .deploymentEnvironments import DeploymentEnvironments
from .groupPermissions import GroupPermissions
from .pipelines import Pipelines
from .pullRequests import PullRequests
from .refs import Branches, Tags
from .repositoryVariables import RepositoryVariables


class RepositoriesBase(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(RepositoriesBase, self).__init__(url, *args, **kwargs)

    def _get_object(self, data):
        return Repository(data, **self._new_session_args)


class Repositories(RepositoriesBase):
    def __init__(self, url, *args, **kwargs):
        super(Repositories, self).__init__(url, *args, **kwargs)

    def each(self, after=None, role=None, q=None, sort=None, pagelen=None):
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
        :param pagelen: int: Name of a response property to change page size.
                             See https://developer.atlassian.com/cloud/bitbucket/rest/intro/#pagination for details.

        :return: A generator for the repository objects

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories#get
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
        if pagelen is not None:
            params["pagelen"] = pagelen
        for repository in self._get_paged(None, params):
            yield self._get_object(repository)

    def get(self, workspace, repo_slug):
        """
        Returns the requested repository.

        Since this method accesses the repository endpoint
        directly it is usable if you do not have permission
        to access the workspace endpoint.

        :param workspace: string: The workspace of the repository
        :param repo_slug: string: The requested repository.

        :return: The requested Repository object

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-repositories/#api-repositories-workspace-repo-slug-get
        """
        return self._get_object(super(Repositories, self).get(f"{workspace}/{repo_slug}"))


class WorkspaceRepositories(RepositoriesBase):
    ALLOW_FORKS = "allow_forks"
    NO_PUBLIC_FORKS = "no_public_forks"
    NO_FORKS = "no_forks"
    FORK_POLICIES = [
        ALLOW_FORKS,
        NO_PUBLIC_FORKS,
        NO_FORKS,
    ]

    def __init__(self, url, *args, **kwargs):
        super(WorkspaceRepositories, self).__init__(url, *args, **kwargs)

    def create(self, repo_slug, project_key=None, is_private=None, fork_policy=None):
        """
        Creates a new repository with the given repo_slug.

        :param repo_slug: string: The repo_slug of the project.
        :param project_key: string: The key of the project. If the project is not provided, the repository
                                    is automatically assigned to the oldest project in the workspace.
        :param is_private: boolean: Set to false if the repository shall be public.
        :param fork_policy: string: The fork policy (one of WorkspaceRepositories.ALLOW_FORKS,
                                    WorkspaceRepositories.NO_PUBLIC_FORKS, WorkspaceRepositories.NO_FORKS).

        :return: The created project object

        API docs:
        https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D#post
        """

        data = {"scm": "git"}
        if project_key is not None:
            data["project"] = {"key": project_key}
        if is_private is not None:
            data["is_private"] = is_private
        if fork_policy is not None:
            if fork_policy not in self.FORK_POLICIES:
                raise ValueError(f"fork_policy must be one of {self.FORK_POLICIES}")
            data["fork_policy"] = fork_policy
        return self._get_object(self.post(repo_slug, data=data))

    def each(self, role=None, q=None, sort=None):
        """
        Get all repositories in the workspace matching the criteria.

        :param role: string: Filters the workspaces based on the authenticated user's role on each workspace.
                             * member: returns a list of all the workspaces which the caller is a member of
                               at least one workspace group or repository
                             * collaborator: returns a list of workspaces which the caller has write access
                               to at least one repository in the workspace
                             * owner: returns a list of workspaces which the caller has administrator access
        :param q: string: Query string to narrow down the response. role parameter must also be specified.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the workspace objects

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D#get
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

        API docs:
        https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D#get
        """
        if by == "slug":
            return self._get_object(super(WorkspaceRepositories, self).get(repository))
        elif by == "name":
            for r in self.each():
                if r.name == repository:
                    return r
        else:
            ValueError(f"Unknown value '{by}' for argument [by], expected 'key' or 'name'")

        raise Exception(f"Unknown repository {by} '{repository}'")

    def exists(self, repository, by="slug"):
        """
        Check if repository exist.

        :param repository: string: The requested repository.
        :param by: string (default is "slug"): How to interpret repository, can be 'slug' or 'name'.

        :return: True if the repository exists

        API docs:
        https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D#get
        """
        exists = False
        try:
            self.get(repository, by)
            exists = True
        except HTTPError as e:
            if e.response.status_code in (401, 404):
                pass
        except Exception as e:
            if not str(e) == f"Unknown project {by} '{repository}'":
                raise e
        return exists


class ProjectRepositories(RepositoriesBase):
    def __init__(self, url, *args, **kwargs):
        super(ProjectRepositories, self).__init__(url, *args, **kwargs)

    def each(self, sort=None):
        """
        Get all repositories in the project matching the criteria.

        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the repository objects

        API docs:
        https://developer.atlassian.com/bitbucket/api/2/reference/resource/workspaces/%7Bworkspace%7D/projects/%7Bproject_key%7D#get
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

        API docs:
        https://developer.atlassian.com/bitbucket/api/2/reference/resource/workspaces/%7Bworkspace%7D/projects/%7Bproject_key%7D#get
        """
        if by not in ("slug", "name"):
            ValueError(f"Unknown value '{by}' for argument [by], expected 'slug' or 'name'")

        for r in self.each():
            if ((by == "slug") and (r.slug == repository)) or ((by == "name") and (r.name == repository)):
                return r

        raise Exception(f"Unknown repository {by} '{repository}'")


class Repository(BitbucketCloudBase):
    def __init__(self, data, *args, **kwargs):
        super(Repository, self).__init__(None, *args, data=data, expected_type="repository", **kwargs)
        self.__branch_restrictions = BranchRestrictions(f"{self.url}/branch-restrictions", **self._new_session_args)
        self.__branches = Branches(f"{self.url}/refs/branches", **self._new_session_args)
        self.__commits = Commits(
            f"{self.url}/commits",
            data={"links": {"commit": {"href": f"{self.url}/commit"}}},
            **self._new_session_args
        )  # fmt: skip
        self.__hooks = Hooks(
            f"{self.url}/hooks",
            data={"links": {"hooks": {"href": f"{self.url}/hooks"}}},
            **self._new_session_args
        )  # fmt: skip
        self.__default_reviewers = DefaultReviewers(f"{self.url}/default-reviewers", **self._new_session_args)
        self.__deployment_environments = DeploymentEnvironments(f"{self.url}/environments", **self._new_session_args)
        self.__group_permissions = GroupPermissions(f"{self.url}/permissions-config/groups", **self._new_session_args)
        self.__issues = Issues(f"{self.url}/issues", **self._new_session_args)
        self.__pipelines = Pipelines(f"{self.url}/pipelines", **self._new_session_args)
        self.__pullrequests = PullRequests(f"{self.url}/pullrequests", **self._new_session_args)
        self.__repository_variables = RepositoryVariables(
            f"{self.url}/pipelines_config/variables", **self._new_session_args
        )
        self.__tags = Tags(f"{self.url}/refs/tags", **self._new_session_args)

    def update(self, **kwargs):
        """
        Update the repository properties. Fields not present in the request body are ignored.

        :param kwargs: dict: The data to update.

        :return: The updated repository

        API docs:
        https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D#put
        """
        return self._update_data(self.put(None, data=kwargs))

    def delete(self, redirect_to=None):
        """
        Delete the repostory.

        :param redirect_to: string (default is None): If a repository has been moved to a new location, use this
                                                      parameter to show users a friendly message in the Bitbucket UI
                                                      that the repository has moved to a new location. However, a GET
                                                      to this endpoint will still return a 404.

        :return: The response on success

        API docs:
        https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D#delete
        """
        params = {}
        if redirect_to is not None:
            params["redirect_to"] = redirect_to
        return super(Repository, self).delete(None, params=params)

    @property
    def name(self):
        """The repository name"""
        return self.get_data("name")

    @name.setter
    def name(self, name):
        """Setter for the repository name"""
        return self.update(name=name)

    @property
    def slug(self):
        """The repository slug"""
        return self.get_data("slug")

    @property
    def description(self):
        """The repository description"""
        return self.get_data("description")

    @description.setter
    def description(self, description):
        """Setter for the repository description"""
        return self.update(description=description)

    @property
    def is_private(self):
        """The repository private flag"""
        return self.get_data("is_private")

    @is_private.setter
    def is_private(self, is_private):
        """Setter for the repository private flag"""
        return self.update(is_private=is_private)

    @property
    def fork_policy(self):
        """Getter for the repository fork policy"""
        return self.get_data("fork_policy")

    @property
    def uuid(self):
        """The repository uuid"""
        return self.get_data("uuid")

    @property
    def size(self):
        """The repository size"""
        return self.get_data("size")

    @property
    def created_on(self):
        """The repository creation time"""
        return self.get_data("created_on")

    @property
    def updated_on(self):
        """The repository last update time"""
        return self.get_data("updated_on", "never updated")

    def get_avatar(self):
        """The repository avatar"""
        return self.get(self.get_link("avatar"), absolute=True)

    @property
    def branch_restrictions(self):
        """The repository branch restrictions"""
        return self.__branch_restrictions

    @property
    def branches(self):
        """The repository branches."""
        return self.__branches

    @property
    def commits(self):
        """The repository commits."""
        return self.__commits

    @property
    def hooks(self):
        """The repository hooks."""
        return self.__hooks

    @property
    def default_reviewers(self):
        """The repository default reviewers"""
        return self.__default_reviewers

    @property
    def deployment_environments(self):
        """The repository deployment environments"""
        return self.__deployment_environments

    @property
    def issues(self):
        """The repository issues"""
        return self.__issues

    @property
    def group_permissions(self):
        """The repository group permissions"""
        return self.__group_permissions

    @property
    def pipelines(self):
        """The repository pipelines"""
        return self.__pipelines

    @property
    def pullrequests(self):
        """The repository pull requests"""
        return self.__pullrequests

    @property
    def repository_variables(self):
        """The repository variables"""
        return self.__repository_variables

    @property
    def tags(self):
        """The repository tags."""
        return self.__tags
