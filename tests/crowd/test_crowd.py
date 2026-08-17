from unittest.mock import patch

from atlassian.crowd import Crowd


@patch.object(Crowd, "delete")
@patch.object(Crowd, "get")
@patch.object(Crowd, "put")
def test_crowd_user_group_and_attribute_helpers(mock_put, mock_get, mock_delete):
    crowd = Crowd("https://crowd.example.test", "application", "password")
    mock_get.return_value = {"users": [{"name": "ada"}]}

    assert crowd.nested_group_members("engineering") == ["ada"]
    crowd.group_remove_user("ada", "engineering")
    crowd.user_update_password("ada", "new-secret")
    crowd.group_store_attributes("engineering", {"attributes": []})

    assert mock_delete.call_args_list[0].kwargs["params"] == {"username": "ada", "groupname": "engineering"}
    assert mock_put.call_args_list[0].kwargs["data"] == {"value": "new-secret"}
    assert mock_put.call_args_list[1].kwargs["params"] == {"groupname": "engineering"}


@patch.object(Crowd, "post")
def test_group_add_user_sends_group_in_query_and_username_in_body(mock_post):
    crowd = Crowd("https://crowd.example.test", "application", "password")

    crowd.group_add_user("ada", "engineering")

    assert mock_post.call_args.kwargs["params"] == {"groupname": "engineering"}
    assert mock_post.call_args.kwargs["data"] == {"name": "ada"}
    assert mock_post.call_args.args[0].endswith("usermanagement/latest/user/group/direct")


@patch.object(Crowd, "get")
def test_group_child_groups_search_extracts_names(mock_get):
    crowd = Crowd("https://crowd.example.test", "application", "password")
    mock_get.return_value = {"groups": [{"name": "child"}]}

    assert crowd.group_child_groups("parent") == ["child"]
    assert mock_get.call_args.args[0].endswith("usermanagement/latest/group/child-group/direct")
    assert mock_get.call_args.kwargs["params"]["groupname"] == "parent"


@patch.object(Crowd, "post")
@patch.object(Crowd, "delete")
def test_group_child_group_membership_modify_methods(mock_delete, mock_post):
    crowd = Crowd("https://crowd.example.test", "application", "password")

    crowd.group_add_child_group("parent", "child")
    crowd.group_remove_child_group("parent", "child")

    assert mock_post.call_args.kwargs["params"] == {"groupname": "parent"}
    assert mock_post.call_args.kwargs["data"] == {"name": "child"}
    assert mock_delete.call_args.kwargs["params"] == {"groupname": "parent", "child-groupname": "child"}


@patch.object(Crowd, "get")
@patch.object(Crowd, "post")
@patch.object(Crowd, "delete")
def test_group_parent_group_membership_modify_methods(mock_delete, mock_post, mock_get):
    crowd = Crowd("https://crowd.example.test", "application", "password")
    mock_get.return_value = {"groups": [{"name": "parent"}]}

    crowd.group_add_parent_group("child", "parent")
    assert mock_post.call_args.kwargs["params"] == {"groupname": "child"}
    assert mock_post.call_args.kwargs["data"] == {"name": "parent"}

    assert crowd.group_parent_groups("child") == ["parent"]
    assert mock_get.call_args.args[0].endswith("usermanagement/latest/group/parent-group/direct")
    assert mock_delete.call_args is None


@patch.object(Crowd, "post")
@patch.object(Crowd, "get")
@patch.object(Crowd, "delete")
def test_session_management_methods(mock_delete, mock_get, mock_post):
    crowd = Crowd("https://crowd.example.test", "application", "password")
    mock_post.return_value = {"token": "abc123"}

    crowd.session_create("ada", "secret")
    assert mock_post.call_args.args[0].endswith("usermanagement/latest/session")
    assert mock_post.call_args.kwargs["params"] == {"validate-password": "true"}
    assert mock_post.call_args.kwargs["data"] == {"userName": "ada", "password": "secret"}

    crowd.session_validate("abc123", {"validationFactors": []})
    assert mock_post.call_args.args[0].endswith("usermanagement/latest/session/abc123")
    assert mock_post.call_args.kwargs["data"] == {"validationFactors": []}

    crowd.session_get("abc123")
    assert mock_get.call_args.args[0].endswith("usermanagement/latest/session/abc123")

    crowd.session_delete("abc123")
    assert mock_delete.call_args.args[0].endswith("usermanagement/latest/session/abc123")

    crowd.session_delete_user_tokens("ada", exclude="abc123")
    assert mock_delete.call_args.args[0].endswith("usermanagement/latest/session")
    assert mock_delete.call_args.kwargs["params"] == {"username": "ada", "exclude": "abc123"}


