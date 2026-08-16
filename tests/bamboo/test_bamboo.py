from unittest.mock import patch

from atlassian.bamboo import Bamboo


@patch.object(Bamboo, "get")
def test_activity_uses_rest_agent_status_and_returns_active_agents(mock_get):
    mock_get.return_value = [
        {"id": 1, "online": True, "active": True, "busy": True},
        {"id": 2, "online": True, "active": True, "busy": False},
        {"id": 3, "online": False, "active": False, "busy": False},
    ]
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    result = bamboo.activity()

    mock_get.assert_called_once_with("rest/api/latest/agent", params={"online": True})
    assert result == [
        {"id": 1, "online": True, "active": True, "busy": True},
        {"id": 2, "online": True, "active": True, "busy": False},
    ]


@patch.object(Bamboo, "get")
def test_activity_can_filter_idle_agents(mock_get):
    mock_get.return_value = [
        {"id": 1, "online": True, "active": True, "busy": True},
        {"id": 2, "online": True, "active": True, "busy": False},
    ]
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    assert bamboo.activity(busy=False) == [{"id": 2, "online": True, "active": True, "busy": False}]


@patch.object(Bamboo, "post")
@patch.object(Bamboo, "get")
def test_agent_capability_and_plan_variable_methods(mock_get, mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    mock_get.return_value = {"variables": []}

    assert bamboo.get_plan_variables("PROJ-PLAN") == {"variables": []}
    bamboo.add_agent_capability("12", {"type": "system", "key": "jdk", "value": "17"})
    bamboo.create_plan_variable("PROJ-PLAN", {"name": "release", "value": "1.0"})

    assert mock_get.call_args.args[0].endswith("plan/PROJ-PLAN/variable")
    assert mock_post.call_args_list[0].args[0].endswith("agent/12/capability")
    assert mock_post.call_args_list[1].args[0].endswith("plan/PROJ-PLAN/variable")
