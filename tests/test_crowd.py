from unittest.mock import patch

from atlassian.crowd import Crowd


@patch.object(Crowd, "delete")
@patch.object(Crowd, "get")
@patch.object(Crowd, "put")
def test_crowd_user_group_and_attribute_helpers(mock_put, mock_get, mock_delete):
    crowd = Crowd("https://crowd.example.test", "application", "password")
    mock_get.return_value = {"users": [{"name": "ada"}]}

    assert crowd.nested_group_members("engineering") == ["ada"]
    crowd.group_remove_user("ada", "engineering")
    crowd.user_update_password("ada", "new-secret")
    crowd.group_store_attributes("engineering", {"attributes": []})

    assert mock_delete.call_args_list[0].kwargs["params"] == {"username": "ada", "groupname": "engineering"}
    assert mock_put.call_args_list[0].kwargs["data"] == {"value": "new-secret"}
    assert mock_put.call_args_list[1].kwargs["params"] == {"groupname": "engineering"}
