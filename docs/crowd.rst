Crowd module
============

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

Manage groups
-------------

.. code-block:: python

    # Add user to group
    crowd.group_add_user(username, groupname)

    # Get group's members
    crowd.group_members(group, kind='direct', max_results=99999)

