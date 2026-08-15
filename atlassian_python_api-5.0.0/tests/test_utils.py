# coding: utf-8
"""
Unit tests for atlassian.utils module
"""

import pytest
from .mockup import mockup_server
from atlassian.utils import is_email, html_email, html_list, html_table_header_row, html_row_with_ordered_headers


class TestIsEmail:
    """Test cases for is_email function"""

    def test_valid_emails(self):
        """Test valid email addresses"""
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.com",
            "user@subdomain.example.com",
            "user@example.co.uk",
            "user@example-domain.com",
            "user123@example.com",
            "user@123example.com",
        ]

        for email in valid_emails:
            result = is_email(email)
            assert result is not None, f"Email {email} should be valid"

    def test_invalid_emails(self):
        """Test invalid email addresses"""
        invalid_emails = [
            "user@",
            "@example.com",
            "user.example.com",
            "user@example@com",
            "user@@example.com",
            "user@example.com@",
            "",
            None,
            {},
            True,
            False,
        ]

        for email in invalid_emails:
            result = is_email(email)
            assert result is None, f"Email {email} should be invalid"

    def test_edge_cases(self):
        """Test edge cases for email validation"""
        edge_cases = [
            ("user@example.com", True),  # Standard valid email
            ("user@example", False),  # Missing TLD
            ("user@example..com", True),  # Double dots - actually allowed by the regex
            ("user@example.com.", True),  # Trailing dot - actually allowed by the regex
            ("user@.example.com", True),  # Empty subdomain - actually allowed by the regex
            ("user@example_.com", True),  # Trailing underscore in domain - actually allowed by the regex
        ]

        for email, expected in edge_cases:
            result = is_email(email)
            if expected:
                assert result is not None, f"Email {email} should be valid"
            else:
                assert result is None, f"Email {email} should be invalid"

    def test_international_domains(self):
        """Test international domain names"""
        international_domains = [
            "user@example.br",
            "user@example.in",
            "user@example.mx",
        ]

        for email in international_domains:
            result = is_email(email)
            assert result is not None, f"International email {email} should be valid"

    def test_subdomain_emails(self):
        """Test emails with subdomains"""
        subdomain_emails = [
            "user@a.b.c.d.example.com",
            "user@sub-domain.example.com",
            "user@sub_domain.example.com",
        ]

        for email in subdomain_emails:
            result = is_email(email)
            assert result is not None, f"Subdomain email {email} should be valid"


class TestHtmlEmail:
    """Test cases for html_email function"""

    def test_basic_email_link(self):
        """Test basic email link generation"""
        result = html_email("user@example.com")
        expected = '<a href="mailto:user@example.com">user@example.com</a>'
        assert result == expected

    def test_email_with_title(self):
        """Test email link with custom title"""
        result = html_email("user@example.com", "Contact User")
        expected = '<a href="mailto:user@example.com">Contact User</a>'
        assert result == expected

    def test_email_without_title(self):
        """Test email link without title"""
        result = html_email("user@example.com", title=None)
        expected = '<a href="mailto:user@example.com">user@example.com</a>'
        assert result == expected

    def test_special_characters_in_title(self):
        """Test email link with special characters in title"""
        result = html_email("user@example.com", "User's Contact & Info")
        expected = '<a href="mailto:user@example.com">User\'s Contact & Info</a>'
        assert result == expected


