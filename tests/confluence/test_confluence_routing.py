# coding=utf-8
"""Tests for legacy Confluence class URL routing."""

from unittest.mock import patch, MagicMock

import pytest

from atlassian.confluence import Confluence, ConfluenceCloud, ConfluenceServer


class TestConfluenceRouting:
    """Test URL routing in legacy Confluence wrapper."""

    @patch.object(ConfluenceCloud, "__init__", return_value=None)
    @patch.object(ConfluenceServer, "__init__", return_value=None)
    def test_atlassian_net_routes_to_cloud(self, mock_server, mock_cloud):
        """Standard atlassian.net URL routes to Cloud."""
        Confluence("https://mysite.atlassian.net")
        mock_cloud.assert_called_once()
        mock_server.assert_not_called()

    @patch.object(ConfluenceCloud, "__init__", return_value=None)
    @patch.object(ConfluenceServer, "__init__", return_value=None)
    def test_atlassian_net_wiki_routes_to_cloud(self, mock_server, mock_cloud):
        """atlassian.net/wiki URL should still route to Cloud."""
        Confluence("https://mysite.atlassian.net/wiki")
        mock_cloud.assert_called_once()
        mock_server.assert_not_called()

    @patch.object(ConfluenceCloud, "__init__", return_value=None)
    @patch.object(ConfluenceServer, "__init__", return_value=None)
    def test_jira_com_routes_to_cloud(self, mock_server, mock_cloud):
        """jira.com URL routes to Cloud."""
        Confluence("https://mysite.jira.com")
        mock_cloud.assert_called_once()
        mock_server.assert_not_called()

    @patch.object(ConfluenceCloud, "__init__", return_value=None)
    @patch.object(ConfluenceServer, "__init__", return_value=None)
    def test_api_gateway_routes_to_cloud(self, mock_server, mock_cloud):
        """OAuth2 API gateway URL routes to Cloud."""
        Confluence("https://api.atlassian.com/ex/confluence/abc123")
        mock_cloud.assert_called_once()
        mock_server.assert_not_called()

    @patch.object(ConfluenceCloud, "__init__", return_value=None)
    @patch.object(ConfluenceServer, "__init__", return_value=None)
    def test_self_hosted_routes_to_server(self, mock_server, mock_cloud):
        """Self-hosted URL routes to Server."""
        Confluence("https://confluence.mycompany.com")
        mock_server.assert_called_once()
        mock_cloud.assert_not_called()

    @patch.object(ConfluenceCloud, "__init__", return_value=None)
    @patch.object(ConfluenceServer, "__init__", return_value=None)
    def test_explicit_cloud_true_overrides_url(self, mock_server, mock_cloud):
        """cloud=True forces Cloud routing regardless of URL."""
        Confluence("https://confluence.mycompany.com", cloud=True)
        mock_cloud.assert_called_once()
        mock_server.assert_not_called()

    @patch.object(ConfluenceCloud, "__init__", return_value=None)
    @patch.object(ConfluenceServer, "__init__", return_value=None)
    def test_explicit_cloud_false_overrides_url(self, mock_server, mock_cloud):
        """cloud=False forces Server routing regardless of URL."""
        Confluence("https://mysite.atlassian.net", cloud=False)
        mock_server.assert_called_once()
        mock_cloud.assert_not_called()
