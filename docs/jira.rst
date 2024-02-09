Jira module
===========

Get issues from jql search result with all related fields
---------------------------------------------------------

.. code-block:: python

    jql_request = 'project = DEMO AND status NOT IN (Closed, Resolved) ORDER BY issuekey'
    issues = jira.jql(jql_request)
    print(issues)

Reindex Jira
------------

.. code-block:: python

    # Reindexing Jira
    jira.reindex()

    # Reindex status
    jira.reindex_status()

    # Reindex type
    jira.reindex_with_type(indexing_type="BACKGROUND_PREFERRED")
    """
    FOREGROUND - runs a lock/full reindexing
    BACKGROUND - runs a background reindexing.
                 If JIRA fails to finish the background reindexing, respond with 409 Conflict (error message).
    BACKGROUND_PREFERRED  - If possible do a background reindexing.
                            If it's not possible (due to an inconsistent index), do a foreground reindexing.
    """

Manage Permissions
------------------

.. code-block:: python

    # Get permissions
    jira.permissions(permissions, project_id=None, project_key=None, issue_id=None, issue_key=None,)

    # Get all permissions
    jira.get_all_permissions()

Application properties
----------------------

.. code-block:: python

    # Get an application property
    jira.get_property(key=None, permission_level=None, key_filter=None)

    # Set an application property
    jira.set_property(property_id, value)

    # Returns the properties that are displayed on the "General Configuration > Advanced Settings" page.
    jira.get_advanced_settings()

Manage users
------------

.. code-block:: python

    # Get myself
    jira.myself()

    # Get user
    jira.user(account_id)

    # Remove user
    jira.user_remove(username)

    # Deactivate user. Works from 8.3.0 release
    jira.user_deactivate(username)

    # Get web sudo cookies using normal http request
    jira.user_get_websudo()

    # Fuzzy search using emailAddress or displayName
    jira.user_find_by_user_string(query="a.user@example.com", start=0, limit=50, include_inactive_users=False)
    jira.user_find_by_user_string(query="a.user", start=0, limit=50, include_inactive_users=False)
    jira.user_find_by_user_string(query="a user")
    jira.user_find_by_user_string(account_id="a-users-account-id")

    # Get groups of a user. This API is only available for Jira Cloud platform.
    jira.get_user_groups(account_id)

Manage groups
-------------

.. code-block:: python

    # Create a group
    jira.create_group(name)

    # Delete a group
    # If you delete a group and content is restricted to that group, the content will be hidden from all users
    # To prevent this, use this parameter to specify a different group to transfer the restrictions
    # (comments and worklogs only) to
    jira.remove_group(name, swap_group=None)

    # Get all users from group
    jira.get_all_users_from_group(group, include_inactive_users=False, start=0, limit=50)

    # Add given user to a group
    jira.add_user_to_group(username=None, group_name=None, account_id=None)

    # Remove given user from a group
    jira.remove_user_from_group(username=None, group_name=None, account_id=None)

Manage projects
---------------

