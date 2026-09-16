Bamboo module
=============

API reference
-------------

.. autoclass:: atlassian.bamboo.Bamboo
   :members:
   :undoc-members:

Projects & Plans
----------------

.. code-block:: python

    # Get all Projects
    projects(expand=None, favourite=False, clover_enabled=False, max_results=25)

    # Alternative way to get all Projects where pagination used only for soft iteration
    jira.get_projects(start=0, limit=25)

    # Get a single project by the key
    project(project_key, expand=None, favourite=False, clover_enabled=False)

    # Get all build plans in a project
    project_plans(project_key)

    # Get all build plans
    plans(expand=None, favourite=False, clover_enabled=False, start_index=0, max_results=25)

    # Get information about plan build directory
    # Returns information about the directories where artifacts, build logs, and build results will be stored.
    plan_directory_info(plan_key)

    # Get plan information
    get_plan(plan_key)

    # Add a plan to the build queue, including optional custom variables
    bamboo.queue_build("PROJECT-PLAN", {"bamboo.variable.release": "1.2.3"})

    # Export the plan's Bamboo Specs source, including its repositories section
    spec = bamboo.get_plan_specs(plan_key, format="YAML")
    print(spec["spec"]["code"])

    # Search for a plan by name
    search_plans(name, name, fuzzy=True, start_index=0, max_results=25)

    # Delete a plan (or a plan branch)
    delete_plan(plan_key)

    # Disable plan
    disable_plan(plan_key)

    # Enable plan
    enable_plan(plan_key)

    # Retrieve information for project specified as project key.
    get_project(project_key)

    # Delete project
    delete_project(project_key)

Linked repositories and Bamboo Specs
------------------------------------

Bamboo's public REST API can search existing global linked repositories and
authorize one for a project’s Repository-Stored Bamboo Specs. It does not
create a connection on the **Linked repositories** administration page, nor
does it directly change the repositories checked out by an existing plan.
Create the global connection in Bamboo administration; change plan repositories
through that plan's Bamboo Specs and apply the Specs.

.. code-block:: python

    candidates = bamboo.search_linked_repositories("build-specs")
    repository_id = candidates["searchResults"][0]["id"]

    bamboo.link_repository_to_project("PROJECT", repository_id)
    allowed = bamboo.get_project_linked_repositories("PROJECT")
    # Revoke the project-level Repository-Stored Specs authorization:
    bamboo.unlink_repository_from_project("PROJECT", repository_id)

Branches
-------------

.. code-block:: python

    # Search Branches
    search_branches(plan_key, include_default_branch=True, max_results=25)

    # Get all plan Branches
    plan_branches(plan_key, expand=None, favourite=False, clover_enabled=False, max_results=25)

    # Get branch information
    get_branch_info(plan_key, branch_name)

    # Create new branch (vcs or simple)
    create_branch(plan_key, branch_name, vcs_branch=None, enabled=False, cleanup_enabled=False)

    # Get VCS Branches
    get_vcs_branches(plan_key, max_results=25)

Build results
-------------

.. code-block:: python

    # Get build results (Scalable from a single result to all build results)
    results(project_key=None, plan_key=None, job_key=None, build_number=None, expand=None, favourite=False,
            clover_enabled=False, issue_key=None, label=None, start_index=0, max_results=25, include_all_states=False)

    # ``label`` accepts one label or multiple labels (sent as repeated query parameters)
    plan_results("PROJECT", "PLAN", label=["release", "production"])

    # Get latest build results
    latest_results(expand=None, favourite=False, clover_enabled=False, label=None, issue_key=None,
                   start_index=0, max_results=25, include_all_states=False)

    # Get latest build results for the project
    project_latest_results(project_key, expand=None, favourite=False, clover_enabled=False, label=None,
                           issue_key=None, start_index=0, max_results=25, include_all_states=False)

    # Get build results for a single plan
    plan_results(project_key, plan_key, expand=None, favourite=False, clover_enabled=False, label=None,
                 issue_key=None, start_index=0, max_results=25, include_all_states=False)

    # Bamboo has no server-side result sort; order the retrieved history locally.
    newest_success = bamboo.latest_successful_plan_result("PROJECT", "PLAN", max_results=1000)
    oldest_failed = bamboo.oldest_failed_plan_result("PROJECT", "PLAN", max_results=1000)

    # Get a single build result
    build_result(build_key, expand=None, include_all_states=False)

    # Get latest results for a plan
    build_latest_result(plan_key, expand=None, include_all_states=False)

    # Delete build result
    delete_build_result(build_key)

    # Execute build
    execute_build(plan_key, stage=None, execute_all_stages=True, custom_revision=None, **bamboo_variables)

    # Stop Build
    stop_build(plan_key)

Comments & Labels
-----------------

