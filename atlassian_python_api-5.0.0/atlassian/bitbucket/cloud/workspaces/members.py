# coding=utf-8

from ..base import BitbucketCloudBase


class WorkspaceMembers(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(WorkspaceMembers, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        return WorkspaceMember(data, **self._new_session_args)

    def each(self):
        """
        Get all members in the workspace

        :return: A generator for the member objects

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-workspaces/#api-workspaces-workspace-members-get
        """
        for member in self._get_paged(None):
            yield self.__get_object(member)

        return

    def get(self, member):
        """
        Returns the requested member

        :param member: string: Member's UUID or Atlassian ID.

        :return: The requested Member object

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-workspaces/#api-workspaces-workspace-members-member-get
        """

        return self.__get_object(super(WorkspaceMembers, self).get(member))


class WorkspaceMember(BitbucketCloudBase):
    def __init__(self, data, *args, **kwargs):
        super(WorkspaceMember, self).__init__(None, *args, data=data, expected_type="workspace_membership", **kwargs)

    @property
    def links(self):
        """The member links"""
        return self.get_data("links")

    @property
    def type(self):
        """The member type"""
        return self.get_data("type")

    @property
    def user(self):
        """The member user dictionary"""
        return self.get_data("user")

    @property
    def workspace(self):
        """The member workspace dictionary"""
        return self.get_data("workspace")
