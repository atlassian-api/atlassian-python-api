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


@patch.object(Bamboo, "get")
def test_get_plan_specs_exports_yaml_for_repository_audits(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    mock_get.return_value = {"spec": {"code": "repositories:\n- service-repository:\n"}}

    result = bamboo.get_plan_specs("PROJ-PLAN")

    assert result == {"spec": {"code": "repositories:\n- service-repository:\n"}}
    mock_get.assert_called_once_with(
        "rest/api/latest/plan/PROJ-PLAN/specs",
        params={"format": "YAML"},
    )


@patch.object(Bamboo, "get")
def test_get_plan_specs_supports_java_package_exports(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    bamboo.get_plan_specs("PROJ-PLAN", package="com.example.bamboo", format="JAVA")

    mock_get.assert_called_once_with(
        "rest/api/latest/plan/PROJ-PLAN/specs",
        params={"format": "JAVA", "package": "com.example.bamboo"},
    )


@patch.object(Bamboo, "post")
def test_queue_build_passes_custom_variables_without_mutating_params(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    params = {"bamboo.variable.release": "1.2.3"}

    bamboo.queue_build("PROJ-PLAN", params)

    assert params == {"bamboo.variable.release": "1.2.3"}
    mock_post.assert_called_once_with(
        "rest/api/latest/queue/PROJ-PLAN",
        params={"bamboo.variable.release": "1.2.3", "executeAllStages": "true"},
    )


@patch.object(Bamboo, "post")
def test_queue_build_preserves_explicit_queue_parameters(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    bamboo.queue_build("PROJ-PLAN", {"stage": "Deploy", "executeAllStages": "false"})

    mock_post.assert_called_once_with(
        "rest/api/latest/queue/PROJ-PLAN",
        params={"stage": "Deploy", "executeAllStages": "false"},
    )


@patch.object(Bamboo, "get")
def test_plan_results_supports_multiple_labels(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    mock_get.return_value = {"results": {"size": 0, "result": []}}

    assert list(bamboo.plan_results("PROJ", "PLAN", label=["release", "production"])) == []

    assert mock_get.call_args.args[3]["label"] == ["release", "production"]
