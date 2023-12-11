Bamboo module
=============

Projects & Plans
----------------

.. code-block:: python

    # Get all Projects
    projects(expand=None, favourite=False, clover_enabled=False, max_results=25)

    # Get a single project by the key
    project(project_key, expand=None, favourite=False, clover_enabled=False)

    # Get all build plans in a project
    project_plans(project_key)

    # Get all build plans
    plans(expand=None, favourite=False, clover_enabled=False, start_index=0, max_results=25)

    # Get information about plan build directory
    plan_directory_info(plan_key)

    # Get plan information
    get_plan(plan_key)

    # Search for a plan by name
    search_plans(name, name, fuzzy=True, start_index=0, max_results=25)

    # Delete a plan (or a plan branch)
    delete_plan(plan_key)

    # Disable plan
    disable_plan(plan_key)

    # Enable plan
    enable_plan(plan_key)

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

    # Get latest build results
    latest_results(expand=None, favourite=False, clover_enabled=False, label=None, issue_key=None,
                   start_index=0, max_results=25, include_all_states=False)

    # Get latest build results for the project
    project_latest_results(project_key, expand=None, favourite=False, clover_enabled=False, label=None,
                           issue_key=None, start_index=0, max_results=25, include_all_states=False)

    # Get build results for a single plan
    plan_results(project_key, plan_key, expand=None, favourite=False, clover_enabled=False, label=None,
                 issue_key=None, start_index=0, max_results=25, include_all_states=False)

    # Get a single build result
    build_result(build_key, expand=None, include_all_states=False)

    # Get latest results for a plan
    build_latest_result(plan_key, expand=None, include_all_states=False)

    # Delete build result
    delete_build_result(build_key)

    # Execute build
    execute_build(plan_key, stage=None, execute_all_stages=True, custom_revision=None, **bamboo_variables)

Comments & Labels
-----------------

.. code-block:: python

    # Get comments for the build
    comments(project_key, plan_key, build_number, start_index=0, max_results=25)

    # Make a comment
    create_comment(project_key, plan_key, build_number, comment, author=None)

    # Get labels for a build
    labels(project_key, plan_key, build_number, start_index=0, max_results=25)

    # Create a label
    create_label(project_key, plan_key, build_number, label)

    # Delete a label
    delete_label(project_key, plan_key, build_number, label)

Deployments
-----------

.. code-block:: python

    # Get deployment projects
    deployment_projects()

    # Get deployments for a single project
    deployment_project(project_id)

    # Get deployment environment results
    deployment_environment_results(env_id, expand=None, max_results=25)

    # Get deployment dashboard
    deployment_dashboard(project_id=None)

    # Delete deployment project
    delete_deployment_project(project_id)

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
    agent_enable(agent_id=123456)

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

    # Get activity
    activity()

    # Get custom expiry
    get_custom_expiry(limit=25)

    # Get reports
    reports(max_results=25)

    # Get charts
    hart(report_key, build_keys, group_by_period, date_filter=None, date_from=None, date_to=None,
              width=None, height=None, start_index=9, max_results=25)

    # Health check
    health_check()

    # Upload plugin
    upload_plugin(plugin_path)

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