@patch.object(Crowd, "post")
@patch.object(Crowd, "get")
def test_search_methods(mock_get, mock_post):
    crowd = Crowd("https://crowd.example.test", "application", "password")

    crowd.search_cql("user", "email == 'ada@example.com'")
    assert mock_get.call_args.args[0].endswith("usermanagement/latest/search")
    assert mock_get.call_args.kwargs["params"]["entity-type"] == "user"
    assert mock_get.call_args.kwargs["params"]["restriction"] == "email == 'ada@example.com'"

    crowd.search("user", {"restriction-type": "property-search-restriction"})
    assert mock_post.call_args.args[0].endswith("usermanagement/latest/search")
    assert mock_post.call_args.kwargs["params"]["entity-type"] == "user"
    assert mock_post.call_args.kwargs["data"] == {"restriction-type": "property-search-restriction"}


@patch.object(Crowd, "post")
def test_user_authentication_and_notification_methods(mock_post):
    crowd = Crowd("https://crowd.example.test", "application", "password")

    crowd.user_authenticate("ada", "secret")
    assert mock_post.call_args.args[0].endswith("usermanagement/latest/authentication")
    assert mock_post.call_args.kwargs["params"] == {"username": "ada"}
    assert mock_post.call_args.kwargs["data"] == {"value": "secret"}

    crowd.user_authentication_notify("ada")
    assert mock_post.call_args.args[0].endswith("usermanagement/latest/authentication/notify")
    assert mock_post.call_args.kwargs["params"] == {"username": "ada"}


@patch.object(Crowd, "post")
@patch.object(Crowd, "delete")
@patch.object(Crowd, "get")
def test_user_password_and_reminder_methods(mock_get, mock_delete, mock_post):
    crowd = Crowd("https://crowd.example.test", "application", "password")

    crowd.user_delete_password("ada")
    assert mock_delete.call_args.args[0].endswith("usermanagement/latest/user/password")
    assert mock_delete.call_args.kwargs["params"] == {"username": "ada"}

    crowd.user_request_password_reset("ada")
    assert mock_post.call_args.args[0].endswith("usermanagement/latest/user/mail/password")
    assert mock_post.call_args.kwargs["params"] == {"username": "ada"}

    crowd.user_request_usernames_reminder("ada@example.com")
    assert mock_post.call_args.args[0].endswith("usermanagement/latest/user/mail/usernames")
    assert mock_post.call_args.kwargs["params"] == {"email": "ada@example.com"}

    crowd.user_rename("ada", "ada2")
    assert mock_post.call_args.args[0].endswith("usermanagement/latest/user/rename")
    assert mock_post.call_args.kwargs["params"] == {"username": "ada"}
    assert mock_post.call_args.kwargs["data"] == {"newName": "ada2"}

    crowd.user_expire_all_passwords()
    assert mock_post.call_args.args[0].endswith("usermanagement/latest/user/expire-all-passwords")
    assert mock_post.call_args.kwargs["params"] == {"confirm": "true"}

    crowd.user_avatar("ada", size=64)
    assert mock_get.call_args.args[0].endswith("usermanagement/latest/user/avatar")
    assert mock_get.call_args.kwargs["params"] == {"username": "ada", "s": 64}

    crowd.get_cookie_config()
    assert mock_get.call_args.args[0].endswith("usermanagement/latest/config/cookie")


