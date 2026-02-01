# coding=utf-8
"""
Minimal ADF (Atlassian Document Format) data models and utilities.

This module provides basic ADF document structure classes and validation
for Confluence Cloud v2 API support. ADF is the native content format
for Confluence Cloud that enables rich content creation with structured,
JSON-based document representation.

Key Features:
- ADF document construction with Python classes
- Content validation and format detection
- Conversion utilities between different content formats
- Type-safe ADF node creation

Classes:
    ADFDocument: Root document container
    ADFNode: Base class for all ADF nodes
    ADFParagraph: Paragraph content node
    ADFText: Text content with optional formatting
    ADFHeading: Heading nodes (levels 1-6)

Functions:
    create_simple_adf_document: Quick ADF document creation
    convert_text_to_adf: Convert plain text to ADF format
    validate_adf_document: Validate ADF document structure
    convert_storage_to_adf: Basic storage format conversion
    convert_adf_to_storage: Basic ADF to storage conversion

.. versionadded:: 4.1.0
   Added ADF support for Confluence Cloud v2 API

Examples:
    Create a simple ADF document:

    >>> from atlassian.adf import create_simple_adf_document
    >>> doc = create_simple_adf_document("Hello, World!")
    >>> adf_dict = doc.to_dict()

    Build complex ADF using classes:

    >>> from atlassian.adf import ADFDocument, ADFHeading, ADFParagraph, ADFText
    >>>
    >>> document = ADFDocument()
    >>> heading = ADFHeading(level=1, content=[ADFText("My Document")])
    >>> paragraph = ADFParagraph([
    ...     ADFText("This is "),
    ...     ADFText("bold text", marks=[{"type": "strong"}])
    ... ])
    >>>
    >>> document.add_content(heading)
    >>> document.add_content(paragraph)
    >>> adf_dict = document.to_dict()

See Also:
    - :doc:`confluence_adf`: Complete ADF documentation and examples
    - :class:`atlassian.confluence.ConfluenceCloud`: Main Confluence client
"""

from typing import Dict, List, Any, Optional, Union


class ADFNode:
    """
    Base class for ADF document nodes.
    """

    def __init__(self, node_type: str, **kwargs):
        """
        Initialize an ADF node.

        :param node_type: The type of the node (e.g., 'doc', 'paragraph', 'text')
        :param kwargs: Additional node attributes
        """
        self.type: str = node_type
        self.attrs: Dict[str, Any] = kwargs.get("attrs", {})
        self.content: List[Union["ADFNode", Dict[str, Any]]] = kwargs.get("content", [])
        self.text: Optional[str] = kwargs.get("text")
        self.marks: List[Dict[str, Any]] = kwargs.get("marks", [])

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the node to a dictionary representation.

        :return: Dictionary representation of the node
        """
        result: Dict[str, Any] = {"type": self.type}

        if self.attrs:
            result["attrs"] = self.attrs

        if self.content:
            result["content"] = [node.to_dict() if isinstance(node, ADFNode) else node for node in self.content]

        if self.text is not None:
            result["text"] = self.text

        if self.marks:
            result["marks"] = self.marks

        return result


class ADFDocument:
    """
    Represents an ADF document.

    The root container for ADF content that maintains the document structure
    and provides methods for content manipulation. Every ADF document must
    have version=1, type="doc", and a content array.

    Attributes:
        version (int): ADF specification version (always 1)
        type (str): Document type (always "doc")
        content (List[ADFNode]): List of content nodes

    Examples:
        Create an empty document:

        >>> document = ADFDocument()
        >>> print(document.to_dict())
        {'version': 1, 'type': 'doc', 'content': []}

        Create document with initial content:

        >>> paragraph = ADFParagraph([ADFText("Hello, World!")])
        >>> document = ADFDocument([paragraph])

        Add content to existing document:

        >>> document = ADFDocument()
        >>> heading = ADFHeading(level=1, content=[ADFText("Title")])
        >>> document.add_content(heading)
    """

    def __init__(self, content: Optional[List[ADFNode]] = None):
        """
        Initialize an ADF document.

        :param content: List of content nodes
        """
        self.version = 1
        self.type = "doc"
        self.content = content or []

    def add_content(self, node: ADFNode):
        """
        Add a content node to the document.

        :param node: The node to add
        """
        self.content.append(node)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the document to a dictionary representation.

        :return: Dictionary representation of the document
        """
        return {"version": self.version, "type": self.type, "content": [node.to_dict() for node in self.content]}


