# coding=utf-8
"""
Test cases for ADF (Atlassian Document Format) utilities.

This test suite covers ADF document creation, validation, and conversion utilities
used by the Confluence Cloud v2 API implementation.
"""

import pytest
from atlassian.adf import (
    ADFNode,
    ADFDocument,
    ADFParagraph,
    ADFText,
    ADFHeading,
    create_simple_adf_document,
    validate_adf_document,
    convert_text_to_adf,
    convert_storage_to_adf,
    convert_adf_to_storage,
    validate_content_format,
)


class TestADFNode:
    """Test cases for ADFNode base class."""

    def test_create_basic_node(self):
        """Test creating a basic ADF node."""
        node = ADFNode("paragraph")
        assert node.type == "paragraph"
        assert node.attrs == {}
        assert node.content == []
        assert node.text is None
        assert node.marks == []

    def test_create_node_with_attributes(self):
        """Test creating an ADF node with attributes."""
        attrs = {"level": 1}
        node = ADFNode("heading", attrs=attrs)
        assert node.type == "heading"
        assert node.attrs == attrs

    def test_create_node_with_content(self):
        """Test creating an ADF node with content."""
        content = [{"type": "text", "text": "Hello"}]
        node = ADFNode("paragraph", content=content)
        assert node.type == "paragraph"
        assert node.content == content

    def test_create_text_node(self):
        """Test creating a text node."""
        node = ADFNode("text", text="Hello, World!")
        assert node.type == "text"
        assert node.text == "Hello, World!"

    def test_node_to_dict_basic(self):
        """Test converting basic node to dictionary."""
        node = ADFNode("paragraph")
        result = node.to_dict()
        expected = {"type": "paragraph"}
        assert result == expected

    def test_node_to_dict_with_attributes(self):
        """Test converting node with attributes to dictionary."""
        node = ADFNode("heading", attrs={"level": 2})
        result = node.to_dict()
        expected = {"type": "heading", "attrs": {"level": 2}}
        assert result == expected

    def test_node_to_dict_with_text(self):
        """Test converting text node to dictionary."""
        node = ADFNode("text", text="Hello, World!")
        result = node.to_dict()
        expected = {"type": "text", "text": "Hello, World!"}
        assert result == expected

    def test_node_to_dict_with_marks(self):
        """Test converting node with marks to dictionary."""
        marks = [{"type": "strong"}]
        node = ADFNode("text", text="Bold text", marks=marks)
        result = node.to_dict()
        expected = {"type": "text", "text": "Bold text", "marks": marks}
        assert result == expected

    def test_node_to_dict_with_nested_content(self):
        """Test converting node with nested content to dictionary."""
        text_node = ADFNode("text", text="Hello")
        paragraph = ADFNode("paragraph", content=[text_node])
        result = paragraph.to_dict()
        expected = {"type": "paragraph", "content": [{"type": "text", "text": "Hello"}]}
        assert result == expected


class TestADFDocument:
    """Test cases for ADFDocument class."""

    def test_create_empty_document(self):
        """Test creating an empty ADF document."""
        doc = ADFDocument()
        assert doc.version == 1
        assert doc.type == "doc"
        assert doc.content == []

    def test_create_document_with_content(self):
        """Test creating an ADF document with initial content."""
        text_node = ADFText("Hello, World!")
        paragraph = ADFParagraph([text_node])
        doc = ADFDocument([paragraph])
        assert len(doc.content) == 1
        assert doc.content[0] == paragraph

    def test_add_content_to_document(self):
        """Test adding content to an ADF document."""
        doc = ADFDocument()
        text_node = ADFText("Hello, World!")
        paragraph = ADFParagraph([text_node])
        doc.add_content(paragraph)
        assert len(doc.content) == 1
        assert doc.content[0] == paragraph

    def test_document_to_dict(self):
        """Test converting ADF document to dictionary."""
        text_node = ADFText("Hello, World!")
        paragraph = ADFParagraph([text_node])
        doc = ADFDocument([paragraph])
        result = doc.to_dict()
        expected = {
            "version": 1,
            "type": "doc",
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Hello, World!"}]}],
        }
        assert result == expected