class TestHtmlList:
    """Test cases for html_list function"""

    def test_basic_list(self):
        """Test basic HTML list generation"""
        data = ["item1", "item2", "item3"]
        result = html_list(data)
        expected = "<ul><li>item1</li><li>item2</li><li>item3</li></ul>"
        assert result == expected

    def test_list_with_emails(self):
        """Test HTML list generation with email addresses"""
        data = ["user1@example.com", "user2@example.com", "user3@example.com"]
        result = html_list(data)
        expected = (
            "<ul>"
            '<li><a href="mailto:user1@example.com">user1@example.com</a></li>'
            '<li><a href="mailto:user2@example.com">user2@example.com</a></li>'
            '<li><a href="mailto:user3@example.com">user3@example.com</a></li>'
            "</ul>"
        )
        assert result == expected

    def test_list_with_dicts(self):
        """Test HTML list generation with dictionaries"""
        data = [
            {"email": "user1@example.com", "name": "User 1"},
            {"email": "user2@example.com", "name": "User 2"},
            {"name": "User 3", "email": "user3@example.com"},
        ]
        result = html_list(data)
        expected = (
            "<ul>"
            '<li><a href="mailto:user1@example.com">User 1</a></li>'
            '<li><a href="mailto:user2@example.com">User 2</a></li>'
            '<li><a href="mailto:user3@example.com">User 3</a></li>'
            "</ul>"
        )
        assert result == expected

    def test_list_with_dicts_name_only(self):
        """Test HTML list generation with dictionaries that have name but no email"""
        data = [{"name": "User 1"}, {"email": "user2@example.com", "name": "User 2"}, {"name": "User 3"}]
        result = html_list(data)
        expected = (
            "<ul>" "<li>User 1</li>" '<li><a href="mailto:user2@example.com">User 2</a></li>' "<li>User 3</li>" "</ul>"
        )
        assert result == expected

    def test_mixed_content(self):
        """Test HTML list generation with mixed content types"""
        data = [
            "plain_text",
            "user@example.com",
            {"email": "dict@example.com", "name": "Dict User"},
            {"name": "Name Only"},
            "another@example.com",
        ]
        result = html_list(data)
        expected = (
            "<ul>"
            "<li>plain_text</li>"
            '<li><a href="mailto:user@example.com">user@example.com</a></li>'
            '<li><a href="mailto:dict@example.com">Dict User</a></li>'
            "<li>Name Only</li>"
            '<li><a href="mailto:another@example.com">another@example.com</a></li>'
            "</ul>"
        )
        assert result == expected

    def test_empty_list(self):
        """Test HTML list generation with empty list"""
        result = html_list([])
        expected = "<ul></ul>"
        assert result == expected

    def test_single_item(self):
        """Test HTML list generation with single item"""
        result = html_list(["single_item"])
        expected = "<ul><li>single_item</li></ul>"
        assert result == expected

    def test_non_string_items(self):
        """Test HTML list generation with non-string items"""
        data = [123, True, None, {"key": "value"}]
        result = html_list(data)
        expected = "<ul><li>123</li><li>True</li><li>None</li><li>{'key': 'value'}</li></ul>"
        assert result == expected


class TestHtmlTableHeaderRow:
    """Test cases for html_table_header_row function"""

    def test_basic_header_row(self):
        """Test basic HTML table header row generation"""
        headers = ["Name", "Email", "Role"]
        result = html_table_header_row(headers)
        expected = "\n\t<tr><th>Name</th><th>Email</th><th>Role</th></tr>"
        assert result == expected

    def test_headers_with_underscores(self):
        """Test headers with underscores (common in data)"""
        headers = ["user_name", "email_address", "user_role"]
        result = html_table_header_row(headers)
        expected = "\n\t<tr><th>User Name</th><th>Email Address</th><th>User Role</th></tr>"
        assert result == expected

    def test_single_header(self):
        """Test single header column"""
        headers = ["Single"]
        result = html_table_header_row(headers)
        expected = "\n\t<tr><th>Single</th></tr>"
        assert result == expected

    def test_empty_headers(self):
        """Test empty headers list"""
        result = html_table_header_row([])
        expected = "\n\t<tr></tr>"
        assert result == expected

    def test_special_characters(self):
        """Test headers with special characters"""
        headers = ["User's Name", "Email & Contact", "Role (Admin)"]
        result = html_table_header_row(headers)
        expected = "\n\t<tr><th>User'S Name</th><th>Email & Contact</th><th>Role (Admin)</th></tr>"
        assert result == expected