.. code-block:: python

    # Get comments for a specific build
    comments(project_key, plan_key, build_number, start_index=0, max_results=25)

    # Create a comment for a specific build
    create_comment(project_key, plan_key, build_number, comment)

    # Get labels for a build
    labels(project_key, plan_key, build_number, start_index=0, max_results=25)

    # Create a label for a specific build
    create_label(project_key, plan_key, build_number, label)

    # Delete a label for a specific build
    delete_label(project_key, plan_key, build_number, label)

Deployments
-----------

.. code-block:: python

    # Get all deployment projects.
    deployment_projects()

    # Get deployments for a single project
    deployment_project(project_id)

    # Get deployment environment results
    deployment_environment_results(env_id, expand=None, max_results=25)

    # Get deployment dashboard
    deployment_dashboard(project_id=None)

    # Delete deployment project
    delete_deployment_project(project_id)

    # Returns deployment projects associated with a build plan.
    get_deployment_projects_for_plan(plan_key)

    # Triggers a deployment for a release version on the given environment.
    trigger_deployment_for_version_on_environment(version_id, environment_id)

Agents and plan variables
-------------------------

.. code-block:: python

    # activity() filters active online agents using the supported REST agent
    # resource rather than removed Bamboo dashboard endpoints.
    busy_agents = bamboo.activity(busy=True)

    capabilities = bamboo.agent_capabilities(agent_id, include_shared=True)
    bamboo.add_agent_capability(agent_id, {"type": "system", "key": "jdk", "value": "17"})
    bamboo.delete_agent_capability(agent_id, capability_key)

    variables = bamboo.get_plan_variables("PROJ-PLAN")
    bamboo.create_plan_variable("PROJ-PLAN", {"name": "release", "value": "1.0"})
    bamboo.update_plan_variable("PROJ-PLAN", "release", {"value": "1.1"})
    bamboo.delete_plan_variable("PROJ-PLAN", "release")

Users & Groups
--------------

.. code-block:: python

    # Get users in global permissions
    get_users_in_global_permissions(start=0, limit=25)

    # Get Groups
    get_groups(start=0, limit=25)

    # Create Group
    create_group(group_name)

    # Delete Group
    delete_group(group_name)

    # Add users into Group
    add_users_into_group(group_name, users)

    # Remove users from Group
    remove_users_from_group(group_name, users)

    # Get users from Group
    get_users_from_group(group_name, filter_users=None, start=0, limit=25)

    # Get users without Group
    get_users_not_in_group(group_name, filter_users='', start=0, limit=25)

    # Get deployment users
    get_deployment_users(self, deployment_id, filter_name=None, start=0, limit=25)

    # Revoke user from deployment
    revoke_user_from_deployment(self, deployment_id, user, permissions=['READ', 'WRITE', 'BUILD'])

    # Grant user to deployment
    grant_user_to_deployment(self, deployment_id, user, permissions)

    # Get deployment groups
    get_deployment_groups(self, deployment_id, filter_name=None, start=0, limit=25)

    # Revoke group from deployment
    revoke_group_from_deployment(self, deployment_id, group, permissions=['READ', 'WRITE', 'BUILD'])

    # Grant group to deployment
    grant_group_to_deployment(self, deployment_id, group, permissions)

    # Get environment user
    get_environment_users(self, environment_id, filter_name=None, start=0, limit=25)

    # Revoke user from environment
    revoke_user_from_environment(self, environment_id, user, permissions=['READ', 'WRITE', 'BUILD'])

    # Grant user to environment
    grant_user_to_environment(self, environment_id, user, permissions)

    # Get environment groups
    get_environment_groups(self, environment_id, filter_name=None, start=0, limit=25)

    # Revoke group from environment
    revoke_group_from_environment(self, environment_id, group, permissions=['READ', 'WRITE', 'BUILD'])

    # Grant group to environment
    grant_group_to_environment(self, environment_id, group, permissions)

Agents
------

.. code-block:: python

    # Get agents statuses
    agent_status(online=False)

    # Get remote agents. Currently (version 7.2.2) output is the same as for
    # agent_status but uses different API
    agent_remote(online=False)

    # Check if agent is online
    agent_is_online(agent_id=123456)

    # Enable agent
    agent_enable(agent_id=123456)

    # Disable agent
    agent_disable(agent_id)

    # Get agent details
    agent_details(agent_id=123456)
    agent_details(agent_id=123456, expand="capabilities,executableEnvironments,executableJobs")

    # Get agent capabilities
    agent_capabilities(agent_id=123456):
    agent_capabilities(agent_id=123456, include_shared=False):

Other actions
-------------

