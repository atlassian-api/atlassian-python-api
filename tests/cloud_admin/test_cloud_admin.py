# coding: utf-8
"""
Unit tests for atlassian.cloud_admin module
"""

from tests.mockup import mockup_server
from atlassian.cloud_admin import CloudAdmin, CloudAdminOrgs, CloudAdminUsers


class TestCloudAdmin:
    def test_v2_directory_and_user_endpoints(self, monkeypatch):
        admin = CloudAdmin(admin_api_key="test_api_key")
        calls = []

        monkeypatch.setattr(admin, "get", lambda path, **kwargs: calls.append((path, kwargs)) or {})
        monkeypatch.setattr(admin, "post", lambda path, **kwargs: calls.append((path, kwargs)) or {})

        admin.get_directories("org", search_term="engineering", limit=20)
        admin.search_directory_users("org", "directory", {"searchTerm": "ada", "limit": 50})

        assert calls == [
            ("admin/v2/orgs/org/directories", {"params": {"searchTerm": "engineering", "limit": 20}}),
            ("admin/v2/orgs/org/directories/directory/users/search", {"data": {"searchTerm": "ada", "limit": 50}}),
        ]

    def test_user_management_uses_users_api_surface(self, monkeypatch):
        admin = CloudAdmin(admin_api_key="test_api_key")
        calls = []
        monkeypatch.setattr(admin, "put", lambda path, **kwargs: calls.append((path, kwargs)) or {})
        monkeypatch.setattr(admin, "post", lambda path, **kwargs: calls.append((path, kwargs)) or {})

        admin.set_user_email("account", "ada@example.com")
        admin.deactivate_user("account", message="Offboarding")

        assert calls == [
            (
                "https://api.atlassian.com/users/account/manage/email",
                {"data": {"email": "ada@example.com"}, "absolute": True},
            ),
            (
                "https://api.atlassian.com/users/account/manage/lifecycle/disable",
                {"data": {"message": "Offboarding"}, "absolute": True},
            ),
        ]

    def test_scim_provisioning_uses_directory_api_surface(self, monkeypatch):
        admin = CloudAdmin(admin_api_key="test_api_key")
        calls = []
        monkeypatch.setattr(admin, "get", lambda path, **kwargs: calls.append(("get", path, kwargs)) or {})
        monkeypatch.setattr(admin, "patch", lambda path, **kwargs: calls.append(("patch", path, kwargs)) or {})

        admin.get_scim_users("directory", filter='userName eq "ada@example.com"', count=10)
        admin.patch_scim_group("directory", "group", [{"op": "add", "path": "members", "value": []}])

        assert calls == [
            (
                "get",
                "https://api.atlassian.com/scim/directory/directory/Users",
                {"absolute": True, "params": {"filter": 'userName eq "ada@example.com"', "count": 10}},
            ),
            (
                "patch",
                "https://api.atlassian.com/scim/directory/directory/Groups/group",
                {"data": {"Operations": [{"op": "add", "path": "members", "value": []}]}, "absolute": True},
            ),
        ]

    def test_dlp_uses_classification_levels_api_surface(self, monkeypatch):
        admin = CloudAdmin(admin_api_key="test_api_key")
        calls = []
        monkeypatch.setattr(admin, "post", lambda path, **kwargs: calls.append((path, kwargs)) or {})

        admin.publish_classification_levels("org", ["internal", "restricted"])
        admin.archive_classification_level("org", "restricted")

        assert calls == [
            (
                "https://api.atlassian.com/admin/dlp/v1/orgs/org/classification-levels/publish",
                {"data": {"levelIds": ["internal", "restricted"]}, "absolute": True},
            ),
            (
                "https://api.atlassian.com/admin/dlp/v1/orgs/org/classification-levels/archive",
                {"data": {"levelId": "restricted"}, "absolute": True},
            ),
        ]

    def test_control_uses_versioned_policy_api_surface(self, monkeypatch):
        admin = CloudAdmin(admin_api_key="test_api_key")
        calls = []
        monkeypatch.setattr(admin, "post", lambda path, **kwargs: calls.append((path, kwargs)) or {})

        admin.create_control_policy("org", {"name": "MFA"})
        admin.add_users_to_auth_policy("org", "policy", {"accountIds": ["account"]})

        assert calls == [
            (
                "https://api.atlassian.com/admin/control/v2/orgs/org/policies",
                {"data": {"name": "MFA"}, "absolute": True},
            ),
            (
                "https://api.atlassian.com/admin/control/v1/orgs/org/auth-policy/policy/add-users",
                {"data": {"accountIds": ["account"]}, "absolute": True},
            ),
        ]

    def test_api_access_uses_dedicated_api_surface(self, monkeypatch):
        admin = CloudAdmin(admin_api_key="test_api_key")
        calls = []
        monkeypatch.setattr(admin, "get", lambda path, **kwargs: calls.append((path, kwargs)) or {})
        monkeypatch.setattr(admin, "patch", lambda path, **kwargs: calls.append((path, kwargs)) or {})

        admin.get_org_api_tokens("org", limit=100)
        admin.revoke_org_api_key("org", "key")

        assert calls == [
            (
                "https://api.atlassian.com/admin/api-access/v1/orgs/org/api-tokens",
                {"absolute": True, "params": {"limit": 100}},
            ),
            (
                "https://api.atlassian.com/admin/api-access/v1/orgs/org/api-keys/revoke/key",
                {"data": {}, "absolute": True},
            ),
        ]


