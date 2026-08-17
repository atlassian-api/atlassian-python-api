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

    # Get user by name or by key
    crowd.user(username)
    crowd.user(key="557057:927441f1-cc92-4030-b633-8a2bbdf7136e")

    # Get user by the v2 OpenID URL
    crowd.user_by_openid("https://crowd.example.test/openidserver/users/ada")

    # Get user's all group info
    crowd.user_groups(username, kind='direct', groupname=None, start_index=0, max_results=99999)

    # Check whether the user is a member of the group
    crowd.is_user_in_group(username, group, kind='direct')

    crowd.user_update(username, {"name": username, "email": "ada@example.com", "active": True})
    crowd.user_update_password(username, "new-password")
    crowd.user_delete_password(username)
    crowd.user_attributes(username)
    crowd.user_store_attributes(username, {"attributes": []})
    crowd.user_remove_attribute(username, "attribute-name")
    crowd.nested_user_groups(username)
    crowd.group_remove_user(username, groupname)
    crowd.user_authenticate(username, "password")
    crowd.user_authentication_notify(username)
    crowd.user_request_password_reset(username)
    crowd.user_request_usernames_reminder("ada@example.com")
    crowd.user_rename(username, "new-username")
    crowd.user_expire_all_passwords(confirm=True)
    crowd.user_avatar(username, size=64)

Manage groups
-------------

.. code-block:: python

    # Add user to group
    crowd.group_add_user(username, groupname)

    # Get group's members
    crowd.group_members(group, kind='direct', username=None, start_index=0, max_results=99999)

    # Create new group method
    crowd.group_create(groupname, description, active=True)

    crowd.group(groupname)
    crowd.group_update(groupname, {"name": groupname, "active": True})
    crowd.group_attributes(groupname)
    crowd.group_store_attributes(groupname, {"attributes": []})
    crowd.group_remove_attribute(groupname, "attribute-name")
    crowd.nested_group_members(groupname)
    crowd.group_delete(groupname)
    crowd.group_child_groups(groupname)
    crowd.nested_group_child_groups(groupname)
    crowd.group_add_child_group(groupname, "child-group")
    crowd.group_remove_child_group(groupname, "child-group")
    crowd.group_parent_groups(groupname)
    crowd.nested_group_parent_groups(groupname)
    crowd.group_add_parent_group(groupname, "parent-group")

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

Manage sessions
---------------

.. code-block:: python

    # Create/authenticate a session
    crowd.session_create(username, password, validate_password=True, duration=None)

    # Validate a session token
    crowd.session_validate(token, validation_factors=None)

    # Get session info
    crowd.session_get(token)

    # Invalidate a session token
    crowd.session_delete(token)

    # Delete all tokens for a user
    crowd.session_delete_user_tokens(username, exclude=None)

Search
------

.. code-block:: python

    # Search by CQL (GET)
    crowd.search_cql("user", "email == 'ada@example.com'")

    # Search with a restriction body (POST)
    crowd.search("user", {"restriction-type": "property-search-restriction", "property": {"name": "email", "type": "STRING", "value": "ada@example.com"}})

Configuration
-------------

.. code-block:: python

    # Get cookie configuration
    crowd.get_cookie_config()

Account
-------

.. code-block:: python

    crowd.account_change_password(username, "old-password", "new-password")
    crowd.account_forgotten_password(username)
    crowd.account_forgotten_username("ada@example.com")
    crowd.account_reset_password(username, "reset-token", "new-password")
    crowd.account_validate_token(username, "reset-token")

Directory management
--------------------

.. code-block:: python

    crowd.directory_test_azure_ad({"tenantId": "..."})
    crowd.directory_test_crowd({"url": "https://crowd.example.test"})
    crowd.directory_test_ldap({"url": "ldaps://ldap.example.test"})
    crowd.directory_test_ldap_search({"baseDN": "dc=example,dc=com"})

Application management
----------------------

.. code-block:: python

    crowd.get_applications(name="confluence")
    crowd.create_application({"name": "confluence"})
    crowd.get_application("application-id")
    crowd.update_application("application-id", {"name": "confluence"})
    crowd.delete_application("application-id")
    crowd.get_remote_addresses("application-id")
    crowd.add_remote_address("application-id", "192.168.1.1")
    crowd.remove_remote_address("application-id", "192.168.1.1")

    # Aliases
    crowd.user_aliases(username)
    crowd.set_user_aliases(username, {"app1": "alias1"})
    crowd.delete_user_aliases(username)
    crowd.get_alias("application-id", username)
    crowd.set_alias("application-id", username, "alias1")
    crowd.delete_alias("application-id", username)
    crowd.get_username_for_alias("application-id", "alias1")