class TestHtmlRowWithOrderedHeaders:
    """Test cases for html_row_with_ordered_headers function"""

    def test_basic_row_generation(self):
        """Test basic HTML row generation with ordered headers"""
        headers = ["name", "email", "role"]
        data = {"name": "John Doe", "email": "john@example.com", "role": "Admin"}
        result = html_row_with_ordered_headers(data, headers)
        expected = '\n\t<tr><td>John Doe</td><td><a href="mailto:john@example.com">john@example.com</a></td><td>Admin</td></tr>'
        assert result == expected

    def test_row_with_row_header(self):
        """Test HTML row generation with row header"""
        headers = ["name", "email", "role"]
        data = {"name": "John Doe", "email": "john@example.com", "role": "Admin"}
        row_header = "User"
        result = html_row_with_ordered_headers(data, headers, row_header)
        expected = '\n\t<tr><th>User</th><td>John Doe</td><td><a href="mailto:john@example.com">john@example.com</a></td><td>Admin</td></tr>'
        assert result == expected

    def test_row_with_lists(self):
        """Test HTML row generation with list values"""
        headers = ["name", "emails", "roles"]
        data = {"name": "John Doe", "emails": ["john@example.com", "jdoe@example.com"], "roles": ["Admin", "User"]}
        result = html_row_with_ordered_headers(data, headers)
        expected = (
            "\n\t<tr>"
            "<td>John Doe</td>"
            '<td><ul><li><a href="mailto:john@example.com">john@example.com</a></li><li><a href="mailto:jdoe@example.com">jdoe@example.com</a></li></ul></td>'
            "<td><ul><li>Admin</li><li>User</li></ul></td>"
            "</tr>"
        )
        assert result == expected

    def test_missing_keys(self):
        """Test HTML row generation with missing data keys"""
        headers = ["name", "email", "role", "department"]
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            # Missing role and department
        }

        with pytest.raises(KeyError):
            html_row_with_ordered_headers(data, headers)

    def test_empty_data(self):
        """Test HTML row generation with empty data"""
        headers = ["name", "email"]
        data = {}

        with pytest.raises(KeyError):
            html_row_with_ordered_headers(data, headers)

    def test_complex_data(self):
        """Test HTML row generation with complex nested data"""
        headers = ["name", "contact_info", "permissions"]
        data = {
            "name": "Jane Smith",
            "contact_info": {"email": "jane@example.com", "phone": "555-1234"},
            "permissions": ["read", "write", "admin"],
        }

        # This should handle the nested dict and list appropriately
        result = html_row_with_ordered_headers(data, headers)
        assert "Jane Smith" in result
        assert "jane@example.com" in result
        assert "555-1234" in result
        assert "read" in result
        assert "write" in result
        assert "admin" in result

    def test_email_detection(self):
        """Test that email detection works correctly in ordered headers"""
        headers = ["name", "email", "backup_email"]
        data = {"name": "Test User", "email": "test@example.com", "backup_email": "backup@example.com"}
        result = html_row_with_ordered_headers(data, headers)

        # Both emails should be converted to mailto links
        assert '<a href="mailto:test@example.com">test@example.com</a>' in result
        assert '<a href="mailto:backup@example.com">backup@example.com</a>' in result
        assert "Test User" in result  # Non-email should remain as text

    def test_mockup_integration(self):
        """Test that utils work with the mockup system"""
        # This test ensures that our utility functions don't interfere with the mockup system
        mockup_url = mockup_server()
        assert isinstance(mockup_url, str)
        assert len(mockup_url) > 0

        # Test that our utility functions still work
        result = is_email("test@example.com")
        assert result is not None
        assert html_email("test@example.com") == '<a href="mailto:test@example.com">test@example.com</a>'
