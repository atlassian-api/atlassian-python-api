# coding: utf-8
"""
Unit tests for atlassian.errors module
"""

from atlassian.errors import (
    ApiError,
    JsonRPCError,
    ApiNotFoundError,
    ApiPermissionError,
    ApiValueError,
    ApiConflictError,
    ApiNotAcceptable,
    JsonRPCRestrictionsError,
)


class TestApiError:
    """Test cases for ApiError class"""

    def test_init_with_message(self):
        """Test initialization with message only"""
        error = ApiError("Test error message")
        assert str(error) == "Test error message"
        assert error.reason is None

    def test_init_with_reason(self):
        """Test initialization with reason"""
        error = ApiError("Test error message", reason="Test reason")
        assert str(error) == "Test error message"
        assert error.reason == "Test reason"

    def test_init_with_args(self):
        """Test initialization with multiple args"""
        error = ApiError("Error", "arg1", "arg2", reason="Test reason")
        assert str(error) == "('Error', 'arg1', 'arg2')"
        assert error.reason == "Test reason"

    def test_inheritance(self):
        """Test that ApiError inherits from Exception"""
        error = ApiError("Test error")
        assert isinstance(error, Exception)


class TestJsonRPCError:
    """Test cases for JsonRPCError class"""

    def test_init_with_message(self):
        """Test initialization with message only"""
        error = JsonRPCError("Test JSON-RPC error message")
        assert str(error) == "Test JSON-RPC error message"

    def test_init_with_args(self):
        """Test initialization with multiple args"""
        error = JsonRPCError("Error", "arg1", "arg2")
        assert str(error) == "('Error', 'arg1', 'arg2')"

    def test_inheritance(self):
        """Test that JsonRPCError inherits from Exception"""
        error = JsonRPCError("Test error")
        assert isinstance(error, Exception)


class TestApiNotFoundError:
    """Test cases for ApiNotFoundError class"""

    def test_init_with_message(self):
        """Test initialization with message only"""
        error = ApiNotFoundError("Resource not found")
        assert str(error) == "Resource not found"
        assert error.reason is None

    def test_init_with_reason(self):
        """Test initialization with reason"""
        error = ApiNotFoundError("Resource not found", reason="404 Not Found")
        assert str(error) == "Resource not found"
        assert error.reason == "404 Not Found"

    def test_inheritance(self):
        """Test that ApiNotFoundError inherits from ApiError"""
        error = ApiNotFoundError("Test error")
        assert isinstance(error, ApiError)
        assert isinstance(error, Exception)


class TestApiPermissionError:
    """Test cases for ApiPermissionError class"""

    def test_init_with_message(self):
        """Test initialization with message only"""
        error = ApiPermissionError("Permission denied")
        assert str(error) == "Permission denied"
        assert error.reason is None

    def test_init_with_reason(self):
        """Test initialization with reason"""
        error = ApiPermissionError("Permission denied", reason="403 Forbidden")
        assert str(error) == "Permission denied"
        assert error.reason == "403 Forbidden"

    def test_inheritance(self):
        """Test that ApiPermissionError inherits from ApiError"""
        error = ApiPermissionError("Test error")
        assert isinstance(error, ApiError)
        assert isinstance(error, Exception)


class TestApiValueError:
    """Test cases for ApiValueError class"""

    def test_init_with_message(self):
        """Test initialization with message only"""
        error = ApiValueError("Invalid value")
        assert str(error) == "Invalid value"
        assert error.reason is None

    def test_init_with_reason(self):
        """Test initialization with reason"""
        error = ApiValueError("Invalid value", reason="400 Bad Request")
        assert str(error) == "Invalid value"
        assert error.reason == "400 Bad Request"

    def test_inheritance(self):
        """Test that ApiValueError inherits from ApiError"""
        error = ApiValueError("Test error")
        assert isinstance(error, ApiError)
        assert isinstance(error, Exception)


class TestApiConflictError:
    """Test cases for ApiConflictError class"""

    def test_init_with_message(self):
        """Test initialization with message only"""
        error = ApiConflictError("Resource conflict")
        assert str(error) == "Resource conflict"
        assert error.reason is None

    def test_init_with_reason(self):
        """Test initialization with reason"""
        error = ApiConflictError("Resource conflict", reason="409 Conflict")
        assert str(error) == "Resource conflict"
        assert error.reason == "409 Conflict"

    def test_inheritance(self):
        """Test that ApiConflictError inherits from ApiError"""
        error = ApiConflictError("Test error")
        assert isinstance(error, ApiError)
        assert isinstance(error, Exception)


