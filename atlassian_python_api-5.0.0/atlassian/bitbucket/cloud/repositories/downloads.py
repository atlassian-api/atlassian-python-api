from datetime import datetime

from ..base import BitbucketCloudBase
from ..common.users import AppUser


class Download(BitbucketCloudBase):
    def __init__(self, url, data, *args, **kwargs):
        super(Download, self).__init__(url, *args, data=data, expected_type="download", **kwargs)

    @property
    def name(self):
        """The download file name"""
        return self.get_data("name")

    @property
    def size(self):
        """The download size in bytes"""
        return self.get_data("size")

    @property
    def created_on(self):
        """The download created date"""
        created_on = self.get_data("created_on")
        if created_on is None:
            return None
        return datetime.strptime(created_on, self.CONF_TIMEFORMAT)

    @property
    def user(self):
        """The user who created this download"""
        return AppUser(None, self.get_data("user"))

    @property
    def downloads(self):
        """The number of times this file was downloaded"""
        return self.get_data("downloads")

    @property
    def links(self):
        """The download links"""
        return self.get_data("links")

    def get_content(self):
        """Download file content"""
        return self.get(self.url, absolute=True)


class Downloads(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(Downloads, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        url = self.url_joiner(self.url, data["name"])
        if data["links"] and data["links"]["self"] and data["links"]["self"]["href"]:
            url = data["links"]["self"]["href"]

        return Download(
            url,
            data,
            **self._new_session_args
        )  # fmt: skip

    def each(self):
        """
        Returns the list of downloads in this repository.

        :return: A generator for the Download objects

        API docs: https://developer.atlassian.com/cloud/bitbucket/rest/api-group-downloads/#api-repositories-workspace-repo-slug-downloads-get
        """
        for issue in self._get_paged(None):
            yield self.__get_object(issue)

        return
