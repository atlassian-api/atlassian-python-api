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

    assert mock_get.call_args.args[0] == "rest/api/latest/plan/PROJ-PLAN/variables"
    assert mock_post.call_args_list[0].args[0] == "rest/api/latest/agent/12/capability"
    assert mock_post.call_args_list[1].args[0] == "rest/api/latest/plan/PROJ-PLAN/variables"


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
    assert mock_put.call_args.args[0] == "rest/api/latest/deploy/project"
    assert mock_put.call_args.kwargs["data"] == {"name": "Deploy PROJ"}

    bamboo.update_deployment_project("100", {"name": "New name"})
    assert mock_post.call_args.args[0] == "rest/api/latest/deploy/project/100"

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


@patch.object(Bamboo, "get")
def test_ordered_plan_results_accepts_extra_query_params(mock_get):
    """Regression: ordered_plan_results(**kwargs) used to hit plan_results' fixed signature -> TypeError."""
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    mock_get.return_value = {"results": {"size": 0, "result": []}}

    assert list(bamboo.ordered_plan_results("PROJ", "PLAN", issueKey="BUG-1")) == []

    call = mock_get.call_args
    assert call.args[0].endswith("result/PROJ-PLAN")
    params = call.args[3]
    assert params["issueKey"] == "BUG-1"
    assert params["max-results"] == 25


