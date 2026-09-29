# coding=utf-8
"""
Test cases for Crowd API client.
"""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock, ANY

from atlassian.crowd import Crowd


class TestCrowdInit(unittest.TestCase):
    """Test cases for Crowd client initialization."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    def test_init_defaults(self):
        """Test Crowd client initialization with defaults."""
        crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )
        self.assertEqual(crowd.url, "https://crowd.example.com")
        self.assertEqual(crowd.username, "admin")
        self.assertEqual(crowd.password, "password")
        self.assertEqual(crowd.timeout, 60)
        self.assertEqual(crowd.api_root, "rest")
        self.assertEqual(crowd.api_version, "latest")

    def test_init_custom_values(self):
        """Test Crowd client with custom values."""
        crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
            timeout=30,
            api_root="api",
            api_version="1",
        )
        self.assertEqual(crowd.timeout, 30)
        self.assertEqual(crowd.api_root, "api")
        self.assertEqual(crowd.api_version, "1")


class TestCrowdUserManagement(unittest.TestCase):
    """Test cases for Crowd user management operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "get")
    def test_user(self, mock_get):
        """Test user method."""
        mock_get.return_value = {
            "name": "john",
            "display-name": "John Doe",
            "first-name": "John",
            "last-name": "Doe",
            "email": "john@example.com",
        }
        result = self.crowd.user("john")
        mock_get.assert_called_once_with(
            "/rest/usermanagement/latest/user",
            params={"username": "john"},
        )
        self.assertEqual(result["name"], "john")

    @patch.object(Crowd, "get")
    @patch.object(Crowd, "put")
    def test_user_activate(self, mock_put, mock_get):
        """Test user_activate method."""
        mock_get.return_value = {
            "name": "john",
            "display-name": "John Doe",
            "first-name": "John",
            "last-name": "Doe",
            "email": "john@example.com",
        }
        mock_put.return_value = {"name": "john", "active": True}
        result = self.crowd.user_activate("john")
        mock_put.assert_called_once()
        self.assertTrue(result["active"])

    @patch.object(Crowd, "get")
    @patch.object(Crowd, "put")
    def test_user_deactivate(self, mock_put, mock_get):
        """Test user_deactivate method."""
        mock_get.return_value = {
            "name": "john",
            "display-name": "John Doe",
            "first-name": "John",
            "last-name": "Doe",
            "email": "john@example.com",
        }
        mock_put.return_value = {"name": "john", "active": False}
        result = self.crowd.user_deactivate("john")
        mock_put.assert_called_once()
        self.assertFalse(result["active"])

    @patch.object(Crowd, "post")
    def test_user_create(self, mock_post):
        """Test user_create method."""
        mock_post.return_value = {"name": "john", "active": True}
        result = self.crowd.user_create(
            username="john",
            active=True,
            first_name="John",
            last_name="Doe",
            display_name="John Doe",
            email="john@example.com",
            password="secret123",
        )
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[1]["data"]["name"], "john")
        self.assertEqual(call_args[1]["data"]["password"]["value"], "secret123")
        self.assertEqual(result["name"], "john")

    @patch.object(Crowd, "delete")
    def test_user_delete(self, mock_delete):
        """Test user_delete method."""
        mock_delete.return_value = {}
        self.crowd.user_delete("john")
        mock_delete.assert_called_once_with(
            "/rest/usermanagement/latest/user",
            params={"username": "john"},
        )

    @patch.object(Crowd, "get")
    def test_user_groups(self, mock_get):
        """Test user_groups method."""
        mock_get.return_value = {"groups": [{"name": "group1"}, {"name": "group2"}]}
        result = self.crowd.user_groups("john")
        mock_get.assert_called_once()
        self.assertEqual(len(result), 2)
        self.assertIn("group1", result)

    @patch.object(Crowd, "get")
    def test_user_groups_nested(self, mock_get):
        """Test user_groups method with nested kind."""
        mock_get.return_value = {"groups": [{"name": "nested-group"}]}
        result = self.crowd.user_groups("john", kind="nested")
        mock_get.assert_called_once_with(
            "/rest/usermanagement/latest/user/group/nested",
            params={"username": "john"},
        )
        self.assertEqual(result, ["nested-group"])

    @patch.object(Crowd, "get")
    def test_group_members(self, mock_get):
        """Test group_members method."""
        mock_get.return_value = {"users": [{"name": "user1"}, {"name": "user2"}]}
        result = self.crowd.group_members("admins")
        mock_get.assert_called_once()
        self.assertEqual(len(result), 2)

    @patch.object(Crowd, "get")
    def test_is_user_in_group_true(self, mock_get):
        """Test is_user_in_group method when user is in group."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        result = self.crowd.is_user_in_group("john", "admins")
        mock_get.assert_called_once_with(
            "/rest/usermanagement/latest/group/user/direct",
            params={"username": "john", "groupname": "admins"},
            advanced_mode=True,
        )
        self.assertTrue(result)

    @patch.object(Crowd, "get")
    def test_is_user_in_group_false(self, mock_get):
        """Test is_user_in_group method when user is not in group."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        result = self.crowd.is_user_in_group("john", "admins")
        self.assertFalse(result)

    @patch.object(Crowd, "post")
    def test_group_add_user(self, mock_post):
        """Test group_add_user method."""
        mock_post.return_value = {}
        self.crowd.group_add_user("john", "admins")
        mock_post.assert_called_once_with(
            "/rest/usermanagement/latest/user/group/direct",
            params={"groupname": "admins"},
            data={"name": "john"},
        )

    @patch.object(Crowd, "delete")
    def test_group_remove_user(self, mock_delete):
        """Test group_remove_user method."""
        mock_delete.return_value = {}
        self.crowd.group_remove_user("john", "admins")
        mock_delete.assert_called_once_with(
            "/rest/usermanagement/latest/user/group/direct",
            params={"username": "john", "groupname": "admins"},
        )

    @patch.object(Crowd, "put")
    def test_user_update(self, mock_put):
        """Test user_update method."""
        mock_put.return_value = {"name": "john", "active": True}
        result = self.crowd.user_update("john", {"active": False})
        mock_put.assert_called_once_with(
            "/rest/usermanagement/latest/user",
            params={"username": "john"},
            data={"active": False},
        )
        self.assertEqual(result["name"], "john")

    @patch.object(Crowd, "put")
    def test_user_update_password(self, mock_put):
        """Test user_update_password method."""
        mock_put.return_value = {}
        self.crowd.user_update_password("john", "newpassword")
        mock_put.assert_called_once_with(
            "/rest/usermanagement/latest/user/password",
            params={"username": "john"},
            data={"value": "newpassword"},
        )

    @patch.object(Crowd, "get")
    def test_user_attributes(self, mock_get):
        """Test user_attributes method."""
        mock_get.return_value = {"email": "john@example.com", "department": "Engineering"}
        result = self.crowd.user_attributes("john")
        mock_get.assert_called_once_with(
            "/rest/usermanagement/latest/user/attribute",
            params={"username": "john"},
        )
        self.assertEqual(result["email"], "john@example.com")

    @patch.object(Crowd, "put")
    def test_user_store_attributes(self, mock_put):
        """Test user_store_attributes method."""
        mock_put.return_value = {}
        self.crowd.user_store_attributes("john", {"department": "Sales"})
        mock_put.assert_called_once_with(
            "/rest/usermanagement/latest/user/attribute",
            params={"username": "john"},
            data={"department": "Sales"},
        )

    @patch.object(Crowd, "delete")
    def test_user_remove_attribute(self, mock_delete):
        """Test user_remove_attribute method."""
        mock_delete.return_value = {}
        self.crowd.user_remove_attribute("john", "department")
        mock_delete.assert_called_once_with(
            "/rest/usermanagement/latest/user/attribute",
            params={"username": "john", "attributename": "department"},
        )

    @patch.object(Crowd, "delete")
    def test_user_delete_password(self, mock_delete):
        """Test user_delete_password method."""
        mock_delete.return_value = {}
        self.crowd.user_delete_password("john")
        mock_delete.assert_called_once_with(
            "/rest/usermanagement/latest/user/password",
            params={"username": "john"},
        )

    @patch.object(Crowd, "post")
    def test_user_request_password_reset(self, mock_post):
        """Test user_request_password_reset method."""
        mock_post.return_value = {}
        self.crowd.user_request_password_reset("john")
        mock_post.assert_called_once_with(
            "/rest/usermanagement/latest/user/mail/password",
            params={"username": "john"},
        )

    @patch.object(Crowd, "post")
    def test_user_request_usernames_reminder(self, mock_post):
        """Test user_request_usernames_reminder method."""
        mock_post.return_value = {}
        self.crowd.user_request_usernames_reminder("john@example.com")
        mock_post.assert_called_once_with(
            "/rest/usermanagement/latest/user/mail/usernames",
            params={"email": "john@example.com"},
        )

    @patch.object(Crowd, "post")
    def test_user_rename(self, mock_post):
        """Test user_rename method."""
        mock_post.return_value = {}
        self.crowd.user_rename("john", "jdoe")
        mock_post.assert_called_once_with(
            "/rest/usermanagement/latest/user/rename",
            params={"username": "john"},
            data={"newName": "jdoe"},
        )

    @patch.object(Crowd, "post")
    def test_user_expire_all_passwords(self, mock_post):
        """Test user_expire_all_passwords method."""
        mock_post.return_value = {}
        self.crowd.user_expire_all_passwords(confirm=True)
        mock_post.assert_called_once_with(
            "/rest/usermanagement/latest/user/expire-all-passwords",
            params={"confirm": "true"},
        )

    def test_user_expire_all_passwords_requires_confirmation(self):
        """Test user_expire_all_passwords refuses to run without explicit confirmation."""
        with self.assertRaises(ValueError):
            self.crowd.user_expire_all_passwords()
        with self.assertRaises(ValueError):
            self.crowd.user_expire_all_passwords(confirm=False)

    @patch.object(Crowd, "get")
    def test_user_avatar(self, mock_get):
        """Test user_avatar method returns raw image bytes."""
        mock_get.return_value = b"avatar-data"
        result = self.crowd.user_avatar("john")
        self.assertEqual(result, b"avatar-data")
        mock_get.assert_called_once_with(
            "/rest/usermanagement/latest/user/avatar",
            params={"username": "john"},
            not_json_response=True,
        )

    @patch.object(Crowd, "get")
    def test_user_avatar_with_size(self, mock_get):
        """Test user_avatar method with size parameter."""
        mock_get.return_value = b"avatar-data"
        result = self.crowd.user_avatar("john", size=64)
        self.assertEqual(result, b"avatar-data")
        mock_get.assert_called_once_with(
            "/rest/usermanagement/latest/user/avatar",
            params={"username": "john", "s": 64},
            not_json_response=True,
        )

    @patch.object(Crowd, "get")
    def test_get_cookie_config(self, mock_get):
        """Test get_cookie_config method."""
        mock_get.return_value = {"cookie-name": "crowd.token_key"}
        result = self.crowd.get_cookie_config()
        mock_get.assert_called_once_with("/rest/usermanagement/latest/config/cookie")
        self.assertEqual(result["cookie-name"], "crowd.token_key")

    @patch.object(Crowd, "post")
    def test_user_authenticate(self, mock_post):
        """Test user_authenticate method."""
        mock_post.return_value = {"name": "john", "authenticated": True}
        result = self.crowd.user_authenticate("john", "password")
        mock_post.assert_called_once_with(
            "/rest/usermanagement/latest/authentication",
            params={"username": "john"},
            data={"value": "password"},
        )
        self.assertTrue(result["authenticated"])

    @patch.object(Crowd, "post")
    def test_user_authentication_notify(self, mock_post):
        """Test user_authentication_notify method."""
        mock_post.return_value = {}
        self.crowd.user_authentication_notify("john")
        mock_post.assert_called_once_with(
            "/rest/usermanagement/latest/authentication/notify",
            params={"username": "john"},
        )

    @patch.object(Crowd, "get")
    def test_search_cql(self, mock_get):
        """Test search_cql method."""
        mock_get.return_value = [{"name": "user1"}, {"name": "user2"}]
        result = self.crowd.search_cql("USER", restriction="startIndex < 100")
        mock_get.assert_called_once()
        self.assertEqual(len(result), 2)

    @patch.object(Crowd, "post")
    def test_search(self, mock_post):
        """Test search method."""
        mock_post.return_value = [{"name": "user1"}]
        result = self.crowd.search("USER", restriction={"startIndex": 0})
        mock_post.assert_called_once()
        self.assertEqual(len(result), 1)

    @patch.object(Crowd, "post")
    def test_user_authenticate_via_post(self, mock_post):
        """Test user_authenticate method."""
        mock_post.return_value = {"name": "john", "authenticated": True}
        result = self.crowd.user_authenticate("john", "password")
        self.assertTrue(result["authenticated"])