@patch.object(Crowd, "post")
def test_account_methods(mock_post):
    crowd = Crowd("https://crowd.example.test", "application", "password")

    crowd.account_change_password("ada", "old", "new")
    assert mock_post.call_args.args[0].endswith("account/1/change-password")
    assert mock_post.call_args.kwargs["data"] == {"username": "ada", "oldPassword": "old", "newPassword": "new"}

    crowd.account_forgotten_password("ada")
    assert mock_post.call_args.args[0].endswith("account/1/forgotten-password")
    assert mock_post.call_args.kwargs["params"] == {"username": "ada"}

    crowd.account_forgotten_username("ada@example.com")
    assert mock_post.call_args.args[0].endswith("account/1/forgotten-username")
    assert mock_post.call_args.kwargs["params"] == {"email": "ada@example.com"}

    crowd.account_reset_password("ada", "token123", "new")
    assert mock_post.call_args.args[0].endswith("account/1/reset-password")
    assert mock_post.call_args.kwargs["data"] == {"username": "ada", "token": "token123", "password": "new"}

    crowd.account_validate_token("ada", "token123")
    assert mock_post.call_args.args[0].endswith("account/1/token-status")
    assert mock_post.call_args.kwargs["data"] == {"username": "ada", "token": "token123"}


@patch.object(Crowd, "post")
def test_directory_test_methods(mock_post):
    crowd = Crowd("https://crowd.example.test", "application", "password")
    config = {"url": "https://ldap.example.test"}

    crowd.directory_test_azure_ad(config)
    assert mock_post.call_args.args[0].endswith("rest/directorymanagement/1/directory/testazuread")

    crowd.directory_test_crowd(config)
    assert mock_post.call_args.args[0].endswith("rest/directorymanagement/1/directory/testcrowd")

    crowd.directory_test_ldap(config, directory_id=1)
    assert mock_post.call_args.args[0].endswith("rest/directorymanagement/1/directory/testldap/1")

    crowd.directory_test_ldap_search(config)
    assert mock_post.call_args.args[0].endswith("rest/directorymanagement/1/directory/testsearch")
    assert mock_post.call_args.kwargs["data"] == config


@patch.object(Crowd, "get")
@patch.object(Crowd, "post")
@patch.object(Crowd, "put")
@patch.object(Crowd, "delete")
def test_application_management_methods(mock_delete, mock_put, mock_post, mock_get):
    crowd = Crowd("https://crowd.example.test", "application", "password")
    mock_get.return_value = {"applications": []}

    crowd.user_aliases("ada")
    assert mock_get.call_args.args[0].endswith("appmanagement/1/aliases")
    assert mock_get.call_args.kwargs["params"] == {"user": "ada"}

    crowd.set_user_aliases("ada", {"app1": "alias1"})
    assert mock_put.call_args.args[0].endswith("appmanagement/1/aliases")
    assert mock_put.call_args.kwargs["params"] == {"user": "ada"}
    assert mock_put.call_args.kwargs["data"] == {"app1": "alias1"}

    crowd.delete_user_aliases("ada")
    assert mock_delete.call_args.args[0].endswith("appmanagement/1/aliases")
    assert mock_delete.call_args.kwargs["params"] == {"user": "ada"}

    crowd.get_alias("app1", "ada")
    assert mock_get.call_args.args[0].endswith("appmanagement/1/aliases/app1/alias")
    assert mock_get.call_args.kwargs["params"] == {"user": "ada"}

    crowd.set_alias("app1", "ada", "alias1")
    assert mock_put.call_args.args[0].endswith("appmanagement/1/aliases/app1/alias")
    assert mock_put.call_args.kwargs["params"] == {"user": "ada"}
    assert mock_put.call_args.kwargs["data"] == "alias1"
    assert mock_put.call_args.kwargs["headers"] == {"Content-Type": "text/plain"}

    crowd.delete_alias("app1", "ada")
    assert mock_delete.call_args.args[0].endswith("appmanagement/1/aliases/app1/alias")

    crowd.get_username_for_alias("app1", "alias1")
    assert mock_get.call_args.args[0].endswith("appmanagement/1/aliases/app1/username")
    assert mock_get.call_args.kwargs["params"] == {"alias": "alias1"}

    crowd.get_applications(name="confluence")
    assert mock_get.call_args.args[0].endswith("appmanagement/1/application")
    assert mock_get.call_args.kwargs["params"] == {"name": "confluence"}

    crowd.create_application({"name": "confluence"})
    assert mock_post.call_args.args[0].endswith("appmanagement/1/application")
    assert mock_post.call_args.kwargs["data"] == {"name": "confluence"}

    crowd.get_application("app1")
    assert mock_get.call_args.args[0].endswith("appmanagement/1/application/app1")

    crowd.update_application("app1", {"name": "confluence"})
    assert mock_put.call_args.args[0].endswith("appmanagement/1/application/app1")
    assert mock_put.call_args.kwargs["data"] == {"name": "confluence"}

    crowd.delete_application("app1")
    assert mock_delete.call_args.args[0].endswith("appmanagement/1/application/app1")

    crowd.get_remote_addresses("app1")
    assert mock_get.call_args.args[0].endswith("appmanagement/1/application/app1/remote_address")

    crowd.add_remote_address("app1", "192.168.1.1")
    assert mock_post.call_args.args[0].endswith("appmanagement/1/application/app1/remote_address")
    assert mock_post.call_args.kwargs["data"] == {"value": "192.168.1.1"}

    crowd.remove_remote_address("app1", "192.168.1.1")
    assert mock_delete.call_args.args[0].endswith("appmanagement/1/application/app1/remote_address")
    assert mock_delete.call_args.kwargs["params"] == {"address": "192.168.1.1"}