.. code-block:: python

    # Get build queue
    get_build_queue(expand='queuedBuilds')

    # Get deployment queue
    get_deployment_queue(expand='queuedDeployments')

    # Get server information
    server_info()

    # Get active online agents, including each agent's ``busy`` state
    activity()

    # Get only idle active agents
    activity(busy=False)

    # Get custom expiry
    get_custom_expiry(limit=25)

    # Get reports
    reports(max_results=25)

    # Get charts
    chart(report_key, build_keys, group_by_period, date_filter=None, date_from=None, date_to=None,
              width=None, height=None, start_index=9, max_results=25)

    # Returns status of the current indexing operation.
    reindex()

    # Kicks off a reindex.
    stop_reindex()

    # Health check
    health_check()

    # Upload plugin
    upload_plugin(plugin_path)

Responsibility and triggers
---------------------------

.. code-block:: python

    bamboo.get_broken_builds_by_user("ada")
    bamboo.get_my_broken_builds()
    bamboo.get_broken_build("PROJ-PLAN-42")
    bamboo.take_responsibility("PROJ-PLAN-42", "ada")
    bamboo.remove_responsibility("PROJ-PLAN-42", "ada")

    bamboo.remote_trigger_change_detection()

Access tokens
-------------

.. code-block:: python

    bamboo.get_access_tokens()
    bamboo.create_access_token()
    bamboo.delete_access_token("token-id")

Deployment management
---------------------

.. code-block:: python

    bamboo.create_deployment_project({"name": "Deploy PROJ"})
    bamboo.update_deployment_project("project-id", {"name": "New name"})
    bamboo.create_deployment_environment("project-id", {"name": "Staging"})
    bamboo.get_deployment_environment("environment-id")
    bamboo.update_deployment_environment("environment-id", {"name": "Production"})
    bamboo.delete_deployment_environment("environment-id")
    bamboo.get_deployment_versions("project-id")
    bamboo.create_deployment_version("project-id", {"name": "1.2.3"})
    bamboo.get_deployment_version("version-id")
    bamboo.delete_deployment_version("version-id")
    bamboo.get_deployment_dashboard_paginate()
    bamboo.get_deployment_dashboard_paginate("project-id")
    bamboo.get_deployment_dashboard_status({"environmentIds": [1]})

Admin configuration
-------------------

.. code-block:: python

    # Artifact handlers
    bamboo.get_artifact_handler_config("s3")
    bamboo.update_artifact_handler_config("s3", {"bucketName": "artifacts"})

    # General system configuration
    bamboo.get_agent_config()
    bamboo.get_offline_agent_removal_config()
    bamboo.update_offline_agent_removal_config({"enabled": True})
    bamboo.get_general_config()
    bamboo.update_general_config({"baseUrl": "https://bamboo.example.test"})
    bamboo.get_build_concurrency_config()
    bamboo.update_build_concurrency_config({"numberOfConcurrentBuilds": 10})
    bamboo.get_build_monitoring_config()
    bamboo.update_build_monitoring_config({"enabled": True})
    bamboo.get_mail_server_config()
    bamboo.update_mail_server_config({"host": "smtp.example.test"})
    bamboo.delete_mail_server_config()
    bamboo.get_im_server_config()
    bamboo.update_im_server_config({"host": "xmpp.example.test"})
    bamboo.delete_im_server_config()
    bamboo.get_remote_agent_support_config()
    bamboo.update_remote_agent_support_config({"enabled": True})
    bamboo.get_quarantine_config()
    bamboo.update_quarantine_config({"enabled": True})
    bamboo.get_audit_log_config()
    bamboo.update_audit_log_config({"enabled": True})

    # Dark features
    bamboo.get_dark_features()
    bamboo.get_dark_feature("feature-key")
    bamboo.update_dark_feature("feature-key", True)
    bamboo.get_dark_feature_user("feature-key", "ada")
    bamboo.update_dark_feature_user("feature-key", "ada", True)

    # Global variables and security
    bamboo.get_global_variables()
    bamboo.create_global_variable({"key": "KEY", "value": "value"})
    bamboo.get_global_variable("variable-id")
    bamboo.update_global_variable("variable-id", {"value": "new"})
    bamboo.delete_global_variable("variable-id")
    bamboo.verify_global_variables({"variables": []})
    bamboo.get_security_settings()
    bamboo.update_security_settings({"captchaEnabled": True})
    bamboo.get_security_groups()
    bamboo.create_security_group({"name": "admins"})
    bamboo.get_trusted_keys()
    bamboo.add_trusted_key({"key": "ssh-rsa ..."})
    bamboo.delete_trusted_key("key-id")

Resource permissions
--------------------

.. code-block:: python

    # Available principals
    bamboo.get_available_users_for_permission("deployment", "resource-id")
    bamboo.get_available_groups_for_permission("deployment", "resource-id")
    bamboo.get_roles_for_permission("deployment", "resource-id")

    # Users
    bamboo.get_permission_users("deployment", "resource-id")
    bamboo.grant_user_permission("deployment", "resource-id", "ada", ["READ", "BUILD"])
    bamboo.revoke_user_permission("deployment", "resource-id", "ada", ["READ", "BUILD"])

    # Groups
    bamboo.get_permission_groups("deployment", "resource-id")
    bamboo.grant_group_permission("deployment", "resource-id", "bamboo-admins", ["ADMIN"])
    bamboo.revoke_group_permission("deployment", "resource-id", "bamboo-admins", ["ADMIN"])

    # Roles
    bamboo.grant_role_permission("deployment", "resource-id", "ROLE_ADMIN", ["READ", "BUILD"])
    bamboo.revoke_role_permission("deployment", "resource-id", "ROLE_ADMIN", ["READ", "BUILD"])

