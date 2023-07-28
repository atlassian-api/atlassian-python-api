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

Manage groups
-------------

.. code-block:: python

    # Add user to group
    crowd.group_add_user(username, groupname)

