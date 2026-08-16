Crowd module
============

API reference
-------------

.. autoclass:: atlassian.crowd.Crowd
   :members:
   :undoc-members:

Manage users
------------

.. code-block:: python

    # Activate user
    crowd.user_activate(username)

    # Add user
    crowd.user_create(username, active, first_name, last_name, display_name, email, password)

    # Deactivate user
    crowd.user_deactivate(username)

    # Delete user
    crowd.user_delete(username)

    # Get user
    crowd.user(username)

    # Get user's all group info
    crowd.user_groups(username, kind='direct')

    # Check whether the user is a member of the group
    crowd.is_user_in_group(username, group, kind='direct')

    crowd.user_update(username, {"name": username, "email": "ada@example.com", "active": True})
    crowd.user_update_password(username, "new-password")
    crowd.user_store_attributes(username, {"attributes": []})
    crowd.nested_user_groups(username)
    crowd.group_remove_user(username, groupname)

Manage groups
-------------

.. code-block:: python

    # Add user to group
    crowd.group_add_user(username, groupname)

    # Get group's members
    crowd.group_members(group, kind='direct', max_results=99999)

    # Create new group method
    crowd.group_create(groupname, description, active=True)

    crowd.group(groupname)
    crowd.group_update(groupname, {"name": groupname, "active": True})
    crowd.group_store_attributes(groupname, {"attributes": []})
    crowd.nested_group_members(groupname)
    crowd.group_delete(groupname)

Get memberships
----------------

.. code-block:: python

    # Retrieves full details of all group memberships.
    # Return data structure:
    # {
    #     GroupName1<str>: [ Member1<str>, Member2<str>, ... ],
    #     GroupName2<str>: [ MemberA<str>, MemberB<str>, ... ],
    #     ...
    # }
    crowd.memberships

Healthcheck
-------------

.. code-block:: python

    # Check if the Crowd server is reachable
    crowd.health_check()

    # Provide plugins info
    crowd.get_plugins_info()

    # Provide plugin info
    crowd.get_plugin_info(plugin_key)

    # Provide plugin license info
    crowd.get_plugin_license_info(plugin_key)

    # Provide plugin path for upload into Jira e.g. useful for auto deploy
    crowd.upload_plugin(plugin_path)

    # Delete plugin
    crowd.delete_plugin(plugin_key)

    # Check plugin manager status
    crowd.check_plugin_manager_status()

    # Update plugin license
    crowd.update_plugin_license(plugin_key, license_key)