Admin users
-----------

.. code-block:: python

    bamboo.get_users()
    bamboo.create_user({"name": "ada", "email": "ada@example.com"})
    bamboo.delete_user("ada")
    bamboo.update_user_credentials({"name": "ada", "password": "new-password"})
    bamboo.rename_user({"oldName": "ada", "newName": "ada2"})
    bamboo.get_user_access_tokens("ada")
    bamboo.delete_user_access_token("ada", "token-id")
    bamboo.get_user_alias("ada")
    bamboo.set_user_alias("ada", {"alias": "alias-ada"})
    bamboo.delete_user_alias("ada")

Server, queue and quick filters
-------------------------------

.. code-block:: python

    bamboo.get_server()
    bamboo.get_server_nodes()
    bamboo.pause_server()
    bamboo.resume_server()
    bamboo.prepare_for_restart()
    bamboo.get_current_user()

    bamboo.remove_build_from_queue("PROJ", "PLAN", 42)
    bamboo.pause_build_in_queue("PROJ", "PLAN", 42)
    bamboo.remove_deployment_from_queue("deployment-result-id")

    bamboo.get_quick_filters()
    bamboo.create_quick_filter({"name": "My builds"})
    bamboo.get_active_quick_filters()
    bamboo.get_visible_quick_filters()
    bamboo.set_visible_quick_filters([1, 2])
    bamboo.deactivate_quick_filters([1, 2])
    bamboo.get_quick_filter("filter-id")
    bamboo.update_quick_filter("filter-id", {"name": "Updated"})
    bamboo.delete_quick_filter("filter-id")
    bamboo.activate_quick_filter("filter-id")

Elastic Bamboo
--------------

.. code-block:: python

    # Get elastic bamboo instance logs
    get_elastic_instance_logs('i-12ab34cd56ef')

    # Get elastic bamboo configurations
    get_elastic_configurations()

    # Create elastic bamboo configuration
    create_elastic_configuration({"name": "value"})

    # Get elastic bamboo configuration
    get_elastic_configuration('123456')

    # Update elastic bamboo configuration
    update_elastic_configuration('123456')

    # Delete elastic bamboo configuration
    delete_elastic_configuration('123456')

    # Get elastic bamboo configuration
    get_elastic_bamboo()

    # Set elastic bamboo configuration
    set_elastic_bamboo({"enabled": True, "awsCredentialsType": "INSTANCE_PROFILE", "region": "ASIA_PACIFIC_SE_2",
    "privateKeyFile": "", "certificateFile": "", "maxNumOfElasticInstances": 1, "allocatePublicIpToVpcInstances": False,
    "elasticInstanceManagement": {"type": "Disabled"}, "uploadAwsAccountIdentifierToElasticInstances": False,
    "elasticAutoTermination": { "enabled": True, "shutdownDelay": 300}})

Plugins information
-------------------

.. code-block:: python

    # Get plugins information
    get_plugins_info()

    # Get plugin information
    get_plugin_info(plugin_key)

    # Provide plugin license information
    get_plugin_license_info(plugin_key)

    # Provide plugin path for upload into Bamboo e.g. useful for auto deploy
    upload_plugin(plugin_path)

    # Disable plugin
    disable_plugin(plugin_key)

    # Enable plugin
    enable_plugin(plugin_key)

    # Uninstall plugin
    delete_plugin(plugin_key)

    # Check plugin manager status
    get_plugin_module_info(plugin_key, module_key)

    # Update license for plugin (app)
    update_plugin_license(plugin_key, raw_license)

Full spec coverage (missing operations from the bundled Bamboo REST spec)
-------------------------------------------------------------------------

Admin (root API)
----------------

.. code-block:: python

    # Invalidate active sessions of the given user
    invalidate_user_sessions(name, user)

    # Retrieves ephemeral agents configuration.
    get_configuration()

    # Retrieves global build and deployment expiry configuration for this Bamboo instance.
    get_configuration_1()

    # Retrieves build and deployment expiry status.
    get_status()

    # Gets the collection of jobs currently scheduled to run.
    get_jobs()

    # Read system information.
    get_system_info()

    # Test connection to ephemeral agents provider.
    test_connection(data)

    # Trigger background job execution.
    trigger_job(data)

    # Renames specified user.
    rename_user_post(data, external_rename=...)

    # Modify ephemeral agents configuration.
    save_configuration(data)

    # Update global build and deployment expiry configuration for this Bamboo instance. Partial configuration is not allowed (it will fail validation).
    set_configuration(data)

    # Executes build and deployment expiry process. Will only start each process if it's not currently running.
    run()

    # Renames specified user.
    rename_user_put(new_user_name, data, external_rename=...)