class TestADFParagraph:
    """Test cases for ADFParagraph class."""

    def test_create_empty_paragraph(self):
        """Test creating an empty paragraph."""
        paragraph = ADFParagraph()
        assert paragraph.type == "paragraph"
        assert paragraph.content == []

    def test_create_paragraph_with_text(self):
        """Test creating a paragraph with text content."""
        text_node = ADFText("Hello, World!")
        paragraph = ADFParagraph([text_node])
        assert paragraph.type == "paragraph"
        assert len(paragraph.content) == 1
        assert paragraph.content[0] == text_node

    def test_paragraph_to_dict(self):
        """Test converting paragraph to dictionary."""
        text_node = ADFText("Hello, World!")
        paragraph = ADFParagraph([text_node])
        result = paragraph.to_dict()
        expected = {"type": "paragraph", "content": [{"type": "text", "text": "Hello, World!"}]}
        assert result == expected


class TestADFText:
    """Test cases for ADFText class."""

    def test_create_simple_text(self):
        """Test creating simple text node."""
        text_node = ADFText("Hello, World!")
        assert text_node.type == "text"
        assert text_node.text == "Hello, World!"
        assert text_node.marks == []

    def test_create_text_with_marks(self):
        """Test creating text node with formatting marks."""
        marks = [{"type": "strong"}, {"type": "em"}]
        text_node = ADFText("Bold and italic", marks)
        assert text_node.type == "text"
        assert text_node.text == "Bold and italic"
        assert text_node.marks == marks

    def test_text_to_dict(self):
        """Test converting text node to dictionary."""
        text_node = ADFText("Hello, World!")
        result = text_node.to_dict()
        expected = {"type": "text", "text": "Hello, World!"}
        assert result == expected

    def test_text_with_marks_to_dict(self):
        """Test converting text node with marks to dictionary."""
        marks = [{"type": "strong"}]
        text_node = ADFText("Bold text", marks)
        result = text_node.to_dict()
        expected = {"type": "text", "text": "Bold text", "marks": marks}
        assert result == expected


