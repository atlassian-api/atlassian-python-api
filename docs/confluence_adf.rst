Confluence ADF (Atlassian Document Format)
==========================================

ADF (Atlassian Document Format) is the native content format for Confluence Cloud v2 API. It provides a structured, JSON-based representation of rich content that enables precise control over formatting and layout.

Overview
--------

ADF is a tree-based document format where each node has a type and optional attributes, content, and marks. This structure allows for rich content creation while maintaining consistency and enabling advanced features like collaborative editing.

**Key Benefits:**

- **Rich Content Support**: Native support for headings, lists, tables, media, and more
- **Structured Data**: JSON-based format that's easy to parse and manipulate
- **Version Control**: Built-in versioning for collaborative editing
- **Extensibility**: Support for custom content types and extensions
- **Performance**: Optimized for Confluence Cloud's modern architecture

Basic ADF Structure
-------------------

Every ADF document follows this basic structure:

.. code-block:: json

    {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Hello, World!"
                    }
                ]
            }
        ]
    }

**Required Fields:**

- ``version``: Always 1 for current ADF specification
- ``type``: Always "doc" for the root document
- ``content``: Array of content nodes

Node Types
----------

Text Nodes
~~~~~~~~~~~

Text nodes represent plain text content with optional formatting marks:

.. code-block:: python

    # Plain text
    text_node = {
        "type": "text",
        "text": "Plain text content"
    }

    # Formatted text with marks
    formatted_text = {
        "type": "text",
        "text": "Bold and italic text",
        "marks": [
            {"type": "strong"},
            {"type": "em"}
        ]
    }

    # Text with link
    link_text = {
        "type": "text",
        "text": "Visit our website",
        "marks": [
            {
                "type": "link",
                "attrs": {
                    "href": "https://example.com",
                    "title": "Example Website"
                }
            }
        ]
    }

Paragraph Nodes
~~~~~~~~~~~~~~~

Paragraphs are the most common block-level content:

.. code-block:: python

    paragraph = {
        "type": "paragraph",
        "content": [
            {
                "type": "text",
                "text": "This is a paragraph with "
            },
            {
                "type": "text",
                "text": "bold text",
                "marks": [{"type": "strong"}]
            },
            {
                "type": "text",
                "text": " and normal text."
            }
        ]
    }

Heading Nodes
~~~~~~~~~~~~~

Headings support levels 1-6:

.. code-block:: python

    # Level 1 heading
    h1 = {
        "type": "heading",
        "attrs": {"level": 1},
        "content": [
            {"type": "text", "text": "Main Heading"}
        ]
    }

    # Level 2 heading with formatting
    h2 = {
        "type": "heading",
        "attrs": {"level": 2},
        "content": [
            {
                "type": "text",
                "text": "Subheading with emphasis",
                "marks": [{"type": "em"}]
            }
        ]
    }

List Nodes
~~~~~~~~~~

Both bullet and ordered lists are supported:

.. code-block:: python

    # Bullet list
    bullet_list = {
        "type": "bulletList",
        "content": [
            {
                "type": "listItem",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "First item"}
                        ]
                    }
                ]
            },
            {
                "type": "listItem",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "Second item"}
                        ]
                    }
                ]
            }
        ]
    }

    # Ordered list
    ordered_list = {
        "type": "orderedList",
        "content": [
            {
                "type": "listItem",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "First numbered item"}
                        ]
                    }
                ]
            },
            {
                "type": "listItem",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "Second numbered item"}
                        ]
                    }
                ]
            }
        ]
    }

Code Blocks
~~~~~~~~~~~

Code blocks support syntax highlighting:

.. code-block:: python

    # Inline code
    inline_code = {
        "type": "text",
        "text": "print('hello')",
        "marks": [{"type": "code"}]
    }

    # Code block
    code_block = {
        "type": "codeBlock",
        "attrs": {
            "language": "python"
        },
        "content": [
            {
                "type": "text",
                "text": "def hello_world():\n    print('Hello, World!')\n    return True"
            }
        ]
    }

Tables
~~~~~~

Tables support complex structures with headers and formatting:

.. code-block:: python

    table = {
        "type": "table",
        "attrs": {
            "isNumberColumnEnabled": False,
            "layout": "default"
        },
        "content": [
            {
                "type": "tableRow",
                "content": [
                    {
                        "type": "tableHeader",
                        "attrs": {},
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {"type": "text", "text": "Name"}
                                ]
                            }
                        ]
                    },
                    {
                        "type": "tableHeader",
                        "attrs": {},
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {"type": "text", "text": "Role"}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "type": "tableRow",
                "content": [
                    {
                        "type": "tableCell",
                        "attrs": {},
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {"type": "text", "text": "John Doe"}
                                ]
                            }
                        ]
                    },
                    {
                        "type": "tableCell",
                        "attrs": {},
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {"type": "text", "text": "Developer"}
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

Text Marks
----------

Marks provide inline formatting for text nodes:

.. code-block:: python

    # Available marks
    marks_examples = {
        "strong": {"type": "strong"},  # Bold
        "em": {"type": "em"},          # Italic
        "code": {"type": "code"},      # Inline code
        "strike": {"type": "strike"},  # Strikethrough
        "underline": {"type": "underline"},  # Underline
        "subsup": {                    # Subscript/Superscript
            "type": "subsup",
            "attrs": {"type": "sub"}   # or "sup"
        },
        "textColor": {                 # Text color
            "type": "textColor",
            "attrs": {"color": "#ff0000"}
        },
        "link": {                      # Hyperlink
            "type": "link",
            "attrs": {
                "href": "https://example.com",
                "title": "Example"
            }
        }
    }

    # Text with multiple marks
    formatted_text = {
        "type": "text",
        "text": "Bold, italic, and colored text",
        "marks": [
            {"type": "strong"},
            {"type": "em"},
            {
                "type": "textColor",
                "attrs": {"color": "#0066cc"}
            }
        ]
    }

Using ADF with Python Classes
-----------------------------

The library provides Python classes for easier ADF construction:

.. code-block:: python

    from atlassian.adf import (
        ADFDocument,
        ADFParagraph,
        ADFText,
        ADFHeading,
        create_simple_adf_document,
        convert_text_to_adf
    )

    # Create document using classes
    document = ADFDocument()
    
    # Add heading
    heading = ADFHeading(level=1, content=[
        ADFText("Welcome to ADF")
    ])
    document.add_content(heading)
    
    # Add paragraph with formatted text
    paragraph = ADFParagraph([
        ADFText("This is "),
        ADFText("bold text", marks=[{"type": "strong"}]),
        ADFText(" and this is "),
        ADFText("italic text", marks=[{"type": "em"}]),
        ADFText(".")
    ])
    document.add_content(paragraph)
    
    # Convert to dictionary for API submission
    adf_dict = document.to_dict()
    
    # Create page with constructed ADF
    page = confluence.create_page_with_adf("SPACE123", "My Page", adf_dict)

Utility Functions
----------------

Content Conversion
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from atlassian.adf import (
        convert_text_to_adf,
        convert_storage_to_adf,
        convert_adf_to_storage,
        validate_adf_document
    )

    # Convert plain text to ADF
    text = "Hello, World!"
    adf_content = convert_text_to_adf(text)

    # Convert storage format to ADF (basic conversion)
    storage_content = "<p>Hello, <strong>World</strong>!</p>"
    adf_content = convert_storage_to_adf(storage_content)

    # Convert ADF back to storage format
    storage_content = convert_adf_to_storage(adf_content)

    # Validate ADF structure
    is_valid = validate_adf_document(adf_content)
    if not is_valid:
        print("Invalid ADF structure")

Content Detection
~~~~~~~~~~~~~~~~

.. code-block:: python

    from atlassian.request_utils import (
        detect_content_format,
        is_adf_content,
        validate_adf_structure
    )

    # Detect content format
    content_format = detect_content_format(content)
    print(f"Content format: {content_format}")  # 'adf', 'storage', 'wiki', or 'unknown'

    # Check if content is ADF
    if is_adf_content(content):
        print("Content is in ADF format")

    # Validate ADF structure
    if validate_adf_structure(adf_content):
        print("Valid ADF structure")

Complex ADF Examples
--------------------

Rich Document Example
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Create a complex document with multiple content types
    complex_adf = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "heading",
                "attrs": {"level": 1},
                "content": [
                    {"type": "text", "text": "Project Documentation"}
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "This document contains important information about our project."}
                ]
            },
            {
                "type": "heading",
                "attrs": {"level": 2},
                "content": [
                    {"type": "text", "text": "Features"}
                ]
            },
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "ADF Support",
                                        "marks": [{"type": "strong"}]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "Cursor-based Pagination",
                                        "marks": [{"type": "strong"}]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "type": "heading",
                "attrs": {"level": 2},
                "content": [
                    {"type": "text", "text": "Code Example"}
                ]
            },
            {
                "type": "codeBlock",
                "attrs": {"language": "python"},
                "content": [
                    {
                        "type": "text",
                        "text": "# Create a page with ADF content\npage = confluence.create_page_with_adf(\n    space_id=\"SPACE123\",\n    title=\"My Page\",\n    adf_content=adf_content\n)"
                    }
                ]
            }
        ]
    }

    # Create the page
    page = confluence.create_page_with_adf("SPACE123", "Complex Document", complex_adf)