Administration
--------------

.. code-block:: python

    # Applications and directories
    crowd.get_admin_applications(name="confluence")
    crowd.get_admin_application("application-id")
    crowd.update_admin_application("application-id", {"name": "confluence"})
    crowd.get_directory_mappings("application-id")
    crowd.add_directory_mapping("application-id", {"directoryId": "dir1"})
    crowd.get_directory_mapping("application-id", "directory-id")
    crowd.update_directory_mapping("application-id", "directory-id", {"directoryId": "dir1"})
    crowd.delete_directory_mapping("application-id", "directory-id")
    crowd.move_directory_mapping("application-id", "directory-id", {"position": 1})
    crowd.get_access_based_synchronization("application-id")
    crowd.update_access_based_synchronization("application-id", {"filterType": "USER_ONLY_FILTERING"})
    crowd.get_email_scan_result("application-id")
    crowd.trigger_email_scan("application-id")

    # Directories
    crowd.get_detailed_directories(active=True)
    crowd.get_detailed_directory("directory-id")
    crowd.synchronize_directory("directory-id")
    crowd.get_managed_directories()

    # Groups and users
    crowd.search_directory_groups("directory-id", "engineer")
    crowd.get_admin_group_nested_groups("group-id")
    crowd.add_admin_group_nested_groups("group-id", {"groups": ["nested-group"]})
    crowd.get_admin_group_details("group-id")
    crowd.get_admin_group_members("group-id")
    crowd.add_users_to_admin_group("group-id", {"users": ["ada"]})
    crowd.remove_users_from_admin_group("group-id", {"users": ["ada"]})
    crowd.search_admin_group_user_suggestions("group-id", "ada")
    crowd.search_administered_groups({"name": "engineer"})
    crowd.search_admin_users({"name": "ada"})
    crowd.add_user_to_admin_group("user-id", {"groups": ["group-id"]})
    crowd.remove_user_from_admin_group("user-id", {"groups": ["group-id"]})

    # Group-level administrators
    crowd.get_group_administrators("group-id")
    crowd.add_group_administrators("group-id", {"users": ["ada"]})
    crowd.get_group_admin_candidates("group-id", "ada")
    crowd.remove_group_admin_user("group-id", "user-id")
    crowd.remove_group_admin_group("group-id", "admin-group-id")

    # Server and sessions
    crowd.get_server_info()
    crowd.get_application_sessions(search="confluence")
    crowd.get_user_sessions(directory_id="directory-id")
    crowd.expire_session("session-hash")

    # Licensing
    crowd.get_licensing_summary("application-id")
    crowd.get_licensed_directories("application-id")
    crowd.get_licensed_jira_types("application-id")
    crowd.search_licensed_users("application-id", {"name": "ada"})
    crowd.export_licensed_users("application-id", search="ada")

    # Backup
    crowd.get_backup_summary()
    crowd.get_backup_configuration()
    crowd.save_backup_configuration({"schedule": "daily"})
    crowd.create_backup()

    # Audit log
    crowd.get_audit_log_configuration()
    crowd.set_audit_log_configuration({"enabled": True})
    crowd.add_audit_log_changeset({"author": "ada", "events": []})
    crowd.search_audit_log({"dateRange": {}})
    crowd.get_audit_log_filter_values(projection="EVENT_TYPE")

    # Look and feel
    crowd.get_look_and_feel_config()
    crowd.update_look_and_feel_config({"color": "#0052CC"})
    crowd.reset_look_and_feel_config()

    # Remember me
    crowd.get_remember_me_config()
    crowd.update_remember_me_config({"tokenValidityDays": 14})
    crowd.expire_all_remember_me_tokens()

    # SAML
    crowd.get_saml_config()
    crowd.get_saml_application_config("application-id")
    crowd.update_saml_application_config("application-id", {"enabled": True})
    crowd.parse_saml_metadata("<xml>...</xml>")
    crowd.parse_saml_metadata_file("/path/to/metadata.xml")
    crowd.reset_saml_certificates()
    crowd.get_saml_idp_metadata()
    crowd.find_saml_directory_mapping_mismatch("application-id")

    # Mail and LDAP
    crowd.save_mail_configuration({"host": "smtp.example.com"})
    crowd.test_mail_configuration({"host": "smtp.example.com"})
    crowd.validate_mail_configuration({"host": "smtp.example.com"})
    crowd.get_dynamic_ldap_pool_statistics()

    # Database encryption
    crowd.get_encryption_settings()
    crowd.set_default_encryptor({"key": "AES"})
    crowd.change_encryption_key()
    crowd.disable_encryption()

    # Console messages
    crowd.dismiss_message("message-key")

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
