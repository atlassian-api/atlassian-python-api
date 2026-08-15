"""Backward-compatible import path for the Confluence REST API v2 client."""

from .confluence.cloud.cloud import ConfluenceCloud

ConfluenceV2 = ConfluenceCloud

__all__ = ["ConfluenceV2"]
