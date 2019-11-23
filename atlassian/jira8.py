# coding=utf-8
import logging

from .jira import Jira

log = logging.getLogger(__name__)


class Jira8(Jira):
    # methods migrated into main module
