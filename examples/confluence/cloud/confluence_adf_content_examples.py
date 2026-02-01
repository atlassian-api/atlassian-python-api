#!/usr/bin/env python3
# coding=utf-8
"""
Example: Confluence Cloud ADF Content Creation

This example demonstrates how to create rich content using ADF (Atlassian Document Format)
with the Confluence Cloud v2 API. ADF is Confluence's native content format that supports
rich text, tables, panels, code blocks, and other advanced content types.

Key features demonstrated:
- Creating various ADF content types (headings, paragraphs, lists, tables)
- Working with text formatting (bold, italic, links, code)
- Using panels, code blocks, and other advanced elements
- Converting between different content formats
- Best practices for ADF content creation

Prerequisites:
- Confluence Cloud instance
- API token (not username/password)
- Python 3.9+

Usage:
    python confluence_adf_content_examples.py

Configuration:
    Update the CONFLUENCE_URL and API_TOKEN variables below with your credentials.
"""

import os
import sys
from typing import Dict, Any, List
from datetime import datetime

# Add the parent directory to the path to import atlassian
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from atlassian.confluence import ConfluenceCloud

# Configuration - Update these with your Confluence Cloud details
CONFLUENCE_URL = "https://your-domain.atlassian.net"
API_TOKEN = "your-api-token"
TEST_SPACE_KEY = "DEMO"  # Update with your test space key


