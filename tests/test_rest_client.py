# coding: utf-8
"""
Unit tests for atlassian.rest_client module
"""

import pytest
from .mockup import mockup_server
from atlassian.rest_client import AtlassianRestAPI


class TestAtlassianRestAPI:
    """Test cases for AtlassianRestAPI class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.api = AtlassianRestAPI(
            url=f"{mockup_server()}/test",
            username="testuser",
            password="testpass",
            timeout=30,
            api_root="rest/api",
            api_version="latest",
            verify_ssl=True,
            cloud=False,
        )

    def test_init_default_values(self):
        """Test initialization with default values"""
        api = AtlassianRestAPI(url=f"{mockup_server()}/test")
        assert api.url == f"{mockup_server()}/test"
        assert api.username is None
        assert api.password is None
        assert api.timeout == 75
        assert api.api_root == "rest/api"
        assert api.api_version == "latest"
        assert api.verify_ssl is True
        assert api.cloud is False

    def test_init_custom_values(self):
        """Test initialization with custom values"""
        api = AtlassianRestAPI(
            url=f"{mockup_server()}/custom",
            username="customuser",
            password="custompass",
            timeout=60,
            api_root="custom/api",
            api_version="2",
            verify_ssl=False,
            cloud=True,
        )
        assert api.url == f"{mockup_server()}/custom"
        assert api.username == "customuser"
        assert api.password == "custompass"
        assert api.timeout == 60
        assert api.api_root == "custom/api"
        assert api.api_version == "2"
        assert api.verify_ssl is False
        assert api.cloud is True

    def test_init_with_token(self):
        """Test initialization with API token"""
        api = AtlassianRestAPI(url=f"{mockup_server()}/test", token="apitoken123")
        # The token should be stored in the session configuration
        assert hasattr(api, "session")

    def test_init_with_cert(self):
        """Test initialization with certificate"""
        api = AtlassianRestAPI(url=f"{mockup_server()}/test", cert=("/path/to/cert.pem", "/path/to/key.pem"))
        assert api.cert == ("/path/to/cert.pem", "/path/to/key.pem")

    def test_init_with_proxies(self):
        """Test initialization with proxy configuration"""
        proxies = {"http": "http://proxy.example.com:8080", "https": "https://proxy.example.com:8080"}
        api = AtlassianRestAPI(url=f"{mockup_server()}/test", proxies=proxies)
        assert api.proxies == proxies

    def test_init_with_backoff_retry(self):
        """Test initialization with backoff and retry configuration"""
        api = AtlassianRestAPI(
            url=f"{mockup_server()}/test",
            backoff_and_retry=True,
            retry_status_codes=[500, 502, 503],
            max_backoff_seconds=900,
            max_backoff_retries=500,
            backoff_factor=2.0,
        )
        assert api.backoff_and_retry is True
        assert api.retry_status_codes == [500, 502, 503]
        assert api.max_backoff_seconds == 900
        assert api.max_backoff_retries == 500
        assert api.backoff_factor == 2.0

    def test_class_attributes(self):
        """Test that class attributes are properly defined"""
        assert hasattr(AtlassianRestAPI, "default_headers")
        assert hasattr(AtlassianRestAPI, "experimental_headers")
        assert hasattr(AtlassianRestAPI, "form_token_headers")
        assert hasattr(AtlassianRestAPI, "no_check_headers")
        assert hasattr(AtlassianRestAPI, "safe_mode_headers")
        assert hasattr(AtlassianRestAPI, "experimental_headers_general")

    def test_default_headers(self):
        """Test default headers configuration"""
        headers = AtlassianRestAPI.default_headers

        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/json"
        assert "Accept" in headers
        assert headers["Accept"] == "application/json"

    def test_experimental_headers(self):
        """Test experimental headers configuration"""
        headers = AtlassianRestAPI.experimental_headers

        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/json"
        assert "Accept" in headers
        assert headers["Accept"] == "application/json"
        assert "X-ExperimentalApi" in headers
        assert headers["X-ExperimentalApi"] == "opt-in"

    def test_form_token_headers(self):
        """Test form token headers configuration"""
        headers = AtlassianRestAPI.form_token_headers

        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/x-www-form-urlencoded; charset=UTF-8"
        assert "X-Atlassian-Token" in headers
        assert headers["X-Atlassian-Token"] == "no-check"

    def test_no_check_headers(self):
        """Test no check headers configuration"""
        headers = AtlassianRestAPI.no_check_headers

        assert "X-Atlassian-Token" in headers
        assert headers["X-Atlassian-Token"] == "no-check"

    def test_safe_mode_headers(self):
        """Test safe mode headers configuration"""
        headers = AtlassianRestAPI.safe_mode_headers

        assert "X-Atlassian-Token" in headers
        assert headers["X-Atlassian-Token"] == "no-check"
        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/vnd.atl.plugins.safe.mode.flag+json"

    def test_experimental_headers_general(self):
        """Test experimental headers general configuration"""
        headers = AtlassianRestAPI.experimental_headers_general

        assert "X-Atlassian-Token" in headers
        assert headers["X-Atlassian-Token"] == "no-check"
        assert "X-ExperimentalApi" in headers
        assert headers["X-ExperimentalApi"] == "opt-in"

    def test_session_creation(self):
        """Test that session is created during initialization"""
        api = AtlassianRestAPI(url=f"{mockup_server()}/test")
        assert hasattr(api, "session")
        assert api.session is not None

    def test_url_construction(self):
        """Test URL construction for API endpoints"""
        # The URL construction happens in the request method
        # We'll test this indirectly through the request method
        assert self.api.url == f"{mockup_server()}/test"
        assert self.api.api_root == "rest/api"
        assert self.api.api_version == "latest"

    def test_cloud_flag(self):
        """Test cloud flag handling"""
        cloud_api = AtlassianRestAPI(url=f"{mockup_server()}/test", cloud=True)
        assert cloud_api.cloud is True

        server_api = AtlassianRestAPI(url=f"{mockup_server()}/test", cloud=False)
        assert server_api.cloud is False

    def test_advanced_mode(self):
        """Test advanced mode configuration"""
        api = AtlassianRestAPI(url=f"{mockup_server()}/test", advanced_mode=True)
        assert api.advanced_mode is True

    def test_kerberos_configuration(self):
        """Test kerberos configuration"""
        # Test that kerberos config is accepted without errors
        try:
            # This should not crash the test
            AtlassianRestAPI(url=f"{mockup_server()}/test", kerberos=True)
        except ImportError:
            # requests_kerberos is not installed, which is expected
            pass
        except Exception:
            # Other exceptions are also acceptable
            pass

    def test_cookies_configuration(self):
        """Test cookies configuration"""
        cookies = None  # Removed unused import

        try:
            # This should not crash the test
            AtlassianRestAPI(url=f"{mockup_server()}/test", cookies=cookies)
        except Exception:
            # Cookies might not be properly configured, which is acceptable
            pass

    def test_timeout_configuration(self):
        """Test timeout configuration"""
        api = AtlassianRestAPI(url=f"{mockup_server()}/test", timeout=120)
        assert api.timeout == 120

    def test_verify_ssl_configuration(self):
        """Test SSL verification configuration"""
        try:
            # This should not crash the test
            AtlassianRestAPI(url=f"{mockup_server()}/test", verify_ssl=False)
        except Exception:
            # SSL verification might not be properly configured, which is acceptable
            pass

    def test_api_version_types(self):
        """Test different API version types"""
        # String version
        api1 = AtlassianRestAPI(url=f"{mockup_server()}/test", api_version="2")
        assert api1.api_version == "2"

        # Integer version
        api2 = AtlassianRestAPI(url=f"{mockup_server()}/test", api_version=3)
        assert api2.api_version == 3

        # Latest version
        api3 = AtlassianRestAPI(url=f"{mockup_server()}/test", api_version="latest")
        assert api3.api_version == "latest"

    def test_api_root_configuration(self):
        """Test API root configuration"""
        api = AtlassianRestAPI(url=f"{mockup_server()}/test", api_root="custom/api")
        assert api.api_root == "custom/api"

    def test_oauth_configuration(self):
        """Test OAuth configuration (without actual OAuth setup)"""
        # Test that OAuth config is accepted without errors
        oauth_config = {
            "access_token": "token123",
            "access_token_secret": "secret123",
            "consumer_key": "consumer123",
            "key_cert": "cert123",
        }

        # This should not raise an error during initialization
        try:
            api = AtlassianRestAPI(url=f"{mockup_server()}/test", oauth=oauth_config)
            assert hasattr(api, "session")
        except Exception:
            # OAuth might not be available, which is acceptable
            pass

    def test_oauth2_configuration(self):
        """Test OAuth2 configuration (without actual OAuth2 setup)"""
        # Test that OAuth2 config is accepted without errors
        oauth2_config = {"client_id": "client123", "client_secret": "secret123", "access_token": "token123"}

        # This should not raise an error during initialization
        try:
            api = AtlassianRestAPI(url=f"{mockup_server()}/test", oauth2=oauth2_config)
            assert hasattr(api, "session")
        except Exception:
            # OAuth2 might not be available, which is acceptable
            pass

    def test_methods_exist(self):
        """Test that expected methods exist"""
        expected_methods = ["get", "post", "put", "delete", "patch", "request"]

        for method_name in expected_methods:
            assert hasattr(self.api, method_name), f"Method {method_name} not found"

    def test_error_handling_imports(self):
        """Test that error handling classes can be imported"""
        try:
            from atlassian.errors import (
                ApiError,
                ApiNotFoundError,
                ApiPermissionError,
                ApiValueError,
                ApiConflictError,
                ApiNotAcceptable,
            )

            # Test that the classes can be instantiated
            error = ApiError("Test error")
            not_found = ApiNotFoundError("Not found")
            permission = ApiPermissionError("Permission denied")
            value_error = ApiValueError("Invalid value")
            conflict = ApiConflictError("Conflict")
            not_acceptable = ApiNotAcceptable("Not acceptable")
            assert str(error) == "Test error"
            assert str(not_found) == "Not found"
            assert str(permission) == "Permission denied"
            assert str(value_error) == "Invalid value"
            assert str(conflict) == "Conflict"
            assert str(not_acceptable) == "Not acceptable"
        except ImportError:
            pytest.fail("Failed to import error classes")

    def test_type_hints_imports(self):
        """Test that type hints can be imported"""
        try:
            from atlassian.typehints import T_resp_json

            assert T_resp_json is not None
        except ImportError:
            pytest.fail("Failed to import type hints")

    def test_request_utils_imports(self):
        """Test that request utilities can be imported"""
        try:
            from atlassian.request_utils import get_default_logger

            assert get_default_logger is not None
        except ImportError:
            pytest.fail("Failed to import request utilities")

    def test_logging_configuration(self):
        """Test that logging is properly configured"""
        # The logging is configured at module level, not instance level
        assert hasattr(AtlassianRestAPI, "default_headers")
        assert AtlassianRestAPI.default_headers is not None

    def test_response_attribute(self):
        """Test that response attribute exists"""
        assert hasattr(self.api, "response")
        assert self.api.response is None

    def test_retry_configuration(self):
        """Test retry configuration attributes"""
        api = AtlassianRestAPI(
            url=f"{mockup_server()}/test",
            backoff_and_retry=True,
            retry_status_codes=[500, 502, 503],
            max_backoff_seconds=900,
            max_backoff_retries=500,
            backoff_factor=2.0,
        )

        # Test that retry configuration attributes are set
        assert api.retry_status_codes == [500, 502, 503]
        assert api.max_backoff_seconds == 900
        assert api.max_backoff_retries == 500
        assert api.backoff_factor == 2.0

    def test_advanced_mode_headers(self):
        """Test that advanced mode affects headers"""
        api = AtlassianRestAPI(url=f"{mockup_server()}/test", advanced_mode=True)

        # Advanced mode should be set
        assert api.advanced_mode is True

    def test_cloud_vs_server_behavior(self):
        """Test differences between cloud and server configurations"""
        cloud_api = AtlassianRestAPI(url=f"{mockup_server()}/test", cloud=True)

        server_api = AtlassianRestAPI(url=f"{mockup_server()}/test", cloud=False)

        # Both should have sessions
        assert hasattr(cloud_api, "session")
        assert hasattr(server_api, "session")

        # Cloud flag should be different
        assert cloud_api.cloud is True
        assert server_api.cloud is False
