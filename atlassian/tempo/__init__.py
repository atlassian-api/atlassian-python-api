# coding=utf-8
"""
Tempo API client package for Atlassian Python API.

This package provides both Cloud and Server implementations of the Tempo API.
"""

from .cloud import Cloud as TempoCloud
from .server import Server as TempoServer

__all__ = [
    "TempoCloud",
    "TempoServer",
]
