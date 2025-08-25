# coding=utf-8

from .base import TempoServerBase
from .accounts import Accounts
from .teams import Teams
from .planner import Planner
from .budgets import Budgets
from .timesheets import Timesheets
from .servlet import Servlet
from .events import Events


class Server(TempoServerBase):
    """
    Tempo Server REST API wrapper
    """

    def __init__(self, url, *args, **kwargs):
        # Set default API configuration for Tempo Server, but allow overrides
        if "cloud" not in kwargs:
            kwargs["cloud"] = False
        if "api_version" not in kwargs:
            kwargs["api_version"] = "1"
        if "api_root" not in kwargs:
            kwargs["api_root"] = "rest/tempo-core/1"
        super(Server, self).__init__(url, *args, **kwargs)

        # Initialize specialized modules with reference to this instance
        self.__accounts = Accounts(self._sub_url("accounts"), parent=self, **self._new_session_args)
        self.__teams = Teams(self._sub_url("teams"), parent=self, **self._new_session_args)
        self.__planner = Planner(self._sub_url("plans"), parent=self, **self._new_session_args)
        self.__budgets = Budgets(self._sub_url("budgets"), parent=self, **self._new_session_args)
        self.__timesheets = Timesheets(self._sub_url("timesheets"), parent=self, **self._new_session_args)
        self.__servlet = Servlet(self._sub_url("worklogs"), parent=self, **self._new_session_args)
        self.__events = Events(self._sub_url("events"), parent=self, **self._new_session_args)

    @property
    def accounts(self):
        """Property to access the accounts module."""
        return self.__accounts

    @property
    def teams(self):
        """Property to access the teams module."""
        return self.__teams

    @property
    def planner(self):
        """Property to access the planner module."""
        return self.__planner

    @property
    def budgets(self):
        """Property to access the budgets module."""
        return self.__budgets

    @property
    def timesheets(self):
        """Property to access the timesheets module."""
        return self.__timesheets

    @property
    def servlet(self):
        """Property to access the servlet module."""
        return self.__servlet

    @property
    def events(self):
        """Property to access the events module."""
        return self.__events

    def get_health(self, **kwargs):
        """Get API health status."""
        return self.get("health", **kwargs)

    def get_metadata(self, **kwargs):
        """Get API metadata."""
        return self.get("metadata", **kwargs)