class TestCrowdGroupManagement(unittest.TestCase):
    """Test cases for Crowd group management operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "get")
    def test_group(self, mock_get):
        """Test group method."""
        mock_get.return_value = {"name": "admins", "active": True}
        result = self.crowd.group("admins")
        mock_get.assert_called_once_with(
            "/rest/usermanagement/latest/group",
            params={"groupname": "admins"},
        )
        self.assertEqual(result["name"], "admins")

    @patch.object(Crowd, "put")
    def test_group_update(self, mock_put):
        """Test group_update method."""
        mock_put.return_value = {"name": "admins", "active": True}
        result = self.crowd.group_update("admins", {"description": "Admin group"})
        mock_put.assert_called_once_with(
            "/rest/usermanagement/latest/group",
            params={"groupname": "admins"},
            data={"description": "Admin group"},
        )
        self.assertEqual(result["name"], "admins")

    @patch.object(Crowd, "delete")
    def test_group_delete(self, mock_delete):
        """Test group_delete method."""
        mock_delete.return_value = {}
        self.crowd.group_delete("admins")
        mock_delete.assert_called_once_with(
            "/rest/usermanagement/latest/group",
            params={"groupname": "admins"},
        )

    @patch.object(Crowd, "get")
    def test_group_attributes(self, mock_get):
        """Test group_attributes method."""
        mock_get.return_value = {"description": "Admin group"}
        result = self.crowd.group_attributes("admins")
        mock_get.assert_called_once_with(
            "/rest/usermanagement/latest/group/attribute",
            params={"groupname": "admins"},
        )
        self.assertEqual(result["description"], "Admin group")

    @patch.object(Crowd, "put")
    def test_group_store_attributes(self, mock_put):
        """Test group_store_attributes method."""
        mock_put.return_value = {}
        self.crowd.group_store_attributes("admins", {"description": "Updated"})
        mock_put.assert_called_once_with(
            "/rest/usermanagement/latest/group/attribute",
            params={"groupname": "admins"},
            data={"description": "Updated"},
        )

    @patch.object(Crowd, "delete")
    def test_group_remove_attribute(self, mock_delete):
        """Test group_remove_attribute method."""
        mock_delete.return_value = {}
        self.crowd.group_remove_attribute("admins", "description")
        mock_delete.assert_called_once_with(
            "/rest/usermanagement/latest/group/attribute",
            params={"groupname": "admins", "attributename": "description"},
        )

    @patch.object(Crowd, "get")
    def test_nested_group_members(self, mock_get):
        """Test nested_group_members method."""
        mock_get.return_value = {"users": [{"name": "user1"}, {"name": "user2"}]}
        result = self.crowd.nested_group_members("admins")
        mock_get.assert_called_once_with(
            "/rest/usermanagement/latest/group/user/nested",
            params={"groupname": "admins", "max-results": 99999},
        )
        self.assertEqual(len(result), 2)

    @patch.object(Crowd, "get")
    def test_nested_user_groups(self, mock_get):
        """Test nested_user_groups method."""
        mock_get.return_value = {"groups": [{"name": "group1"}]}
        result = self.crowd.nested_user_groups("john")
        mock_get.assert_called_once_with(
            "/rest/usermanagement/latest/user/group/nested",
            params={"username": "john"},
        )
        self.assertEqual(result, ["group1"])

    @patch.object(Crowd, "get")
    def test_group_child_groups(self, mock_get):
        """Test group_child_groups method."""
        mock_get.return_value = {"groups": [{"name": "subgroup1"}]}
        result = self.crowd.group_child_groups("parent")
        mock_get.assert_called_once()
        self.assertEqual(result, ["subgroup1"])

    @patch.object(Crowd, "get")
    def test_nested_group_child_groups(self, mock_get):
        """Test nested_group_child_groups method."""
        mock_get.return_value = {"groups": [{"name": "nested-subgroup"}]}
        result = self.crowd.nested_group_child_groups("parent")
        mock_get.assert_called_once()
        self.assertEqual(result, ["nested-subgroup"])

    @patch.object(Crowd, "post")
    def test_group_add_child_group(self, mock_post):
        """Test group_add_child_group method."""
        mock_post.return_value = {}
        self.crowd.group_add_child_group("parent", "child")
        mock_post.assert_called_once_with(
            "/rest/usermanagement/latest/group/child-group/direct",
            params={"groupname": "parent"},
            data={"name": "child"},
        )

    @patch.object(Crowd, "delete")
    def test_group_remove_child_group(self, mock_delete):
        """Test group_remove_child_group method."""
        mock_delete.return_value = {}
        self.crowd.group_remove_child_group("parent", "child")
        mock_delete.assert_called_once_with(
            "/rest/usermanagement/latest/group/child-group/direct",
            params={"groupname": "parent", "child-groupname": "child"},
        )

    @patch.object(Crowd, "get")
    def test_group_parent_groups(self, mock_get):
        """Test group_parent_groups method."""
        mock_get.return_value = {"groups": [{"name": "parent1"}]}
        result = self.crowd.group_parent_groups("child")
        mock_get.assert_called_once()
        self.assertEqual(result, ["parent1"])

    @patch.object(Crowd, "get")
    def test_nested_group_parent_groups(self, mock_get):
        """Test nested_group_parent_groups method."""
        mock_get.return_value = {"groups": [{"name": "nested-parent"}]}
        result = self.crowd.nested_group_parent_groups("child")
        mock_get.assert_called_once()
        self.assertEqual(result, ["nested-parent"])

    @patch.object(Crowd, "post")
    def test_group_add_parent_group(self, mock_post):
        """Test group_add_parent_group method."""
        mock_post.return_value = {}
        self.crowd.group_add_parent_group("child", "parent")
        mock_post.assert_called_once_with(
            "/rest/usermanagement/latest/group/parent-group/direct",
            params={"groupname": "child"},
            data={"name": "parent"},
        )

    @patch.object(Crowd, "post")
    def test_group_create(self, mock_post):
        """Test group_create method."""
        mock_post.return_value = {"name": "newgroup", "active": True}
        result = self.crowd.group_create("newgroup", description="New group")
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[1]["data"]["name"], "newgroup")
        self.assertEqual(call_args[1]["data"]["description"], "New group")
        self.assertEqual(call_args[1]["data"]["type"], "GROUP")
        self.assertTrue(result["active"])


class TestCrowdSessionManagement(unittest.TestCase):
    """Test cases for Crowd session management operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "post")
    def test_session_create(self, mock_post):
        """Test session_create method."""
        mock_post.return_value = {"token": "session-token", "userName": "john"}
        result = self.crowd.session_create("john", "password")
        mock_post.assert_called_once()
        self.assertEqual(result["token"], "session-token")

    @patch.object(Crowd, "post")
    def test_session_create_with_duration(self, mock_post):
        """Test session_create method with duration."""
        mock_post.return_value = {"token": "session-token"}
        self.crowd.session_create("john", "password", duration=3600)
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[1]["params"]["duration"], 3600)

    @patch.object(Crowd, "post")
    def test_session_validate(self, mock_post):
        """Test session_validate method."""
        mock_post.return_value = {"valid": True}
        result = self.crowd.session_validate("session-token")
        mock_post.assert_called_once_with(
            "/rest/usermanagement/latest/session/session-token",
            data={},
        )
        self.assertTrue(result["valid"])

    @patch.object(Crowd, "post")
    def test_session_validate_with_factors(self, mock_post):
        """Test session_validate method with validation factors."""
        mock_post.return_value = {"valid": True}
        self.crowd.session_validate("session-token", validation_factors={"ipAddress": "192.168.1.1"})
        mock_post.assert_called_once_with(
            "/rest/usermanagement/latest/session/session-token",
            data={"ipAddress": "192.168.1.1"},
        )

    @patch.object(Crowd, "get")
    def test_session_get(self, mock_get):
        """Test session_get method."""
        mock_get.return_value = {"token": "session-token", "userName": "john"}
        result = self.crowd.session_get("session-token")
        mock_get.assert_called_once_with("/rest/usermanagement/latest/session/session-token")
        self.assertEqual(result["token"], "session-token")

    @patch.object(Crowd, "delete")
    def test_session_delete(self, mock_delete):
        """Test session_delete method."""
        mock_delete.return_value = {}
        self.crowd.session_delete("session-token")
        mock_delete.assert_called_once_with("/rest/usermanagement/latest/session/session-token")

    @patch.object(Crowd, "delete")
    def test_session_delete_user_tokens(self, mock_delete):
        """Test session_delete_user_tokens method."""
        mock_delete.return_value = {}
        self.crowd.session_delete_user_tokens("john")
        mock_delete.assert_called_once_with(
            "/rest/usermanagement/latest/session",
            params={"username": "john"},
        )

    @patch.object(Crowd, "delete")
    def test_session_delete_user_tokens_with_exclude(self, mock_delete):
        """Test session_delete_user_tokens method with exclude."""
        mock_delete.return_value = {}
        self.crowd.session_delete_user_tokens("john", exclude="session-token")
        mock_delete.assert_called_once_with(
            "/rest/usermanagement/latest/session",
            params={"username": "john", "exclude": "session-token"},
        )