@patch.object(Crowd, "get")
def test_admin_application_and_directory_methods(mock_get):
    crowd = Crowd("https://crowd.example.test", "application", "password")

    crowd.get_admin_applications(name="confluence")
    assert mock_get.call_args.args[0].endswith("admin/1.0/application")
    assert mock_get.call_args.kwargs["params"] == {"start": 0, "limit": 99999, "name": "confluence"}

    crowd.get_admin_application("app1")
    assert mock_get.call_args.args[0].endswith("admin/1.0/application/app1")

    crowd.get_directory_mappings("app1")
    assert mock_get.call_args.args[0].endswith("admin/1.0/application/app1/directory-mapping")

    crowd.get_detailed_directories(active=True)
    assert mock_get.call_args.args[0].endswith("admin/1.0/directory/detailed")

    crowd.get_detailed_directory("dir1")
    assert mock_get.call_args.args[0].endswith("admin/1.0/directory/detailed/dir1")

    crowd.get_managed_directories()
    assert mock_get.call_args.args[0].endswith("admin/1.0/directory/managed")

    crowd.get_server_info()
    assert mock_get.call_args.args[0].endswith("admin/1.0/server-info")


@patch.object(Crowd, "post")
@patch.object(Crowd, "get")
def test_admin_session_and_licensing_methods(mock_get, mock_post):
    crowd = Crowd("https://crowd.example.test", "application", "password")

    crowd.get_application_sessions(search="confluence")
    assert mock_get.call_args.args[0].endswith("admin/1.0/sessions/application")
    assert mock_get.call_args.kwargs["params"]["search"] == "confluence"

    crowd.get_user_sessions(directory_id="dir1")
    assert mock_get.call_args.args[0].endswith("admin/1.0/sessions/user")
    assert mock_get.call_args.kwargs["params"]["directoryId"] == "dir1"

    crowd.get_licensing_summary("app1")
    assert mock_get.call_args.args[0].endswith("admin/1.0/licensing/app1/summary")

    crowd.search_licensed_users("app1", {"query": "ada"})
    assert mock_post.call_args.args[0].endswith("admin/1.0/licensing/app1/licensed-users/search")


