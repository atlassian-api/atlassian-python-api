"""
Atlassian Document Format (ADF) support for Jira descriptions and comments
Reference: https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/
"""

from atlassian.jira.cloud.cloud import CloudJira


class RichTextJira(CloudJira):
    """
    Jira Cloud API for working with rich text content using Atlassian Document Format (ADF)
    """

    def convert_wiki_to_adf(self, wiki_representation: str) -> dict:
        """
        Convert wiki markdown to Atlassian Document Format (ADF)

        :param wiki_representation: String containing wiki markup
        :return: JSON object containing ADF
        """
        url = "rest/api/3/wiki/convertToADF"
        data = {"wiki": wiki_representation}
        return self.post(url, data=data)

    def convert_text_to_adf(self, plain_text: str) -> dict:
        """
        Create an ADF document from plain text

        :param plain_text: Plain text to convert to ADF
        :return: ADF document as dictionary
        """
        # Simple implementation for plain text
        adf = {
            "version": 1,
            "type": "doc",
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": plain_text}]}],
        }
        return adf

    def create_adf_paragraph(self, text: str = "", marks: list = None) -> dict:
        """
        Create an ADF paragraph with optional marks

        :param text: Text content
        :param marks: List of marks like ["strong", "em", "code", etc.]
        :return: ADF paragraph node
        """
        text_node = {"type": "text", "text": text}

        if marks:
            text_node["marks"] = [{"type": mark} for mark in marks]

        return {"type": "paragraph", "content": [text_node]}

    def create_adf_bullet_list(self, items: list) -> dict:
        """
        Create an ADF bullet list

        :param items: List of text items
        :return: ADF bullet list node
        """
        content = []
        for item in items:
            content.append(
                {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": item}]}]}
            )

        return {"type": "bulletList", "content": content}

    def create_adf_numbered_list(self, items: list) -> dict:
        """
        Create an ADF numbered list

        :param items: List of text items
        :return: ADF numbered list node
        """
        content = []
        for item in items:
            content.append(
                {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": item}]}]}
            )

        return {"type": "orderedList", "content": content}

    def create_adf_code_block(self, text: str, language: str = None) -> dict:
        """
        Create an ADF code block

        :param text: Code content
        :param language: Optional language for syntax highlighting
        :return: ADF code block node
        """
        node = {"type": "codeBlock", "content": [{"type": "text", "text": text}]}

        if language:
            node["attrs"] = {"language": language}

        return node

    def create_adf_quote(self, text: str) -> dict:
        """
        Create an ADF blockquote

        :param text: Quote content
        :return: ADF blockquote node
        """
        return {"type": "blockquote", "content": [{"type": "paragraph", "content": [{"type": "text", "text": text}]}]}

    def create_adf_heading(self, text: str, level: int = 1) -> dict:
        """
        Create an ADF heading

        :param text: Heading text
        :param level: Heading level (1-6)
        :return: ADF heading node
        """
        if level < 1:
            level = 1
        elif level > 6:
            level = 6

        return {"type": "heading", "attrs": {"level": level}, "content": [{"type": "text", "text": text}]}

    def create_adf_link(self, text: str, url: str) -> dict:
        """
        Create an ADF link node

        :param text: Link text
        :param url: URL
        :return: ADF link node
        """
        return {
            "type": "paragraph",
            "content": [{"type": "text", "text": text, "marks": [{"type": "link", "attrs": {"href": url}}]}],
        }

    def create_adf_mention(self, account_id: str) -> dict:
        """
        Create an ADF mention node

        :param account_id: User account ID
        :return: ADF mention node
        """
        return {"type": "paragraph", "content": [{"type": "mention", "attrs": {"id": account_id, "text": "@user"}}]}

    def create_adf_document(self, content: list) -> dict:
        """
        Create a complete ADF document from a list of nodes

        :param content: List of ADF nodes
        :return: Complete ADF document
        """
        return {"version": 1, "type": "doc", "content": content}

    def create_issue_with_adf(self, fields: dict) -> dict:
        """
        Create an issue with ADF content in description or other rich text fields

        :param fields: Issue fields with ADF for description or comments
        :return: Created issue
        """
        url = "rest/api/3/issue"
        return self.post(url, data=fields)

    def add_comment_with_adf(self, issue_key_or_id: str, adf_document: dict) -> dict:
        """
        Add a comment to an issue using ADF

        :param issue_key_or_id: Issue key or ID
        :param adf_document: Comment content in ADF format
        :return: Added comment
        """
        url = f"rest/api/3/issue/{issue_key_or_id}/comment"
        data = {"body": adf_document}
        return self.post(url, data=data)

    def update_comment_with_adf(self, issue_key_or_id: str, comment_id: str, adf_document: dict) -> dict:
        """
        Update an existing comment using ADF

        :param issue_key_or_id: Issue key or ID
        :param comment_id: Comment ID
        :param adf_document: Comment content in ADF format
        :return: Updated comment
        """
        url = f"rest/api/3/issue/{issue_key_or_id}/comment/{comment_id}"
        data = {"body": adf_document}
        return self.put(url, data=data)
