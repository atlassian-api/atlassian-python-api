BitBucket module
================

Manage projects
---------------

.. code-block:: python

    # Project list
    bitbucket.project_list()

    # Repo list
    bitbucket.repo_list(project_key)

    # Project info
    bitbucket.project(key)

    # Create project
    bitbucket.create_project(key, name, description="My pretty project")

    # Get users who has permission in project
    bitbucket.project_users(key, limit=99999, filter_str=None)

    # Get project administrators for project
    bitbucket.project_users_with_administrator_permissions(key)

    # Get Project Groups
    bitbucket.project_groups(key, limit=99999, filter_str=None)

    # Get groups with admin permissions
    bitbucket.project_groups_with_administrator_permissions(key)

    # Project summary
    bitbucket.project_summary(key)

    # Check default permission for project
    bitbucket.project_default_permissions(project_key, permission)

    # Grant default permission for project
    bitbucket.project_grant_default_permissions(project_key, permission)

    # Grant project permission to a specific user
    bitbucket.project_grant_user_permissions(project_key, username, permission)

    # Grant project permission to a specific group
    bitbucket.project_grant_group_permissions(project_key, groupname, permission)

    # Remove default permission for project
    bitbucket.project_remove_default_permissions(project_key, permission)

    # Remove all project permissions for a specific user
    bitbucket.project_remove_user_permissions(project_key, username)

    # Remove all project permissions for a specific group
    bitbucket.project_remove_group_permissions(project_key, groupname)

Manage repositories
-------------------

.. code-block:: python

    # Get single repository
    bitbucket.get_repo(project_key, repository_slug)

    # Update single repository
    bitbucket.update_repo(project_key, repository_slug, description="Repo description")

    # Get labels for a single repository
    bitbucket.get_repo_labels(project_key, repository_slug)

    # Set label for a single repository
    bitbucket.set_repo_label(project_key, repository_slug, label_name)

    # Disable branching model
    bitbucket.disable_branching_model(project_key, repo_key)

    # Enable branching model
    bitbucket.enable_branching_model(project_key, repo_key)

    # Get branching model
    bitbucket.get_branching_model(project_key, repo_key)

    # Set branching model
    data = {'development': {'refId': None, 'useDefault': True},
            'types': [{'displayName': 'Bugfix',
                       'enabled': True,
                       'id': 'BUGFIX',
                       'prefix': 'bugfix-'},
                      {'displayName': 'Feature',
                       'enabled': True,
                       'id': 'FEATURE',
                       'prefix': 'feature-'},
                      {'displayName': 'Hotfix',
                       'enabled': True,
                       'id': 'HOTFIX',
                       'prefix': 'hotfix-'},
                      {'displayName': 'Release',
                       'enabled': True,
                       'id': 'RELEASE',
                       'prefix': 'release/'}]}
    bitbucket.set_branching_model(project_key, repo_key, data)

    bitbucket.repo_users(project_key, repo_key, limit=99999, filter_str=None)

    bitbucket.repo_groups(project_key, repo_key, limit=99999, filter_str=None)

    # Grant repository permission to an specific user
    bitbucket.repo_grant_user_permissions(project_key, repo_key, username, permission)

    # Grant repository permission to an specific group
    bitbucket.repo_grant_group_permissions(project_key, repo_key, groupname, permission)

    # Delete a repository (DANGER!)
    bitbucket.delete_repo(project_key, repository_slug)

    # Fork repo inside same project
    fork_repository(project_key, repository_slug, new_repository_slug)

    # Fork repo to new project
    fork_repository_new_project(project_key, repository_slug, new_project_key, new_repository_slug)

Manage Code Insights
--------------------