Admin (users)
-------------

.. code-block:: python

    # Delete custom plan expiry settings.
    remove_plan_custom_expiry_settings(plan_key)

    # Remove a user from multiple groups.  The authenticated user must have restricted administrative permission or higher to use this resource.
    unassign_groups(name, data)

    # Retrieves a list of groups to which the user belongs. The authenticated user must have restricted administrative permission or higher to use this resource.
    find_assigned_groups(name, filter=..., limit=..., start=...)

    # Retrieves a list of unlinked aliases to which the user does not belong. The authenticated user must have restricted administrative permission or higher to use this resource.
    find_unassigned_user_repository_aliases(name, filter=..., limit=..., start=...)

    # Retrieves a list of groups to which the user does not belong. The authenticated user must have restricted administrative permission or higher to use this resource.
    find_unassigned_groups(name, filter=..., limit=..., start=...)

    # Add a user to multiple groups. The authenticated user must have restricted administrative permission or higher to use this resource.
    assign_groups(name, data)


Agents & assignments
--------------------

.. code-block:: python

    # Remove build agent.
    delete_agent(agent_id)

    # Remove agent's assignment.
    remove_assignment(executor_type=..., executor_id=..., entity_id=..., assignment_type=...)

    # Remove agent/image from list of dedicated executors for given job.
    remove_agent_assignment_from_job(job_key, executor_key)

    # Search for assignments in specified entity's agents
    search_entity_for_agent(max_result=..., executor_type=..., search_term=..., executor_id=..., entity_type=..., start_index=..., assignment_type=...)

    # Get a list of agents/images assigned to given job.
    find_assigned_agents_by_job(job_key)

    # Get a list of agents/images/templates which can be dedicated for given job.
    find_possible_agents_for_job(job_key, max_result=..., search_term=..., start_index=...)

    # Dedicate agent, elastic image or ephemeral template.
    add_agent_assignment(executor_type=..., executor_id=..., entity_id=..., assignment_type=...)

    # Add agent assignment for job. agentAssignmentKey is a map with one key-value: name - agentAssignmentKey. 
    add_agent_assignment_for_job(job_key, data)

    # Update existing agent capability. It's allowed to skip capability key at request payload.
    update_agent_capability(agent_id, capability_key, data)


Avatars
-------

.. code-block:: python

    # Deletes the current avatar for the currently authenticated user.
    delete_avatar()

    # Returns either the avatar file for a specified user or the gravatar URL. The priority order: custom user avatar as a file, gravatar URL, default avatar as a file. The endpoint supports Last-Modified/If-Modified-Since headers and sets cache policy with expiration equal by default to 90 seconds.
    retrieve_avatar(user_name, s=...)

    # Updated the avatar for the currently authenticated user.
    upload_avatar(data)


Deployments
-----------

