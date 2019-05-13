Bitbucket module
================

Manage projects
---------------

.. code-block:: python

    # Project list
    bitbucket.project_list()

    # Project info
    bitbucket.project(key)

    # Create project
    bitbucket.create_project(key, name, description="My pretty project")

    # Get users who has permission in project
    bitbucket.project_users(key, limit=99999, filter_str=None)

    # Get project administrators for project
    butbucket.project_users_with_administrator_permissions(key)

    # Get Project Groups
    bitbucket.project_groups(key, limit=99999, filter_str=None)

    # Get groups with admin permissions
    bitbucket.project_groups_with_administrator_permissions(key)

    # Project summary
    bitbucket.project_summary(key)

    # Grant project permission to an specific user
    bitbucket.project_grant_user_permissions(project_key, username, permission)

    # Grant project permission to an specific group
    bitbucket.project_grant_group_permissions(project_key, groupname, permission)

Manage repositories
---------------

.. code-block:: python

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

    bitbucket.repo_users(self, project_key, repo_key, limit=99999, filter_str=None)

    bitbucket.repo_groups(self, project_key, repo_key, limit=99999, filter_str=None)

    # Grant repository permission to an specific user
    bitbucket.repo_grant_user_permissions(project_key, repo_key, username, permission)

    # Grant repository permission to an specific group
    bitbucket.repo_grant_group_permissions(project_key, repo_key, groupname, permission)

Groups and admins
-----------------

.. code-block:: python

    # Get group of members
    bitbucket.group_members(group, limit=99999)

    # All project administrators
    bitbucket.all_project_administrators()

Manage code
-----------

.. code-block:: python

    # Get repositories list from project
    bitbucket.repo_list(project_key, limit=25)

    # Create a new repository.
    # Requires an existing project in which this repository will be created. The only parameters which will be used
    # are name and scmId.
    # The authenticated user must have PROJECT_ADMIN permission for the context project to call this resource.
    bitbucket.create_repo(project_key, repository, forkable=False, is_private=True):

    # Get branches from repo
    bitbucket.get_branches(project, repository, filter='', limit=99999, details=True)

    # Creates a branch using the information provided in the request.
    # The authenticated user must have REPO_WRITE permission for the context repository to call this resource.
    bitbucket.create_branch(project_key, repository, name, start_point, message)

    # Delete branch from related repo
    bitbucket.delete_branch(project, repository, name, end_point)

    # Get pull requests
    bitbucket.get_pull_requests(project, repository, state='OPEN', order='newest', limit=100, start=0)

    # Get pull request activities
    bitbucket.get_pull_requests_activities(self, project, repository, pull_request_id)

    # Get pull request changes
    bitbucket.get_pull_requests_changes(self, project, repository, pull_request_id)

    # Get pull request commits
    bitbucket.get_pull_requests_commits(self, project, repository, pull_request_id)

    # Add comment into pull request
    bitbucket.add_pull_request_comment(self, project, repository, pull_request_id, text)

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