class TestADFHeading:
    """Test cases for ADFHeading class."""

    def test_create_heading_level_1(self):
        """Test creating a level 1 heading."""
        text_node = ADFText("Main Title")
        heading = ADFHeading(1, [text_node])
        assert heading.type == "heading"
        assert heading.attrs == {"level": 1}
        assert len(heading.content) == 1

    def test_create_heading_level_6(self):
        """Test creating a level 6 heading."""
        text_node = ADFText("Subtitle")
        heading = ADFHeading(6, [text_node])
        assert heading.type == "heading"
        assert heading.attrs == {"level": 6}

    def test_create_heading_invalid_level_low(self):
        """Test creating heading with invalid level (too low)."""
        with pytest.raises(ValueError, match="Heading level must be between 1 and 6"):
            ADFHeading(0, [])

    def test_create_heading_invalid_level_high(self):
        """Test creating heading with invalid level (too high)."""
        with pytest.raises(ValueError, match="Heading level must be between 1 and 6"):
            ADFHeading(7, [])

    def test_heading_to_dict(self):
        """Test converting heading to dictionary."""
        text_node = ADFText("Chapter Title")
        heading = ADFHeading(2, [text_node])
        result = heading.to_dict()
        expected = {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Chapter Title"}]}
        assert result == expected


class TestADFUtilityFunctions:
    """Test cases for ADF utility functions."""

    def test_create_simple_adf_document(self):
        """Test creating a simple ADF document from text."""
        text = "Hello, World!"
        doc = create_simple_adf_document(text)

        assert isinstance(doc, ADFDocument)
        assert doc.version == 1
        assert doc.type == "doc"
        assert len(doc.content) == 1

        paragraph = doc.content[0]
        assert isinstance(paragraph, ADFParagraph)
        assert len(paragraph.content) == 1

        text_node = paragraph.content[0]
        assert isinstance(text_node, ADFText)
        assert text_node.text == text

    def test_validate_adf_document_valid(self):
        """Test validating a valid ADF document."""
        valid_adf = {
            "version": 1,
            "type": "doc",
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Hello, World!"}]}],
        }
        assert validate_adf_document(valid_adf) is True

    def test_validate_adf_document_invalid_type(self):
        """Test validating ADF document with invalid type."""
        invalid_adf = {"version": 1, "type": "invalid", "content": []}
        assert validate_adf_document(invalid_adf) is False

    def test_validate_adf_document_invalid_version(self):
        """Test validating ADF document with invalid version."""
        invalid_adf = {"version": 2, "type": "doc", "content": []}
        assert validate_adf_document(invalid_adf) is False

    def test_validate_adf_document_missing_content(self):
        """Test validating ADF document missing content field."""
        invalid_adf = {"version": 1, "type": "doc"}
        assert validate_adf_document(invalid_adf) is False

    def test_validate_adf_document_invalid_content_type(self):
        """Test validating ADF document with invalid content type."""
        invalid_adf = {"version": 1, "type": "doc", "content": "not a list"}
        assert validate_adf_document(invalid_adf) is False

    def test_validate_adf_document_not_dict(self):
        """Test validating non-dictionary input."""
        assert validate_adf_document("not a dict") is False
        assert validate_adf_document(None) is False
        assert validate_adf_document([]) is False

    def test_convert_text_to_adf(self):
        """Test converting plain text to ADF format."""
        text = "Hello, World!"
        result = convert_text_to_adf(text)

        assert validate_adf_document(result)
        assert result["version"] == 1
        assert result["type"] == "doc"
        assert len(result["content"]) == 1

        paragraph = result["content"][0]
        assert paragraph["type"] == "paragraph"
        assert len(paragraph["content"]) == 1

        text_node = paragraph["content"][0]
        assert text_node["type"] == "text"
        assert text_node["text"] == text

    def test_convert_empty_text_to_adf(self):
        """Test converting empty text to ADF format."""
        result = convert_text_to_adf("")

        assert validate_adf_document(result)
        # Should still create a valid document structure
        assert result["version"] == 1
        assert result["type"] == "doc"

    def test_convert_storage_to_adf_simple(self):
        """Test converting simple storage format to ADF."""
        storage_content = "<p>Hello, World!</p>"
        result = convert_storage_to_adf(storage_content)

        assert validate_adf_document(result)
        assert result["version"] == 1
        assert result["type"] == "doc"

    def test_convert_storage_to_adf_with_tags(self):
        """Test converting storage format with HTML tags to ADF."""
        storage_content = "<p>Hello, <strong>World</strong>!</p>"
        result = convert_storage_to_adf(storage_content)

        assert validate_adf_document(result)
        # Basic conversion should strip HTML tags
        assert result["version"] == 1
        assert result["type"] == "doc"

    def test_convert_storage_to_adf_empty(self):
        """Test converting empty storage format to ADF."""
        storage_content = "<p></p>"
        result = convert_storage_to_adf(storage_content)

        assert validate_adf_document(result)
        assert result["version"] == 1
        assert result["type"] == "doc"

    def test_convert_adf_to_storage_simple(self):
        """Test converting simple ADF to storage format."""
        adf_content = {
            "version": 1,
            "type": "doc",
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Hello, World!"}]}],
        }
        result = convert_adf_to_storage(adf_content)

        assert isinstance(result, str)
        assert "Hello, World!" in result
        assert result.startswith("<p>")
        assert result.endswith("</p>")

    def test_convert_adf_to_storage_multiple_paragraphs(self):
        """Test converting ADF with multiple paragraphs to storage format."""
        adf_content = {
            "version": 1,
            "type": "doc",
            "content": [
                {"type": "paragraph", "content": [{"type": "text", "text": "First paragraph"}]},
                {"type": "paragraph", "content": [{"type": "text", "text": "Second paragraph"}]},
            ],
        }
        result = convert_adf_to_storage(adf_content)

        assert isinstance(result, str)
        assert "First paragraph" in result
        assert "Second paragraph" in result

    def test_convert_adf_to_storage_invalid_adf(self):
        """Test converting invalid ADF to storage format raises error."""
        invalid_adf = {"type": "invalid", "content": []}

        with pytest.raises(ValueError, match="Invalid ADF document structure"):
            convert_adf_to_storage(invalid_adf)

    def test_convert_adf_to_storage_empty_content(self):
        """Test converting ADF with empty content to storage format."""
        adf_content = {"version": 1, "type": "doc", "content": []}
        result = convert_adf_to_storage(adf_content)

        assert isinstance(result, str)
        assert "Empty content" in result

    def test_validate_content_format_adf(self):
        """Test validating ADF content format."""
        adf_content = {"version": 1, "type": "doc", "content": []}
        assert validate_content_format(adf_content, "adf") is True
        assert validate_content_format(adf_content, "storage") is False
        assert validate_content_format(adf_content, "wiki") is False

    def test_validate_content_format_storage(self):
        """Test validating storage content format."""
        storage_content = "<p>Hello, World!</p>"
        assert validate_content_format(storage_content, "storage") is True
        assert validate_content_format(storage_content, "adf") is False
        assert validate_content_format(storage_content, "wiki") is True  # Also valid as wiki

    def test_validate_content_format_wiki(self):
        """Test validating wiki content format."""
        wiki_content = "h1. Hello, World!"
        assert validate_content_format(wiki_content, "wiki") is True
        assert validate_content_format(wiki_content, "adf") is False
        assert validate_content_format(wiki_content, "storage") is False

    def test_validate_content_format_invalid(self):
        """Test validating content with invalid format."""
        content = "Hello, World!"
        assert validate_content_format(content, "invalid") is False

    def test_validate_content_format_wrong_type(self):
        """Test validating content with wrong type for format."""
        # String content for ADF format should fail
        assert validate_content_format("Hello", "adf") is False

        # Dict content for storage format should fail
        assert validate_content_format({"test": "data"}, "storage") is False


class TestADFComplexScenarios:
    """Test cases for complex ADF scenarios."""

    def test_complex_adf_document(self):
        """Test creating and validating a complex ADF document."""
        # Create a document with heading, paragraph, and formatted text
        heading_text = ADFText("Chapter 1: Introduction")
        heading = ADFHeading(1, [heading_text])

        plain_text = ADFText("This is a regular paragraph with ")
        bold_text = ADFText("bold text", [{"type": "strong"}])
        more_text = ADFText(" and some more content.")
        paragraph = ADFParagraph([plain_text, bold_text, more_text])

        doc = ADFDocument([heading, paragraph])
        result = doc.to_dict()

        # Validate the structure
        assert validate_adf_document(result)
        assert len(result["content"]) == 2

        # Check heading
        heading_dict = result["content"][0]
        assert heading_dict["type"] == "heading"
        assert heading_dict["attrs"]["level"] == 1

        # Check paragraph
        paragraph_dict = result["content"][1]
        assert paragraph_dict["type"] == "paragraph"
        assert len(paragraph_dict["content"]) == 3

        # Check formatted text
        bold_text_dict = paragraph_dict["content"][1]
        assert bold_text_dict["type"] == "text"
        assert bold_text_dict["text"] == "bold text"
        assert bold_text_dict["marks"] == [{"type": "strong"}]

    def test_nested_adf_conversion(self):
        """Test converting nested ADF structures."""
        # Create nested structure and convert back and forth
        original_text = "Hello, World!"
        adf_doc = convert_text_to_adf(original_text)
        storage_content = convert_adf_to_storage(adf_doc)

        # Should contain the original text
        assert original_text in storage_content
        assert storage_content.startswith("<p>")
        assert storage_content.endswith("</p>")

    def test_adf_roundtrip_conversion(self):
        """Test roundtrip conversion between formats."""
        # Start with storage format
        original_storage = "<p>Test content for roundtrip</p>"

        # Convert to ADF
        adf_content = convert_storage_to_adf(original_storage)
        assert validate_adf_document(adf_content)

        # Convert back to storage
        final_storage = convert_adf_to_storage(adf_content)

        # Should contain the essential content
        assert "Test content for roundtrip" in final_storage
        assert final_storage.startswith("<p>")
        assert final_storage.endswith("</p>")
