# Jira v3 Rich Text and ADF Guide

This guide explains how to work with rich text content in Jira using the Atlassian Document Format (ADF) and the specialized RichText client.

## Introduction to ADF

Atlassian Document Format (ADF) is a format used for storing rich text content in Jira issues, comments, and other text fields. It replaces the older wiki markup format and provides more consistent rendering across Atlassian products.

ADF is a JSON-based document structure that consists of nodes with different types, attributes, and content. The format allows for complex formatting, including:

- Headings, paragraphs, and text formatting
- Lists (bullet, numbered)
- Tables
- Code blocks
- Block quotes
- Links
- Mentions
- Emojis
- Panels
- Status lozenge
- And more

## Getting Started with the RichText Client

The Jira v3 API implementation includes a specialized client for working with rich text content. You can use this client to create, convert, and manipulate ADF documents.

### Creating a RichText Client

```python
from atlassian.jira import get_richtext_jira_instance

# Create a rich text client
richtext_jira = get_richtext_jira_instance(
    url="https://your-instance.atlassian.net",
    username="your-email@example.com",
    password="your-api-token"
)
```

### Converting Text to ADF

```python
# Convert plain text to ADF
plain_text = "This is a simple text that will be converted to ADF."
adf_document = richtext_jira.convert_text_to_adf(plain_text)

# Convert wiki markup to ADF (if your Jira instance supports it)
wiki_text = "h1. Heading\n\nThis is a paragraph with *bold* and _italic_ text."
try:
    adf_document = richtext_jira.convert_wiki_to_adf(wiki_text)
except Exception as e:
    print(f"Wiki conversion not supported: {e}")
```

### Creating ADF Content

The RichText client provides methods to create various ADF nodes:

```python
# Create paragraphs
paragraph = richtext_jira.create_adf_paragraph("This is a paragraph.")

# Create headings
heading = richtext_jira.create_adf_heading("This is a heading", level=2)

# Create bullet lists
bullet_list = richtext_jira.create_adf_bullet_list(["Item 1", "Item 2", "Item 3"])

# Create numbered lists
numbered_list = richtext_jira.create_adf_numbered_list(["First", "Second", "Third"])

# Create code blocks
code_block = richtext_jira.create_adf_code_block("def hello():\n    print('Hello, world!')", language="python")

# Create block quotes
blockquote = richtext_jira.create_adf_quote("This is a quote.")

# Create links
link = richtext_jira.create_adf_link("Atlassian", "https://atlassian.com")

# Create mentions
mention = richtext_jira.create_adf_mention("account-id-123")
```

### Building Complete ADF Documents

You can combine multiple ADF nodes to create a complete document:

```python
# Create an empty document
document = richtext_jira.create_adf_document([
    richtext_jira.create_adf_heading("Document Title", level=1),
    richtext_jira.create_adf_paragraph("This is an introduction paragraph."),
    richtext_jira.create_adf_bullet_list(["Point 1", "Point 2", "Point 3"]),
    richtext_jira.create_adf_code_block("console.log('Hello');", language="javascript")
])
```

## Using the JiraADF Helper Class

For more advanced ADF document creation, you can use the `JiraADF` helper class, which provides a more intuitive API:

```python
from atlassian.jira_adf import JiraADF

# Create an empty ADF document
doc = JiraADF.create_doc()

# Add content
doc["content"].extend([
    JiraADF.heading("Document Title", 1),
    JiraADF.paragraph("This is an introduction paragraph."),
    JiraADF.bullet_list(["Point 1", "Point 2", "Point 3"]),
    JiraADF.code_block("console.log('Hello');", language="javascript"),
    JiraADF.rule(),  # Horizontal rule
    JiraADF.heading("Section with Table", 2),
    JiraADF.table([
        ["Header 1", "Header 2", "Header 3"],
        ["Cell 1", "Cell 2", "Cell 3"],
        ["Cell 4", "Cell 5", "Cell 6"]
    ]),
    JiraADF.panel("This is an info panel", panel_type="info"),
    JiraADF.status("Done", color="green")
])
```

### Available JiraADF Methods

The JiraADF class provides the following static methods:

- `create_doc()` - Create an empty ADF document
- `paragraph(text, marks)` - Create a paragraph node
- `text(content, mark)` - Create a text node
- `heading(text, level)` - Create a heading node
- `bullet_list(items)` - Create a bullet list node
- `numbered_list(items)` - Create a numbered list node
- `code_block(text, language)` - Create a code block node
- `blockquote(text)` - Create a blockquote node
- `link(text, url)` - Create a paragraph with a link
- `inline_link(text, url)` - Create an inline link node
- `mention(account_id, text)` - Create a mention node
- `inline_mention(account_id, text)` - Create an inline mention node
- `panel(text, panel_type)` - Create a panel node
- `table(rows, headers)` - Create a table node
- `emoji(shortname)` - Create an emoji node
- `rule()` - Create a horizontal rule node
- `date(timestamp)` - Create a date node
- `status(text, color)` - Create a status node
- `from_markdown(markdown_text)` - Convert markdown text to ADF document