class TestCrowdAccountManagement(unittest.TestCase):
    """Test cases for Crowd account management operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "post")
    def test_account_change_password(self, mock_post):
        """Test account_change_password method."""
        mock_post.return_value = {}
        self.crowd.account_change_password("john", "oldpass", "newpass")
        mock_post.assert_called_once_with(
            "/rest/account/1/change-password",
            data={"username": "john", "oldPassword": "oldpass", "newPassword": "newpass"},
        )

    @patch.object(Crowd, "post")
    def test_account_forgotten_password(self, mock_post):
        """Test account_forgotten_password method."""
        mock_post.return_value = {}
        self.crowd.account_forgotten_password("john")
        mock_post.assert_called_once_with(
            "/rest/account/1/forgotten-password",
            params={"username": "john"},
        )

    @patch.object(Crowd, "post")
    def test_account_forgotten_username(self, mock_post):
        """Test account_forgotten_username method."""
        mock_post.return_value = {}
        self.crowd.account_forgotten_username("john@example.com")
        mock_post.assert_called_once_with(
            "/rest/account/1/forgotten-username",
            params={"email": "john@example.com"},
        )

    @patch.object(Crowd, "post")
    def test_account_reset_password(self, mock_post):
        """Test account_reset_password method."""
        mock_post.return_value = {}
        self.crowd.account_reset_password("john", "token123", "newpass")
        mock_post.assert_called_once_with(
            "/rest/account/1/reset-password",
            data={"username": "john", "token": "token123", "password": "newpass"},
        )

    @patch.object(Crowd, "post")
    def test_account_reset_password_with_directory(self, mock_post):
        """Test account_reset_password method with directory_id."""
        mock_post.return_value = {}
        self.crowd.account_reset_password("john", "token123", "newpass", directory_id=1)
        mock_post.assert_called_once_with(
            "/rest/account/1/reset-password",
            data={"username": "john", "token": "token123", "password": "newpass", "directoryId": 1},
        )

    @patch.object(Crowd, "post")
    def test_account_validate_token(self, mock_post):
        """Test account_validate_token method."""
        mock_post.return_value = {"valid": True}
        result = self.crowd.account_validate_token("john", "token123")
        mock_post.assert_called_once_with(
            "/rest/account/1/token-status",
            data={"username": "john", "token": "token123"},
        )
        self.assertTrue(result["valid"])

    @patch.object(Crowd, "post")
    def test_account_validate_token_with_directory(self, mock_post):
        """Test account_validate_token method with directory_id."""
        self.crowd.account_validate_token("john", "token123", directory_id=2)
        mock_post.assert_called_once_with(
            "/rest/account/1/token-status",
            data={"username": "john", "token": "token123", "directoryId": 2},
        )


class TestCrowdApplicationManagement(unittest.TestCase):
    """Test cases for Crowd application management operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "get")
    def test_get_applications(self, mock_get):
        """Test get_applications method."""
        mock_get.return_value = [{"name": "app1"}, {"name": "app2"}]
        result = self.crowd.get_applications()
        mock_get.assert_called_once_with(
            "/rest/appmanagement/1/application",
            params={},
        )
        self.assertEqual(len(result), 2)

    @patch.object(Crowd, "get")
    def test_get_applications_with_name(self, mock_get):
        """Test get_applications method with name filter."""
        mock_get.return_value = [{"name": "app1"}]
        result = self.crowd.get_applications(name="app1")
        mock_get.assert_called_once_with(
            "/rest/appmanagement/1/application",
            params={"name": "app1"},
        )
        self.assertEqual(len(result), 1)

    @patch.object(Crowd, "post")
    def test_create_application(self, mock_post):
        """Test create_application method."""
        mock_post.return_value = {"id": "app1", "name": "New App"}
        result = self.crowd.create_application({"name": "New App"})
        mock_post.assert_called_once_with(
            "/rest/appmanagement/1/application",
            params={},
            data={"name": "New App"},
        )
        self.assertEqual(result["id"], "app1")

    @patch.object(Crowd, "post")
    def test_create_application_with_request_address(self, mock_post):
        """Test create_application method with include_request_address."""
        mock_post.return_value = {"id": "app1"}
        self.crowd.create_application({"name": "New App"}, include_request_address=True)
        mock_post.assert_called_once_with(
            "/rest/appmanagement/1/application",
            params={"include-request-address": True},
            data={"name": "New App"},
        )

    @patch.object(Crowd, "get")
    def test_get_application(self, mock_get):
        """Test get_application method."""
        mock_get.return_value = {"id": "app1", "name": "App 1"}
        result = self.crowd.get_application("app1")
        mock_get.assert_called_once_with("/rest/appmanagement/1/application/app1")
        self.assertEqual(result["id"], "app1")

    @patch.object(Crowd, "put")
    def test_update_application(self, mock_put):
        """Test update_application method."""
        mock_put.return_value = {"id": "app1", "name": "Updated App"}
        result = self.crowd.update_application("app1", {"name": "Updated App"})
        mock_put.assert_called_once_with(
            "/rest/appmanagement/1/application/app1",
            data={"name": "Updated App"},
        )
        self.assertEqual(result["name"], "Updated App")

    @patch.object(Crowd, "delete")
    def test_delete_application(self, mock_delete):
        """Test delete_application method."""
        mock_delete.return_value = {}
        self.crowd.delete_application("app1")
        mock_delete.assert_called_once_with("/rest/appmanagement/1/application/app1")

    @patch.object(Crowd, "get")
    def test_get_remote_addresses(self, mock_get):
        """Test get_remote_addresses method."""
        mock_get.return_value = [{"value": "192.168.1.1"}]
        result = self.crowd.get_remote_addresses("app1")
        mock_get.assert_called_once_with("/rest/appmanagement/1/application/app1/remote_address")
        self.assertEqual(len(result), 1)

    @patch.object(Crowd, "post")
    def test_add_remote_address_string(self, mock_post):
        """Test add_remote_address method with string address."""
        mock_post.return_value = {}
        self.crowd.add_remote_address("app1", "192.168.1.1")
        mock_post.assert_called_once_with(
            "/rest/appmanagement/1/application/app1/remote_address",
            data={"value": "192.168.1.1"},
        )

    @patch.object(Crowd, "post")
    def test_add_remote_address_dict(self, mock_post):
        """Test add_remote_address method with dict address."""
        mock_post.return_value = {}
        self.crowd.add_remote_address("app1", {"value": "192.168.1.1", "description": "Office"})
        mock_post.assert_called_once_with(
            "/rest/appmanagement/1/application/app1/remote_address",
            data={"value": "192.168.1.1", "description": "Office"},
        )

    @patch.object(Crowd, "delete")
    def test_remove_remote_address(self, mock_delete):
        """Test remove_remote_address method."""
        mock_delete.return_value = {}
        self.crowd.remove_remote_address("app1", "192.168.1.1")
        mock_delete.assert_called_once_with(
            "/rest/appmanagement/1/application/app1/remote_address",
            params={"address": "192.168.1.1"},
        )


