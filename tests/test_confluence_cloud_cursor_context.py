from unittest.mock import patch

from atlassian import ConfluenceV2


def test_cloud_v2_cursor_preserves_wiki_context():
    client = ConfluenceV2("https://example.atlassian.net")
    responses = [
        {
            "results": [{"id": "1"}],
            "_links": {"next": "/wiki/api/v2/spaces?limit=1&cursor=CURSOR"},
        },
        {"results": []},
    ]
    with patch.object(client, "get", side_effect=responses) as get:
        assert list(client._get_paged("api/v2/spaces", params={"limit": 1})) == [{"id": "1"}]

    assert get.call_args_list[1].args[0] == "api/v2/spaces"
    assert get.call_args_list[1].kwargs["params"] == {"limit": "1", "cursor": "CURSOR"}


def test_cloud_v2_cursor_preserves_gateway_context():
    client = ConfluenceV2("https://api.atlassian.com/ex/confluence/CLOUD-ID")
    responses = [
        {
            "results": [{"id": "1"}],
            "_links": {"next": "/wiki/api/v2/spaces?limit=1&cursor=CURSOR"},
        },
        {"results": []},
    ]
    with patch.object(client, "get", side_effect=responses) as get:
        list(client._get_paged("api/v2/spaces", params={"limit": 1}))

    assert get.call_args_list[1].args[0] == "api/v2/spaces"
    assert get.call_args_list[1].kwargs["params"] == {"limit": "1", "cursor": "CURSOR"}