.. code-block:: python

    # Get all projects
    # Returns all projects which are visible for the currently logged in user.
    jira.projects(included_archived=None, expand=None)

    # Get all project alternative call
    # Returns all projects which are visible for the currently logged in user.
    jira.get_all_projects(included_archived=None, expand=None)

    # Get all projects only for Jira Cloud
    # Returns all projects which are visible for the currently logged in user.
    jira.projects_from_cloud(included_archived=None, expand=None)

    # Get one page of projects
    # Returns a paginated list of projects visible for the currently logged in user.
    # Use the url formatting to get a specific page as shown here:
    # url = f"{self.resource_url("project/search")}?startAt={start_at}&maxResults={max_results}"
    # Defaults to the first page, which returns a nextPage url when available.
    jira.projects_paginated(included_archived=None, expand=None, url=None)

    # Get all projects only for Jira Server
    # Returns all projects which are visible for the currently logged in user.
    jira.projects_from_server(included_archived=None, expand=None)

    # Delete project
    jira.delete_project(key)

    # Archive Project
    jira.archive_project(key)

    # Get project
    jira.project(key, expand=None)

    # Get project info
    jira.get_project(key, expand=None)

    # Get project components using project key
    jira.get_project_components(key)

    # Get a full representation of a the specified project's versions
    jira.get_project_versions(key, expand=None)

    # Returns all versions for the specified project. Results are paginated.
    # Results can be ordered by the following fields: sequence, name, startDate, releaseDate.
    # Results can be filtered by the following fields: query, status.
    jira.get_project_versions_paginated(key, start=None, limit=None, order_by=None, expand=None, query=None, status=None)

    # Add missing version to project
    jira.add_version(key, project_id, version, is_archived=False, is_released=False)

    # Update an existing version
    jira.update_version(version, name=None, description=None, is_archived=None, is_released=None, start_date=None, release_date=None)

    # Get project leaders
    jira.project_leaders()

    # Get last project issuekey
    jira.get_project_issuekey_last(project)

    # Get all project issue keys.
    # JIRA Cloud API can return up to  100 results  in one API call.
    # If your project has more than 100 issues see following community discussion:
    # https://community.atlassian.com/t5/Jira-Software-questions/Is-there-a-limit-to-the-number-of-quot-items-quot-returned-from/qaq-p/1317195
    jira.get_project_issuekey_all(project)

    # Get project issues count
    jira.get_project_issues_count(project)

    # Get all project issues
    jira.get_all_project_issues(project, fields='*all', start=100, limit=500)

    # Get all assignable users for project
    jira.get_all_assignable_users_for_project(project_key, start=0, limit=50)

    # Update a project
    jira.update_project(project_key, data, expand='lead,description')

    # Get project permission scheme
    # Use 'expand' to get details (default is None)
    jira.get_project_permission_scheme(project_id_or_key, expand='permissions,user,group,projectRole,field,all')

    # Get the issue security scheme for project.
    # Returned if the user has the administrator permission or if the scheme is used in a project in which the
    # user has the administrative permission.
    # Use only_levels=True for get the only levels entries
    jira.get_project_issue_security_scheme(project_id_or_key, only_levels=False)

    # Resource for associating notification schemes and projects.
    # Gets a notification scheme associated with the project.
    # Follow the documentation of /notificationscheme/{id} resource for all details about returned value.
    # Use 'expand' to get details (default is None)  possible values are notificationSchemeEvents,user,group,projectRole,field,all
    jira.get_priority_scheme_of_project(project_key_or_id, expand=None)

    # Returns a list of active users who have browse permission for a project that matches the search string for username.
    # Using " " string (space) for username gives All the active users who have browse permission for a project
    jira.get_users_with_browse_permission_to_a_project(self, username, issue_key=None, project_key=None, start=0, limit=100)

Manage issues
-------------

.. code-block:: python

    # Get issue by key
    jira.issue(key)

    # Get issue field value
    jira.issue_field_value(key, field)

    # Update issue field
    fields = {'summary': 'New summary'}
    jira.update_issue_field(key, fields, notify_users=True)

    # Get existing custom fields or find by filter
    jira.get_custom_fields(self, search=None, start=1, limit=50):

    # Check issue exists
    jira.issue_exists(issue_key)

    # Check issue deleted
    jira.issue_deleted(issue_key)

    # Update issue
    jira.issue_update(issue_key, fields)

    # Assign issue to user
    jira.assign_issue(issue_key, account_id)

    # Create issue
    jira.issue_create(fields)

    # Issue create or update
    jira.issue_create_or_update(fields)

    # Get issue transitions
    jira.get_issue_transitions(issue_key)

    # Get status ID from name
    jira.get_status_id_from_name(status_name)

    # Get transition id to status name
    jira.get_transition_id_to_status_name(issue_key, status_name)

    # Transition issue
    jira.issue_transition(issue_key, status)

    # Set issue status
    jira.set_issue_status(issue_key, status_name, fields=None)

    # Set issue status by transition_id
    jira.set_issue_status_by_transition_id(issue_key, transition_id)

    # Get issue status
    jira.get_issue_status(issue_key)

    # Get Issue Link
    jira.get_issue_link(link_id)

    # Get Issue Edit Meta
    jira.issue_editmeta(issue_key)

    # Get issue create meta, deprecated on Cloud and from Jira 9.0
    jira.issue_createmeta(project, expand="projects.issuetypes.fields")

    # Get create metadata issue types for a project
    jira.issue_createmeta_issuetypes(project, start=None, limit=None)

    # Get create field metadata for a project and issue type id
    jira.issue_createmeta_fieldtypes(self, project, issue_type_id, start=None, limit=None)

    # Create Issue Link
    data = {
            "type": {"name": "Duplicate" },
            "inwardIssue": { "key": "HSP-1"},
            "outwardIssue": {"key": "MKY-1"},
            "comment": { "body": "Linked related issue!",
                         "visibility": { "type": "group", "value": "jira-software-users" }
            }
    }
    jira.create_issue_link(data)

    # Remove Issue Link
    jira.remove_issue_link(link_id)

    # Create or Update Issue Remote Links
    jira.create_or_update_issue_remote_links(issue_key, link_url, title, global_id=None, relationship=None, icon_url=None, icon_title=None, status_resolved=False)

    # Get Issue Remote Link by link ID
    jira.get_issue_remote_link_by_id(issue_key, link_id)

    # Update Issue Remote Link by link ID
    jira.update_issue_remote_link_by_id(issue_key, link_id, url, title, global_id=None, relationship=None)

    # Delete Issue Remote Links
    jira.delete_issue_remote_link_by_id(issue_key, link_id)

    # Export Issues to csv
    jira.csv(jql, all_fields=False)

    # Add watcher to an issue
    jira.issue_add_watcher(issue_key, user)

    # Remove watcher from an issue
    jira.issue_delete_watcher(issue_key, user)

    # Get watchers for an issue
    jira.issue_get_watchers(issue_key)

    # Archive an issue
    jira.issue_archive(issue_id_or_key)

    # Restore an issue
    jira.issue_restore(issue_id_or_key)

    # Add Comments
    jira.issue_add_comment(issue_id_or_key, "This is a sample comment string.")

    # Edit Comments
    jira.issue_edit_comment(issue_key, comment_id, comment, visibility=None, notify_users=True)

    # Issue Comments
    jira.issue_get_comments(issue_id_or_key)

    # Get issue comment by id
    jira.issue_get_comment(issue_id_or_key, comment_id)

    # Get comments over all issues by ids
    jira.issues_get_comments_by_id(comment_id, [comment_id...])

    # Get change history for an issue
    jira.get_issue_changelog(issue_key)

    # Get property keys from an issue
    jira.get_issue_property_keys(issue_key)

    # Set issue property
    data = { "Foo": "Bar" }
    jira.set_issue_property(issue_key, property_key, data)

    # Get issue property
    jira.get_issue_property(issue_key, property_key)

    # Delete issue property
    jira.delete_issue_property(issue_key, property_key)

    # Get worklog for an issue
    jira.issue_get_worklog(issue_key)

    # Create a new worklog entry for an issue
    # started is a date string in the format %Y-%m-%dT%H:%M:%S.000+0000%z
    jira.issue_worklog(issue_key, started, time_in_sec)

    # Scrap regex matches from issue description and comments:
    jira.scrap_regex_from_issue(issue_key, regex)


