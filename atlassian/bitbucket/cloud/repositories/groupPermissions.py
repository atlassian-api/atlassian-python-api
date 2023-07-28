# coding=utf-8

from ..base import BitbucketCloudBase


class GroupPermissions(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(GroupPermissions, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        return GroupPermission(
            self.url,
            data,
            **self._new_session_args
        )  # fmt: skip

    def each(self, q=None, sort=None):
        """
        Returns the list of group permissions in this repository.

        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the GroupPermission objects

        API docs: https://developer.atlassian.com/cloud/bitbucket/rest/api-group-repositories/#api-repositories-workspace-repo-slug-permissions-config-groups-get
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        for group_permission in self._get_paged(
            None,
            trailing=True,
            params=params,
        ):
            yield self.__get_object(group_permission)

        return

    def get(self, group_slug):
        """
        Returns the group permission with the group slug in this repository.

        :param group_slug: string: The requested permission group_slug

        :return: The requested GroupPermission objects

        API docs: https://developer.atlassian.com/cloud/bitbucket/rest/api-group-repositories/#api-repositories-workspace-repo-slug-permissions-config-groups-group-slug-get
        """
        return self.__get_object(super(GroupPermissions, self).get(group_slug))


class GroupPermission(BitbucketCloudBase):
    def __init__(self, url, data, *args, **kwargs):
        super(GroupPermission, self).__init__(
            url, *args, data=data, expected_type="repository_group_permission", **kwargs
        )

    @property
    def type(self):
        """The repository variable type"""
        return self.get_data("type")

    @property
    def permission(self):
        """The repository variable permission"""
        return self.get_data("permission")

    @property
    def group(self):
        """The repository variable group"""
        return self.get_data("group")

    @property
    def links(self):
        """The repository variable links"""
        return self.get_data("links")