.. code-block:: python

    # Delete an existing Code Insights report
    bitbucket.delete_code_insights_report(project_key, repository_slug, commit_hash, report_key)

    # Create a new Code Insights report
    report = {
        'details': 'This is an example report',
        'result': 'FAIL',
        'reporter': 'Anonymous',
        'link': 'http://some-url',
        'logo-url': 'http://some-url',
        'data': [
            {
                'title': 'Example coverage',
                'type': 'PERCENTAGE',
                'value': 85
            }
        ]
    }
    bitbucket.create_code_insights_report(project_key, repository_slug, commit_hash, report_key, 'Code Insights Report', **report)

    # Add annotations to a Code Insights report
    annotations = [
        {
        'path': 'some/path/to/file',
        'line': 32,
        'message': 'Roses are red, Violets are blue, Unexpected { on line 32',
        'severity': 'MEDIUM'
        }
    ]
    bitbucket.add_code_insights_annotations_to_report(project_key, repository_slug, commit_hash, report_key, **annotations)

Groups and admins
-----------------

.. code-block:: python

    # Get group of members
    bitbucket.group_members(group, limit=99999)

    # All project administrators
    bitbucket.all_project_administrators()

    # Get users. Use 'user_filter' parameter to get specific users.
    bitbucket.get_users(user_filter="username", limit=25, start=0)

Manage code
-----------

.. code-block:: python

    # Get repositories list from project
    bitbucket.repo_list(project_key, limit=25)

    # Create a new repository.
    # Requires an existing project in which this repository will be created. The only parameters which will be used
    # are name and scmId.
    # The authenticated user must have PROJECT_ADMIN permission for the context project to call this resource.
    bitbucket.create_repo(project_key, repository, forkable=False, is_private=True)

    # Get branches from repo
    bitbucket.get_branches(project, repository, filter='', limit=99999, details=True)

    # Creates a branch using the information provided in the request.
    # The authenticated user must have REPO_WRITE permission for the context repository to call this resource.
    bitbucket.create_branch(project_key, repository, name, start_point, message)

    # Delete branch from related repo
    bitbucket.delete_branch(project, repository, name, end_point=None)

    # Get pull requests
    bitbucket.get_pull_requests(project, repository, state='OPEN', order='newest', limit=100, start=0)

    # Get pull request activities
    bitbucket.get_pull_requests_activities(project, repository, pull_request_id)

    # Get pull request changes
    bitbucket.get_pull_requests_changes(project, repository, pull_request_id)

    # Get pull request commits
    bitbucket.get_pull_requests_commits(project, repository, pull_request_id)

    # Add comment into pull request
    bitbucket.add_pull_request_comment(project, repository, pull_request_id, text)

    # Reply to a comment of a pull request
    bitbucket.add_pull_request_comment(project, repository, pull_request_id, text, parent_id=None)

    # Create a new pull request between two branches.
    bitbucket.open_pull_request(source_project, source_repo, dest_project, dest_repo, source_branch, destination_branch, title, description)

    # Create a new pull request between two branches with one reviewer
    bitbucket.open_pull_request(source_project, source_repo, dest_project, dest_repo, source_branch, destination_branch, title, description, reviewers='name')

    # Create a new pull request between two branches with multiple reviewers.
    bitbucket.open_pull_request(source_project, source_repo, dest_project, dest_repo, source_branch, destination_branch, title, description, reviewers=['name1', 'name2'])

    # Delete a pull request
    bitbucket.delete_pull_request(project, repository, pull_request_id, pull_request_version)

    # Get tags for related repo
    bitbucket.get_tags(project, repository, filter='', limit=99999)

    # Get project tags
    # The authenticated user must have REPO_READ permission for the context repository to call this resource
    bitbucket.get_project_tags(project, repository, tag_name)

    # Set tag
    # The authenticated user must have REPO_WRITE permission for the context repository to call this resource
    bitbucket.set_tag(project, repository, tag_name, commit_revision, description=None)

    # Delete tag
    # The authenticated user must have REPO_WRITE permission for the context repository to call this resource
    bitbucket.delete_tag(project, repository, tag_name)

    # Get diff
    bitbucket.get_diff(project, repository, path, hash_oldest, hash_newest)

    # Get commit list from repo
    bitbucket.get_commits(project, repository, hash_oldest, hash_newest, limit=99999)

    # Get change log between 2 refs
    bitbucket.get_changelog(project, repository, ref_from, ref_to, limit=99999)

    # Get raw content of the file from repo
    bitbucket.get_content_of_file(project, repository, filename, at=None, markup=None)
    """
        Retrieve the raw content for a file path at a specified revision.
        The authenticated user must have REPO_READ permission for the specified repository to call this resource.
    """