Epic Issues
-------------

*Uses the Jira Agile API*

.. code-block:: python

    # Move issues to backlog
    jira.move_issues_to_backlog(issue_keys)

    # Add issues to backlog
    jira.add_issues_to_backlog(issue_keys)

    # Get agile board by filter id
    jira.get_agile_board_by_filter_id(filter_id)

    # Issues within an Epic
    jira.epic_issues(epic_key)

    # Returns all epics from the board, for the given board Id.
    # This only includes epics that the user has permission to view.
    # Note, if the user does not have permission to view the board, no epics will be returned at all.
    jira.get_epics(board_id, done=False, start=0, limit=50, )

    # Returns all issues that belong to an epic on the board,
    # for the given epic Id and the board Id.
    # This only includes issues that the user has permission to view.
    # Issues returned from this resource include Agile fields, like sprint, closedSprints, flagged, and epic.
    # By default, the returned issues are ordered by rank.
    jira.get_issues_for_epic(board_id, epic_id, jql="", validate_query="", fields="*all", expand="", start=0, limit=50, )

Manage Boards
-------------

.. code-block:: python

   # Board
    # Creates a new board. Board name, type and filter Id is required.
    jira.create_agile_board(name, type, filter_id, location=None)

    # Returns all boards.
    # This only includes boards that the user has permission to view.
    jira.get_all_agile_boards(board_name=None, project_key=None, board_type=None, start=0, limit=50)

    # Delete agile board by id
    jira.delete_agile_board(board_id)

    # Get agile board by id
    jira.get_agile_board(board_id)

    # Get issues for backlog
    jira.get_issues_for_board(board_id, start_at=0, max_results=50, jql=None,
                              validate_query=True, fields=None, expand=None,
                              override_screen_security=None, override_editable_flag=None)

    # Get issues for board
    jira.get_issues_for_board(board_id, jql, fields="*all", start=0, limit=None, expand=None)

    # Get agile board configuration by board id
    jira.get_agile_board_configuration(board_id)

    # Gets a list of all the board properties
    jira.get_agile_board_properties(board_id)

    # Sets the value of the specified board's property.
    jira.set_agile_board_property(board_id, property_key)

    # Get Agile board property
    jira.get_agile_board_property(board_id, property_key)

    # Delete Agile board property
    jira.delete_agile_board_property(board_id, property_key)

    # Get Agile board refined velocity
    jira.get_agile_board_refined_velocity(board_id)

    # Set Agile board refined velocity
    jira.set_agile_board_refined_velocity(board_id, refined_velocity)