class ADFParagraph(ADFNode):
    """
    Represents an ADF paragraph node.
    """

    def __init__(self, content: Optional[List[ADFNode]] = None):
        """
        Initialize a paragraph node.

        :param content: List of content nodes (typically text nodes)
        """
        super().__init__("paragraph", content=content or [])


class ADFText(ADFNode):
    """
    Represents an ADF text node.
    """

    def __init__(self, text: str, marks: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize a text node.

        :param text: The text content
        :param marks: List of text formatting marks
        """
        super().__init__("text", text=text, marks=marks or [])


class ADFHeading(ADFNode):
    """
    Represents an ADF heading node.
    """

    def __init__(self, level: int, content: Optional[List[ADFNode]] = None):
        """
        Initialize a heading node.

        :param level: Heading level (1-6)
        :param content: List of content nodes
        """
        if not 1 <= level <= 6:
            raise ValueError("Heading level must be between 1 and 6")

        super().__init__("heading", attrs={"level": level}, content=content or [])


def create_simple_adf_document(text: str) -> ADFDocument:
    """
    Create a simple ADF document with a single paragraph of text.

    This is a convenience function for quickly creating basic ADF documents
    from plain text content. The resulting document contains a single
    paragraph with the provided text.

    :param text: The text content for the paragraph
    :return: ADF document containing a single paragraph with the text

    Examples:
        Create a simple document:

        >>> doc = create_simple_adf_document("Hello, World!")
        >>> adf_dict = doc.to_dict()
        >>> print(adf_dict['content'][0]['type'])  # 'paragraph'

        Use with Confluence API:

        >>> doc = create_simple_adf_document("My page content")
        >>> page = confluence.create_page_with_adf("SPACE123", "My Page", doc.to_dict())
    """
    text_node = ADFText(text)
    paragraph = ADFParagraph([text_node])
    document = ADFDocument([paragraph])
    return document


def validate_adf_document(adf_dict: Dict[str, Any]) -> bool:
    """
    Validate an ADF document dictionary structure.

    Performs basic validation of ADF document structure to ensure it meets
    the minimum requirements for a valid ADF document. Checks for required
    fields and correct data types.

    :param adf_dict: Dictionary representation of ADF document to validate
    :return: True if the document structure is valid, False otherwise

    Validation checks:
        - Document is a dictionary
        - Has required 'type' field with value 'doc'
        - Has required 'version' field with value 1
        - Has required 'content' field that is a list

    Examples:
        Validate a correct ADF document:

        >>> adf_doc = {
        ...     "version": 1,
        ...     "type": "doc",
        ...     "content": [
        ...         {
        ...             "type": "paragraph",
        ...             "content": [{"type": "text", "text": "Hello"}]
        ...         }
        ...     ]
        ... }
        >>> is_valid = validate_adf_document(adf_doc)
        >>> print(is_valid)  # True

        Validate an invalid document:

        >>> invalid_doc = {"content": []}  # Missing version and type
        >>> is_valid = validate_adf_document(invalid_doc)
        >>> print(is_valid)  # False

        Use before API submission:

        >>> if validate_adf_document(adf_content):
        ...     page = confluence.create_page_with_adf("SPACE123", "Title", adf_content)
        ... else:
        ...     print("Invalid ADF structure")

    Note:
        This function performs basic structural validation only. It does not
        validate the content of individual nodes or their specific attributes.
        For more comprehensive validation, consider using the official
        Atlassian ADF validator tools.
    """
    if not isinstance(adf_dict, dict):
        return False

    # Check required fields
    if adf_dict.get("type") != "doc":
        return False

    if adf_dict.get("version") != 1:
        return False

    if "content" not in adf_dict:
        return False

    if not isinstance(adf_dict["content"], list):
        return False

    return True


def convert_text_to_adf(text: str) -> Dict[str, Any]:
    """
    Convert plain text to ADF format.

    Creates a valid ADF document containing a single paragraph with the
    provided text. This is useful for converting simple text content to
    ADF format for use with Confluence Cloud v2 API.

    :param text: Plain text content to convert
    :return: ADF document dictionary with the text in a paragraph

    Examples:
        Convert simple text:

        >>> adf_dict = convert_text_to_adf("Hello, World!")
        >>> print(adf_dict['content'][0]['content'][0]['text'])  # "Hello, World!"

        Use with Confluence API:

        >>> text_content = "This is my page content"
        >>> adf_content = convert_text_to_adf(text_content)
        >>> page = confluence.create_page_with_adf("SPACE123", "My Page", adf_content)

        Convert multiline text:

        >>> multiline_text = "Line 1\\nLine 2\\nLine 3"
        >>> adf_content = convert_text_to_adf(multiline_text)
        # Creates a single paragraph with the full text including newlines

    Note:
        This function creates a single paragraph containing all the text.
        Newlines in the input text are preserved as literal newline characters
        within the paragraph. For more complex text processing (like converting
        newlines to separate paragraphs), additional processing is needed.
    """
    document = create_simple_adf_document(text)
    return document.to_dict()


def convert_storage_to_adf(storage_content: str) -> Dict[str, Any]:
    """
    Convert Confluence storage format to ADF format (basic conversion).

    This is a minimal implementation that handles simple cases.
    For complex storage format, consider using Atlassian's official converters.

    :param storage_content: Storage format content (HTML-like)
    :return: ADF document dictionary
    """
    # Basic conversion - treat as plain text for now
    # In a full implementation, this would parse HTML and convert to ADF nodes
    import re

    # Remove HTML tags for basic conversion
    text_content = re.sub(r"<[^>]+>", "", storage_content)
    text_content = text_content.strip()

    if not text_content:
        text_content = "Empty content"

    return convert_text_to_adf(text_content)


def convert_adf_to_storage(adf_content: Dict[str, Any]) -> str:
    """
    Convert ADF format to Confluence storage format (basic conversion).

    This is a minimal implementation that handles simple cases.

    :param adf_content: ADF document dictionary
    :return: Storage format content (HTML-like)
    """
    if not validate_adf_document(adf_content):
        raise ValueError("Invalid ADF document structure")

    # Basic conversion - extract text content and wrap in paragraph
    text_parts = []

    def extract_text_from_node(node):
        if isinstance(node, dict):
            if node.get("type") == "text" and "text" in node:
                text_parts.append(node["text"])
            elif "content" in node:
                for child in node["content"]:
                    extract_text_from_node(child)

    for content_node in adf_content.get("content", []):
        extract_text_from_node(content_node)

    text_content = " ".join(text_parts).strip()
    if not text_content:
        text_content = "Empty content"

    return f"<p>{text_content}</p>"


def validate_content_format(content: Union[str, Dict[str, Any]], expected_format: str) -> bool:
    """
    Validate content format matches expected format.

    :param content: Content to validate
    :param expected_format: Expected format ('adf', 'storage', 'wiki')
    :return: True if format matches
    """
    if expected_format == "adf":
        return isinstance(content, dict) and validate_adf_document(content)
    elif expected_format == "storage":
        return isinstance(content, str) and content.strip().startswith("<")
    elif expected_format == "wiki":
        return isinstance(content, str)
    else:
        return False