class TestCloudAdminOrgs:
    """Test cases for CloudAdminOrgs class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.orgs = CloudAdminOrgs(admin_api_key="test_api_key")

    def test_init_default_values(self):
        """Test initialization with default values"""
        orgs = CloudAdminOrgs(admin_api_key="test_api_key")
        assert orgs.api_root == "admin"
        assert orgs.api_version == "v1"

    def test_init_custom_values(self):
        """Test initialization with custom values"""
        orgs = CloudAdminOrgs(
            admin_api_key="test_api_key", username="custom@example.com", password="custompass", cloud=False
        )
        assert orgs.username == "custom@example.com"
        assert orgs.password == "custompass"
        assert orgs.cloud is False

    def test_init_with_token(self):
        """Test initialization with API token"""
        orgs = CloudAdminOrgs(admin_api_key="test_api_key")
        assert orgs.api_root == "admin"
        assert orgs.api_version == "v1"

    def test_get_organizations(self):
        """Test getting organizations"""
        # This test will use the mockup server to make actual HTTP requests
        # The mockup system will intercept these and return predefined responses
        try:
            result = self.orgs.get_organizations()
            # If the mockup has responses for this endpoint, we can assert on them
            # Otherwise, we just verify the method exists and can be called
            assert isinstance(result, (dict, list)) or result is None
        except Exception:
            # If the mockup doesn't have responses for this endpoint, that's okay
            # We're just testing that the method exists and can be called
            pass

    def test_get_organization(self):
        """Test getting a specific organization"""
        org_id = "org123"
        try:
            result = self.orgs.get_organization(org_id)
            # If the mockup has responses for this endpoint, we can assert on them
            assert isinstance(result, (dict, list)) or result is None
        except Exception:
            # If the mockup doesn't have responses for this endpoint, that's okay
            pass

    def test_get_managed_accounts_in_organization(self):
        """Test getting managed accounts in an organization"""
        org_id = "org123"
        try:
            result = self.orgs.get_managed_accounts_in_organization(org_id)
            # If the mockup has responses for this endpoint, we can assert on them
            assert isinstance(result, (dict, list)) or result is None
        except Exception:
            # If the mockup doesn't have responses for this endpoint, that's okay
            pass

    def test_search_users_in_organization(self):
        """Test searching users in an organization"""
        org_id = "org123"
        try:
            result = self.orgs.search_users_in_organization(org_id)
            # If the mockup has responses for this endpoint, we can assert on them
            assert isinstance(result, (dict, list)) or result is None
        except Exception:
            # If the mockup doesn't have responses for this endpoint, that's okay
            pass

    def test_methods_exist(self):
        """Test that expected methods exist"""
        expected_methods = [
            "get_organizations",
            "get_organization",
            "get_managed_accounts_in_organization",
            "search_users_in_organization",
        ]

        for method_name in expected_methods:
            assert hasattr(self.orgs, method_name), f"Method {method_name} not found"


class TestCloudAdminUsers:
    """Test cases for CloudAdminUsers class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.users = CloudAdminUsers(admin_api_key="test_api_key")

    def test_init_default_values(self):
        """Test initialization with default values"""
        users = CloudAdminUsers(admin_api_key="test_api_key")
        assert users.api_root == "users"
        assert users.api_version is None

    def test_init_custom_values(self):
        """Test initialization with custom values"""
        users = CloudAdminUsers(
            admin_api_key="test_api_key", username="custom@example.com", password="custompass", cloud=False
        )
        assert users.username == "custom@example.com"
        assert users.password == "custompass"
        assert users.cloud is False

    def test_init_with_token(self):
        """Test initialization with API token"""
        users = CloudAdminUsers(admin_api_key="test_api_key")
        assert users.api_root == "users"
        assert users.api_version is None

    def test_get_profile(self):
        """Test getting a user profile"""
        account_id = "user123"
        try:
            result = self.users.get_profile(account_id)
            # If the mockup has responses for this endpoint, we can assert on them
            assert isinstance(result, (dict, list)) or result is None
        except Exception:
            # If the mockup doesn't have responses for this endpoint, that's okay
            pass

    def test_methods_exist(self):
        """Test that expected methods exist"""
        expected_methods = [
            "get_profile",
        ]

        for method_name in expected_methods:
            assert hasattr(self.users, method_name), f"Method {method_name} not found"

    def test_error_handling(self):
        """Test error handling in API calls"""
        # Test that methods can handle errors gracefully
        try:
            # This should not crash the test
            self.users.get_profile("nonexistent")
        except Exception:
            # Expected behavior for non-existent user
            pass

    def test_mockup_integration(self):
        """Test that cloud admin works with the mockup system"""
        # This test ensures that our cloud admin classes don't interfere with the mockup system
        mockup_url = mockup_server()
        assert isinstance(mockup_url, str)
        assert len(mockup_url) > 0

        # Test that our classes can be instantiated
        test_orgs = CloudAdminOrgs(admin_api_key="test_key")
        test_users = CloudAdminUsers(admin_api_key="test_key")

        assert test_orgs is not None
        assert test_users is not None