class TestCrowdAdminOperations(unittest.TestCase):
    """Test cases for Crowd admin operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "get")
    def test_get_admin_applications(self, mock_get):
        """Test get_admin_applications method."""
        mock_get.return_value = [{"id": "app1", "name": "App 1"}]
        result = self.crowd.get_admin_applications()
        mock_get.assert_called_once_with("/rest/admin/1.0/application", params={"start": 0, "limit": 99999})
        self.assertEqual(len(result), 1)

    @patch.object(Crowd, "get")
    def test_get_admin_applications_with_filters(self, mock_get):
        """Test get_admin_applications method with filters."""
        mock_get.return_value = [{"id": "app1"}]
        self.crowd.get_admin_applications(name="app1", active=True)
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/application",
            params={"start": 0, "limit": 99999, "name": "app1", "active": True},
        )

    @patch.object(Crowd, "get")
    def test_get_admin_application(self, mock_get):
        """Test get_admin_application method."""
        mock_get.return_value = {"id": "app1", "name": "App 1"}
        result = self.crowd.get_admin_application("app1")
        mock_get.assert_called_once_with("/rest/admin/1.0/application/app1")
        self.assertEqual(result["id"], "app1")

    @patch.object(Crowd, "put")
    def test_update_admin_application(self, mock_put):
        """Test update_admin_application method."""
        mock_put.return_value = {"id": "app1", "name": "Updated"}
        result = self.crowd.update_admin_application("app1", {"name": "Updated"})
        mock_put.assert_called_once_with("/rest/admin/1.0/application/app1", data={"name": "Updated"})
        self.assertEqual(result["name"], "Updated")

    @patch.object(Crowd, "get")
    def test_get_access_based_synchronization(self, mock_get):
        """Test get_access_based_synchronization method."""
        mock_get.return_value = {"enabled": True}
        result = self.crowd.get_access_based_synchronization("app1")
        mock_get.assert_called_once_with("/rest/admin/1.0/application/app1/access-based-synchronization")
        self.assertTrue(result["enabled"])

    @patch.object(Crowd, "put")
    def test_update_access_based_synchronization(self, mock_put):
        """Test update_access_based_synchronization method."""
        mock_put.return_value = {"enabled": False}
        result = self.crowd.update_access_based_synchronization("app1", {"enabled": False})
        mock_put.assert_called_once_with(
            "/rest/admin/1.0/application/app1/access-based-synchronization",
            data={"enabled": False},
        )
        self.assertFalse(result["enabled"])


class TestCrowdDirectoryOperations(unittest.TestCase):
    """Test cases for Crowd directory operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "get")
    def test_get_detailed_directories(self, mock_get):
        """Test get_detailed_directories method."""
        mock_get.return_value = [{"id": "dir1", "name": "LDAP"}]
        result = self.crowd.get_detailed_directories()
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/directory/detailed",
            params={"start": 0, "limit": 99999},
        )
        self.assertEqual(len(result), 1)

    @patch.object(Crowd, "get")
    def test_get_detailed_directories_with_filters(self, mock_get):
        """Test get_detailed_directories method with filters."""
        mock_get.return_value = [{"id": "dir1"}]
        self.crowd.get_detailed_directories(search="ldap", active=True)
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/directory/detailed",
            params={"start": 0, "limit": 99999, "search": "ldap", "active": True},
        )

    @patch.object(Crowd, "get")
    def test_get_detailed_directory(self, mock_get):
        """Test get_detailed_directory method."""
        mock_get.return_value = {"id": "dir1", "name": "LDAP Directory"}
        result = self.crowd.get_detailed_directory("dir1")
        mock_get.assert_called_once_with("/rest/admin/1.0/directory/detailed/dir1")
        self.assertEqual(result["name"], "LDAP Directory")

    @patch.object(Crowd, "post")
    def test_synchronize_directory(self, mock_post):
        """Test synchronize_directory method."""
        mock_post.return_value = {}
        self.crowd.synchronize_directory("dir1")
        mock_post.assert_called_once_with("/rest/admin/1.0/directory/detailed/dir1/synchronize")

    @patch.object(Crowd, "get")
    def test_get_managed_directories(self, mock_get):
        """Test get_managed_directories method."""
        mock_get.return_value = [{"id": "dir1"}]
        self.crowd.get_managed_directories()
        mock_get.assert_called_once_with("/rest/admin/1.0/directory/managed", params={"start": 0, "limit": 99999})

    @patch.object(Crowd, "get")
    def test_search_directory_groups(self, mock_get):
        """Test search_directory_groups method."""
        mock_get.return_value = [{"name": "group1"}]
        result = self.crowd.search_directory_groups("dir1", "admin")
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/group/search/dir1",
            params={"term": "admin", "start": 0, "limit": 99999},
        )
        self.assertEqual(len(result), 1)


class TestCrowdPluginOperations(unittest.TestCase):
    """Test cases for Crowd plugin operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "get")
    def test_get_plugins_info(self, mock_get):
        """Test get_plugins_info method."""
        mock_response = MagicMock()
        mock_response.headers = {"upm-token": "token123"}
        mock_response.json.return_value = [{"key": "plugin1"}]
        mock_get.return_value = mock_response
        self.crowd.get_plugins_info()
        mock_get.assert_called_once_with(
            "rest/plugins/1.0/",
            headers=Crowd.no_check_headers,
            trailing=True,
        )

    @patch.object(Crowd, "get")
    def test_get_plugin_info(self, mock_get):
        """Test get_plugin_info method."""
        mock_get.return_value = {"key": "plugin1", "name": "Plugin 1"}
        result = self.crowd.get_plugin_info("plugin1")
        mock_get.assert_called_once_with(
            "rest/plugins/1.0/plugin1-key",
            headers=Crowd.no_check_headers,
            trailing=True,
        )
        self.assertEqual(result["key"], "plugin1")

    @patch.object(Crowd, "get")
    def test_get_plugin_license_info(self, mock_get):
        """Test get_plugin_license_info method."""
        mock_get.return_value = {"active": True}
        result = self.crowd.get_plugin_license_info("plugin1")
        mock_get.assert_called_once_with(
            "rest/plugins/1.0/plugin1-key/license",
            headers=Crowd.no_check_headers,
            trailing=True,
        )
        self.assertTrue(result["active"])


class TestCrowdUrlHelpers(unittest.TestCase):
    """Test cases for Crowd URL helper methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    def test_crowd_api_url_defaults(self):
        """Test _crowd_api_url with default version."""
        url = self.crowd._crowd_api_url("usermanagement", "user")
        self.assertEqual(url, "/rest/usermanagement/latest/user")

    def test_crowd_api_url_custom_version(self):
        """Test _crowd_api_url with custom version."""
        url = self.crowd._crowd_api_url("usermanagement", "user", api_version="1")
        self.assertEqual(url, "/rest/usermanagement/1/user")

    def test_admin_api_url(self):
        """Test _admin_api_url."""
        url = self.crowd._admin_api_url("application")
        self.assertEqual(url, "/rest/admin/1.0/application")