@patch.object(Bamboo, "get")
def test_plan_results_forwards_extra_kwargs_as_query_params(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    mock_get.return_value = {"results": {"size": 0, "result": []}}

    assert list(bamboo.plan_results("PROJ", "PLAN", build_state="Successful", issueStatus="all")) == []

    params = mock_get.call_args.args[3]
    assert params["buildstate"] == "Successful"
    assert params["issueStatus"] == "all"





# ----------------------------------------------------------------------------
# Spec-coverage tests: one per spec operation (var/specs/server/bamboo/bamboo-swagger.v3.txt)
# ----------------------------------------------------------------------------

@patch.object(Bamboo, "delete")
def test_spec_op_invalidate_user_sessions(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.invalidate_user_sessions('alpha', 'alpha')
    assert mock_delete.call_args.args[0] == "rest/admin/latest/session/alpha"

@patch.object(Bamboo, "get")
def test_spec_op_get_configuration(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_configuration()
    assert mock_get.call_args.args[0] == "rest/admin/latest/ephemeral/config"

@patch.object(Bamboo, "get")
def test_spec_op_get_configuration_1(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_configuration_1()
    assert mock_get.call_args.args[0] == "rest/admin/latest/expiry/configuration"

@patch.object(Bamboo, "get")
def test_spec_op_get_status(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_status()
    assert mock_get.call_args.args[0] == "rest/admin/latest/expiry/status"

@patch.object(Bamboo, "get")
def test_spec_op_get_jobs(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_jobs()
    assert mock_get.call_args.args[0] == "rest/admin/latest/scheduler/jobs"

@patch.object(Bamboo, "get")
def test_spec_op_get_system_info(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_system_info()
    assert mock_get.call_args.args[0] == "rest/admin/latest/systemInfo"

@patch.object(Bamboo, "post")
def test_spec_op_test_connection(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.test_connection({"k": "v"})
    assert mock_post.call_args.args[0] == "rest/admin/latest/ephemeral/config/test-connection"
    assert mock_post.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "post")
def test_spec_op_trigger_job(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.trigger_job({"k": "v"})
    assert mock_post.call_args.args[0] == "rest/admin/latest/scheduler/jobs/trigger"
    assert mock_post.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "post")
def test_spec_op_rename_user_post(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.rename_user_post({"k": "v"}, "beta")
    assert mock_post.call_args.args[0] == "rest/admin/latest/user"
    assert mock_post.call_args.kwargs.get("params") == {"externalRename": "beta"}
    assert mock_post.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_save_configuration(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.save_configuration({"k": "v"})
    assert mock_put.call_args.args[0] == "rest/admin/latest/ephemeral/config"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_set_configuration(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.set_configuration({"k": "v"})
    assert mock_put.call_args.args[0] == "rest/admin/latest/expiry/configuration"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_run(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.run()
    assert mock_put.call_args.args[0] == "rest/admin/latest/expiry/run"

@patch.object(Bamboo, "put")
def test_spec_op_rename_user_put(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.rename_user_put('alpha', {"k": "v"}, "beta")
    assert mock_put.call_args.args[0] == "rest/admin/latest/user/alpha"
    assert mock_put.call_args.kwargs.get("params") == {"externalRename": "beta"}
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "delete")
def test_spec_op_remove_plan_custom_expiry_settings(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.remove_plan_custom_expiry_settings('alpha')
    assert mock_delete.call_args.args[0] == "rest/api/latest/admin/expiry/custom/plan/alpha"

@patch.object(Bamboo, "delete")
def test_spec_op_unassign_groups(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.unassign_groups('alpha', {"k": "v"})
    assert mock_delete.call_args.args[0] == "rest/api/latest/admin/users/alpha/groups"
    assert mock_delete.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "get")
def test_spec_op_find_assigned_groups(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.find_assigned_groups('alpha', "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/admin/users/alpha/assigned-groups"
    assert mock_get.call_args.kwargs.get("params") == {"filter": "beta", "limit": "beta", "start": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_find_unassigned_user_repository_aliases(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.find_unassigned_user_repository_aliases('alpha', "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/admin/users/alpha/unassigned-aliases"
    assert mock_get.call_args.kwargs.get("params") == {"filter": "beta", "limit": "beta", "start": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_find_unassigned_groups(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.find_unassigned_groups('alpha', "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/admin/users/alpha/unassigned-groups"
    assert mock_get.call_args.kwargs.get("params") == {"filter": "beta", "limit": "beta", "start": "beta"}

@patch.object(Bamboo, "post")
def test_spec_op_assign_groups(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.assign_groups('alpha', {"k": "v"})
    assert mock_post.call_args.args[0] == "rest/api/latest/admin/users/alpha/groups"
    assert mock_post.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "delete")
def test_spec_op_delete_agent(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.delete_agent('7')
    assert mock_delete.call_args.args[0] == "rest/api/latest/agent/7"

@patch.object(Bamboo, "delete")
def test_spec_op_remove_assignment(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.remove_assignment("beta", "beta", "beta", "beta")
    assert mock_delete.call_args.args[0] == "rest/api/latest/agent/assignment"
    assert mock_delete.call_args.kwargs.get("params") == {"executorType": "beta", "executorId": "beta", "entityId": "beta", "assignmentType": "beta"}

@patch.object(Bamboo, "delete")
def test_spec_op_remove_agent_assignment_from_job(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.remove_agent_assignment_from_job('alpha', 'alpha')
    assert mock_delete.call_args.args[0] == "rest/api/latest/config/job/alpha/agent-assignment/alpha"

@patch.object(Bamboo, "get")
def test_spec_op_search_entity_for_agent(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.search_entity_for_agent("beta", "beta", "beta", "beta", "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/agent/assignment/search"
    assert mock_get.call_args.kwargs.get("params") == {"max-result": "beta", "executorType": "beta", "searchTerm": "beta", "executorId": "beta", "entityType": "beta", "start-index": "beta", "assignmentType": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_find_assigned_agents_by_job(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.find_assigned_agents_by_job('alpha')
    assert mock_get.call_args.args[0] == "rest/api/latest/config/job/alpha/agent-assignment"

@patch.object(Bamboo, "get")
def test_spec_op_find_possible_agents_for_job(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.find_possible_agents_for_job('alpha', "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/config/job/alpha/agent-assignment/possible-agent-assignment"
    assert mock_get.call_args.kwargs.get("params") == {"max-result": "beta", "searchTerm": "beta", "start-index": "beta"}

@patch.object(Bamboo, "post")
def test_spec_op_add_agent_assignment(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.add_agent_assignment("beta", "beta", "beta", "beta")
    assert mock_post.call_args.args[0] == "rest/api/latest/agent/assignment"
    assert mock_post.call_args.kwargs.get("params") == {"executorType": "beta", "executorId": "beta", "entityId": "beta", "assignmentType": "beta"}

@patch.object(Bamboo, "post")
def test_spec_op_add_agent_assignment_for_job(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.add_agent_assignment_for_job('alpha', {"k": "v"})
    assert mock_post.call_args.args[0] == "rest/api/latest/config/job/alpha/agent-assignment"
    assert mock_post.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_update_agent_capability(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.update_agent_capability('7', 'alpha', {"k": "v"})
    assert mock_put.call_args.args[0] == "rest/api/latest/agent/7/capability/alpha"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "delete")
def test_spec_op_delete_avatar(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.delete_avatar()
    assert mock_delete.call_args.args[0] == "rest/api/latest/avatar/user/avatar.png"

@patch.object(Bamboo, "get")
def test_spec_op_retrieve_avatar(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.retrieve_avatar('alpha', "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/avatar/user/alpha/avatar.png"
    assert mock_get.call_args.kwargs.get("params") == {"s": "beta"}

@patch.object(Bamboo, "put")
def test_spec_op_upload_avatar(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.upload_avatar({"k": "v"})
    assert mock_put.call_args.args[0] == "rest/api/latest/avatar/user/avatar.png"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "delete")
def test_spec_op_remove_agent_assignment_from_environment(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.remove_agent_assignment_from_environment('7', 'alpha')
    assert mock_delete.call_args.args[0] == "rest/api/latest/deploy/environment/7/agent-assignment/alpha"

@patch.object(Bamboo, "delete")
def test_spec_op_remove_requirement_from_environment(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.remove_requirement_from_environment('7', '7')
    assert mock_delete.call_args.args[0] == "rest/api/latest/deploy/environment/7/requirement/7"

@patch.object(Bamboo, "delete")
def test_spec_op_delete_environment_variable(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.delete_environment_variable('7', 'alpha')
    assert mock_delete.call_args.args[0] == "rest/api/latest/deploy/environment/7/variable/alpha"

@patch.object(Bamboo, "delete")
def test_spec_op_delete_repository_mapping(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.delete_repository_mapping('alpha', 'alpha')
    assert mock_delete.call_args.args[0] == "rest/api/latest/deploy/project/alpha/repository/alpha"

@patch.object(Bamboo, "get")
def test_spec_op_get_all_deployment_projects(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_all_deployment_projects()
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/dashboard"

@patch.object(Bamboo, "get")
def test_spec_op_get_deployment_project(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_deployment_project('alpha')
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/dashboard/alpha"

@patch.object(Bamboo, "get")
def test_spec_op_get_deployment_projects(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_deployment_projects("beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/dashboard/paginate"
    assert mock_get.call_args.kwargs.get("params") == {"filter": "beta", "limit": "beta", "start": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_paginate_deployment_project(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_paginate_deployment_project('alpha', "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/dashboard/paginate/alpha"
    assert mock_get.call_args.kwargs.get("params") == {"filter": "beta", "limit": "beta", "start": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_find_assigned_agents_by_environment(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.find_assigned_agents_by_environment('7')
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/environment/7/agent-assignment"

@patch.object(Bamboo, "get")
def test_spec_op_get_docker_pipelines_configuration(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_docker_pipelines_configuration('7')
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/environment/7/docker"

@patch.object(Bamboo, "get")
def test_spec_op_find_possible_agents_for_environment(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.find_possible_agents_for_environment('7', "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/environment/7/possible-agent-assignment"
    assert mock_get.call_args.kwargs.get("params") == {"max-result": "beta", "searchTerm": "beta", "start-index": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_requirements_for_environment(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_requirements_for_environment('7')
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/environment/7/requirement"

@patch.object(Bamboo, "get")
def test_spec_op_get_requirement_for_environment(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_requirement_for_environment('7', '7')
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/environment/7/requirement/7"

@patch.object(Bamboo, "get")
def test_spec_op_get_detailed_agent_matches_for_environment(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_detailed_agent_matches_for_environment('7')
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/environment/7/requirement/detailedSummary"

@patch.object(Bamboo, "get")
def test_spec_op_get_agent_matches_for_environment(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_agent_matches_for_environment('7')
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/environment/7/requirement/summary"

@patch.object(Bamboo, "get")
def test_spec_op_get_environment_variable(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_environment_variable('7', 'alpha')
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/environment/7/variable/alpha"

@patch.object(Bamboo, "get")
def test_spec_op_get_all_environment_variables(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_all_environment_variables('7')
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/environment/7/variables"

@patch.object(Bamboo, "get")
def test_spec_op_get_jira_issue_status_for_project(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_jira_issue_status_for_project('alpha')
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/issue-status/alpha"

@patch.object(Bamboo, "get")
def test_spec_op_get_jira_issue_status_for_project_1(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_jira_issue_status_for_project_1('alpha', 'alpha')
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/issue-status/alpha/alpha"

@patch.object(Bamboo, "get")
def test_spec_op_get_possible_results(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_possible_results("beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/preview/possibleResults"
    assert mock_get.call_args.kwargs.get("params") == {"deploymentProjectId": "beta", "planKey": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_version_preview_1(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_version_preview_1("beta", "beta", "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/preview/result"
    assert mock_get.call_args.kwargs.get("params") == {"previousVersionId": "beta", "deploymentProjectId": "beta", "planKey": "beta", "resultKey": "beta", "buildNumber": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_version_preview(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_version_preview("beta", "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/preview/version"
    assert mock_get.call_args.kwargs.get("params") == {"previousVersionId": "beta", "versionId": "beta", "deploymentProjectId": "beta", "versionName": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_version_name(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_version_name("beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/preview/versionName"
    assert mock_get.call_args.kwargs.get("params") == {"resultKey": "beta", "deploymentProjectId": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_list_assigned_repositories(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.list_assigned_repositories('alpha')
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/project/alpha/repository"

@patch.object(Bamboo, "get")
def test_spec_op_search_available_repositories(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.search_available_repositories('alpha', "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/project/alpha/repository/search"
    assert mock_get.call_args.kwargs.get("params") == {"max-result": "beta", "searchTerm": "beta", "start-index": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_export_deployment_spec(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.export_deployment_spec('alpha', "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/project/alpha/specs"
    assert mock_get.call_args.kwargs.get("params") == {"package": "beta", "format": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_deployment_project_versions(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_deployment_project_versions('alpha', "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/project/alpha/version"
    assert mock_get.call_args.kwargs.get("params") == {"branchKey": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_deployment_naming_preview(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_deployment_naming_preview('alpha', "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/projectVersioning/alpha/namingPreview"
    assert mock_get.call_args.kwargs.get("params") == {"nextVersionName": "beta", "incrementableVariables": "beta", "incrementNumbers": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_next_deployment_versions(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_next_deployment_versions('alpha', "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/projectVersioning/alpha/nextVersion"
    assert mock_get.call_args.kwargs.get("params") == {"resultKey": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_variables_from_name(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_variables_from_name('alpha', "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/projectVersioning/alpha/parseVariables"
    assert mock_get.call_args.kwargs.get("params") == {"nextVersionName": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_deployment_project_variables(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_deployment_project_variables('alpha')
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/projectVersioning/alpha/variables"

@patch.object(Bamboo, "get")
def test_spec_op_get_deployment_result(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_deployment_result('7', "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/result/7"
    assert mock_get.call_args.kwargs.get("params") == {"includeLogs": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_version_and_plan_result(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_version_and_plan_result('7')
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/version/7/build-result"

@patch.object(Bamboo, "get")
def test_spec_op_get_latest_version_statuses(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_latest_version_statuses('7')
    assert mock_get.call_args.args[0] == "rest/api/latest/deploy/version/7/status"

@patch.object(Bamboo, "post")
def test_spec_op_add_agent_assignment_for_environment(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.add_agent_assignment_for_environment('7', {"k": "v"})
    assert mock_post.call_args.args[0] == "rest/api/latest/deploy/environment/7/agent-assignment"
    assert mock_post.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "post")
def test_spec_op_move_environment(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.move_environment('7', '7', 'alpha')
    assert mock_post.call_args.args[0] == "rest/api/latest/deploy/environment/7/move/7/alpha"

@patch.object(Bamboo, "post")
def test_spec_op_add_requirement_for_environment(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.add_requirement_for_environment('7', {"k": "v"})
    assert mock_post.call_args.args[0] == "rest/api/latest/deploy/environment/7/requirement"
    assert mock_post.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "post")
def test_spec_op_create_environment_variable(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.create_environment_variable('7', {"k": "v"})
    assert mock_post.call_args.args[0] == "rest/api/latest/deploy/environment/7/variable"
    assert mock_post.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "post")
def test_spec_op_add_assigned_repository(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.add_assigned_repository('alpha', {"k": "v"})
    assert mock_post.call_args.args[0] == "rest/api/latest/deploy/project/alpha/repository"
    assert mock_post.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "post")
def test_spec_op_update_version_status(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.update_version_status('7', 'alpha')
    assert mock_post.call_args.args[0] == "rest/api/latest/deploy/version/7/status/alpha"

@patch.object(Bamboo, "put")
def test_spec_op_save_docker_pipelines_configuration(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.save_docker_pipelines_configuration('7', {"k": "v"})
    assert mock_put.call_args.args[0] == "rest/api/latest/deploy/environment/7/docker"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_update_environment_prerequisites(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.update_environment_prerequisites('7', {"k": "v"})
    assert mock_put.call_args.args[0] == "rest/api/latest/deploy/environment/7/prerequisites"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_update_requirement_for_environment(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.update_requirement_for_environment('7', '7', {"k": "v"})
    assert mock_put.call_args.args[0] == "rest/api/latest/deploy/environment/7/requirement/7"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_update_environment_variable(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.update_environment_variable('7', 'alpha', {"k": "v"})
    assert mock_put.call_args.args[0] == "rest/api/latest/deploy/environment/7/variable/alpha"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "delete")
def test_spec_op_delete_template_configuration(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.delete_template_configuration('7')
    assert mock_delete.call_args.args[0] == "rest/api/latest/ephemeral/templateConfiguration/7"

@patch.object(Bamboo, "delete")
def test_spec_op_delete_capability(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.delete_capability('7', 'alpha')
    assert mock_delete.call_args.args[0] == "rest/api/latest/ephemeral/templateConfiguration/7/capability/alpha"

@patch.object(Bamboo, "get")
def test_spec_op_get_ephemeral_agent_pod_logs(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_ephemeral_agent_pod_logs('alpha', "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/ephemeral/pod/alpha/logs"
    assert mock_get.call_args.kwargs.get("params") == {"containerName": "beta", "limit": "beta", "afterTimestamp": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_ephemeral_agent_pod_raw_logs(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_ephemeral_agent_pod_raw_logs('alpha', "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/ephemeral/pod/alpha/logs/raw"
    assert mock_get.call_args.kwargs.get("params") == {"containerName": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_template_configurations_page(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_template_configurations_page("beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/ephemeral/templateConfiguration"
    assert mock_get.call_args.kwargs.get("params") == {"filter": "beta", "limit": "beta", "start": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_template_configuration(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_template_configuration('7')
    assert mock_get.call_args.args[0] == "rest/api/latest/ephemeral/templateConfiguration/7"

@patch.object(Bamboo, "get")
def test_spec_op_get_capabilities(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_capabilities('7', "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/ephemeral/templateConfiguration/7/capability"
    assert mock_get.call_args.kwargs.get("params") == {"limit": "beta", "start": "beta"}

@patch.object(Bamboo, "post")
def test_spec_op_create_template_configuration(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.create_template_configuration({"k": "v"})
    assert mock_post.call_args.args[0] == "rest/api/latest/ephemeral/templateConfiguration"
    assert mock_post.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "post")
def test_spec_op_add_capability(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.add_capability('7', {"k": "v"})
    assert mock_post.call_args.args[0] == "rest/api/latest/ephemeral/templateConfiguration/7/capability"
    assert mock_post.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_update_template_configuration(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.update_template_configuration('7', {"k": "v"})
    assert mock_put.call_args.args[0] == "rest/api/latest/ephemeral/templateConfiguration/7"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_update_capability(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.update_capability('7', {"k": "v"})
    assert mock_put.call_args.args[0] == "rest/api/latest/ephemeral/templateConfiguration/7/capability"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "delete")
def test_spec_op_remove_permissions_for_group_2(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.remove_permissions_for_group_2('alpha', {"k": "v"}, "beta")
    assert mock_delete.call_args.args[0] == "rest/api/latest/permissions/global/groups/alpha"
    assert mock_delete.call_args.kwargs.get("params") == {"ignore": "beta"}
    assert mock_delete.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "delete")
def test_spec_op_remove_permissions_for_role_2(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.remove_permissions_for_role_2('alpha', {"k": "v"}, "beta")
    assert mock_delete.call_args.args[0] == "rest/api/latest/permissions/global/roles/alpha"
    assert mock_delete.call_args.kwargs.get("params") == {"ignore": "beta"}
    assert mock_delete.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "delete")
def test_spec_op_remove_permissions_for_user_2(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.remove_permissions_for_user_2('alpha', {"k": "v"}, "beta")
    assert mock_delete.call_args.args[0] == "rest/api/latest/permissions/global/users/alpha"
    assert mock_delete.call_args.kwargs.get("params") == {"ignore": "beta"}
    assert mock_delete.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "get")
def test_spec_op_get_available_groups_2(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_available_groups_2("beta", "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/permissions/global/available-groups"
    assert mock_get.call_args.kwargs.get("params") == {"limit": "beta", "start": "beta", "name": "beta", "ignore": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_available_users_2(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_available_users_2("beta", "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/permissions/global/available-users"
    assert mock_get.call_args.kwargs.get("params") == {"limit": "beta", "start": "beta", "name": "beta", "ignore": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_list_group_permissions_2(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.list_group_permissions_2("beta", "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/permissions/global/groups"
    assert mock_get.call_args.kwargs.get("params") == {"limit": "beta", "start": "beta", "name": "beta", "ignore": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_list_role_permissions_2(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.list_role_permissions_2("beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/permissions/global/roles"
    assert mock_get.call_args.kwargs.get("params") == {"limit": "beta", "start": "beta", "ignore": "beta"}

@patch.object(Bamboo, "put")
def test_spec_op_add_permissions_for_group_2(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.add_permissions_for_group_2('alpha', {"k": "v"}, "beta")
    assert mock_put.call_args.args[0] == "rest/api/latest/permissions/global/groups/alpha"
    assert mock_put.call_args.kwargs.get("params") == {"ignore": "beta"}
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_add_permissions_for_role_2(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.add_permissions_for_role_2('alpha', {"k": "v"}, "beta")
    assert mock_put.call_args.args[0] == "rest/api/latest/permissions/global/roles/alpha"
    assert mock_put.call_args.kwargs.get("params") == {"ignore": "beta"}
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_add_permissions_for_user_2(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.add_permissions_for_user_2('alpha', {"k": "v"}, "beta")
    assert mock_put.call_args.args[0] == "rest/api/latest/permissions/global/users/alpha"
    assert mock_put.call_args.kwargs.get("params") == {"ignore": "beta"}
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "delete")
def test_spec_op_unmark_plan_favourite(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.unmark_plan_favourite('alpha', 'alpha')
    assert mock_delete.call_args.args[0] == "rest/api/latest/plan/alpha-alpha/favourite"

@patch.object(Bamboo, "delete")
def test_spec_op_remove_plan_label(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.remove_plan_label('alpha', 'alpha', 'alpha')
    assert mock_delete.call_args.args[0] == "rest/api/latest/plan/alpha-alpha/label/alpha"

@patch.object(Bamboo, "get")
def test_spec_op_get_plan_artifact_definition(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_plan_artifact_definition('alpha', 'alpha', "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/plan/alpha-alpha/artifact"
    assert mock_get.call_args.kwargs.get("params") == {"max-result": "beta", "start-index": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_issue_details(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_issue_details('alpha', 'alpha', 'alpha')
    assert mock_get.call_args.args[0] == "rest/api/latest/plan/alpha-alpha/issue/alpha"

@patch.object(Bamboo, "get")
def test_spec_op_get_plan_labels(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_plan_labels('alpha', 'alpha')
    assert mock_get.call_args.args[0] == "rest/api/latest/plan/alpha-alpha/label"

@patch.object(Bamboo, "post")
def test_spec_op_enable_specs_for_branches(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.enable_specs_for_branches('alpha', 'alpha')
    assert mock_post.call_args.args[0] == "rest/api/latest/plan/alpha-alpha/branch/enableSpecsForBranches"

@patch.object(Bamboo, "post")
def test_spec_op_mark_plan_favourite(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.mark_plan_favourite('alpha', 'alpha')
    assert mock_post.call_args.args[0] == "rest/api/latest/plan/alpha-alpha/favourite"

@patch.object(Bamboo, "post")
def test_spec_op_add_plan_label(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.add_plan_label('alpha', 'alpha', {"k": "v"})
    assert mock_post.call_args.args[0] == "rest/api/latest/plan/alpha-alpha/label"
    assert mock_post.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "post")
def test_spec_op_quarantine_test(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.quarantine_test('alpha', 'alpha', '7')
    assert mock_post.call_args.args[0] == "rest/api/latest/plan/alpha-alpha/test/7/quarantine"

@patch.object(Bamboo, "post")
def test_spec_op_unleash_test(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.unleash_test('alpha', 'alpha', '7')
    assert mock_post.call_args.args[0] == "rest/api/latest/plan/alpha-alpha/test/7/unleash"

@patch.object(Bamboo, "delete")
def test_spec_op_delete_project_shared_credentials(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.delete_project_shared_credentials('alpha', '7')
    assert mock_delete.call_args.args[0] == "rest/api/latest/project/alpha/sharedCredentials/7"

@patch.object(Bamboo, "delete")
def test_spec_op_delete_project_variable(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.delete_project_variable('alpha', 'alpha')
    assert mock_delete.call_args.args[0] == "rest/api/latest/project/alpha/variable/alpha"

@patch.object(Bamboo, "get")
def test_spec_op_get_paginated_project_repositories(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_paginated_project_repositories('alpha', "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/project/alpha/repositories"
    assert mock_get.call_args.kwargs.get("params") == {"filter": "beta", "limit": "beta", "start": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_search_available_repositories_1(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.search_available_repositories_1('alpha', "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/project/alpha/repository/search"
    assert mock_get.call_args.kwargs.get("params") == {"searchTerm": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_paginated_project_shared_credentials(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_paginated_project_shared_credentials('alpha', "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/project/alpha/sharedCredentials"
    assert mock_get.call_args.kwargs.get("params") == {"filter": "beta", "limit": "beta", "start": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_export_project_specs(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.export_project_specs('alpha', "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/project/alpha/specs"
    assert mock_get.call_args.kwargs.get("params") == {"package": "beta", "format": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_project_variable(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_project_variable('alpha', 'alpha')
    assert mock_get.call_args.args[0] == "rest/api/latest/project/alpha/variable/alpha"

@patch.object(Bamboo, "get")
def test_spec_op_get_project_variables(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_project_variables('alpha')
    assert mock_get.call_args.args[0] == "rest/api/latest/project/alpha/variables"

@patch.object(Bamboo, "post")
def test_spec_op_create_project(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.create_project({"k": "v"})
    assert mock_post.call_args.args[0] == "rest/api/latest/project"
    assert mock_post.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "post")
def test_spec_op_create_or_update_variable(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.create_or_update_variable('alpha', {"k": "v"})
    assert mock_post.call_args.args[0] == "rest/api/latest/project/alpha/variable"
    assert mock_post.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_enable_all_repositories_access(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.enable_all_repositories_access('alpha', 'alpha', {"k": "v"})
    assert mock_put.call_args.args[0] == "rest/api/latest/project/alpha/repository/alpha/enableAllRepositoriesAccess"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "delete")
def test_spec_op_revoke_permission_to_use_repository_by_rss_repo(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.revoke_permission_to_use_repository_by_rss_repo('7', 'alpha')
    assert mock_delete.call_args.args[0] == "rest/api/latest/repository/7/rssrepository/alpha"

@patch.object(Bamboo, "get")
def test_spec_op_search_specs_branches(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.search_specs_branches('alpha', "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/repository/alpha/rssBranches"
    assert mock_get.call_args.kwargs.get("params") == {"searchTerm": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_rss_repositories_allowed_to_access_repository(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_rss_repositories_allowed_to_access_repository('alpha')
    assert mock_get.call_args.args[0] == "rest/api/latest/repository/alpha/rssrepository"

@patch.object(Bamboo, "get")
def test_spec_op_search_available_repositories_2(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.search_available_repositories_2('alpha', "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/repository/alpha/rssrepository/search"
    assert mock_get.call_args.kwargs.get("params") == {"searchTerm": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_specs_detection_status(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_specs_detection_status('alpha', "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/repository/alpha/scan/status"
    assert mock_get.call_args.kwargs.get("params") == {"max-result": "beta", "branch": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_find_usage(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.find_usage('alpha', "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/repository/alpha/usage"
    assert mock_get.call_args.kwargs.get("params") == {"max-plans": "beta", "max-environments": "beta"}

@patch.object(Bamboo, "post")
def test_spec_op_grant_rss_repository_access(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.grant_rss_repository_access('alpha', {"k": "v"})
    assert mock_post.call_args.args[0] == "rest/api/latest/repository/alpha/rssrepository"
    assert mock_post.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "post")
def test_spec_op_trigger_specs_scanning(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.trigger_specs_scanning('alpha', "beta")
    assert mock_post.call_args.args[0] == "rest/api/latest/repository/alpha/scanNow"
    assert mock_post.call_args.kwargs.get("params") == {"branch": "beta"}

@patch.object(Bamboo, "post")
def test_spec_op_trigger_specs_scanning_1(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.trigger_specs_scanning_1("beta", "beta", "beta", "beta")
    assert mock_post.call_args.args[0] == "rest/api/latest/repository/scan"
    assert mock_post.call_args.kwargs.get("params") == {"name": "beta", "repositoryId": "beta", "id": "beta", "repositoryName": "beta"}

@patch.object(Bamboo, "put")
def test_spec_op_enable_all_projects_access(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.enable_all_projects_access('alpha', {"k": "v"})
    assert mock_put.call_args.args[0] == "rest/api/latest/repository/alpha/enableAllProjectsAccess"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_enable_all_repositories_access_1(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.enable_all_repositories_access_1('alpha', {"k": "v"})
    assert mock_put.call_args.args[0] == "rest/api/latest/repository/alpha/enableAllRepositoriesAccess"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_enable_ci(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.enable_ci('alpha', {"k": "v"})
    assert mock_put.call_args.args[0] == "rest/api/latest/repository/alpha/enableCi"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_enable_project_creation(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.enable_project_creation('alpha', {"k": "v"})
    assert mock_put.call_args.args[0] == "rest/api/latest/repository/alpha/enableProjectCreation"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_test_connection_1(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.test_connection_1({"k": "v"})
    assert mock_put.call_args.args[0] == "rest/api/latest/repository/testConnection"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "delete")
def test_spec_op_remove_build_comment(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.remove_build_comment('alpha', 'alpha', 'alpha', '7')
    assert mock_delete.call_args.args[0] == "rest/api/latest/result/alpha-alpha-alpha/comment/7"

@patch.object(Bamboo, "get")
def test_spec_op_get_branch_history(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_branch_history('alpha', 'alpha', 'alpha', "beta", "beta", "beta", "beta", "beta", "beta", "beta", "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/result/alpha-alpha/branch/alpha"
    assert mock_get.call_args.kwargs.get("params") == {"includeAllStates": "beta", "continuable": "beta", "issueKey": "beta", "max-results": "beta", "start-index": "beta", "label": "beta", "buildstate": "beta", "favourite": "beta", "expand": "beta", "lifeCycleState": "beta"}

@patch.object(Bamboo, "delete")
def test_spec_op_remove_web_sudo_from_session(mock_delete):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.remove_web_sudo_from_session()
    assert mock_delete.call_args.args[0] == "rest/api/latest/websudo-session"

@patch.object(Bamboo, "get")
def test_spec_op_get_expiry(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_expiry()
    assert mock_get.call_args.args[0] == "rest/api/latest/websudo-session"

@patch.object(Bamboo, "put")
def test_spec_op_refresh_web_sudo_session(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.refresh_web_sudo_session()
    assert mock_put.call_args.args[0] == "rest/api/latest/websudo-session"

@patch.object(Bamboo, "get")
def test_spec_op_get_all_services(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_all_services()
    assert mock_get.call_args.args[0] == "rest/api/latest/"

@patch.object(Bamboo, "get")
def test_spec_op_get_next_build_number(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_next_build_number('alpha', 'alpha')
    assert mock_get.call_args.args[0] == "rest/api/latest/buildNumber/alpha-alpha"

@patch.object(Bamboo, "put")
def test_spec_op_bump_build_number(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.bump_build_number('alpha', 'alpha', {"k": "v"})
    assert mock_put.call_args.args[0] == "rest/api/latest/buildNumber/alpha-alpha/bump"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_get_clone(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_clone('alpha', 'alpha', 'alpha', 'alpha')
    assert mock_put.call_args.args[0] == "rest/api/latest/clone/alpha-alpha:alpha-alpha"

@patch.object(Bamboo, "get")
def test_spec_op_get_all_capabilities_on_server(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_all_capabilities_on_server("beta", "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/capability/groupedListing"
    assert mock_get.call_args.kwargs.get("params") == {"max-result": "beta", "searchTerm": "beta", "lastGroup": "beta", "start-index": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_plan_summary(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_plan_summary("beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/chart/planSummary"
    assert mock_get.call_args.kwargs.get("params") == {"buildKeys": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_search_for_available_plan_child_dependencies(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.search_for_available_plan_child_dependencies('alpha', 'alpha', "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/dependency/search/alpha-alpha/child"
    assert mock_get.call_args.kwargs.get("params") == {"max-result": "beta", "searchTerm": "beta", "start-index": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_search_for_available_plan_parent_dependencies(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.search_for_available_plan_parent_dependencies('alpha', 'alpha', "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/dependency/search/alpha-alpha/parent"
    assert mock_get.call_args.kwargs.get("params") == {"max-result": "beta", "searchTerm": "beta", "start-index": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_docker_pipeline_configuration(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_docker_pipeline_configuration('alpha')
    assert mock_get.call_args.args[0] == "rest/api/latest/job/alpha/docker"

@patch.object(Bamboo, "put")
def test_spec_op_set_docker_pipeline_configuration(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.set_docker_pipeline_configuration('alpha', {"k": "v"})
    assert mock_put.call_args.args[0] == "rest/api/latest/job/alpha/docker"
    assert mock_put.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "get")
def test_spec_op_search(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.search("beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/quicksearch"
    assert mock_get.call_args.kwargs.get("params") == {"searchTerm": "beta", "searchEntity": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_search_authors(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.search_authors("beta", "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/search/authors"
    assert mock_get.call_args.kwargs.get("params") == {"max-result": "beta", "unlinkedOnly": "beta", "searchTerm": "beta", "start-index": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_search_deployments(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.search_deployments("beta", "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/search/deployments"
    assert mock_get.call_args.kwargs.get("params") == {"max-result": "beta", "searchTerm": "beta", "start-index": "beta", "permission": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_search_jobs(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.search_jobs('alpha', "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/search/jobs/alpha"
    assert mock_get.call_args.kwargs.get("params") == {"max-result": "beta", "searchTerm": "beta", "start-index": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_search_projects(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.search_projects("beta", "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/search/projects"
    assert mock_get.call_args.kwargs.get("params") == {"max-result": "beta", "searchTerm": "beta", "start-index": "beta", "permission": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_search_stages(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.search_stages('alpha', "beta", "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/search/stages/alpha"
    assert mock_get.call_args.kwargs.get("params") == {"max-result": "beta", "searchTerm": "beta", "start-index": "beta", "stageId": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_search_users(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.search_users("beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/search/users"
    assert mock_get.call_args.kwargs.get("params") == {"max-result": "beta", "searchTerm": "beta", "start-index": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_search_versions(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.search_versions("beta", "beta", "beta", "beta", "beta", "beta")
    assert mock_get.call_args.args[0] == "rest/api/latest/search/versions"
    assert mock_get.call_args.kwargs.get("params") == {"max-result": "beta", "branchKey": "beta", "searchTerm": "beta", "start-index": "beta", "deploymentProjectId": "beta", "chronologicalOrder": "beta"}

@patch.object(Bamboo, "get")
def test_spec_op_get_status_2(mock_get):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.get_status_2()
    assert mock_get.call_args.args[0] == "rest/api/latest/status"

@patch.object(Bamboo, "post")
def test_spec_op_encrypt(mock_post):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.encrypt({"k": "v"})
    assert mock_post.call_args.args[0] == "rest/api/latest/encrypt"
    assert mock_post.call_args.kwargs.get("data") == {"k": "v"}

@patch.object(Bamboo, "put")
def test_spec_op_update_all_image_ids(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.update_all_image_ids('alpha', "beta")
    assert mock_put.call_args.args[0] == "rest/api/latest/elasticConfiguration/image-id/alpha"
    assert mock_put.call_args.kwargs.get("params") == {"newImageId": "beta"}

@patch.object(Bamboo, "put")
def test_spec_op_deactivate_filter(mock_put):
    bamboo = Bamboo("https://bamboo.example.test", token="token")
    bamboo.deactivate_filter('7')
    assert mock_put.call_args.args[0] == "rest/api/latest/quickFilter/7/deactivate"
