# coding=utf-8
import logging

from .jira import Jira

log = logging.getLogger(__name__)


class Jira8(Jira):
    # methods migrated into main module
    @staticmethod
    def print_module_name():
        print(__name__)