.. code-block:: python

    # Remove agent/image from list of dedicated executors for given environment.
    remove_agent_assignment_from_environment(environment_id, executor_key)

    # Removes a requirement for an environment.
    remove_requirement_from_environment(environment_id, requirement_id)

    # Delete the environment variable.
    delete_environment_variable(environment_id, variable_name)

    # Remove approval to create plans in given deployment project by given repository.
    delete_repository_mapping(deployment_project_id, repository_id)

    # Get all deployment projects. This method fetch all deployment projects visible to user. It's not optimized for instances with large count of deployment projects and environments, use paged versions instead.
    get_all_deployment_projects()

    # Get deployment project environments with deployment status. It's not optimized for instances with large count of deployment projects and environments, use paged versions instead.
    get_deployment_project(project_id)

    # Get paginated deployment projects with environments list.
    get_deployment_projects(filter=..., limit=..., start=...)

    # Get deployment project environments.
    get_paginate_deployment_project(project_id, filter=..., limit=..., start=...)

    # Get a list of agents/images assigned to given environment.
    find_assigned_agents_by_environment(environment_id)

    # Get Docker configuration for given environment.
    get_docker_pipelines_configuration(environment_id)

    # Get a list of agents/images/templates which can be dedicated for given environment.
    find_possible_agents_for_environment(environment_id, max_result=..., search_term=..., start_index=...)

    # Gets all the requirements of an environment.
    get_requirements_for_environment(environment_id)

    # Gets the details of a requirement for a given environment.
    get_requirement_for_environment(environment_id, requirement_id)

    # Gets a detailed summary of the agents that are capable of running an environment, based of its requirements.
    get_detailed_agent_matches_for_environment(environment_id)

    # Gets a summary of the agents that are capable of running an environment, based of its requirements.
    get_agent_matches_for_environment(environment_id)

    # Get the environment variable by its name.
    get_environment_variable(environment_id, variable_name)

    # Get a list of environment variables.
    get_all_environment_variables(environment_id)

    # Get all deployment projects associated with Jira issue key
    get_jira_issue_status_for_project(issue_key)

    # Get deployment project environments and versions associated with Jira issue
    get_jira_issue_status_for_project_1(issue_key, deployment_project_id)

    # Get possible deployment results.
    get_possible_results(plan_key, deployment_project_id=...)

    # Get a preview of the deployment version.
    get_version_preview_1(previous_version_id=..., deployment_project_id=..., plan_key=..., result_key=..., build_number=...)

    # Get a preview of the deployment version.
    get_version_preview(previous_version_id=..., version_id=..., deployment_project_id=..., version_name=...)

    # Get version name.
    get_version_name(deployment_project_id, result_key=...)

    # List of repositories which granted to create/edit environment in given deployment project by Repository stored Bamboo Specs.
    list_assigned_repositories(deployment_project_id)

    # Search for linked repositories which can be granted to create/modify environment by Repository stored Bamboo Specs in given deployment project.
    search_available_repositories(deployment_project_id, max_result=..., search_term=..., start_index=...)

    # Export a deployment project to Bamboo Specs.
    export_deployment_spec(deployment_project_id, package=..., format=...)

    # Get list of deployment versions.
    get_deployment_project_versions(deployment_project_id, branch_key=...)

    # Get deployment version name preview.
    get_deployment_naming_preview(deployment_project_id, next_version_name, incrementable_variables=..., increment_numbers=...)

    # Get next deployment version name.
    get_next_deployment_versions(deployment_project_id, result_key=...)

    # Extract variables value from version name.
    get_variables_from_name(deployment_project_id, next_version_name)

    # Get variables associated with deployment project.
    get_deployment_project_variables(deployment_project_id)

    # Get result of version deployment to environment.
    get_deployment_result(deployment_result_id, include_logs=...)

    # Get associated build result of deployment version.
    get_version_and_plan_result(deployment_version_id)

    # Get the all users' latest statuses of deployment version.
    get_latest_version_statuses(deployment_version_id)

    # Add agent assignment for environment. agentAssignmentKey is a map with one key-value: name - agentAssignmentKey. 
    add_agent_assignment_for_environment(environment_id, data)

    # Change environment position within deployment project.
    move_environment(environment_id, position, relative_environment_id)

    # Adds a requirement for a given environment.
    add_requirement_for_environment(environment_id, data)

    # Create the environment variable.
    create_environment_variable(environment_id, data)

    # Grant permission to create/edit plan in given deployment project by Bamboo Specs from given repository.
    add_assigned_repository(deployment_project_id, data)

    # Update deployment version status.
    update_version_status(deployment_version_id, new_status)

    # Save Docker configuration for given environment.
    save_docker_pipelines_configuration(environment_id, data)

    # Updates the environment prerequisites.
    update_environment_prerequisites(environment_id, data)

    # Updates a requirement for a given environment.
    update_requirement_for_environment(environment_id, requirement_id, data)

    # Update the environment variable.
    update_environment_variable(environment_id, variable_name, data)


Ephemeral agents
----------------

.. code-block:: python

    # Delete ephemeral template configuration.
    delete_template_configuration(configuration_id)

    # Remove ephemeral agent template capability.
    delete_capability(configuration_id, name)

    # Gets either pod or container related logs.
    get_ephemeral_agent_pod_logs(pod, container_name=..., limit=..., after_timestamp=...)

    # Gets either pod or container all logs in the raw, plain text form.
    get_ephemeral_agent_pod_raw_logs(pod, container_name=...)

    # Fetch page of ephemeral templates.
    get_template_configurations_page(filter=..., limit=..., start=...)

    # Gets ephemeral template configuration details.
    get_template_configuration(configuration_id)

    # Fetch page of ephemeral agent template capabilities.
    get_capabilities(configuration_id, limit=..., start=...)

    # Create ephemeral template configuration.
    create_template_configuration(data)

    # Add ephemeral agent template capability.
    add_capability(configuration_id, data)

    # Update ephemeral agent template.
    update_template_configuration(configuration_id, data)

    # Update ephemeral agent template capability.
    update_capability(configuration_id, data)


Global permissions
------------------

