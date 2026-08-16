"""Requirement Yogi Cloud client for Jira applications."""

from .cloud import YogiCloud


class YogiJiraCloud(YogiCloud):
    """Requirement Yogi Cloud API client scoped to Jira applications."""


JiraCloud = YogiJiraCloud