class TestCrowdDirectoryConnection(unittest.TestCase):
    """Test cases for directory connection test operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "post")
    def test_directory_test_azure_ad(self, mock_post):
        """Test directory_test_azure_ad method."""
        config = {"name": "azure", "tenantId": "tenant-1"}
        self.crowd.directory_test_azure_ad(config)
        mock_post.assert_called_once_with(
            "rest/directorymanagement/1/directory/testazuread",
            data=config,
        )

    @patch.object(Crowd, "post")
    def test_directory_test_azure_ad_with_directory_id(self, mock_post):
        """Test directory_test_azure_ad with a directory id."""
        config = {"name": "azure"}
        self.crowd.directory_test_azure_ad(config, directory_id=77)
        mock_post.assert_called_once_with(
            "rest/directorymanagement/1/directory/testazuread/77",
            data=config,
        )

    @patch.object(Crowd, "post")
    def test_directory_test_crowd(self, mock_post):
        """Test directory_test_crowd method."""
        config = {"url": "https://other-crowd.example.com"}
        self.crowd.directory_test_crowd(config)
        mock_post.assert_called_once_with(
            "rest/directorymanagement/1/directory/testcrowd",
            data=config,
        )

    @patch.object(Crowd, "post")
    def test_directory_test_crowd_with_directory_id(self, mock_post):
        """Test directory_test_crowd with a directory id."""
        config = {"url": "https://other-crowd.example.com"}
        self.crowd.directory_test_crowd(config, directory_id=12)
        mock_post.assert_called_once_with(
            "rest/directorymanagement/1/directory/testcrowd/12",
            data=config,
        )

    @patch.object(Crowd, "post")
    def test_directory_test_ldap(self, mock_post):
        """Test directory_test_ldap method."""
        config = {"url": "ldap://ldap.example.com"}
        self.crowd.directory_test_ldap(config)
        mock_post.assert_called_once_with(
            "rest/directorymanagement/1/directory/testldap",
            data=config,
        )

    @patch.object(Crowd, "post")
    def test_directory_test_ldap_with_directory_id(self, mock_post):
        """Test directory_test_ldap with a directory id."""
        config = {"url": "ldap://ldap.example.com"}
        self.crowd.directory_test_ldap(config, directory_id=33)
        mock_post.assert_called_once_with(
            "rest/directorymanagement/1/directory/testldap/33",
            data=config,
        )

    @patch.object(Crowd, "post")
    def test_directory_test_ldap_search(self, mock_post):
        """Test directory_test_ldap_search method."""
        config = {"baseDN": "dc=example,dc=com"}
        self.crowd.directory_test_ldap_search(config)
        mock_post.assert_called_once_with(
            "rest/directorymanagement/1/directory/testsearch",
            data=config,
        )

    @patch.object(Crowd, "post")
    def test_directory_test_ldap_search_with_directory_id(self, mock_post):
        """Test directory_test_ldap_search with a directory id."""
        config = {"baseDN": "dc=example,dc=com"}
        self.crowd.directory_test_ldap_search(config, directory_id=44)
        mock_post.assert_called_once_with(
            "rest/directorymanagement/1/directory/testsearch/44",
            data=config,
        )


class TestCrowdAliases(unittest.TestCase):
    """Test cases for user alias operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "get")
    def test_user_aliases(self, mock_get):
        """Test user_aliases method."""
        mock_get.return_value = {"alias": "jdoe"}
        result = self.crowd.user_aliases("john")
        mock_get.assert_called_once_with(
            "/rest/appmanagement/1/aliases",
            params={"user": "john"},
        )
        self.assertEqual(result["alias"], "jdoe")

    @patch.object(Crowd, "put")
    def test_set_user_aliases(self, mock_put):
        """Test set_user_aliases method."""
        aliases = {"1": "jdoe", "2": "john.doe"}
        self.crowd.set_user_aliases("john", aliases)
        mock_put.assert_called_once_with(
            "/rest/appmanagement/1/aliases",
            params={"user": "john"},
            data=aliases,
        )

    @patch.object(Crowd, "delete")
    def test_delete_user_aliases(self, mock_delete):
        """Test delete_user_aliases method."""
        self.crowd.delete_user_aliases("john")
        mock_delete.assert_called_once_with(
            "/rest/appmanagement/1/aliases",
            params={"user": "john"},
        )

    @patch.object(Crowd, "get")
    def test_get_alias(self, mock_get):
        """Test get_alias method."""
        mock_get.return_value = "jdoe"
        result = self.crowd.get_alias("app-1", "john")
        mock_get.assert_called_once_with(
            "/rest/appmanagement/1/aliases/app-1/alias",
            params={"user": "john"},
        )
        self.assertEqual(result, "jdoe")

    @patch.object(Crowd, "put")
    def test_set_alias(self, mock_put):
        """Test set_alias method."""
        self.crowd.set_alias("app-1", "john", "jdoe")
        mock_put.assert_called_once_with(
            "/rest/appmanagement/1/aliases/app-1/alias",
            params={"user": "john"},
            data="jdoe",
            headers={"Content-Type": "text/plain"},
        )

    @patch.object(Crowd, "delete")
    def test_delete_alias(self, mock_delete):
        """Test delete_alias method."""
        self.crowd.delete_alias("app-1", "john")
        mock_delete.assert_called_once_with(
            "/rest/appmanagement/1/aliases/app-1/alias",
            params={"user": "john"},
        )

    @patch.object(Crowd, "get")
    def test_get_username_for_alias(self, mock_get):
        """Test get_username_for_alias method."""
        mock_get.return_value = {"username": "john"}
        result = self.crowd.get_username_for_alias("app-1", "jdoe")
        mock_get.assert_called_once_with(
            "/rest/appmanagement/1/aliases/app-1/username",
            params={"alias": "jdoe"},
        )
        self.assertEqual(result["username"], "john")


class TestCrowdGroupFilters(unittest.TestCase):
    """Test cases for group listing with optional child/parent filters."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "get")
    def test_group_child_groups_with_child(self, mock_get):
        """Test group_child_groups with a child group filter."""
        mock_get.return_value = {"groups": [{"name": "child-a"}]}
        result = self.crowd.group_child_groups("parent", child_groupname="child-a")
        mock_get.assert_called_once_with(
            "/rest/usermanagement/latest/group/child-group/direct",
            params={
                "groupname": "parent",
                "start-index": 0,
                "max-results": 99999,
                "child-groupname": "child-a",
            },
        )
        self.assertEqual(result, ["child-a"])

    @patch.object(Crowd, "get")
    def test_nested_group_child_groups_with_child(self, mock_get):
        """Test nested_group_child_groups with a child group filter."""
        mock_get.return_value = {"groups": [{"name": "child-b"}]}
        result = self.crowd.nested_group_child_groups("parent", child_groupname="child-b")
        mock_get.assert_called_once_with(
            "/rest/usermanagement/latest/group/child-group/nested",
            params={
                "groupname": "parent",
                "start-index": 0,
                "max-results": 99999,
                "child-groupname": "child-b",
            },
        )
        self.assertEqual(result, ["child-b"])

    @patch.object(Crowd, "get")
    def test_group_parent_groups_with_child(self, mock_get):
        """Test group_parent_groups with a child group filter."""
        mock_get.return_value = {"groups": [{"name": "top"}]}
        result = self.crowd.group_parent_groups("child", child_groupname="top")
        mock_get.assert_called_once_with(
            "/rest/usermanagement/latest/group/parent-group/direct",
            params={
                "groupname": "child",
                "start-index": 0,
                "max-results": 99999,
                "child-groupname": "top",
            },
        )
        self.assertEqual(result, ["top"])

    @patch.object(Crowd, "get")
    def test_nested_group_parent_groups_with_parent(self, mock_get):
        """Test nested_group_parent_groups with a parent group filter."""
        mock_get.return_value = {"groups": [{"name": "root"}]}
        result = self.crowd.nested_group_parent_groups("child", parent_groupname="root")
        mock_get.assert_called_once_with(
            "/rest/usermanagement/latest/group/parent-group/nested",
            params={
                "groupname": "child",
                "start-index": 0,
                "max-results": 99999,
                "parent-groupname": "root",
            },
        )
        self.assertEqual(result, ["root"])


class TestCrowdDirectoryMappings(unittest.TestCase):
    """Test cases for application directory mapping operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "get")
    def test_get_directory_mappings(self, mock_get):
        """Test get_directory_mappings method."""
        mock_get.return_value = {"directories": []}
        result = self.crowd.get_directory_mappings("app-1", start=5, limit=50)
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/application/app-1/directory-mapping",
            params={"start": 5, "limit": 50},
        )
        self.assertEqual(result, {"directories": []})

    @patch.object(Crowd, "post")
    def test_add_directory_mapping(self, mock_post):
        """Test add_directory_mapping method."""
        data = {"directory": {"id": 1}}
        self.crowd.add_directory_mapping("app-1", data)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/application/app-1/directory-mapping",
            data=data,
        )

    @patch.object(Crowd, "get")
    def test_get_directory_mapping(self, mock_get):
        """Test get_directory_mapping method."""
        mock_get.return_value = {"directory": {"id": 1}}
        result = self.crowd.get_directory_mapping("app-1", 1)
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/application/app-1/directory-mapping/1",
        )
        self.assertEqual(result["directory"]["id"], 1)

    @patch.object(Crowd, "put")
    def test_update_directory_mapping(self, mock_put):
        """Test update_directory_mapping method."""
        data = {"allowedOperations": ["CREATE_USER"]}
        self.crowd.update_directory_mapping("app-1", 1, data)
        mock_put.assert_called_once_with(
            "/rest/admin/1.0/application/app-1/directory-mapping/1",
            data=data,
        )

    @patch.object(Crowd, "delete")
    def test_delete_directory_mapping(self, mock_delete):
        """Test delete_directory_mapping method."""
        self.crowd.delete_directory_mapping("app-1", 1)
        mock_delete.assert_called_once_with(
            "/rest/admin/1.0/application/app-1/directory-mapping/1",
        )

    @patch.object(Crowd, "post")
    def test_move_directory_mapping(self, mock_post):
        """Test move_directory_mapping method."""
        data = {"index": 0}
        self.crowd.move_directory_mapping("app-1", 1, data)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/application/app-1/directory-mapping/1/move",
            data=data,
        )


