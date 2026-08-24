from unittest.mock import patch

from atlassian.confluence.cloud.cloud import ConfluenceCloud


def test_admin_key_and_space_role_operations_use_v2_routes():
    client = ConfluenceCloud("https://example.atlassian.net")
    with patch.object(client, "get", return_value={}) as get:
        client.get_admin_key()
        client.get_space_roles(space_id="S1", limit=10)
    assert get.call_args_list[0].args == ("api/v2/admin-key",)
    assert get.call_args_list[1].args == ("api/v2/space-roles",)
    assert get.call_args_list[1].kwargs["params"] == {"space-id": "S1", "limit": 10}


def test_global_comment_and_data_policy_operations():
    client = ConfluenceCloud("https://example.atlassian.net")
    with patch.object(client, "post", return_value={}) as post:
        client.create_global_footer_comment({"body": {}})
        client.bulk_get_users({"accountIds": ["A1"]})
    assert post.call_args_list[0].args == ("api/v2/footer-comments",)
    assert post.call_args_list[1].args == ("api/v2/users-bulk",)

    with patch.object(client, "get", return_value={}) as get:
        client.get_data_policy_spaces(ids=["S1"], limit=10)
    get.assert_called_once_with("api/v2/data-policies/spaces", params={"ids": ["S1"], "limit": 10})
