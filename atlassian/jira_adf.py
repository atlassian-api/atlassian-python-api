"""
Atlassian Document Format (ADF) helper for Jira v3 API

This module provides utility methods for creating ADF documents for rich text fields
in Jira issues, comments, and other places that support ADF.

Reference: https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/
"""

from typing import List, Dict, Any, Union, Optional


class JiraADF:
    """
    Helper class for creating Atlassian Document Format (ADF) documents
    for use with Jira API v3.
    
    This class provides static methods to create various ADF nodes and complete documents
    without needing to understand the full ADF specification.
    
    Usage Example:
    ```python
    # Create a new ADF document
    doc = JiraADF.create_doc()
    
    # Add content
    doc["content"].extend([
        JiraADF.heading("Section Title", 2),
        JiraADF.paragraph("This is a paragraph with some *formatted* text."),
        JiraADF.bullet_list(["Item 1", "Item 2", "Item 3"])
    ])
    
    # Use in Jira API
    jira.update_issue("ISSUE-123", {"description": doc})
    ```
    """
    
    @staticmethod
    def create_doc() -> Dict[str, Any]:
        """
        Create an empty ADF document.
        
        Returns:
            Dict[str, Any]: Empty ADF document structure
        """
        return {
            "version": 1,
            "type": "doc",
            "content": []
        }
    
    @staticmethod
    def paragraph(text: str = "", marks: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Create a paragraph node. Can include formatted text with marks.
        
        Args:
            text: The text content of the paragraph
            marks: Optional list of formatting marks (e.g., ["strong", "em"])
            
        Returns:
            Dict[str, Any]: ADF paragraph node
        """
        text_node = {"type": "text", "text": text}
        
        if marks:
            text_node["marks"] = [{"type": mark} for mark in marks]
            
        return {
            "type": "paragraph",
            "content": [text_node]
        }
    
    @staticmethod
    def text(content: str, mark: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a text node with optional formatting.
        
        Args:
            content: The text content
            mark: Optional formatting mark (e.g., "strong", "em", "code")
            
        Returns:
            Dict[str, Any]: ADF text node
        """
        node = {"type": "text", "text": content}
        
        if mark:
            node["marks"] = [{"type": mark}]
            
        return node
    
    @staticmethod
    def heading(text: str, level: int = 1) -> Dict[str, Any]:
        """
        Create a heading node.
        
        Args:
            text: The heading text
            level: Heading level (1-6)
            
        Returns:
            Dict[str, Any]: ADF heading node
        """
        if level < 1:
            level = 1
        elif level > 6:
            level = 6
            
        return {
            "type": "heading",
            "attrs": {"level": level},
            "content": [
                {"type": "text", "text": text}
            ]
        }
    
    @staticmethod
    def bullet_list(items: List[str]) -> Dict[str, Any]:
        """
        Create a bullet list node.
        
        Args:
            items: List of text items
            
        Returns:
            Dict[str, Any]: ADF bullet list node
        """
        content = []
        for item in items:
            content.append({
                "type": "listItem",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": item}
                        ]
                    }
                ]
            })
            
        return {
            "type": "bulletList",
            "content": content
        }
    
    @staticmethod
    def numbered_list(items: List[str]) -> Dict[str, Any]:
        """
        Create a numbered list node.
        
        Args:
            items: List of text items
            
        Returns:
            Dict[str, Any]: ADF numbered list node
        """
        content = []
        for item in items:
            content.append({
                "type": "listItem",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": item}
                        ]
                    }
                ]
            })
            
        return {
            "type": "orderedList",
            "content": content
        }
    
    @staticmethod
    def code_block(text: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a code block node.
        
        Args:
            text: The code content
            language: Optional language for syntax highlighting
            
        Returns:
            Dict[str, Any]: ADF code block node
        """
        node = {
            "type": "codeBlock",
            "content": [
                {"type": "text", "text": text}
            ]
        }
        
        if language:
            node["attrs"] = {"language": language}
            
        return node
    
    @staticmethod
    def blockquote(text: str) -> Dict[str, Any]:
        """
        Create a blockquote node.
        
        Args:
            text: The quote content
            
        Returns:
            Dict[str, Any]: ADF blockquote node
        """
        return {
            "type": "blockquote",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": text}
                    ]
                }
            ]
        }
    
    @staticmethod
    def link(text: str, url: str) -> Dict[str, Any]:
        """
        Create a paragraph containing a link.
        
        Args:
            text: The link text
            url: The URL
            
        Returns:
            Dict[str, Any]: ADF paragraph with link
        """
        return {
            "type": "paragraph",
            "content": [
                {
                    "type": "text",
                    "text": text,
                    "marks": [
                        {
                            "type": "link",
                            "attrs": {
                                "href": url
                            }
                        }
                    ]
                }
            ]
        }
    
    @staticmethod
    def inline_link(text: str, url: str) -> Dict[str, Any]:
        """
        Create an inline link node (without surrounding paragraph).
        
        Args:
            text: The link text
            url: The URL
            
        Returns:
            Dict[str, Any]: ADF text node with link mark
        """
        return {
            "type": "text",
            "text": text,
            "marks": [
                {
                    "type": "link",
                    "attrs": {
                        "href": url
                    }
                }
            ]
        }
    
    @staticmethod
    def mention(account_id: str, text: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a mention node.
        
        Args:
            account_id: User account ID
            text: Optional display text (defaults to "@user")
            
        Returns:
            Dict[str, Any]: ADF paragraph with mention
        """
        return {
            "type": "paragraph",
            "content": [
                {
                    "type": "mention",
                    "attrs": {
                        "id": account_id,
                        "text": text or "@user"
                    }
                }
            ]
        }
    
    @staticmethod
    def inline_mention(account_id: str, text: Optional[str] = None) -> Dict[str, Any]:
        """
        Create an inline mention node (without surrounding paragraph).
        
        Args:
            account_id: User account ID
            text: Optional display text (defaults to "@user")
            
        Returns:
            Dict[str, Any]: ADF mention node
        """
        return {
            "type": "mention",
            "attrs": {
                "id": account_id,
                "text": text or "@user"
            }
        }
    
    @staticmethod
    def panel(text: str, panel_type: str = "info") -> Dict[str, Any]:
        """
        Create a panel node.
        
        Args:
            text: The panel content
            panel_type: Panel type ("info", "note", "warning", "success", "error")
            
        Returns:
            Dict[str, Any]: ADF panel node
        """
        valid_types = ["info", "note", "warning", "success", "error"]
        if panel_type not in valid_types:
            panel_type = "info"
            
        return {
            "type": "panel",
            "attrs": {
                "panelType": panel_type
            },
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": text}
                    ]
                }
            ]
        }
    
    @staticmethod
    def table(rows: List[List[str]], headers: bool = False) -> Dict[str, Any]:
        """
        Create a table node.
        
        Args:
            rows: List of rows, each containing a list of cell values
            headers: Whether the first row should be treated as headers
            
        Returns:
            Dict[str, Any]: ADF table node
        """
        # Create table content
        content = []
        
        for i, row in enumerate(rows):
            row_content = []
            for cell in row:
                cell_content = {
                    "type": "tableCell",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "text": cell}
                            ]
                        }
                    ]
                }
                row_content.append(cell_content)
                
            row_node = {
                "type": "tableRow",
                "content": row_content
            }
            content.append(row_node)
        
        return {
            "type": "table",
            "attrs": {
                "isNumberColumnEnabled": False,
                "layout": "default"
            },
            "content": content
        }
    
    @staticmethod
    def emoji(shortname: str) -> Dict[str, Any]:
        """
        Create an emoji node.
        
        Args:
            shortname: Emoji shortname (e.g., ":smile:")
            
        Returns:
            Dict[str, Any]: ADF emoji node
        """
        return {
            "type": "emoji",
            "attrs": {
                "shortName": shortname
            }
        }
    
    @staticmethod
    def rule() -> Dict[str, Any]:
        """
        Create a horizontal rule node.
        
        Returns:
            Dict[str, Any]: ADF rule node
        """
        return {
            "type": "rule"
        }
    
    @staticmethod
    def date(timestamp: str) -> Dict[str, Any]:
        """
        Create a date node.
        
        Args:
            timestamp: ISO format date
            
        Returns:
            Dict[str, Any]: ADF date node
        """
        return {
            "type": "date",
            "attrs": {
                "timestamp": timestamp
            }
        }
    
    @staticmethod
    def status(text: str, color: str = "neutral") -> Dict[str, Any]:
        """
        Create a status node.
        
        Args:
            text: Status text
            color: Status color ("neutral", "green", "yellow", "red", "blue", "purple")
            
        Returns:
            Dict[str, Any]: ADF status node
        """
        valid_colors = ["neutral", "green", "yellow", "red", "blue", "purple"]
        if color not in valid_colors:
            color = "neutral"
            
        return {
            "type": "status",
            "attrs": {
                "text": text,
                "color": color
            }
        }
    
    @staticmethod
    def from_markdown(markdown_text: str) -> Dict[str, Any]:
        """
        Convert markdown text to ADF document.
        
        This is a simple implementation that handles basic markdown.
        For complete conversion, use Jira's API methods.
        
        Args:
            markdown_text: Markdown formatted text
            
        Returns:
            Dict[str, Any]: ADF document
        """
        # This is a simplified implementation that handles some basic markdown
        # For a proper implementation, use Jira's built-in conversion API
        
        lines = markdown_text.split("\n")
        doc = JiraADF.create_doc()
        
        current_list = None
        current_list_items = []
        
        for line in lines:
            if not line.strip():
                continue
                
            # Heading
            if line.startswith("#"):
                count = 0
                for char in line:
                    if char == "#":
                        count += 1
                    else:
                        break
                text = line[count:].strip()
                doc["content"].append(JiraADF.heading(text, count))
                
            # Bullet list
            elif line.strip().startswith("* ") or line.strip().startswith("- "):
                text = line.strip()[2:].strip()
                
                if current_list != "bullet":
                    # Finish previous list if any
                    if current_list == "numbered" and current_list_items:
                        doc["content"].append(JiraADF.numbered_list(current_list_items))
                        current_list_items = []
                    
                    current_list = "bullet"
                
                current_list_items.append(text)
                
            # Numbered list
            elif line.strip() and line.strip()[0].isdigit() and ". " in line:
                text = line.strip().split(". ", 1)[1].strip()
                
                if current_list != "numbered":
                    # Finish previous list if any
                    if current_list == "bullet" and current_list_items:
                        doc["content"].append(JiraADF.bullet_list(current_list_items))
                        current_list_items = []
                    
                    current_list = "numbered"
                
                current_list_items.append(text)
                
            # Normal paragraph
            else:
                # Finish any ongoing list
                if current_list == "bullet" and current_list_items:
                    doc["content"].append(JiraADF.bullet_list(current_list_items))
                    current_list_items = []
                    current_list = None
                elif current_list == "numbered" and current_list_items:
                    doc["content"].append(JiraADF.numbered_list(current_list_items))
                    current_list_items = []
                    current_list = None
                
                # Simple formatting
                text = line.strip()
                doc["content"].append(JiraADF.paragraph(text))
        
        # Handle any remaining list items
        if current_list == "bullet" and current_list_items:
            doc["content"].append(JiraADF.bullet_list(current_list_items))
        elif current_list == "numbered" and current_list_items:
            doc["content"].append(JiraADF.numbered_list(current_list_items))
        
        return doc 