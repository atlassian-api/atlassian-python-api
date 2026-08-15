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
