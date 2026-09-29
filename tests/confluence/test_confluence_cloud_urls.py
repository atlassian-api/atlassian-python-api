# coding=utf-8
"""Regression tests for legacy Confluence Cloud URL construction.

These tests spy on the transport layer (``AtlassianRestAPI.request``) instead
of mocking ``Cloud.get`` so they verify the full URL — scheme, host, ``/wiki``
context path, and API root prefixes.  They exist because the 3.41 split of the
monolithic ``confluence.py`` silently dropped both the ``/wiki`` rewrite and
the ``rest/api`` prefixes from every legacy Cloud method.
"""

from unittest.mock import MagicMock, patch

from atlassian.confluence import Confluence
from atlassian.confluence.cloud import Cloud


def _spy():
    """Return (sent_urls, request spy) capturing fully joined URLs."""
    sent = []

    def fake_request(self, method, path="/", **kwargs):
        sent.append(self.url_joiner(None if kwargs.get("absolute") else self.url, path))
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"results": []}
        return response

    return sent, fake_request


def _cloud_client(url="https://example.atlassian.net"):
    client = Confluence(url=url, username="u", password="p")
    assert isinstance(client._impl, Cloud)
    return client._impl


class TestCloudUrlContext:
    """Tenant URLs must carry the /wiki context path exactly once."""

    def test_bare_tenant_url_gets_wiki_suffix(self):
        assert _cloud_client().url == "https://example.atlassian.net/wiki"

    def test_explicit_wiki_url_is_not_doubled(self):
        assert _cloud_client("https://example.atlassian.net/wiki").url == "https://example.atlassian.net/wiki"

    def test_gateway_url_is_not_rewritten(self):
        client = Confluence(url="https://api.atlassian.com/ex/confluence/abc123", username="u", password="p")
        assert client.url == "https://api.atlassian.com/ex/confluence/abc123"


class TestCloudEndpointPaths:
    """Legacy Cloud methods must hit versioned API roots under /wiki."""

    def test_v1_content_methods_use_rest_api(self):
        impl = _cloud_client()
        sent, spy = _spy()
        with patch("atlassian.rest_client.AtlassianRestAPI.request", autospec=True, side_effect=spy):
            impl.get_content("123")
            impl.get_page_by_title("SPACE", "Title")
            impl.get_current_user()
        assert sent[0] == "https://example.atlassian.net/wiki/rest/api/content/123"
        assert sent[1] == "https://example.atlassian.net/wiki/rest/api/content"
        assert sent[2] == "https://example.atlassian.net/wiki/rest/api/user/current"

    def test_v2_space_methods_use_api_v2(self):
        impl = _cloud_client()
        sent, spy = _spy()
        with patch("atlassian.rest_client.AtlassianRestAPI.request", autospec=True, side_effect=spy):
            impl.get_spaces()
        assert sent[0] == "https://example.atlassian.net/wiki/api/v2/spaces"

    def test_search_uses_rest_api_content_search(self):
        impl = _cloud_client()
        sent, spy = _spy()
        with patch("atlassian.rest_client.AtlassianRestAPI.request", autospec=True, side_effect=spy):
            impl.search_content("type=page")
        assert sent[0] == "https://example.atlassian.net/wiki/rest/api/content/search"