@patch.object(Crowd, "post")
@patch.object(Crowd, "put")
@patch.object(Crowd, "delete")
def test_admin_modify_methods(mock_delete, mock_put, mock_post):
    crowd = Crowd("https://crowd.example.test", "application", "password")

    crowd.update_admin_application("app1", {"name": "confluence"})
    assert mock_put.call_args.args[0].endswith("admin/1.0/application/app1")
    assert mock_put.call_args.kwargs["data"] == {"name": "confluence"}

    crowd.add_directory_mapping("app1", {"directoryId": "dir1"})
    assert mock_post.call_args.args[0].endswith("admin/1.0/application/app1/directory-mapping")

    crowd.delete_directory_mapping("app1", "dir1")
    assert mock_delete.call_args.args[0].endswith("admin/1.0/application/app1/directory-mapping/dir1")

    crowd.synchronize_directory("dir1")
    assert mock_post.call_args.args[0].endswith("admin/1.0/directory/detailed/dir1/synchronize")

    crowd.add_group_administrators("group1", {"users": ["ada"]})
    assert mock_post.call_args.args[0].endswith("admin/1.0/group-level-admin/group1/admins")

    crowd.remove_group_admin_user("group1", "ada")
    assert mock_delete.call_args.args[0].endswith("admin/1.0/group-level-admin/group1/admins/users/ada")

    crowd.add_users_to_admin_group("group1", {"users": ["ada"]})
    assert mock_post.call_args.args[0].endswith("admin/1.0/groups/group1/users")

    crowd.remove_users_from_admin_group("group1", {"users": ["ada"]})
    assert mock_delete.call_args.args[0].endswith("admin/1.0/groups/group1/users")

    crowd.search_admin_users({"name": "ada"})
    assert mock_post.call_args.args[0].endswith("admin/1.0/users/search")

    crowd.expire_session("hash123")
    assert mock_delete.call_args.args[0].endswith("admin/1.0/sessions/hash123")

    crowd.create_backup()
    assert mock_post.call_args.args[0].endswith("admin/1.0/backup")

    crowd.save_backup_configuration({"schedule": "daily"})
    assert mock_post.call_args.args[0].endswith("admin/1.0/backup/configuration")

    crowd.update_look_and_feel_config({"color": "blue"})
    assert mock_put.call_args.args[0].endswith("admin/1.0/look-and-feel/config")

    crowd.expire_all_remember_me_tokens()
    assert mock_post.call_args.args[0].endswith("admin/1.0/remember-me/expire-all")

    crowd.reset_saml_certificates()
    assert mock_post.call_args.args[0].endswith("admin/1.0/samlconfig/reset-certificates")

    crowd.save_mail_configuration({"host": "smtp.example.com"})
    assert mock_post.call_args.args[0].endswith("admin/1.0/mail/configuration")


@patch.object(Crowd, "post")
@patch.object(Crowd, "get")
def test_admin_group_and_user_search_methods(mock_get, mock_post):
    crowd = Crowd("https://crowd.example.test", "application", "password")

    crowd.search_directory_groups("dir1", "engineer")
    assert mock_get.call_args.args[0].endswith("admin/1.0/group/search/dir1")
    assert mock_get.call_args.kwargs["params"]["term"] == "engineer"

    crowd.get_admin_group_details("group1")
    assert mock_get.call_args.args[0].endswith("admin/1.0/groups/group1")

    crowd.get_admin_group_members("group1")
    assert mock_get.call_args.args[0].endswith("admin/1.0/groups/group1/users")

    crowd.search_admin_group_user_suggestions("group1", "ada")
    assert mock_get.call_args.args[0].endswith("admin/1.0/groups/group1/users/suggestions")

    crowd.search_administered_groups({"name": "engineer"})
    assert mock_post.call_args.args[0].endswith("admin/1.0/groups/query")

    crowd.get_group_admin_candidates("group1")
    assert mock_get.call_args.args[0].endswith("admin/1.0/group-level-admin/group1/admins/suggestions")


@patch.object(Crowd, "get")
@patch.object(Crowd, "post")
def test_admin_saml_and_ldap_methods(mock_post, mock_get):
    crowd = Crowd("https://crowd.example.test", "application", "password")

    crowd.parse_saml_metadata("<xml/>")
    assert mock_post.call_args.args[0].endswith("admin/1.0/samlconfig/application/parse_metadata")
    assert mock_post.call_args.kwargs["headers"] == {"Content-Type": "application/octet-stream"}

    crowd.get_dynamic_ldap_pool_statistics()
    assert mock_get.call_args.args[0].endswith("admin/1.0/dynamic-ldap-pool-statistics")
