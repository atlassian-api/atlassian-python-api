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


@patch.object(Bamboo, "delete")
@patch.object(Bamboo, "post")
@patch.object(Bamboo, "get")
def test_project_linked_repository_methods(mock_get, mock_post, mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    mock_get.side_effect = [{"searchResults": []}, [{"id": 42, "name": "Specs repository"}]]

    bamboo.search_linked_repositories("specs")
    bamboo.get_project_linked_repositories("PROJ")
    bamboo.link_repository_to_project("PROJ", 42)
    bamboo.unlink_repository_from_project("PROJ", 42)

    assert mock_get.call_args_list[0].args[0] == "rest/api/latest/repository"
    assert mock_get.call_args_list[0].kwargs["params"] == {"searchTerm": "specs"}
    assert mock_get.call_args_list[1].args[0] == "rest/api/latest/project/PROJ/repository"
    mock_post.assert_called_once_with("rest/api/latest/project/PROJ/repository", data={"id": 42})
    mock_delete.assert_called_once_with("rest/api/latest/project/PROJ/repository/42")


def test_ordered_plan_results_and_convenience_filters(monkeypatch):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    calls = []
    results = [
        {"buildCompletedTime": "2024-01-02T00:00:00.000Z", "state": "Failed"},
        {"buildCompletedTime": "2024-01-03T00:00:00.000Z", "state": "Successful"},
        {"buildCompletedTime": "2024-01-01T00:00:00.000Z", "state": "Failed"},
    ]

    def plan_results(project_key, plan_key, **kwargs):
        calls.append((project_key, plan_key, kwargs))
        return (result for result in results)

    monkeypatch.setattr(bamboo, "plan_results", plan_results)

    assert [result["buildCompletedTime"] for result in bamboo.ordered_plan_results("PROJ", "PLAN")] == [
        "2024-01-03T00:00:00.000Z",
        "2024-01-02T00:00:00.000Z",
        "2024-01-01T00:00:00.000Z",
    ]
    assert bamboo.latest_successful_plan_result("PROJ", "PLAN")["state"] == "Successful"
    assert bamboo.oldest_failed_plan_result("PROJ", "PLAN")["buildCompletedTime"] == "2024-01-01T00:00:00.000Z"
    assert calls[1][2]["build_state"] == "Successful"
    assert calls[2][2]["build_state"] == "Failed"


@patch.object(Bamboo, "get")
def test_plan_results_forwards_supported_build_state_filter(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    mock_get.return_value = {"results": {"size": 0, "result": []}}

    assert list(bamboo.plan_results("PROJ", "PLAN", build_state="Successful")) == []

    assert mock_get.call_args.args[3]["buildstate"] == "Successful"