.. code-block:: python

    # Revokes global permissions from a given group.
    remove_permissions_for_group_2(name, data, ignore=...)

    # Revokes global permissions from a given role.
    remove_permissions_for_role_2(name, data, ignore=...)

    # Revokes global permissions from a given user.
    remove_permissions_for_user_2(name, data, ignore=...)

    # Returns list of groups which weren't granted explicitly any permissions. Resource is paged, returns single page of resources.
    get_available_groups_2(limit=..., start=..., name=..., ignore=...)

    # Returns list of users which weren't granted explicitly any permissions. Resource is paged, returns single page of resources.
    get_available_users_2(limit=..., start=..., name=..., ignore=...)

    # Retrieve a list of groups with their global permissions. The list can be filtered by some attributes. This resource is paged returns a single page of results.
    list_group_permissions_2(limit=..., start=..., name=..., ignore=...)

    # Retrieve a list of roles with their global permissions. This resource is paged returns a single page of results, although only 2 roles are supported: LOGGED IN users, ANONYMOUS users
    list_role_permissions_2(limit=..., start=..., ignore=...)

    # Grants global permissions to a given group.
    add_permissions_for_group_2(name, data, ignore=...)

    # Grants global permissions to a given role.
    add_permissions_for_role_2(name, data, ignore=...)

    # Grants global permissions to a given user.
    add_permissions_for_user_2(name, data, ignore=...)


Plans
-----

.. code-block:: python

    # Remove plan from favorites.
    unmark_plan_favourite(project_key, build_key)

    # Remove label from plan.
    remove_plan_label(project_key, build_key, label_name)

    # Fetch plan's shared artifact definitions.
    get_plan_artifact_definition(project_key, build_key, max_result=..., start_index=...)

    # Fetch linked Jira issue details.
    get_issue_details(project_key, build_key, issue_key)

    # List of labels for plan.
    get_plan_labels(project_key, build_key)

    # Enable specs scanning for all branches.
    enable_specs_for_branches(project_key, build_key)

    # Add plan to favourite.
    mark_plan_favourite(project_key, build_key)

    # Add new label to plan.
    add_plan_label(project_key, build_key, data)

    # Quarantine plan's test.
    quarantine_test(project_key, build_key, test_id)

    # Unleash plan's test from quarantine.
    unleash_test(project_key, build_key, test_id)


Projects & repositories
-----------------------

.. code-block:: python

    # Deletes shared project credentials specified by id.
    delete_project_shared_credentials(project_key, shared_credential_id)

    # Delete the project variable.
    delete_project_variable(project_key, variable_name)

    # Retrieves paginated project repositories specified by the project key.
    get_paginated_project_repositories(project_key, filter=..., limit=..., start=...)

    # Search for linked repositories which can be granted to create plans by Repository stored Bamboo Specs in given project
    search_available_repositories_1(project_key, search_term=...)

    # Retrieves paginated shared credentials for the project specified by the project key.
    get_paginated_project_shared_credentials(project_key, filter=..., limit=..., start=...)

    # Export all of the plans for a project to Bamboo specs.
    export_project_specs(project_key, package=..., format=...)

    # Retrieve the project variable by given name.
    get_project_variable(project_key, variable_name)

    # Retrieve the list of all variables for a project.
    get_project_variables(project_key)

    # Create project.
    create_project(data)

    # Create or update project variable.
    create_or_update_variable(project_key, data)

    # Enables access (i.e. allowing usage) to all project's repositories by the Bamboo Specs code stored in this repository.
    enable_all_repositories_access(project_key, repository_id, data)


Repositories
------------

.. code-block:: python

    # Revoke access of RSS code stored in repository defined by repositoryId from repository defined by targetRepositoryId. Use this method when need to prevent usage of target repository by RSS code stored in repository referenced by repositoryId.
    revoke_permission_to_use_repository_by_rss_repo(target_repository_id, repository_id)

    # Search for divergent branches names (i.e. vcs branches that have RSS execution results).
    search_specs_branches(repository_id, search_term=...)

    # Fetch list of RSS repositories which can use given repository by RSS code.
    get_rss_repositories_allowed_to_access_repository(repository_id)

    # Search for existing linked repositories which can be granted to use given repository by RSS.
    search_available_repositories_2(repository_id, search_term=...)

    # Resource providing status of RSS processing for a given repository and optional branch.
    get_specs_detection_status(repository_id, max_result=..., branch=...)

    # Search for usages of given repository.
    find_usage(repository_id, max_plans=..., max_environments=...)

    # Grant repository with RSS code to use target repository in build plans and deployments. If permission is not granted RSS import will fail when code tries to use target repository.
    grant_rss_repository_access(repository_id, data)

    # Resource for triggering Repository-stored Bamboo Specs in a 'forced' way. Successful requests to this resource will trigger Bamboo Specs execution even if standard processing would have been skipped (e.g. no new commits to process).
    trigger_specs_scanning(repository_id, branch=...)

    # Webhook resource for triggering Repository-stored Bamboo Specs. Either repository ID or name must be provided via query parameters to identify the linked repository in which Bamboo Specs are defined.
    trigger_specs_scanning_1(name=..., repository_id=..., id=..., repository_name=...)

    # Enables access (i.e. allowing modifications) for all Bamboo projects by the Bamboo Specs code stored in this repository. Changes in Bamboo Specs detected will trigger execution of Specs and thus an update of corresponding entities (such as build plans or deployments).
    enable_all_projects_access(repository_id, data)

    # Enables access (i.e. allowing usage in plans or deployment projects) for all Bamboo linked repositories by the Bamboo Specs code stored in this repository.
    enable_all_repositories_access_1(repository_id, data)

    # Enables or disables detection of Bamboo Specs stored in the repository. If enabled, code changes detected in Bamboo Specs in new commits will trigger execution of Bamboo Specs and thus an update of corresponding entities (such as build plans, deployments or permissions).
    enable_ci(repository_id, data)

    # Enables build and deployment project creation by the Bamboo Specs code stored in this repository.
    enable_project_creation(repository_id, data)

    # Tests connection to a repository if the repository type supports connection testing. Request payload should contain repository configuration.
    test_connection_1(data)