def create_comprehensive_adf_document() -> Dict[str, Any]:
    """
    Create a comprehensive ADF document showcasing various content types.

    This demonstrates the full range of ADF capabilities including:
    - Text formatting (bold, italic, underline, strikethrough)
    - Headings and paragraphs
    - Lists (bullet and numbered)
    - Tables with formatting
    - Panels (info, note, warning, error)
    - Code blocks and inline code
    - Links and mentions
    - Media and attachments

    Returns:
        Dict containing a comprehensive ADF document
    """
    return {
        "version": 1,
        "type": "doc",
        "content": [
            # Title
            {"type": "heading", "attrs": {"level": 1}, "content": [{"type": "text", "text": "ADF Content Showcase"}]},
            # Introduction paragraph with various text formatting
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "This page demonstrates "},
                    {"type": "text", "text": "ADF (Atlassian Document Format)", "marks": [{"type": "strong"}]},
                    {"type": "text", "text": " capabilities including "},
                    {"type": "text", "text": "rich text formatting", "marks": [{"type": "em"}]},
                    {"type": "text", "text": ", "},
                    {"type": "text", "text": "underlined text", "marks": [{"type": "underline"}]},
                    {"type": "text", "text": ", "},
                    {"type": "text", "text": "strikethrough text", "marks": [{"type": "strike"}]},
                    {"type": "text", "text": ", and "},
                    {"type": "text", "text": "inline code", "marks": [{"type": "code"}]},
                    {"type": "text", "text": "."},
                ],
            },
            # Info panel
            {
                "type": "panel",
                "attrs": {"panelType": "info"},
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "💡 "},
                            {"type": "text", "text": "Tip: ", "marks": [{"type": "strong"}]},
                            {
                                "type": "text",
                                "text": "ADF provides a structured way to create rich content that renders consistently across Confluence.",
                            },
                        ],
                    }
                ],
            },
            # Section: Lists
            {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Lists and Formatting"}]},
            # Bullet list
            {"type": "paragraph", "content": [{"type": "text", "text": "Bullet list example:"}]},
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {"type": "text", "text": "First item with "},
                                    {"type": "text", "text": "bold text", "marks": [{"type": "strong"}]},
                                ],
                            }
                        ],
                    },
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {"type": "text", "text": "Second item with "},
                                    {"type": "text", "text": "italic text", "marks": [{"type": "em"}]},
                                ],
                            }
                        ],
                    },
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [{"type": "text", "text": "Third item with nested list:"}],
                            },
                            {
                                "type": "bulletList",
                                "content": [
                                    {
                                        "type": "listItem",
                                        "content": [
                                            {
                                                "type": "paragraph",
                                                "content": [{"type": "text", "text": "Nested item 1"}],
                                            }
                                        ],
                                    },
                                    {
                                        "type": "listItem",
                                        "content": [
                                            {
                                                "type": "paragraph",
                                                "content": [{"type": "text", "text": "Nested item 2"}],
                                            }
                                        ],
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
            # Numbered list
            {"type": "paragraph", "content": [{"type": "text", "text": "Numbered list example:"}]},
            {
                "type": "orderedList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [{"type": "text", "text": "Step one: Initialize the client"}],
                            }
                        ],
                    },
                    {
                        "type": "listItem",
                        "content": [
                            {"type": "paragraph", "content": [{"type": "text", "text": "Step two: Enable v2 API"}]}
                        ],
                    },
                    {
                        "type": "listItem",
                        "content": [
                            {"type": "paragraph", "content": [{"type": "text", "text": "Step three: Create content"}]}
                        ],
                    },
                ],
            },
            # Section: Code blocks
            {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Code Examples"}]},
            # Code block
            {
                "type": "codeBlock",
                "attrs": {"language": "python"},
                "content": [
                    {
                        "type": "text",
                        "text": '# Python example\nfrom atlassian.confluence import ConfluenceCloud\n\n# Initialize client\nconfluence = ConfluenceCloud(\n    url="https://your-domain.atlassian.net",\n    token="your-api-token"\n)\n\n# Enable v2 API\nconfluence.enable_v2_api()\n\n# Create page with ADF content\npage = confluence._v2_client.create_page(\n    space_id="space123",\n    title="My Page",\n    content=adf_content,\n    content_format="adf"\n)',
                    }
                ],
            },
            # Section: Tables
            {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Tables"}]},
            # Table example
            {
                "type": "table",
                "attrs": {"isNumberColumnEnabled": False, "layout": "default"},
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
                                        "content": [{"type": "text", "text": "Feature", "marks": [{"type": "strong"}]}],
                                    }
                                ],
                            },
                            {
                                "type": "tableHeader",
                                "attrs": {},
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [{"type": "text", "text": "v1 API", "marks": [{"type": "strong"}]}],
                                    }
                                ],
                            },
                            {
                                "type": "tableHeader",
                                "attrs": {},
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [{"type": "text", "text": "v2 API", "marks": [{"type": "strong"}]}],
                                    }
                                ],
                            },
                        ],
                    },
                    {
                        "type": "tableRow",
                        "content": [
                            {
                                "type": "tableCell",
                                "attrs": {},
                                "content": [
                                    {"type": "paragraph", "content": [{"type": "text", "text": "Content Format"}]}
                                ],
                            },
                            {
                                "type": "tableCell",
                                "attrs": {},
                                "content": [
                                    {"type": "paragraph", "content": [{"type": "text", "text": "Storage Format"}]}
                                ],
                            },
                            {
                                "type": "tableCell",
                                "attrs": {},
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [
                                            {"type": "text", "text": "ADF (Native)", "marks": [{"type": "strong"}]}
                                        ],
                                    }
                                ],
                            },
                        ],
                    },
                    {
                        "type": "tableRow",
                        "content": [
                            {
                                "type": "tableCell",
                                "attrs": {},
                                "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Pagination"}]}],
                            },
                            {
                                "type": "tableCell",
                                "attrs": {},
                                "content": [
                                    {"type": "paragraph", "content": [{"type": "text", "text": "Offset-based"}]}
                                ],
                            },
                            {
                                "type": "tableCell",
                                "attrs": {},
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [
                                            {"type": "text", "text": "Cursor-based", "marks": [{"type": "strong"}]}
                                        ],
                                    }
                                ],
                            },
                        ],
                    },
                    {
                        "type": "tableRow",
                        "content": [
                            {
                                "type": "tableCell",
                                "attrs": {},
                                "content": [
                                    {"type": "paragraph", "content": [{"type": "text", "text": "Performance"}]}
                                ],
                            },
                            {
                                "type": "tableCell",
                                "attrs": {},
                                "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Standard"}]}],
                            },
                            {
                                "type": "tableCell",
                                "attrs": {},
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [
                                            {"type": "text", "text": "Enhanced", "marks": [{"type": "strong"}]}
                                        ],
                                    }
                                ],
                            },
                        ],
                    },
                ],
            },
            # Section: Panels
            {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Panels and Callouts"}]},
            # Note panel
            {
                "type": "panel",
                "attrs": {"panelType": "note"},
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "📝 "},
                            {"type": "text", "text": "Note: ", "marks": [{"type": "strong"}]},
                            {
                                "type": "text",
                                "text": "This is a note panel. Use it for additional information that supplements the main content.",
                            },
                        ],
                    }
                ],
            },
            # Warning panel
            {
                "type": "panel",
                "attrs": {"panelType": "warning"},
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "⚠️ "},
                            {"type": "text", "text": "Warning: ", "marks": [{"type": "strong"}]},
                            {
                                "type": "text",
                                "text": "Always validate ADF content structure before submitting to the API.",
                            },
                        ],
                    }
                ],
            },
            # Error panel
            {
                "type": "panel",
                "attrs": {"panelType": "error"},
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "❌ "},
                            {"type": "text", "text": "Error: ", "marks": [{"type": "strong"}]},
                            {"type": "text", "text": "Invalid ADF structure will result in API errors."},
                        ],
                    }
                ],
            },
            # Success panel
            {
                "type": "panel",
                "attrs": {"panelType": "success"},
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "✅ "},
                            {"type": "text", "text": "Success: ", "marks": [{"type": "strong"}]},
                            {"type": "text", "text": "Well-formed ADF content renders beautifully in Confluence!"},
                        ],
                    }
                ],
            },
            # Section: Links and references
            {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Links and References"}]},
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "External link: "},
                    {
                        "type": "text",
                        "text": "Confluence Cloud REST API v2",
                        "marks": [
                            {
                                "type": "link",
                                "attrs": {"href": "https://developer.atlassian.com/cloud/confluence/rest/v2/intro/"},
                            }
                        ],
                    },
                ],
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Another useful resource: "},
                    {
                        "type": "text",
                        "text": "ADF Documentation",
                        "marks": [
                            {"type": "link", "attrs": {"href": "https://developer.atlassian.com/cloud/confluence/adf/"}}
                        ],
                    },
                ],
            },
            # Footer
            {"type": "rule"},
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Generated on "},
                    {"type": "text", "text": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "marks": [{"type": "code"}]},
                    {"type": "text", "text": " using the Confluence Cloud v2 API."},
                ],
            },
        ],
    }