Manage Sprints
--------------

.. code-block:: python

    # Get all sprints from board
    jira.get_all_sprints_from_board(board_id, state=None, start=0, limit=50)

    # Get all issues for sprint in board
    jira.get_all_issues_for_sprint_in_board(board_id, state=None, start=0, limit=50)

    # Get all versions for sprint in board
    jira.get_all_versions_from_board(self, board_id, released="true", start=0, limit=50)

    # Create sprint
    jira.jira.create_sprint(sprint_name, origin_board_id,  start_datetime, end_datetime, goal)

    # Rename sprint
    jira.rename_sprint(sprint_id, name, start_date, end_date)

    # Add/Move Issues to sprint
    jira.add_issues_to_sprint(sprint_id, issues_list)


Manage dashboards
-----------------

.. code-block:: python

    # Get dashboard by ID
    jira.get_dashboard(dashboard_id)

Attachments actions
-------------------

.. code-block:: python

    # Add attachment to issue
    jira.add_attachment(issue_key, filename)

    # Add attachment (IO Object) to issue
    jira.add_attachment_object(issue_key, attachment)

    # Download attachments from the issue
    jira.download_attachments_from_issue(issue, path=None, cloud=True):

    # Get list of attachments ids from issue
    jira.get_attachments_ids_from_issue(issue_key)

Manage components
-----------------

.. code-block:: python

    # Get component
    jira.component(component_id)

    # Create component
    jira.create_component(component)

    # Update component
    jira.update_component(component, component_id)

    # Delete component
    jira.delete_component(component_id)

Upload Jira plugin
------------------

.. code-block:: python

    upload_plugin(plugin_path)

Issue link types
----------------
.. code-block:: python

    # Get Issue link types
    jira.get_issue_link_types():

    # Create Issue link types
    jira.create_issue_link_type(data):
    """Create a new issue link type.
        :param data:
                {
                    "name": "Duplicate",
                    "inward": "Duplicated by",
                    "outward": "Duplicates"
                }
    """

    # Get issue link type by id
    jira.get_issue_link_type(issue_link_type_id):

    # Delete issue link type
    jira.delete_issue_link_type(issue_link_type_id):

    # Update issue link type
    jira.update_issue_link_type(issue_link_type_id, data):

Issue security schemes
----------------------
.. code-block:: python

    # Get all security schemes.
    # Returned if the user has the administrator permission or if the scheme is used in a project in which the
    # user has the administrative permission.
    jira.get_issue_security_schemes()

    # Get issue security scheme.
    # Returned if the user has the administrator permission or if the scheme is used in a project in which the
    # user has the administrative permission.
    # Use only_levels=True for get the only levels entries
    jira.get_issue_security_scheme(scheme_id, only_levels=False)

Cluster methods (only for DC edition)
-------------------------------------
.. code-block:: python

    # Get all cluster nodes.
    jira.get_cluster_all_nodes()

    # Request current index from node (the request is processed asynchronously).
    jira.request_current_index_from_node(node_id)

TEMPO
----------------------
.. code-block:: python

    # Find existing worklogs with the search parameters.
    # Look at the tempo docs for additional information:
    # https://www.tempo.io/server-api-documentation/timesheets#operation/searchWorklogs
    # NOTE: check if you are using correct types for the parameters!
    #     :param date_from: string From Date
    #     :param date_to: string To Date
    #     :param worker: Array of strings
    #     :param taskId: Array of integers
    #     :param taskKey: Array of strings
    #     :param projectId: Array of integers
    #     :param projectKey: Array of strings
    #     :param teamId: Array of integers
    #     :param roleId: Array of integers
    #     :param accountId: Array of integers
    #     :param accountKey: Array of strings
    #     :param filterId: Array of integers
    #     :param customerId: Array of integers
    #     :param categoryId: Array of integers
    #     :param categoryTypeId: Array of integers
    #     :param epicKey: Array of strings
    #     :param updatedFrom: string
    #     :param includeSubtasks: boolean
    #     :param pageNo: integer
    #     :param maxResults: integer
    #     :param offset: integer
    jira.tempo_4_timesheets_find_worklogs(date_from=None, date_to=None, **params)

    # :PRIVATE:
    # Get Tempo timesheet worklog by issue key or id.
    jira.tempo_timesheets_get_worklogs_by_issue(issue)
