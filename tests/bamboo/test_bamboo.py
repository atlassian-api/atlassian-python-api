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


@patch.object(Bamboo, "get")
def test_broken_build_responsibility_methods(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    bamboo.get_broken_builds_by_user("ada")
    assert mock_get.call_args.args[0] == "rest/responsibility/latest/brokenBuild/byUser/ada"

    bamboo.get_my_broken_builds()
    assert mock_get.call_args.args[0] == "rest/responsibility/latest/brokenBuild/myBrokenBuilds"

    bamboo.get_broken_build("PROJ-PLAN-42")
    assert mock_get.call_args.args[0] == "rest/responsibility/latest/brokenBuild/PROJ-PLAN-42"


@patch.object(Bamboo, "post")
@patch.object(Bamboo, "delete")
def test_take_and_remove_responsibility(mock_delete, mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    bamboo.take_responsibility("PROJ-PLAN-42", "ada")
    assert mock_post.call_args.args[0] == "rest/responsibility/latest/brokenBuild/PROJ-PLAN-42/ada"

    bamboo.remove_responsibility("PROJ-PLAN-42", "ada")
    assert mock_delete.call_args.args[0] == "rest/responsibility/latest/brokenBuild/PROJ-PLAN-42/ada"


@patch.object(Bamboo, "post")
def test_remote_trigger_change_detection(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.remote_trigger_change_detection()
    assert mock_post.call_args.args[0] == "rest/triggers/latest/remote/changeDetection"


@patch.object(Bamboo, "delete")
@patch.object(Bamboo, "post")
@patch.object(Bamboo, "get")
def test_access_token_methods(mock_get, mock_post, mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    bamboo.get_access_tokens()
    assert mock_get.call_args.args[0] == "rest/api/latest/access-token"

    bamboo.create_access_token()
    assert mock_post.call_args.args[0] == "rest/api/latest/access-token"

    bamboo.delete_access_token("token-123")
    assert mock_delete.call_args.args[0] == "rest/api/latest/access-token/token-123"


@patch.object(Bamboo, "post")
@patch.object(Bamboo, "put")
@patch.object(Bamboo, "get")
@patch.object(Bamboo, "delete")
def test_deployment_management_methods(mock_delete, mock_get, mock_put, mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    bamboo.create_deployment_project({"name": "Deploy PROJ"})
    assert mock_post.call_args.args[0] == "rest/api/latest/deploy/project"
    assert mock_post.call_args.kwargs["data"] == {"name": "Deploy PROJ"}

    bamboo.update_deployment_project("100", {"name": "New name"})
    assert mock_put.call_args.args[0] == "rest/api/latest/deploy/project/100"

    bamboo.create_deployment_environment("100", {"name": "Staging"})
    assert mock_post.call_args.args[0] == "rest/api/latest/deploy/project/100/environment"

    bamboo.get_deployment_environment("200")
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/environment/200"

    bamboo.update_deployment_environment("200", {"name": "Production"})
    assert mock_put.call_args.args[0] == "rest/api/latest/deploy/environment/200"

    bamboo.delete_deployment_environment("200")
    assert mock_delete.call_args.args[0] == "rest/api/latest/deploy/environment/200"

    bamboo.create_deployment_version("100", {"name": "1.2.3"})
    assert mock_post.call_args.args[0] == "rest/api/latest/deploy/project/100/version"

    bamboo.get_deployment_version("300")
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/version/300"

    bamboo.delete_deployment_version("300")
    assert mock_delete.call_args.args[0] == "rest/api/latest/deploy/version/300"


@patch.object(Bamboo, "get")
def test_deployment_dashboard_methods(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    bamboo.get_deployment_dashboard_paginate()
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/dashboard/paginate"

    bamboo.get_deployment_dashboard_paginate("50")
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/dashboard/paginate/50"


@patch.object(Bamboo, "post")
def test_deployment_dashboard_status(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_deployment_dashboard_status({"environmentIds": [1]})
    assert mock_post.call_args.args[0] == "rest/api/latest/deploy/dashboard/status"


@patch.object(Bamboo, "put")
@patch.object(Bamboo, "get")
def test_admin_artifact_handler_methods(mock_get, mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    bamboo.get_artifact_handler_config("s3")
    assert mock_get.call_args.args[0] == "rest/admin/latest/artifactHandlers/s3"

    bamboo.update_artifact_handler_config("s3", {"bucket": "bamboo-artifacts"})
    assert mock_put.call_args.args[0] == "rest/admin/latest/artifactHandlers/s3"
    assert mock_put.call_args.kwargs["data"] == {"bucket": "bamboo-artifacts"}


@patch.object(Bamboo, "put")
@patch.object(Bamboo, "get")
def test_admin_config_methods(mock_get, mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    bamboo.get_agent_config()
    assert mock_get.call_args.args[0] == "rest/admin/latest/config/agents"

    bamboo.get_offline_agent_removal_config()
    assert mock_get.call_args.args[0] == "rest/admin/latest/config/agents/offlineAgentRemoval"

    bamboo.update_offline_agent_removal_config({"enabled": True})
    assert mock_put.call_args.args[0] == "rest/admin/latest/config/agents/offlineAgentRemoval"

    bamboo.get_general_config()
    assert mock_get.call_args.args[0] == "rest/admin/latest/config/general"

    bamboo.update_general_config({"baseUrl": "https://bamboo.example.test"})
    assert mock_put.call_args.args[0] == "rest/admin/latest/config/general"

    bamboo.get_mail_server_config()
    assert mock_get.call_args.args[0] == "rest/admin/latest/config/mailServer"

    bamboo.update_mail_server_config({"host": "smtp.example.test"})
    assert mock_put.call_args.args[0] == "rest/admin/latest/config/mailServer"


@patch.object(Bamboo, "delete")
@patch.object(Bamboo, "put")
@patch.object(Bamboo, "get")
@patch.object(Bamboo, "post")
def test_admin_security_and_global_variables_methods(mock_post, mock_get, mock_put, mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    bamboo.get_global_variables()
    assert mock_get.call_args.args[0] == "rest/admin/latest/globalVariables"

    bamboo.create_global_variable({"key": "KEY", "value": "value"})
    assert mock_post.call_args.args[0] == "rest/admin/latest/globalVariables"

    bamboo.get_global_variable("1")
    assert mock_get.call_args.args[0] == "rest/admin/latest/globalVariables/1"

    bamboo.update_global_variable("1", {"value": "new"})
    assert mock_put.call_args.args[0] == "rest/admin/latest/globalVariables/1"

    bamboo.delete_global_variable("1")
    assert mock_delete.call_args.args[0] == "rest/admin/latest/globalVariables/1"

    bamboo.get_security_settings()
    assert mock_get.call_args.args[0] == "rest/admin/latest/security/settings"

    bamboo.update_security_settings({"captcha": True})
    assert mock_put.call_args.args[0] == "rest/admin/latest/security/settings"

    bamboo.get_trusted_keys()
    assert mock_get.call_args.args[0] == "rest/admin/latest/security/trustedKey"

    bamboo.add_trusted_key({"key": "abc"})
    assert mock_post.call_args.args[0] == "rest/admin/latest/security/trustedKey"

    bamboo.delete_trusted_key("5")
    assert mock_delete.call_args.args[0] == "rest/admin/latest/security/trustedKey/5"


@patch.object(Bamboo, "get")
def test_permission_available_and_role_methods(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    bamboo.get_available_users_for_permission("deployment", "10")
    assert mock_get.call_args.args[0] == "rest/api/latest/permissions/deployment/10/available-users"

    bamboo.get_available_groups_for_permission("environment", "20")
    assert mock_get.call_args.args[0] == "rest/api/latest/permissions/environment/20/available-groups"

    bamboo.get_roles_for_permission("project", "30")
    assert mock_get.call_args.args[0] == "rest/api/latest/permissions/project/30/roles"


@patch.object(Bamboo, "delete")
@patch.object(Bamboo, "put")
def test_permission_grant_and_revoke_methods(mock_put, mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    bamboo.grant_user_permission("plan", "40", "ada", ["READ", "BUILD"])
    assert mock_put.call_args.args[0] == "rest/api/latest/permissions/plan/40/users/ada"
    assert mock_put.call_args.kwargs["data"] == ["READ", "BUILD"]

    bamboo.revoke_user_permission("plan", "40", "ada", ["READ"])
    assert mock_delete.call_args.args[0] == "rest/api/latest/permissions/plan/40/users/ada"

    bamboo.grant_group_permission("repository", "50", "bamboo-admins", ["ADMIN"])
    assert mock_put.call_args.args[0] == "rest/api/latest/permissions/repository/50/groups/bamboo-admins"

    bamboo.revoke_group_permission("repository", "50", "bamboo-admins", ["ADMIN"])
    assert mock_delete.call_args.args[0] == "rest/api/latest/permissions/repository/50/groups/bamboo-admins"


@patch.object(Bamboo, "get")
def test_admin_user_methods(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    bamboo.get_users()
    assert mock_get.call_args.args[0] == "rest/api/latest/admin/users"

    bamboo.get_user_access_tokens("ada")
    assert mock_get.call_args.args[0] == "rest/api/latest/admin/users/ada/access-token"

    bamboo.get_user_alias("ada")
    assert mock_get.call_args.args[0] == "rest/api/latest/admin/users/ada/alias"


@patch.object(Bamboo, "delete")
@patch.object(Bamboo, "post")
@patch.object(Bamboo, "put")
def test_admin_user_modify_methods(mock_put, mock_post, mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    bamboo.create_user({"name": "ada"})
    assert mock_post.call_args.args[0] == "rest/api/latest/admin/users"

    bamboo.delete_user("ada")
    assert mock_delete.call_args.args[0] == "rest/api/latest/admin/users/ada"

    bamboo.update_user_credentials({"name": "ada", "password": "new"})
    assert mock_put.call_args.args[0] == "rest/api/latest/admin/users/credentials"

    bamboo.rename_user({"oldName": "ada", "newName": "ada2"})
    assert mock_put.call_args.args[0] == "rest/api/latest/admin/users/rename"

    bamboo.set_user_alias("ada", {"alias": "alias-ada"})
    assert mock_post.call_args.args[0] == "rest/api/latest/admin/users/ada/alias"

    bamboo.delete_user_alias("ada")
    assert mock_delete.call_args.args[0] == "rest/api/latest/admin/users/ada/alias"

    bamboo.delete_user_access_token("ada", "token-1")
    assert mock_delete.call_args.args[0] == "rest/api/latest/admin/users/ada/access-token/token-1"


@patch.object(Bamboo, "post")
@patch.object(Bamboo, "put")
@patch.object(Bamboo, "get")
def test_server_and_queue_methods(mock_get, mock_put, mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    bamboo.get_server()
    assert mock_get.call_args.args[0] == "rest/api/latest/server"

    bamboo.get_server_nodes()
    assert mock_get.call_args.args[0] == "rest/api/latest/server/nodes"

    bamboo.pause_server()
    assert mock_post.call_args.args[0] == "rest/api/latest/server/pause"

    bamboo.resume_server()
    assert mock_post.call_args.args[0] == "rest/api/latest/server/resume"

    bamboo.prepare_for_restart()
    assert mock_put.call_args.args[0] == "rest/api/latest/server/prepareForRestart"

    bamboo.get_current_user()
    assert mock_get.call_args.args[0] == "rest/api/latest/currentUser"


@patch.object(Bamboo, "delete")
@patch.object(Bamboo, "put")
def test_queue_management_methods(mock_put, mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    bamboo.remove_build_from_queue("PROJ", "PLAN", 42)
    assert mock_delete.call_args.args[0] == "rest/api/latest/queue/PROJ-PLAN-42"

    bamboo.pause_build_in_queue("PROJ", "PLAN", 42)
    assert mock_put.call_args.args[0] == "rest/api/latest/queue/PROJ-PLAN-42"

    bamboo.remove_deployment_from_queue("deploy-1")
    assert mock_delete.call_args.args[0] == "rest/api/latest/queue/deployment/deploy-1"


@patch.object(Bamboo, "delete")
@patch.object(Bamboo, "put")
@patch.object(Bamboo, "post")
@patch.object(Bamboo, "get")
def test_quick_filter_methods(mock_get, mock_post, mock_put, mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")

    bamboo.get_quick_filters()
    assert mock_get.call_args.args[0] == "rest/api/latest/quickFilter"

    bamboo.create_quick_filter({"name": "My filter"})
    assert mock_post.call_args.args[0] == "rest/api/latest/quickFilter"

    bamboo.get_active_quick_filters()
    assert mock_get.call_args.args[0] == "rest/api/latest/quickFilter/active"

    bamboo.get_visible_quick_filters()
    assert mock_get.call_args.args[0] == "rest/api/latest/quickFilter/visible"

    bamboo.set_visible_quick_filters([1, 2])
    assert mock_put.call_args.args[0] == "rest/api/latest/quickFilter/visible"

    bamboo.deactivate_quick_filters([1, 2])
    assert mock_put.call_args.args[0] == "rest/api/latest/quickFilter/deactivate"

    bamboo.get_quick_filter("1")
    assert mock_get.call_args.args[0] == "rest/api/latest/quickFilter/1"

    bamboo.update_quick_filter("1", {"name": "Updated"})
    assert mock_put.call_args.args[0] == "rest/api/latest/quickFilter/1"

    bamboo.delete_quick_filter("1")
    assert mock_delete.call_args.args[0] == "rest/api/latest/quickFilter/1"

    bamboo.activate_quick_filter("1")
    assert mock_put.call_args.args[0] == "rest/api/latest/quickFilter/1/activate"


@patch.object(Bamboo, "get")
def test_get_users_from_group_keeps_paging_params_with_filter(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_users_from_group("bamboo-users", filter_users="ada", start=10, limit=5)
    assert mock_get.call_args.kwargs["params"] == {"limit": 5, "start": 10, "filter": "ada"}


@patch.object(Bamboo, "get")
def test_get_users_not_in_group_keeps_paging_params_with_filter(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_users_not_in_group("bamboo-users", filter_users="ada", start=10, limit=5)
    assert mock_get.call_args.kwargs["params"] == {"limit": 5, "start": 10, "filter": "ada"}
