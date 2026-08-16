"""Requirement Yogi Cloud client for Confluence applications."""

from .cloud import YogiCloud


class YogiConfluenceCloud(YogiCloud):
    """Requirement Yogi Cloud API client scoped to Confluence applications."""


ConfluenceCloud = YogiConfluenceCloud