Template-Based Content Creation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_meeting_notes_adf(meeting_title, date, attendees, agenda_items, notes):
        """Create ADF content for meeting notes."""
        
        content = [
            {
                "type": "heading",
                "attrs": {"level": 1},
                "content": [{"type": "text", "text": meeting_title}]
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Date: "},
                    {"type": "text", "text": date, "marks": [{"type": "strong"}]}
                ]
            },
            {
                "type": "heading",
                "attrs": {"level": 2},
                "content": [{"type": "text", "text": "Attendees"}]
            }
        ]
        
        # Add attendees list
        attendees_list = {
            "type": "bulletList",
            "content": []
        }
        
        for attendee in attendees:
            attendees_list["content"].append({
                "type": "listItem",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": attendee}]
                    }
                ]
            })
        
        content.append(attendees_list)
        
        # Add agenda
        content.append({
            "type": "heading",
            "attrs": {"level": 2},
            "content": [{"type": "text", "text": "Agenda"}]
        })
        
        agenda_list = {
            "type": "orderedList",
            "content": []
        }
        
        for item in agenda_items:
            agenda_list["content"].append({
                "type": "listItem",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": item}]
                    }
                ]
            })
        
        content.append(agenda_list)
        
        # Add notes section
        content.append({
            "type": "heading",
            "attrs": {"level": 2},
            "content": [{"type": "text", "text": "Notes"}]
        })
        
        content.append({
            "type": "paragraph",
            "content": [{"type": "text", "text": notes}]
        })
        
        return {
            "version": 1,
            "type": "doc",
            "content": content
        }

    # Use the template
    meeting_adf = create_meeting_notes_adf(
        meeting_title="Weekly Team Standup",
        date="2024-01-15",
        attendees=["Alice", "Bob", "Charlie"],
        agenda_items=[
            "Review last week's progress",
            "Discuss current blockers",
            "Plan next week's tasks"
        ],
        notes="Team discussed the new feature implementation and agreed on the timeline."
    )

    # Create the meeting notes page
    page = confluence.create_page_with_adf("TEAM", "Weekly Standup - Jan 15", meeting_adf)

Best Practices
--------------

Structure and Organization
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Good: Well-structured document hierarchy
    good_structure = {
        "version": 1,
        "type": "doc",
        "content": [
            # Main heading
            {
                "type": "heading",
                "attrs": {"level": 1},
                "content": [{"type": "text", "text": "Main Topic"}]
            },
            # Introduction paragraph
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": "Introduction text..."}]
            },
            # Subsection
            {
                "type": "heading",
                "attrs": {"level": 2},
                "content": [{"type": "text", "text": "Subsection"}]
            },
            # Content for subsection
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": "Subsection content..."}]
            }
        ]
    }

    # Avoid: Flat structure without hierarchy
    # Don't create documents with only paragraphs or only headings

Content Validation
~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_safe_adf_page(space_id, title, adf_content):
        """Safely create a page with ADF content validation."""
        
        # Validate ADF structure
        if not validate_adf_document(adf_content):
            raise ValueError("Invalid ADF document structure")
        
        # Check for required fields
        if adf_content.get("version") != 1:
            raise ValueError("ADF version must be 1")
        
        if adf_content.get("type") != "doc":
            raise ValueError("ADF type must be 'doc'")
        
        if not isinstance(adf_content.get("content"), list):
            raise ValueError("ADF content must be a list")
        
        # Create the page
        try:
            return confluence.create_page_with_adf(space_id, title, adf_content)
        except Exception as e:
            print(f"Failed to create page: {e}")
            raise

Performance Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Good: Efficient ADF structure
    # Use appropriate node types for content
    # Avoid deeply nested structures when possible
    # Group related content logically

    # Good: Reasonable document size
    efficient_adf = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Concise, well-structured content"}
                ]
            }
        ]
    }

    # Avoid: Overly complex nested structures
    # Avoid: Extremely large documents (consider splitting)
    # Avoid: Unnecessary nesting levels

Common Pitfalls
--------------

Invalid Structure
~~~~~~~~~~~~~~~~

.. code-block:: python

    # Wrong: Missing required fields
    invalid_adf = {
        "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": "Hello"}]}
        ]
    }
    # Missing "version" and "type" fields

    # Wrong: Incorrect version
    invalid_version = {
        "version": 2,  # Should be 1
        "type": "doc",
        "content": []
    }

    # Correct: Proper structure
    valid_adf = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": "Hello"}]
            }
        ]
    }

Incorrect Node Types
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Wrong: Invalid node type
    invalid_node = {
        "type": "invalidType",  # Not a valid ADF node type
        "content": []
    }

    # Wrong: Missing required attributes
    invalid_heading = {
        "type": "heading",
        # Missing "attrs" with "level"
        "content": [{"type": "text", "text": "Heading"}]
    }

    # Correct: Valid heading with required attributes
    valid_heading = {
        "type": "heading",
        "attrs": {"level": 1},
        "content": [{"type": "text", "text": "Heading"}]
    }

Text Mark Issues
~~~~~~~~~~~~~~~

.. code-block:: python

    # Wrong: Invalid mark structure
    invalid_marks = {
        "type": "text",
        "text": "Bold text",
        "marks": "strong"  # Should be a list
    }

    # Wrong: Invalid mark type
    invalid_mark_type = {
        "type": "text",
        "text": "Text",
        "marks": [{"type": "invalidMark"}]
    }

    # Correct: Valid marks structure
    valid_marks = {
        "type": "text",
        "text": "Bold text",
        "marks": [{"type": "strong"}]
    }

Resources
---------

- `Atlassian Document Format Specification <https://developer.atlassian.com/cloud/confluence/adf/>`_
- `Confluence Cloud REST API v2 Documentation <https://developer.atlassian.com/cloud/confluence/rest/v2/>`_
- `ADF Builder Tool <https://developer.atlassian.com/cloud/confluence/adf-builder/>`_