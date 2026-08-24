from unittest.mock import patch

from atlassian.confluence_base import ConfluenceBase


def test_v2_relative_cursor_preserves_tenant_context_path():
    client = ConfluenceBase("https://example.atlassian.net", api_version=2)
    responses = [
        {
            "results": [{"id": "1"}],
            "_links": {
                "base": "https://example.atlassian.net/wiki",
                "next": "/wiki/api/v2/spaces?limit=1&cursor=CURSOR",
            },
        },
        {"results": []},
    ]
    with patch.object(client, "get", side_effect=responses) as get:
        assert list(client._get_paged("api/v2/spaces", params={"limit": 1})) == [{"id": "1"}]

    assert get.call_args_list[1].args[0] == "api/v2/spaces"
    assert get.call_args_list[1].kwargs["params"] == {"limit": "1", "cursor": "CURSOR"}


def test_v2_relative_cursor_preserves_api_gateway_prefix():
    client = ConfluenceBase("https://api.atlassian.com/ex/confluence/CLOUD-ID", api_version=2)
    responses = [
        {
            "results": [{"id": "1"}],
            "_links": {
                "base": "https://example.atlassian.net/wiki",
                "next": "/wiki/api/v2/spaces?limit=1&cursor=CURSOR",
            },
        },
        {"results": []},
    ]
    with patch.object(client, "get", side_effect=responses) as get:
        list(client._get_paged("api/v2/spaces", params={"limit": 1}))

    assert get.call_args_list[1].args[0] == "api/v2/spaces"
    assert get.call_args_list[1].kwargs["params"] == {"limit": "1", "cursor": "CURSOR"}