def create_simple_adf_examples() -> List[Dict[str, Any]]:
    """
    Create a collection of simple ADF examples for common use cases.

    Returns:
        List of ADF documents for different scenarios
    """
    examples = []

    # Simple text document
    examples.append(
        {
            "name": "Simple Text",
            "description": "Basic paragraph with text formatting",
            "adf": {
                "version": 1,
                "type": "doc",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "This is a "},
                            {"type": "text", "text": "simple example", "marks": [{"type": "strong"}]},
                            {"type": "text", "text": " of ADF content."},
                        ],
                    }
                ],
            },
        }
    )

    # Meeting notes template
    examples.append(
        {
            "name": "Meeting Notes",
            "description": "Template for meeting notes",
            "adf": {
                "version": 1,
                "type": "doc",
                "content": [
                    {
                        "type": "heading",
                        "attrs": {"level": 1},
                        "content": [{"type": "text", "text": "Meeting Notes - [Date]"}],
                    },
                    {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Attendees"}]},
                    {
                        "type": "bulletList",
                        "content": [
                            {
                                "type": "listItem",
                                "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[Name 1]"}]}],
                            },
                            {
                                "type": "listItem",
                                "content": [{"type": "paragraph", "content": [{"type": "text", "text": "[Name 2]"}]}],
                            },
                        ],
                    },
                    {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Agenda"}]},
                    {
                        "type": "orderedList",
                        "content": [
                            {
                                "type": "listItem",
                                "content": [
                                    {"type": "paragraph", "content": [{"type": "text", "text": "[Agenda item 1]"}]}
                                ],
                            },
                            {
                                "type": "listItem",
                                "content": [
                                    {"type": "paragraph", "content": [{"type": "text", "text": "[Agenda item 2]"}]}
                                ],
                            },
                        ],
                    },
                    {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Action Items"}]},
                    {
                        "type": "panel",
                        "attrs": {"panelType": "info"},
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {"type": "text", "text": "Add action items here with owners and due dates."}
                                ],
                            }
                        ],
                    },
                ],
            },
        }
    )

    # Technical documentation template
    examples.append(
        {
            "name": "Technical Documentation",
            "description": "Template for technical documentation",
            "adf": {
                "version": 1,
                "type": "doc",
                "content": [
                    {
                        "type": "heading",
                        "attrs": {"level": 1},
                        "content": [{"type": "text", "text": "API Documentation"}],
                    },
                    {
                        "type": "panel",
                        "attrs": {"panelType": "info"},
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "This document describes the API endpoints and usage examples.",
                                    }
                                ],
                            }
                        ],
                    },
                    {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Endpoint"}]},
                    {
                        "type": "codeBlock",
                        "attrs": {"language": "http"},
                        "content": [
                            {
                                "type": "text",
                                "text": "GET /api/v2/pages\nContent-Type: application/json\nAuthorization: Bearer {token}",
                            }
                        ],
                    },
                    {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Response"}]},
                    {
                        "type": "codeBlock",
                        "attrs": {"language": "json"},
                        "content": [
                            {
                                "type": "text",
                                "text": '{\n  "results": [\n    {\n      "id": "123456",\n      "title": "Example Page",\n      "type": "page"\n    }\n  ],\n  "_links": {\n    "next": {\n      "href": "/api/v2/pages?cursor=abc123"\n    }\n  }\n}',
                            }
                        ],
                    },
                ],
            },
        }
    )

    return examples