Branch permissions
------------------

.. code-block:: python

    # Set branches permissions
    bitbucket.set_branches_permissions(project_key, multiple_permissions=False, matcher_type=None, matcher_value=None, permission_type=None, repository_slug=None, except_users=[], except_groups=[], except_access_keys=[], start=0, limit=25)

    # Delete a single branch permission by permission id
    bitbucket.delete_branch_permission(project_key, permission_id, repository_slug=None)

    # Get a single branch permission by permission id
    bitbucket.get_branch_permission(project_key, permission_id, repository_slug=None)

Pull Request management
-----------------------

.. code-block:: python

    # Decline pull request
    bitbucket.decline_pull_request(project_key, repository, pr_id, pr_version)

    # Check if pull request can be merged
    bitbucket.is_pull_request_can_be_merged(project_key, repository, pr_id)

    # Merge pull request
    bitbucket.merge_pull_request(project_key, repository, pr_id, pr_version)

    # Reopen pull request
    bitbucket.reopen_pull_request(project_key, repository, pr_id, pr_version)

Conditions-Reviewers management
-------------------------------

.. code-block:: python

    # Get all project conditions with reviewers list for specific project
    bitbucket.get_project_conditions(project_key)

    # Get a project condition with reviewers list for specific project
    bitbucket.get_project_condition(project_key, id_condition)

    # Create project condition with reviewers for specific project
    # :example condition: '{"sourceMatcher":{"id":"any","type":{"id":"ANY_REF"}},"targetMatcher":{"id":"refs/heads/master","type":{"id":"BRANCH"}},"reviewers":[{"id": 12}],"requiredApprovals":"0"}'
    bitbucket.create_project_condition(project_key, condition)

    # Update a project condition with reviewers for specific project
    # :example condition: '{"sourceMatcher":{"id":"any","type":{"id":"ANY_REF"}},"targetMatcher":{"id":"refs/heads/master","type":{"id":"BRANCH"}},"reviewers":[{"id": 12}],"requiredApprovals":"0"}'
    bitbucket.update_project_condition(project_key, condition, id_condition)

    # Delete a project condition for specific project
    bitbucket.delete_project_condition(project_key, id_condition)

    # Get all repository conditions with reviewers list for specific repository in project
    bitbucket.get_repo_conditions(project_key, repo_key)

    # Get repository conditions with reviewers list only only conditions type PROJECT for specific repository in project
    bitbucket.get_repo_project_conditions(project_key, repo_key)

    # Get repository conditions with reviewers list only conditions type REPOSITORY for specific repository in project
    bitbucket.get_repo_repo_conditions(project_key, repo_key)

    # Get a project condition with reviewers list for specific repository in project
    bitbucket.get_repo_condition(project_key, repo_key, id_condition)

    # Create project condition with reviewers for specific repository in project
    # :example condition: '{"sourceMatcher":{"id":"any","type":{"id":"ANY_REF"}},"targetMatcher":{"id":"refs/heads/master","type":{"id":"BRANCH"}},"reviewers":[{"id": 12}],"requiredApprovals":"0"}'
    bitbucket.create_repo_condition(project_key, repo_key, condition)

    # Update a project condition with reviewers for specific repository in project
    # :example condition: '{"sourceMatcher":{"id":"any","type":{"id":"ANY_REF"}},"targetMatcher":{"id":"refs/heads/master","type":{"id":"BRANCH"}},"reviewers":[{"id": 12}],"requiredApprovals":"0"}'
    bitbucket.update_repo_condition(project_key, repo_key, condition, id_condition)

    # Delete a project condition for specific repository in project
    bitbucket.delete_repo_condition(project_key, repo_key, id_condition)