class TestApiNotAcceptable:
    """Test cases for ApiNotAcceptable class"""

    def test_init_with_message(self):
        """Test initialization with message only"""
        error = ApiNotAcceptable("Not acceptable")
        assert str(error) == "Not acceptable"
        assert error.reason is None

    def test_init_with_reason(self):
        """Test initialization with reason"""
        error = ApiNotAcceptable("Not acceptable", reason="406 Not Acceptable")
        assert str(error) == "Not acceptable"
        assert error.reason == "406 Not Acceptable"

    def test_inheritance(self):
        """Test that ApiNotAcceptable inherits from ApiError"""
        error = ApiNotAcceptable("Test error")
        assert isinstance(error, ApiError)
        assert isinstance(error, Exception)


class TestJsonRPCRestrictionsError:
    """Test cases for JsonRPCRestrictionsError class"""

    def test_init_with_message(self):
        """Test initialization with message only"""
        error = JsonRPCRestrictionsError("RPC restrictions")
        assert str(error) == "RPC restrictions"

    def test_init_with_args(self):
        """Test initialization with multiple args"""
        error = JsonRPCRestrictionsError("Error", "arg1", "arg2")
        assert str(error) == "('Error', 'arg1', 'arg2')"

    def test_inheritance(self):
        """Test that JsonRPCRestrictionsError inherits from JsonRPCError"""
        error = JsonRPCRestrictionsError("Test error")
        assert isinstance(error, JsonRPCError)
        assert isinstance(error, Exception)


class TestErrorHierarchy:
    """Test cases for error class hierarchy"""

    def test_error_inheritance_chain(self):
        """Test the complete inheritance chain of all error classes"""
        # Test ApiError inheritance
        api_error = ApiError("Test")
        assert isinstance(api_error, Exception)

        # Test JsonRPCError inheritance
        jsonrpc_error = JsonRPCError("Test")
        assert isinstance(jsonrpc_error, Exception)

        # Test specific API error inheritance
        not_found_error = ApiNotFoundError("Test")
        assert isinstance(not_found_error, ApiError)
        assert isinstance(not_found_error, Exception)

        permission_error = ApiPermissionError("Test")
        assert isinstance(permission_error, ApiError)
        assert isinstance(permission_error, Exception)

        value_error = ApiValueError("Test")
        assert isinstance(value_error, ApiError)
        assert isinstance(value_error, Exception)

        conflict_error = ApiConflictError("Test")
        assert isinstance(conflict_error, ApiError)
        assert isinstance(conflict_error, Exception)

        not_acceptable_error = ApiNotAcceptable("Test")
        assert isinstance(not_acceptable_error, ApiError)
        assert isinstance(not_acceptable_error, Exception)

        # Test JsonRPC error inheritance
        rpc_restrictions_error = JsonRPCRestrictionsError("Test")
        assert isinstance(rpc_restrictions_error, JsonRPCError)
        assert isinstance(rpc_restrictions_error, Exception)

    def test_error_attributes(self):
        """Test that error attributes are properly set"""
        # Test ApiError with reason
        error = ApiError("Test message", reason="Test reason")
        assert error.reason == "Test reason"

        # Test that other errors can also have reason
        not_found_error = ApiNotFoundError("Not found", reason="404")
        assert not_found_error.reason == "404"

        permission_error = ApiPermissionError("Forbidden", reason="403")
        assert permission_error.reason == "403"

    def test_error_string_representation(self):
        """Test string representation of errors"""
        # Test basic error
        error = ApiError("Test error message")
        assert str(error) == "Test error message"

        # Test error with reason
        error_with_reason = ApiError("Test error", reason="Test reason")
        assert str(error_with_reason) == "Test error"

        # Test JSON-RPC error
        jsonrpc_error = JsonRPCError("JSON-RPC error")
        assert str(jsonrpc_error) == "JSON-RPC error"

    def test_error_equality(self):
        """Test error equality and comparison"""
        error1 = ApiError("Same message")
        error2 = ApiError("Same message")
        error3 = ApiError("Different message")

        # Errors with same message should not be equal (different instances)
        assert error1 != error2
        assert error1 != error3

        # Test that errors are not equal to non-error objects
        assert error1 != "Same message"
        assert error1 != 123

    def test_error_hashability(self):
        """Test that errors can be used as dictionary keys or in sets"""
        error1 = ApiError("Error 1")
        error2 = ApiError("Error 2")

        # Test dictionary usage
        error_dict = {error1: "value1", error2: "value2"}
        assert error_dict[error1] == "value1"
        assert error_dict[error2] == "value2"

        # Test set usage
        error_set = {error1, error2}
        assert error1 in error_set
        assert error2 in error_set
        assert len(error_set) == 2
