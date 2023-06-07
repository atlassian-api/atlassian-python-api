# coding=utf-8



from ..base import BitbucketCloudBase


class Permissions(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(Permissions, self).__init__(url, *args, **kwargs)

    def __get_object_workspace_membership(self, data):
        return WorkspaceMembership(
            self.url,
            data,
            **self._new_session_args,
        )

    def each(self, q=None, sort=None, pagelen=10):
        """
        Returns the list of pipelines in this repository.

        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the Workspace Permission objects

        API docs: https://developer.atlassian.com/cloud/bitbucket/rest/api-group-workspaces/#api-workspaces-workspace-permissions-get
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        params["pagelen"] = pagelen
        for workspace_membership in self._get_paged(
            None,
            trailing=True,
            paging_workaround=True,
            params=params,
        ):
            yield self.__get_object_workspace_membership(workspace_membership)

        return


class WorkspaceMembership(BitbucketCloudBase):
    def __init__(self, url, data, *args, **kwargs):
        super(WorkspaceMembership, self).__init__(url, *args, data=data, expected_type="workspace_membership", **kwargs)

    @property
    def uuid(self):
        """The workspace_membership uuid"""
        return self.get_data("uuid")

    @property
    def type(self):
        """The workspace_membership type"""
        return self.get_data("type")

    @property
    def user(self):
        """The workspace_membership user"""
        return self.get_data("user")

    @property
    def workspace(self):
        """The workspace_membership workspace"""
        return self.get_data("workspace")

    @property
    def links(self):
        """The workspace_membership links"""
        return self.get_data("links")

    @property
    def added_on(self):
        """The workspace_membership added on"""
        return self.get_time("added_on")

    @property
    def permission(self):
        """The workspace_membership permission"""
        return self.get_data("permission")

    @property
    def last_accessed(self):
        """The workspace_membership last accessed"""
        return self.get_time("last_accessed")