def demonstrate_adf_content_creation():
    """
    Demonstrate ADF content creation with various examples.
    """
    print("=== Confluence Cloud ADF Content Examples ===\n")

    # Initialize Confluence Cloud client
    confluence = ConfluenceCloud(url=CONFLUENCE_URL, token=API_TOKEN)
    confluence.enable_v2_api()

    try:
        # Get a test space
        print("1. Finding test space...")
        spaces_response = confluence._v2_client.get_spaces(limit=10)
        spaces = spaces_response.get("results", [])

        if not spaces:
            print("   No spaces found. Please create a space first.")
            return

        # Find test space or use first available
        test_space = None
        for space in spaces:
            if space.get("key") == TEST_SPACE_KEY:
                test_space = space
                break

        if not test_space:
            test_space = spaces[0]

        space_id = test_space["id"]
        print(f"   Using space: {test_space.get('name')} (ID: {space_id})")

        # Create comprehensive ADF example
        print("\n2. Creating comprehensive ADF showcase page...")
        comprehensive_adf = create_comprehensive_adf_document()

        showcase_page = confluence._v2_client.create_page(
            space_id=space_id, title="ADF Content Showcase", content=comprehensive_adf, content_format="adf"
        )

        print(f"   Created showcase page: {showcase_page.get('title')} (ID: {showcase_page['id']})")
        print(f"   Page URL: {CONFLUENCE_URL}/wiki/spaces/{test_space.get('key')}/pages/{showcase_page['id']}")

        # Create simple examples
        print("\n3. Creating simple ADF examples...")
        simple_examples = create_simple_adf_examples()
        created_pages = []

        for i, example in enumerate(simple_examples, 1):
            print(f"   Creating example {i}: {example['name']}")

            page = confluence._v2_client.create_page(
                space_id=space_id, title=f"ADF Example: {example['name']}", content=example["adf"], content_format="adf"
            )

            created_pages.append(page)
            print(f"     Created: {page.get('title')} (ID: {page['id']})")

        # Demonstrate content format conversion
        print("\n4. Demonstrating content format handling...")

        # Create page with plain text (will be converted to ADF)
        text_content = "This is plain text that will be converted to ADF format automatically."

        text_page = confluence._v2_client.create_page(
            space_id=space_id,
            title="Plain Text to ADF Example",
            content=text_content,
            content_format=None,  # Auto-detect
        )

        print(f"   Created text page: {text_page.get('title')} (ID: {text_page['id']})")

        # Retrieve and show the converted content
        retrieved_page = confluence._v2_client.get_page_by_id(text_page["id"], expand=["body.atlas_doc_format"])

        body = retrieved_page.get("body", {})
        if body.get("representation") == "atlas_doc_format":
            print("   ✅ Plain text was successfully converted to ADF format")

        print("\n5. Summary of created pages:")
        all_pages = [showcase_page] + created_pages + [text_page]

        for page in all_pages:
            page_url = f"{CONFLUENCE_URL}/wiki/spaces/{test_space.get('key')}/pages/{page['id']}"
            print(f"   • {page.get('title')}: {page_url}")

        print(f"\n   Total pages created: {len(all_pages)}")
        print("\n=== ADF Content Examples completed successfully! ===")
        print("\nNext steps:")
        print("1. Visit the created pages to see how ADF content renders")
        print("2. Edit the pages in Confluence to see the ADF structure")
        print("3. Use the browser developer tools to inspect the ADF JSON")
        print("4. Try modifying the ADF examples and re-running the script")

    except Exception as e:
        print(f"\nError occurred: {e}")
        print("Please check your credentials and Confluence Cloud URL.")
        print("Make sure you have appropriate permissions in the test space.")


def main():
    """Main function."""
    if CONFLUENCE_URL == "https://your-domain.atlassian.net" or API_TOKEN == "your-api-token":
        print("Please update the CONFLUENCE_URL and API_TOKEN variables with your credentials.")
        print("You can also set them as environment variables:")
        print("  export CONFLUENCE_URL='https://your-domain.atlassian.net'")
        print("  export CONFLUENCE_TOKEN='your-api-token'")
        return

    demonstrate_adf_content_creation()


if __name__ == "__main__":
    # Allow configuration via environment variables
    CONFLUENCE_URL = os.getenv("CONFLUENCE_URL", CONFLUENCE_URL)
    API_TOKEN = os.getenv("CONFLUENCE_TOKEN", API_TOKEN)
    TEST_SPACE_KEY = os.getenv("TEST_SPACE_KEY", TEST_SPACE_KEY)

    main()
