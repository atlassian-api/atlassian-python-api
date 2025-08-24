# coding=utf-8

from .base import BitbucketCloudBase
from .repositories import Repositories
from .workspaces import Workspaces


class Cloud(BitbucketCloudBase):
    """
    Bitbucket Cloud REST API wrapper
    """

    def __init__(self, url="https://api.bitbucket.org/", *args, **kwargs):
        kwargs["cloud"] = True
        kwargs["api_root"] = None
        kwargs["api_version"] = "2.0"
        url = url.strip("/") + f"/{kwargs['api_version']}"
        super(Cloud, self).__init__(url, *args, **kwargs)
        self.__workspaces = Workspaces(f"{self.url}/workspaces", **self._new_session_args)
        self.__repositories = Repositories(f"{self.url}/repositories", **self._new_session_args)

    @property
    def workspaces(self):
        return self.__workspaces

    @property
    def repositories(self):
        return self.__repositories
