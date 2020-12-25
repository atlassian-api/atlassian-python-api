# coding=utf-8

from .base import BitbucketCloudBase
from .workspaces import Workspaces
from .repositories import Repositories
from .const import CONF_TIMEFORMAT
from datetime import datetime


class Cloud(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        kwargs["cloud"] = True
        kwargs["api_root"] = None
        kwargs["api_version"] = "2.0"
        kwargs["timeformat_func"] = kwargs.pop("timeformat_func", lambda ts: datetime.strptime(ts, CONF_TIMEFORMAT))
        url = url.strip("/") + "/{}".format(kwargs["api_version"])
        super(Cloud, self).__init__(url, *args, **kwargs)
        self.__workspaces = Workspaces("{}/workspaces".format(self.url), **self._new_session_args)
        self.__repositories = Repositories("{}/repositories".format(self.url), **self._new_session_args)

    @property
    def workspaces(self):
        return self.__workspaces

    @property
    def repositories(self):
        return self.__repositories