## Using ADF in Jira Operations

### Creating Issues with ADF

```python
from atlassian.jira import get_jira_instance
from atlassian.jira_adf import JiraADF

# Create a Jira client
jira = get_jira_instance(
    url="https://your-instance.atlassian.net",
    username="your-email@example.com",
    password="your-api-token",
    api_version=3
)

# Create an ADF document for the description
description = JiraADF.create_doc()
description["content"].extend([
    JiraADF.heading("Issue Description", 2),
    JiraADF.paragraph("This issue requires attention."),
    JiraADF.bullet_list([
        "First requirement",
        "Second requirement",
        "Third requirement"
    ])
])

# Create an issue with ADF description
issue = jira.create_issue(
    fields={
        "project": {"key": "PROJ"},
        "summary": "Issue with ADF description",
        "issuetype": {"name": "Task"},
        "description": description
    }
)
```

### Adding Comments with ADF

```python
# Create an ADF document for the comment
comment = JiraADF.create_doc()
comment["content"].extend([
    JiraADF.heading("Comment Title", 3),
    JiraADF.paragraph("This is a comment with formatting."),
    JiraADF.code_block("const x = 42;", language="javascript")
])

# Add the comment to an issue
jira.add_comment("PROJ-123", comment)

# Alternatively, use the richtext client
richtext_jira.add_comment_with_adf("PROJ-123", comment)
```

### Updating Issues with ADF

```python
# Update an issue's description
jira.update_issue(
    "PROJ-123",
    fields={
        "description": JiraADF.from_markdown("# Updated Description\n\nThis is an updated description with **bold** text.")
    }
)
```

### Working with ADF in Comments

```python
# Get all comments for an issue
comments = jira.get_issue_comments("PROJ-123")

# Get a specific comment
comment = jira.get_issue_comment("PROJ-123", "comment-id-123")

# Update a comment with ADF
richtext_jira.update_comment_with_adf(
    "PROJ-123",
    "comment-id-123", 
    JiraADF.create_doc()["content"].extend([
        JiraADF.paragraph("Updated comment text."),
        JiraADF.bullet_list(["New item 1", "New item 2"])
    ])
)
```

## Converting from Markdown to ADF

The JiraADF class provides a simple method to convert Markdown to ADF:

```python
# Convert Markdown to ADF
markdown_text = """
# Heading 1

This is a paragraph with **bold** text.

## Heading 2

- Item 1
- Item 2
- Item 3

1. Numbered item 1
2. Numbered item 2
"""

adf_doc = JiraADF.from_markdown(markdown_text)
```

Note that this is a simple implementation that handles basic Markdown. For more complex Markdown, you might want to use a dedicated Markdown parser or Jira's built-in conversion API if available.

## Working with ADF in Custom Fields

Some Jira custom fields support ADF. You can update these fields using the same approach:

```python
# First, find custom fields that support ADF
custom_fields = jira.get_custom_fields()
adf_fields = [field for field in custom_fields if field.get("supportsADF", False)]

# Update a custom field with ADF content
if adf_fields:
    field_id = adf_fields[0]["id"]
    jira.update_issue(
        "PROJ-123",
        fields={
            field_id: JiraADF.paragraph("Custom field content with ADF")
        }
    )
```

## Best Practices for ADF

1. **Start Simple**: Begin with simple ADF structures and gradually add complexity as needed.
2. **Test Rendering**: Always test how your ADF documents render in Jira's UI, especially for complex structures.
3. **Validate**: Ensure your ADF document follows the correct structure to avoid rendering issues.
4. **Use Helper Methods**: Leverage the RichText client and JiraADF helper class instead of creating ADF JSON manually.
5. **Consider Storage Size**: Complex ADF documents can be larger than plain text, so be mindful of storage limits.

## Limitations and Considerations

- Not all Jira instances support all ADF features, especially older Server versions.
- ADF support may vary between different Jira products (Core, Software, Service Management).
- Some advanced formatting options might only be available through the Jira UI.
- ADF documents can be more verbose than plain text, which can affect API response sizes.

## Conclusion

The Rich Text client and JiraADF helper provide powerful tools for working with formatted text in Jira. By leveraging these tools, you can create rich, well-formatted content in your Jira issues, comments, and other text fields. 