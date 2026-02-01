# coding=utf-8
"""
Test cases for request utilities used by v2 API implementation.

This test suite covers content format detection and validation utilities
that support the Confluence Cloud v2 API.
"""

from atlassian.request_utils import (
    is_adf_content,
    validate_adf_structure,
    get_content_type_header,
    detect_content_format,
)


class TestADFContentDetection:
    """Test cases for ADF content detection."""

    def test_is_adf_content_valid_adf(self):
        """Test detecting valid ADF content."""
        adf_content = {
            "version": 1,
            "type": "doc",
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Hello, World!"}]}],
        }
        assert is_adf_content(adf_content) is True

    def test_is_adf_content_invalid_type(self):
        """Test detecting content with invalid type field."""
        invalid_content = {"version": 1, "type": "invalid", "content": []}
        assert is_adf_content(invalid_content) is False

    def test_is_adf_content_invalid_version(self):
        """Test detecting content with invalid version field."""
        invalid_content = {"version": 2, "type": "doc", "content": []}
        assert is_adf_content(invalid_content) is False

    def test_is_adf_content_missing_content(self):
        """Test detecting content missing content field."""
        invalid_content = {"version": 1, "type": "doc"}
        assert is_adf_content(invalid_content) is False

    def test_is_adf_content_string_input(self):
        """Test detecting ADF content with string input."""
        assert is_adf_content("Hello, World!") is False
        assert is_adf_content("<p>Hello, World!</p>") is False

    def test_is_adf_content_none_input(self):
        """Test detecting ADF content with None input."""
        assert is_adf_content(None) is False

    def test_is_adf_content_list_input(self):
        """Test detecting ADF content with list input."""
        assert is_adf_content([]) is False
        assert is_adf_content([{"type": "doc"}]) is False

    def test_is_adf_content_empty_dict(self):
        """Test detecting ADF content with empty dictionary."""
        assert is_adf_content({}) is False


class TestADFStructureValidation:
    """Test cases for ADF structure validation."""

    def test_validate_adf_structure_valid(self):
        """Test validating valid ADF structure."""
        valid_adf = {
            "version": 1,
            "type": "doc",
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Hello, World!"}]}],
        }
        assert validate_adf_structure(valid_adf) is True

    def test_validate_adf_structure_minimal_valid(self):
        """Test validating minimal valid ADF structure."""
        minimal_adf = {"version": 1, "type": "doc", "content": []}
        assert validate_adf_structure(minimal_adf) is True

    def test_validate_adf_structure_invalid_type_field(self):
        """Test validating ADF structure with invalid type field."""
        invalid_adf = {"version": 1, "type": "paragraph", "content": []}  # Should be "doc"
        assert validate_adf_structure(invalid_adf) is False

    def test_validate_adf_structure_invalid_version_field(self):
        """Test validating ADF structure with invalid version field."""
        invalid_adf = {"version": 2, "type": "doc", "content": []}  # Should be 1
        assert validate_adf_structure(invalid_adf) is False

    def test_validate_adf_structure_missing_version(self):
        """Test validating ADF structure missing version field."""
        invalid_adf = {"type": "doc", "content": []}
        assert validate_adf_structure(invalid_adf) is False

    def test_validate_adf_structure_missing_type(self):
        """Test validating ADF structure missing type field."""
        invalid_adf = {"version": 1, "content": []}
        assert validate_adf_structure(invalid_adf) is False

    def test_validate_adf_structure_missing_content(self):
        """Test validating ADF structure missing content field."""
        invalid_adf = {"version": 1, "type": "doc"}
        assert validate_adf_structure(invalid_adf) is False

    def test_validate_adf_structure_invalid_content_type(self):
        """Test validating ADF structure with invalid content type."""
        invalid_adf = {"version": 1, "type": "doc", "content": "not a list"}
        assert validate_adf_structure(invalid_adf) is False

    def test_validate_adf_structure_non_dict_input(self):
        """Test validating non-dictionary input."""
        assert validate_adf_structure("not a dict") is False
        assert validate_adf_structure(None) is False
        assert validate_adf_structure([]) is False
        assert validate_adf_structure(123) is False


class TestContentTypeHeader:
    """Test cases for content type header generation."""

    def test_get_content_type_header_adf_content(self):
        """Test getting content type header for ADF content."""
        adf_content = {"version": 1, "type": "doc", "content": []}
        result = get_content_type_header(adf_content)
        assert result == "application/json"

    def test_get_content_type_header_string_content(self):
        """Test getting content type header for string content."""
        string_content = "Hello, World!"
        result = get_content_type_header(string_content)
        assert result == "application/json"

    def test_get_content_type_header_storage_content(self):
        """Test getting content type header for storage format content."""
        storage_content = "<p>Hello, World!</p>"
        result = get_content_type_header(storage_content)
        assert result == "application/json"

    def test_get_content_type_header_dict_content(self):
        """Test getting content type header for dictionary content."""
        dict_content = {"key": "value"}
        result = get_content_type_header(dict_content)
        assert result == "application/json"

    def test_get_content_type_header_none_content(self):
        """Test getting content type header for None content."""
        result = get_content_type_header(None)
        assert result == "application/json"