class TestCrowdGroupAdminOperations(unittest.TestCase):
    """Test cases for admin group operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "get")
    def test_search_directory_groups_with_active(self, mock_get):
        """Test search_directory_groups with an active filter."""
        mock_get.return_value = {"groups": []}
        result = self.crowd.search_directory_groups("1", "team", active=True, start=2, limit=10)
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/group/search/1",
            params={"term": "team", "start": 2, "limit": 10, "active": True},
        )
        self.assertEqual(result, {"groups": []})

    @patch.object(Crowd, "get")
    def test_get_admin_group_nested_groups(self, mock_get):
        """Test get_admin_group_nested_groups method."""
        mock_get.return_value = {"groups": []}
        self.crowd.get_admin_group_nested_groups("gid-1", start=1, limit=20)
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/group/gid-1/groups",
            params={"start": 1, "limit": 20},
        )

    @patch.object(Crowd, "post")
    def test_add_admin_group_nested_groups(self, mock_post):
        """Test add_admin_group_nested_groups method."""
        data = {"name": "child-group"}
        self.crowd.add_admin_group_nested_groups("gid-1", data)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/group/gid-1/groups",
            data=data,
        )

    @patch.object(Crowd, "get")
    def test_get_group_administrators(self, mock_get):
        """Test get_group_administrators method."""
        mock_get.return_value = {"admins": []}
        self.crowd.get_group_administrators("gid-1", start=3, limit=30)
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/group-level-admin/gid-1/admins",
            params={"start": 3, "limit": 30},
        )

    @patch.object(Crowd, "post")
    def test_add_group_administrators(self, mock_post):
        """Test add_group_administrators method."""
        data = {"users": [{"id": "u1"}]}
        self.crowd.add_group_administrators("gid-1", data)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/group-level-admin/gid-1/admins",
            data=data,
        )

    @patch.object(Crowd, "get")
    def test_get_group_admin_candidates(self, mock_get):
        """Test get_group_admin_candidates method."""
        mock_get.return_value = {"suggestions": []}
        result = self.crowd.get_group_admin_candidates("gid-1", search="john", limit=15)
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/group-level-admin/gid-1/admins/suggestions",
            params={"limit": 15, "search": "john"},
        )
        self.assertEqual(result, {"suggestions": []})

    @patch.object(Crowd, "get")
    def test_get_group_admin_candidates_no_search(self, mock_get):
        """Test get_group_admin_candidates without a search term."""
        self.crowd.get_group_admin_candidates("gid-1")
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/group-level-admin/gid-1/admins/suggestions",
            params={"limit": 99999},
        )

    @patch.object(Crowd, "delete")
    def test_remove_group_admin_user(self, mock_delete):
        """Test remove_group_admin_user method."""
        self.crowd.remove_group_admin_user("gid-1", "uid-1")
        mock_delete.assert_called_once_with(
            "/rest/admin/1.0/group-level-admin/gid-1/admins/users/uid-1",
        )

    @patch.object(Crowd, "delete")
    def test_remove_group_admin_group(self, mock_delete):
        """Test remove_group_admin_group method."""
        self.crowd.remove_group_admin_group("gid-1", "admingid-1")
        mock_delete.assert_called_once_with(
            "/rest/admin/1.0/group-level-admin/gid-1/admins/groups/admingid-1",
        )

    @patch.object(Crowd, "post")
    def test_search_administered_groups(self, mock_post):
        """Test search_administered_groups method."""
        mock_post.return_value = {"groups": []}
        query = {"criterion": "name"}
        result = self.crowd.search_administered_groups(query=query, start=4, limit=40)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/groups/query",
            params={"start": 4, "limit": 40},
            data=query,
        )
        self.assertEqual(result, {"groups": []})

    @patch.object(Crowd, "post")
    def test_search_administered_groups_default_query(self, mock_post):
        """Test search_administered_groups with no query defaults to empty body."""
        self.crowd.search_administered_groups()
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/groups/query",
            params={"start": 0, "limit": 99999},
            data={},
        )

    @patch.object(Crowd, "get")
    def test_get_admin_group_details(self, mock_get):
        """Test get_admin_group_details method."""
        mock_get.return_value = {"name": "jira-users"}
        result = self.crowd.get_admin_group_details("gid-1")
        mock_get.assert_called_once_with("/rest/admin/1.0/groups/gid-1")
        self.assertEqual(result["name"], "jira-users")

    @patch.object(Crowd, "get")
    def test_get_admin_group_members(self, mock_get):
        """Test get_admin_group_members method."""
        self.crowd.get_admin_group_members("gid-1", start=7, limit=70)
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/groups/gid-1/users",
            params={"start": 7, "limit": 70},
        )

    @patch.object(Crowd, "post")
    def test_add_users_to_admin_group(self, mock_post):
        """Test add_users_to_admin_group method."""
        data = {"users": ["u1", "u2"]}
        self.crowd.add_users_to_admin_group("gid-1", data)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/groups/gid-1/users",
            data=data,
        )

    @patch.object(Crowd, "delete")
    def test_remove_users_from_admin_group(self, mock_delete):
        """Test remove_users_from_admin_group method."""
        data = {"users": ["u1"]}
        self.crowd.remove_users_from_admin_group("gid-1", data)
        mock_delete.assert_called_once_with(
            "/rest/admin/1.0/groups/gid-1/users",
            data=data,
        )

    @patch.object(Crowd, "get")
    def test_search_admin_group_user_suggestions(self, mock_get):
        """Test search_admin_group_user_suggestions method."""
        self.crowd.search_admin_group_user_suggestions("gid-1", search="jo", limit=25)
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/groups/gid-1/users/suggestions",
            params={"limit": 25, "search": "jo"},
        )

    @patch.object(Crowd, "get")
    def test_search_admin_group_user_suggestions_no_search(self, mock_get):
        """Test search_admin_group_user_suggestions without a search term."""
        self.crowd.search_admin_group_user_suggestions("gid-1")
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/groups/gid-1/users/suggestions",
            params={"limit": 99999},
        )

    @patch.object(Crowd, "post")
    def test_search_admin_users(self, mock_post):
        """Test search_admin_users method."""
        mock_post.return_value = {"users": []}
        query = {"criterion": "email"}
        result = self.crowd.search_admin_users(query=query, start=8, limit=80)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/users/search",
            params={"start": 8, "limit": 80},
            data=query,
        )
        self.assertEqual(result, {"users": []})

    @patch.object(Crowd, "post")
    def test_search_admin_users_default_query(self, mock_post):
        """Test search_admin_users with no query defaults to empty body."""
        self.crowd.search_admin_users()
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/users/search",
            params={"start": 0, "limit": 99999},
            data={},
        )


class TestCrowdUserAdminOperations(unittest.TestCase):
    """Test cases for admin user operations and sessions."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "post")
    def test_add_user_to_admin_group(self, mock_post):
        """Test add_user_to_admin_group method."""
        data = {"groups": ["g1", "g2"]}
        self.crowd.add_user_to_admin_group("uid-1", data)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/users/uid-1/groups",
            data=data,
        )

    @patch.object(Crowd, "delete")
    def test_remove_user_from_admin_group(self, mock_delete):
        """Test remove_user_from_admin_group method."""
        data = {"groups": ["g1"]}
        self.crowd.remove_user_from_admin_group("uid-1", data)
        mock_delete.assert_called_once_with(
            "/rest/admin/1.0/users/uid-1/groups",
            data=data,
        )

    @patch.object(Crowd, "get")
    def test_get_server_info(self, mock_get):
        """Test get_server_info method."""
        mock_get.return_value = {"version": "5.3.1"}
        result = self.crowd.get_server_info()
        mock_get.assert_called_once_with("/rest/admin/1.0/server-info")
        self.assertEqual(result["version"], "5.3.1")

    @patch.object(Crowd, "get")
    def test_get_application_sessions(self, mock_get):
        """Test get_application_sessions method."""
        self.crowd.get_application_sessions(search="myapp", start=2, limit=20)
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/sessions/application",
            params={"start": 2, "limit": 20, "search": "myapp"},
        )

    @patch.object(Crowd, "get")
    def test_get_application_sessions_no_search(self, mock_get):
        """Test get_application_sessions without a search keyword."""
        self.crowd.get_application_sessions()
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/sessions/application",
            params={"start": 0, "limit": 99999},
        )

    @patch.object(Crowd, "get")
    def test_get_user_sessions(self, mock_get):
        """Test get_user_sessions method."""
        self.crowd.get_user_sessions(search="john", directory_id="1", start=1, limit=10)
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/sessions/user",
            params={"start": 1, "limit": 10, "search": "john", "directoryId": "1"},
        )

    @patch.object(Crowd, "get")
    def test_get_user_sessions_no_filters(self, mock_get):
        """Test get_user_sessions without filters."""
        self.crowd.get_user_sessions()
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/sessions/user",
            params={"start": 0, "limit": 99999},
        )

    @patch.object(Crowd, "delete")
    def test_expire_session(self, mock_delete):
        """Test expire_session method."""
        self.crowd.expire_session("abc123hash")
        mock_delete.assert_called_once_with(
            "/rest/admin/1.0/sessions/abc123hash",
        )