Bitbucket Cloud
---------------

.. code-block:: python

    # Get a list of workplaces:
    cloud.workspaces.each()

    # Get a single workplace by workplace slug
    workplace = cloud.workspaces.get(workspace_slug)

    # Get a list of permissions in a workspace (this may not work depending on the size of your workspace)
    workplace.permissions.each():

    # Get a list of repository permissions in a workspace (this may not work depending on the size of your workspace)
    workplace.permissions.repositories():

    # Get a single repository permissions in a workspace
    workplace.permissions.repositories(repo_slug):

    # Get a list of projects in a workspace
    workplace.projects.each():

    # Get a single project from a workplace by project key
    project = workplace.projects.get(project_key)

    # Get a list of repos from a project
    project.repositories.each():

    # Get a repository
    repository = workplace.repositories.get(repository_slug)

    # Get a list of deployment environments from a repository
    repository.deployment_environments.each():

    # Get a single deployment environment from a repository by deployment environment key
    deployment_environment = repository.deployment_environments.get(deployment_environment_key)

    # Get a list of deployment environment variables from a deployment environment
    deployment_environment_variables = deployment_environment.deployment_environment_variables.each():

    # Create a new deployment environment variable with a name of 'KEY', value of 'VALUE' and is not secured.
    new_deployment_environment_variable = deployment_environment.deployment_environment_variables.create("KEY", "VALUE", False)

    # Update the 'key' field of repository_variable
    updated_deployment_environment_variable = new_deployment_environment_variable.update(key="UPDATED_DEPLOYMENT_ENVIRONMENT_VARIABLE_KEY")

    # Update the 'value' field of repository_variable
    updated_deployment_environment_variable = new_deployment_environment_variable.update(value="UPDATED_DEPLOYMENT_ENVIRONMENT_VARIABLE_VALUE")

    # Delete deployment environment variable
    updated_deployment_environment_variable.delete()

    # Get a list of group permissions from a repository
    repository.group_permissions.each():

    # Get a single group permission from a repository by group slug
    repository.group_permissions.get(group_slug)

    # Get a list of repository variables from a repository
    repository.repository_variables.each():

    # Get a single repository variable from a repository by repository variable key
    repository_variable = repository.repository_variables.get(repository_variable_key)

    # Create a new repository variable with a name of 'KEY', value of 'VALUE' and is not secured.
    new_repository_variable = repository.repository_variables.create("KEY", "VALUE", False)

    # Update the 'key' field of repository_variable
    updated_repository_variable = repository_variable.update(key="UPDATED_REPOSITORY_VARIABLE_KEY")

    # Update the 'value' field of repository_variable
    updated_repository_variable = repository_variable.update(value="UPDATED_REPOSITORY_VARIABLE_VALUE")

    # Delete repository_variable
    repository_variable.delete()

Pipelines management
--------------------

