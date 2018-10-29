Bitbucket module
================

Manage projects
---------------

.. code-block:: python

    # Project list
    bitbucket.project_list()

    # Project info
    bitbucket.project(key)

    # Get users who has permission in project
    bitbucket.project_users(key, limit=99999)

    # Get project administrators for project
    butbucket.project_users_with_administrator_permissions(key)

    # Get Project Groups
    bitbucket.project_groups(key, limit=99999)

    # Get groups with admin permissions
    bitbucket.project_groups_with_administrator_permissions(key)

    # Project summary
    butbucket.project_summary(key)

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

    # Get branches from repo
    bitbucket.get_branches(project, repository, filter='', limit=99999, details=True)

    # Delete branch from related repo
    bitbucket.delete_branch(project, repository, name, end_point)

    # Get pull requests
    bitbucket.get_pull_requests(project, repository, state='OPEN', order='newest', limit=100, start=0)

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