class TestCrowdLicensing(unittest.TestCase):
    """Test cases for licensing operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "get")
    def test_get_licensing_summary(self, mock_get):
        """Test get_licensing_summary method."""
        mock_get.return_value = {"userCount": 10}
        result = self.crowd.get_licensing_summary("app-1", version="v1", jira_type="software")
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/licensing/app-1/summary",
            params={"version": "v1", "jiraType": "software"},
        )
        self.assertEqual(result["userCount"], 10)

    @patch.object(Crowd, "get")
    def test_get_licensing_summary_no_filters(self, mock_get):
        """Test get_licensing_summary without optional filters."""
        self.crowd.get_licensing_summary("app-1")
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/licensing/app-1/summary",
            params={},
        )

    @patch.object(Crowd, "get")
    def test_get_licensed_directories(self, mock_get):
        """Test get_licensed_directories method."""
        self.crowd.get_licensed_directories("app-1", version="v1", jira_type="core", start=3, limit=30)
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/licensing/app-1/directories",
            params={"start": 3, "limit": 30, "version": "v1", "jiraType": "core"},
        )

    @patch.object(Crowd, "get")
    def test_get_licensed_directories_no_filters(self, mock_get):
        """Test get_licensed_directories without optional filters."""
        self.crowd.get_licensed_directories("app-1")
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/licensing/app-1/directories",
            params={"start": 0, "limit": 99999},
        )

    @patch.object(Crowd, "get")
    def test_get_licensed_jira_types(self, mock_get):
        """Test get_licensed_jira_types method."""
        self.crowd.get_licensed_jira_types("app-1", version="v2")
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/licensing/app-1/jira-types",
            params={"version": "v2"},
        )

    @patch.object(Crowd, "get")
    def test_get_licensed_jira_types_no_version(self, mock_get):
        """Test get_licensed_jira_types without a version."""
        self.crowd.get_licensed_jira_types("app-1")
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/licensing/app-1/jira-types",
            params={},
        )

    @patch.object(Crowd, "post")
    def test_search_licensed_users(self, mock_post):
        """Test search_licensed_users method."""
        mock_post.return_value = {"users": []}
        query = {"criterion": "lastLogin"}
        result = self.crowd.search_licensed_users("app-1", query=query, start=5, limit=50)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/licensing/app-1/licensed-users/search",
            params={"start": 5, "limit": 50},
            data=query,
        )
        self.assertEqual(result, {"users": []})

    @patch.object(Crowd, "post")
    def test_search_licensed_users_default_query(self, mock_post):
        """Test search_licensed_users with no query defaults to empty body."""
        self.crowd.search_licensed_users("app-1")
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/licensing/app-1/licensed-users/search",
            params={"start": 0, "limit": 99999},
            data={},
        )

    @patch.object(Crowd, "get")
    def test_export_licensed_users(self, mock_get):
        """Test export_licensed_users with all filters."""
        self.crowd.export_licensed_users(
            "app-1",
            search="john",
            directory_id="1",
            jira_type="software",
            last_login_before="2024-01-01",
            search_version="v1",
        )
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/licensing/app-1/licensed-users/download",
            params={
                "search": "john",
                "directoryId": "1",
                "jiraType": "software",
                "lastLoginBefore": "2024-01-01",
                "searchVersion": "v1",
            },
        )

    @patch.object(Crowd, "get")
    def test_export_licensed_users_no_filters(self, mock_get):
        """Test export_licensed_users without filters."""
        self.crowd.export_licensed_users("app-1")
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/licensing/app-1/licensed-users/download",
            params={},
        )


class TestCrowdBackupAndAudit(unittest.TestCase):
    """Test cases for backup and audit log operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "post")
    def test_create_backup(self, mock_post):
        """Test create_backup method."""
        data = {"allDirectories": True}
        self.crowd.create_backup(data)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/backup",
            data=data,
        )

    @patch.object(Crowd, "post")
    def test_create_backup_default(self, mock_post):
        """Test create_backup with no data defaults to empty body."""
        self.crowd.create_backup()
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/backup",
            data={},
        )

    @patch.object(Crowd, "get")
    def test_get_backup_summary(self, mock_get):
        """Test get_backup_summary method."""
        mock_get.return_value = {"available": True}
        result = self.crowd.get_backup_summary()
        mock_get.assert_called_once_with("/rest/admin/1.0/backup/summary")
        self.assertTrue(result["available"])

    @patch.object(Crowd, "get")
    def test_get_backup_configuration(self, mock_get):
        """Test get_backup_configuration method."""
        self.crowd.get_backup_configuration()
        mock_get.assert_called_once_with("/rest/admin/1.0/backup/configuration")

    @patch.object(Crowd, "post")
    def test_save_backup_configuration(self, mock_post):
        """Test save_backup_configuration method."""
        data = {"scheduledJobEnabled": True}
        self.crowd.save_backup_configuration(data)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/backup/configuration",
            data=data,
        )

    @patch.object(Crowd, "post")
    def test_add_audit_log_changeset(self, mock_post):
        """Test add_audit_log_changeset method."""
        data = {"changes": []}
        self.crowd.add_audit_log_changeset(data)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/auditlog",
            data=data,
        )

    @patch.object(Crowd, "get")
    def test_get_audit_log_configuration(self, mock_get):
        """Test get_audit_log_configuration method."""
        self.crowd.get_audit_log_configuration()
        mock_get.assert_called_once_with("/rest/admin/1.0/auditlog/configuration")

    @patch.object(Crowd, "put")
    def test_set_audit_log_configuration(self, mock_put):
        """Test set_audit_log_configuration method."""
        data = {"enabled": True}
        self.crowd.set_audit_log_configuration(data)
        mock_put.assert_called_once_with(
            "/rest/admin/1.0/auditlog/configuration",
            data=data,
        )

    @patch.object(Crowd, "post")
    def test_search_audit_log(self, mock_post):
        """Test search_audit_log method."""
        mock_post.return_value = {"entries": []}
        query = {"dateRange": {"startDate": "2024-01-01"}}
        result = self.crowd.search_audit_log(query=query, start=6, limit=60)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/auditlog/query",
            params={"start": 6, "limit": 60},
            data=query,
        )
        self.assertEqual(result, {"entries": []})

    @patch.object(Crowd, "post")
    def test_search_audit_log_default_query(self, mock_post):
        """Test search_audit_log with no query defaults to empty body."""
        self.crowd.search_audit_log()
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/auditlog/query",
            params={"start": 0, "limit": 99999},
            data={},
        )
    @patch.object(Crowd, "post")
    def test_get_audit_log_filter_values(self, mock_post):
        """Test get_audit_log_filter_values method."""
        self.crowd.get_audit_log_filter_values(projection="AUDITED_USERS", search="john", start=9, limit=90)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/auditlog/query/filter",
            params={"start": 9, "limit": 90, "projection": "AUDITED_USERS", "search": "john"},
            data={},
        )

    @patch.object(Crowd, "post")
    def test_get_audit_log_filter_values_no_filters(self, mock_post):
        """Test get_audit_log_filter_values without optional filters."""
        self.crowd.get_audit_log_filter_values()
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/auditlog/query/filter",
            params={"start": 0, "limit": 99999},
            data={},
        )