class TestContentFormatDetection:
    """Test cases for content format detection."""

    def test_detect_content_format_adf(self):
        """Test detecting ADF content format."""
        adf_content = {
            "version": 1,
            "type": "doc",
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Hello, World!"}]}],
        }
        result = detect_content_format(adf_content)
        assert result == "adf"

    def test_detect_content_format_storage(self):
        """Test detecting storage format content."""
        storage_content = "<p>Hello, World!</p>"
        result = detect_content_format(storage_content)
        assert result == "storage"

    def test_detect_content_format_storage_complex(self):
        """Test detecting complex storage format content."""
        storage_content = "<div><p>Hello, <strong>World</strong>!</p></div>"
        result = detect_content_format(storage_content)
        assert result == "storage"

    def test_detect_content_format_wiki(self):
        """Test detecting wiki format content."""
        wiki_content = "h1. Hello, World!"
        result = detect_content_format(wiki_content)
        assert result == "wiki"

    def test_detect_content_format_plain_text(self):
        """Test detecting plain text content."""
        plain_text = "Hello, World!"
        result = detect_content_format(plain_text)
        assert result == "wiki"  # Plain text is treated as wiki format

    def test_detect_content_format_empty_string(self):
        """Test detecting empty string content."""
        empty_string = ""
        result = detect_content_format(empty_string)
        assert result == "wiki"

    def test_detect_content_format_whitespace_string(self):
        """Test detecting whitespace-only string content."""
        whitespace_string = "   \n\t  "
        result = detect_content_format(whitespace_string)
        assert result == "wiki"

    def test_detect_content_format_invalid_adf(self):
        """Test detecting invalid ADF content format."""
        invalid_adf = {"version": 2, "type": "invalid", "content": []}
        result = detect_content_format(invalid_adf)
        assert result == "unknown"

    def test_detect_content_format_generic_dict(self):
        """Test detecting generic dictionary content."""
        generic_dict = {"key": "value", "another": "data"}
        result = detect_content_format(generic_dict)
        assert result == "unknown"

    def test_detect_content_format_none(self):
        """Test detecting None content format."""
        result = detect_content_format(None)
        assert result == "unknown"

    def test_detect_content_format_list(self):
        """Test detecting list content format."""
        list_content = [{"type": "paragraph"}]
        result = detect_content_format(list_content)
        assert result == "unknown"


class TestContentFormatEdgeCases:
    """Test cases for edge cases in content format detection."""

    def test_detect_format_html_like_but_not_storage(self):
        """Test detecting HTML-like content that's not storage format."""
        # Content that starts with < but might not be storage format
        pseudo_html = "<not-really-html>content</not-really-html>"
        result = detect_content_format(pseudo_html)
        assert result == "storage"  # Still detected as storage due to < prefix

    def test_detect_format_adf_missing_fields(self):
        """Test detecting ADF-like content missing required fields."""
        partial_adf = {
            "type": "doc",
            "content": [],
            # Missing version field
        }
        result = detect_content_format(partial_adf)
        assert result == "unknown"

    def test_detect_format_adf_wrong_version(self):
        """Test detecting ADF-like content with wrong version."""
        wrong_version_adf = {"version": 2, "type": "doc", "content": []}  # Wrong version
        result = detect_content_format(wrong_version_adf)
        assert result == "unknown"

    def test_detect_format_complex_nested_dict(self):
        """Test detecting complex nested dictionary."""
        complex_dict = {
            "data": {"nested": {"content": [{"item": "value"}]}},
            "metadata": {"version": 1, "type": "custom"},
        }
        result = detect_content_format(complex_dict)
        assert result == "unknown"

    def test_is_adf_content_with_extra_fields(self):
        """Test ADF detection with extra fields."""
        adf_with_extras = {
            "version": 1,
            "type": "doc",
            "content": [],
            "extra_field": "should not affect detection",
            "metadata": {"custom": "data"},
        }
        assert is_adf_content(adf_with_extras) is True

    def test_validate_adf_structure_with_extra_fields(self):
        """Test ADF structure validation with extra fields."""
        adf_with_extras = {"version": 1, "type": "doc", "content": [], "extra_field": "should not affect validation"}
        assert validate_adf_structure(adf_with_extras) is True


class TestContentFormatIntegration:
    """Integration tests for content format utilities."""

    def test_format_detection_workflow(self):
        """Test complete workflow of format detection and validation."""
        # Test different content types through the workflow
        test_cases = [
            # (content, expected_format, should_be_adf)
            ({"version": 1, "type": "doc", "content": [{"type": "paragraph", "content": []}]}, "adf", True),
            ("<p>Storage format content</p>", "storage", False),
            ("Plain text content", "wiki", False),
            ({"custom": "data"}, "unknown", False),
        ]

        for content, expected_format, should_be_adf in test_cases:
            # Test format detection
            detected_format = detect_content_format(content)
            assert detected_format == expected_format, f"Failed for content: {content}"

            # Test ADF detection
            is_adf = is_adf_content(content)
            assert is_adf == should_be_adf, f"ADF detection failed for content: {content}"

            # Test content type header (should always be JSON for our use cases)
            content_type = get_content_type_header(content)
            assert content_type == "application/json"

    def test_adf_validation_consistency(self):
        """Test consistency between ADF detection and validation."""
        test_contents = [
            # Valid ADF
            {"version": 1, "type": "doc", "content": []},
            # Invalid ADF - wrong type
            {"version": 1, "type": "paragraph", "content": []},
            # Invalid ADF - wrong version
            {"version": 2, "type": "doc", "content": []},
            # Invalid ADF - missing content
            {"version": 1, "type": "doc"},
            # Non-dict content
            "not a dict",
            None,
            [],
        ]

        for content in test_contents:
            is_adf = is_adf_content(content)
            is_valid_structure = validate_adf_structure(content) if isinstance(content, dict) else False

            # If content is detected as ADF, it should have valid structure
            if is_adf:
                assert is_valid_structure, f"ADF content should have valid structure: {content}"

            # If structure is valid, it should be detected as ADF
            if is_valid_structure:
                assert is_adf, f"Valid ADF structure should be detected as ADF: {content}"