.. code-block:: python

    # Object oriented:
        # Get the repository first
        r = cloud.workspaces.get(workspace).repositories.get(repository)

        # Get first ten Pipelines results for repository
        r.pipelines.each()

        # Get twenty last Pipelines results for repository
        r.pipelines.each(sort="-created_on", pagelen=20)

        # Trigger default Pipeline on the latest revision of the master branch
        r.pipelines.trigger()

        # Trigger default Pipeline on the latest revision of the develop branch
        r.pipelines.trigger(branch="develop")

        # Trigger default Pipeline on a specific revision of the develop branch
        r.pipelines.trigger(branch="develop", revision="<40-char hash>")

        # Trigger specific Pipeline on a specific revision of the master branch
        r.pipelines.trigger(revision="<40-char hash>", name="style-check")

        # Trigger specific Pipeline of the master branch with specific variables
        r.pipelines.trigger(name="style-check", variables=[{ "key": "var-name", "value": "var-value" }])

        # Get specific Pipeline by UUID
        pl = r.pipelines.get("{7d6c327d-6336-4721-bfeb-c24caf25045c}")

        # Stop specific Pipeline by UUID
        pl.stop()

        # Get steps of Pipeline specified by UUID
        pl.steps()

        # Get step of Pipeline specified by UUIDs
        s = pl.step("{56d2d8af-6526-4813-a22c-733ec6ecabf3}")

        # Get log of step of Pipeline specified by UUIDs
        s.log()

    # or function oriented:
        # Get most recent Pipelines results for repository
        bitbucket.get_pipelines(workspace, repository)

        # Trigger default Pipeline on the latest revision of the master branch
        bitbucket.trigger_pipeline(workspace, repository)

        # Trigger default Pipeline on the latest revision of the develop branch
        bitbucket.trigger_pipeline(workspace, repository, branch="develop")

        # Trigger default Pipeline on a specific revision of the develop branch
        bitbucket.trigger_pipeline(workspace, repository, branch="develop", revision="<40-char hash>")

        # Trigger specific Pipeline on a specific revision of the master branch
        bitbucket.trigger_pipeline(workspace, repository, revision="<40-char hash>", name="style-check")

        # Get specific Pipeline by UUID
        bitbucket.get_pipeline(workspace, repository, "{7d6c327d-6336-4721-bfeb-c24caf25045c}")

        # Stop specific Pipeline by UUID
        bitbucket.stop_pipeline(workspace, repository, "{7d6c327d-6336-4721-bfeb-c24caf25045c}")

        # Get steps of Pipeline specified by UUID
        bitbucket.get_pipeline_steps(workspace, repository, "{7d6c327d-6336-4721-bfeb-c24caf25045c}")

        # Get step of Pipeline specified by UUIDs
        bitbucket.get_pipeline_step(workspace, repository, "{7d6c327d-6336-4721-bfeb-c24caf25045c}", "{56d2d8af-6526-4813-a22c-733ec6ecabf3}")

        # Get log of step of Pipeline specified by UUIDs
        bitbucket.get_pipeline_step_log(workspace, repository, "{7d6c327d-6336-4721-bfeb-c24caf25045c}", "{56d2d8af-6526-4813-a22c-733ec6ecabf3}")

Manage issues
-------------

.. code-block:: python

    # Object oriented:
        # Get the repository first
        r = cloud.workspaces.get(workspace).repositories.get(repository)

        # Get all tracked issues
        r.issues.each()

        # Get all unassigned issues and sort them by priority
        r.issues.get(sort_by="priority", query='assignee = null')

        # Create a new issue of kind 'enhancement' and priority 'minor'
        r.issues.create("New idea", "How about this", kind="enhancement", priority="minor")

        # Update the 'priority' field of the issue 42
        r.issues.get(42).priority = "blocker"

        # Mark issue 42 as resolved
        r.issues.get(42).state = "resolved"

        # Get information about issue 1
        i = r.issues.get(1)

        # Delete issue 123
        r.issues.get(123).delete()

    # or function oriented:
        # Get all tracked issues
        bitbucket.get_issues(workspace, repository)

        # Get all unassigned issues and sort them by priority
        bitbucket.get_issues(workspace, repository, sort_by="priority", query='assignee = null')

        # Create a new issue
        bitbucket.create_issue(workspace, repository, "The title", "The description")

        # Create a new issue of kind 'enhancement' and priority 'minor'
        bitbucket.create_issue(workspace, repository, "New idea", "How about this", kind="enhancement", priority="minor")

        # Update the 'priority' field of the issue 42
        bitbucket.update_issue(workspace, repository, 42, priority="blocker")

        # Mark issue 42 as resolved
        bitbucket.update_issue(workspace, repository, 42, state="resolved")

        # Get information about issue 1
        bitbucket.get_issue(workspace, repository, 1)

        # Delete issue 123
        bitbucket.delete_issue(workspace, repository, 123)