class TestCrowdSystemConfiguration(unittest.TestCase):
    """Test cases for look-and-feel, remember-me, SAML, and mail configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "get")
    def test_get_look_and_feel_config(self, mock_get):
        """Test get_look_and_feel_config method."""
        self.crowd.get_look_and_feel_config()
        mock_get.assert_called_once_with("/rest/admin/1.0/look-and-feel/config")

    @patch.object(Crowd, "put")
    def test_update_look_and_feel_config(self, mock_put):
        """Test update_look_and_feel_config method."""
        data = {"customLoginUrl": "https://login.example.com"}
        self.crowd.update_look_and_feel_config(data)
        mock_put.assert_called_once_with(
            "/rest/admin/1.0/look-and-feel/config",
            data=data,
        )

    @patch.object(Crowd, "post")
    def test_reset_look_and_feel_config(self, mock_post):
        """Test reset_look_and_feel_config method."""
        self.crowd.reset_look_and_feel_config()
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/look-and-feel/reset-config",
        )

    @patch.object(Crowd, "get")
    def test_get_remember_me_config(self, mock_get):
        """Test get_remember_me_config method."""
        self.crowd.get_remember_me_config()
        mock_get.assert_called_once_with("/rest/admin/1.0/remember-me/config")

    @patch.object(Crowd, "put")
    def test_update_remember_me_config(self, mock_put):
        """Test update_remember_me_config method."""
        data = {"enabled": True, "maxIdleTime": 3600}
        self.crowd.update_remember_me_config(data)
        mock_put.assert_called_once_with(
            "/rest/admin/1.0/remember-me/config",
            data=data,
        )

    @patch.object(Crowd, "post")
    def test_expire_all_remember_me_tokens(self, mock_post):
        """Test expire_all_remember_me_tokens method."""
        self.crowd.expire_all_remember_me_tokens()
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/remember-me/expire-all",
        )

    @patch.object(Crowd, "get")
    def test_get_saml_config(self, mock_get):
        """Test get_saml_config method."""
        self.crowd.get_saml_config()
        mock_get.assert_called_once_with("/rest/admin/1.0/samlconfig")

    @patch.object(Crowd, "get")
    def test_get_saml_application_config(self, mock_get):
        """Test get_saml_application_config method."""
        mock_get.return_value = {"enabled": True}
        result = self.crowd.get_saml_application_config("app-1")
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/samlconfig/application/app-1",
        )
        self.assertTrue(result["enabled"])

    @patch.object(Crowd, "post")
    def test_update_saml_application_config(self, mock_post):
        """Test update_saml_application_config method."""
        data = {"enabled": True}
        self.crowd.update_saml_application_config("app-1", data)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/samlconfig/application/app-1",
            data=data,
        )

    @patch.object(Crowd, "post")
    def test_parse_saml_metadata(self, mock_post):
        """Test parse_saml_metadata method."""
        metadata = b"<EntityDescriptor/>"
        self.crowd.parse_saml_metadata(metadata)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/samlconfig/application/parse_metadata",
            data=metadata,
            headers={"Content-Type": "application/octet-stream"},
        )

    @patch.object(Crowd, "post")
    def test_parse_saml_metadata_file(self, mock_post):
        """Test parse_saml_metadata_file method."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False) as f:
            f.write("<EntityDescriptor/>")
            file_path = f.name
        try:
            self.crowd.parse_saml_metadata_file(file_path)
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            self.assertEqual(call_args[0][0], "/rest/admin/1.0/samlconfig/application/parse_metadata_multipart")
            self.assertIn("file", call_args[1]["files"])
        finally:
            os.unlink(file_path)

    @patch.object(Crowd, "post")
    def test_reset_saml_certificates(self, mock_post):
        """Test reset_saml_certificates method."""
        self.crowd.reset_saml_certificates()
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/samlconfig/reset-certificates",
        )

    @patch.object(Crowd, "get")
    def test_get_saml_idp_metadata(self, mock_get):
        """Test get_saml_idp_metadata method."""
        self.crowd.get_saml_idp_metadata()
        mock_get.assert_called_once_with("/rest/admin/1.0/samlconfig/idp/metadata")

    @patch.object(Crowd, "get")
    def test_find_saml_directory_mapping_mismatch(self, mock_get):
        """Test find_saml_directory_mapping_mismatch method."""
        self.crowd.find_saml_directory_mapping_mismatch("app-1")
        mock_get.assert_called_once_with(
            "/rest/admin/1.0/samlconfig/application/app-1/directory-mapping-mismatch",
        )

    @patch.object(Crowd, "get")
    def test_get_dynamic_ldap_pool_statistics(self, mock_get):
        """Test get_dynamic_ldap_pool_statistics method."""
        self.crowd.get_dynamic_ldap_pool_statistics()
        mock_get.assert_called_once_with("/rest/admin/1.0/dynamic-ldap-pool-statistics")

    @patch.object(Crowd, "post")
    def test_save_mail_configuration(self, mock_post):
        """Test save_mail_configuration method."""
        data = {"host": "smtp.example.com", "port": 587}
        self.crowd.save_mail_configuration(data)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/mail/configuration",
            data=data,
        )

    @patch.object(Crowd, "post")
    def test_test_mail_configuration(self, mock_post):
        """Test test_mail_configuration method."""
        data = {"host": "smtp.example.com", "recipient": "admin@example.com"}
        self.crowd.test_mail_configuration(data)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/mail/configuration/test",
            data=data,
        )

    @patch.object(Crowd, "post")
    def test_validate_mail_configuration(self, mock_post):
        """Test validate_mail_configuration method."""
        data = {"host": "smtp.example.com"}
        self.crowd.validate_mail_configuration(data)
        mock_post.assert_called_once_with(
            "/rest/admin/1.0/mail/configuration/validate",
            data=data,
        )


class TestCrowdHealthAndPlugins(unittest.TestCase):
    """Test cases for health check and plugin operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "get")
    def test_health_check_primary(self, mock_get):
        """Test health_check when the primary endpoint returns data."""
        mock_get.return_value = {"healthy": True}
        result = self.crowd.health_check()
        mock_get.assert_called_once_with("rest/troubleshooting/1.0/check/")
        self.assertTrue(result["healthy"])

    @patch.object(Crowd, "get")
    def test_health_check_fallback(self, mock_get):
        """Test health_check falls back when the primary endpoint is empty."""
        mock_get.side_effect = [None, {"healthy": False}]
        result = self.crowd.health_check()
        self.assertEqual(mock_get.call_count, 2)
        mock_get.assert_called_with("rest/supportHealthCheck/1.0/check/")
        self.assertFalse(result["healthy"])

    @patch.object(Crowd, "request")
    @patch.object(Crowd, "post")
    def test_upload_plugin(self, mock_post, mock_request):
        """Test upload_plugin method."""
        mock_request.return_value.headers = {"upm-token": "token123"}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jar", delete=False) as f:
            f.write("jar-content")
            plugin_path = f.name
        try:
            self.crowd.upload_plugin(plugin_path)
            mock_request.assert_called_once_with(
                method="GET",
                path="rest/plugins/1.0/",
                headers=Crowd.no_check_headers,
                trailing=True,
            )
            mock_post.assert_called_once_with(
                "rest/plugins/1.0/?token=token123",
                files={"plugin": ANY},
                headers=Crowd.no_check_headers,
            )
        finally:
            os.unlink(plugin_path)

    @patch.object(Crowd, "delete")
    def test_delete_plugin(self, mock_delete):
        """Test delete_plugin method."""
        self.crowd.delete_plugin("plugin1")
        mock_delete.assert_called_once_with("rest/plugins/1.0/plugin1-key")

    @patch.object(Crowd, "request")
    def test_check_plugin_manager_status(self, mock_request):
        """Test check_plugin_manager_status method."""
        self.crowd.check_plugin_manager_status()
        mock_request.assert_called_once_with(
            method="GET",
            path="rest/plugins/latest/safe-mode",
            headers=Crowd.safe_mode_headers,
        )

    @patch.object(Crowd, "put")
    def test_update_plugin_license(self, mock_put):
        """Test update_plugin_license method."""
        self.crowd.update_plugin_license("plugin1", "raw-license-text")
        mock_put.assert_called_once_with(
            "rest/plugins/1.0/plugin1/license",
            data={"rawLicense": "raw-license-text"},
            headers={
                "X-Atlassian-Token": "no-check",
                "Content-Type": "application/vnd.atl.plugins+json",
            },
        )


class TestCrowdMemberships(unittest.TestCase):
    """Test cases for the memberships XML property."""

    def setUp(self):
        """Set up test fixtures."""
        self.crowd = Crowd(
            url="https://crowd.example.com",
            username="admin",
            password="password",
        )

    @patch.object(Crowd, "get")
    def test_memberships(self, mock_get):
        """Test memberships property parses XML into a mapping."""
        mock_get.return_value = (
            "<memberships>"
            '<membership group="jira-users"><user name="alice"/><user name="bob"/></membership>'
            '<membership group="admins"><user name="carol"/></membership>'
            '<membership group="empty-group"/>'
            "</memberships>"
        )
        memberships = self.crowd.memberships
        mock_get.assert_called_once_with(
            "/rest/usermanagement/latest/group/membership",
            headers={"Accept": "application/xml"},
        )
        self.assertEqual(memberships["jira-users"], ["alice", "bob"])
        self.assertEqual(memberships["admins"], ["carol"])
        self.assertEqual(memberships["empty-group"], [])

    @patch.object(Crowd, "get")
    def test_memberships_empty_response(self, mock_get):
        """Test memberships property with an empty XML response."""
        mock_get.return_value = "<memberships></memberships>"
        memberships = self.crowd.memberships
        self.assertEqual(memberships, {})


if __name__ == "__main__":
    unittest.main()