Build results
-------------

.. code-block:: python

    # Removes a comment from a build result.
    remove_build_comment(project_key, build_key, build_number, comment_id)

    # Provide list of build results for specified plan's branch. Plan might be top level plan (projectKey-planKey) or job plan (projectKey-planKey-jobKey).
    get_branch_history(project_key, build_key, branch_name, include_all_states=..., continuable=..., issue_key=..., max_results=..., start_index=..., label=..., buildstate=..., favourite=..., expand=..., life_cycle_state=...)


Web sudo
--------

.. code-block:: python

    # Remove web sudo from session.
    remove_web_sudo_from_session()

    # Get the web sudo expiry from session.
    get_expiry()

    # Refresh the web sudo expiry for the current session.
    refresh_web_sudo_session()


General
-------

.. code-block:: python

    # Provides list of available REST resources in Bamboo
    get_all_services()


Build numbers & clone
---------------------

.. code-block:: python

    # Retrieve the next build number for a given plan or plan branch.
    get_next_build_number(project_key, build_key)

    # Bump the next build number for a given plan or plan branch to the specified value.
    bump_build_number(project_key, build_key, data)

    # Clone an existing Plan into a new one, possibly into different project.
    get_clone(project_key, build_key, to_project_key, to_build_key)


Server capabilities
-------------------

.. code-block:: python

    # Provides a list of capabilities for a select list in the UI.  Filterable and paginable.
    get_all_capabilities_on_server(max_result=..., search_term=..., last_group=..., start_index=...)


Plan summary charts
-------------------

.. code-block:: python

    # Get plan summary.
    get_plan_summary(build_keys=...)


Plan dependencies
-----------------

.. code-block:: python

    # Search for available plan child dependencies
    search_for_available_plan_child_dependencies(project_key, build_key, search_term, max_result=..., start_index=...)

    # Search for available plan parent dependencies
    search_for_available_plan_parent_dependencies(project_key, build_key, search_term, max_result=..., start_index=...)


Job configuration
-----------------

.. code-block:: python

    # Retrieves Docker configuration for given job.
    get_docker_pipeline_configuration(job_key)

    # Updates Docker configuration for given job.
    set_docker_pipeline_configuration(job_key, data)


Global search
-------------

.. code-block:: python

    # Performs a starts with search against projects, plans, plan branches, deployment projects
    search(search_term=..., search_entity=...)

    # A starts-with search of authors based on their author name.
    search_authors(search_term, max_result=..., unlinked_only=..., start_index=...)

    # Performs a contains search against deployment project name.
    search_deployments(max_result=..., search_term=..., start_index=..., permission=...)

    # Performs a "starts with" search against full job name and full job key.
    search_jobs(plan_key, max_result=..., search_term=..., start_index=...)

    # Performs a contains search against project name.
    search_projects(max_result=..., search_term=..., start_index=..., permission=...)

    # Performs a "starts with" search against full stage name.
    search_stages(plan_key, max_result=..., search_term=..., start_index=..., stage_id=...)

    # A starts-with search of users based on their username, full-name and if allowed email address.
    search_users(search_term, max_result=..., start_index=...)

    # Performs a contains search against a version name.
    search_versions(deployment_project_id, max_result=..., branch_key=..., search_term=..., start_index=..., chronological_order=...)


Server status
-------------

.. code-block:: python

    # Returns the current status of the Bamboo node. This endpoint enables a basic status check on the status of a Bamboo node.
    get_status_2()


Utility
-------

.. code-block:: python

    # Encrypts a given text based on the instance specific cipher. Encrypted data can be used i.a. in Repository-stored Specs. Feature can be enabled or disabled in Bamboo security configuration. Number of allowed requests per user is limited and can be modified in Bamboo security configuration.
    encrypt(data)


Elastic configuration
---------------------

.. code-block:: python

    # Bulk update of all images AMI id.
    update_all_image_ids(image_id, new_image_id)


Quick filters
-------------

.. code-block:: python

    # Deactivates a quick filter for currently logged in user.
    deactivate_filter(id)
