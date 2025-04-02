"""
Adapter for Jira Rich Text providing backward compatibility with the original Jira client
"""

import logging
import warnings
from typing import Optional, List, Dict, Any, Union

from atlassian.jira.cloud.richtext import RichTextJira


class RichTextJiraAdapter(RichTextJira):
    """
    Adapter for Jira Rich Text providing backward compatibility with the original Jira client
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._legacy_method_map = {
            # No direct mapping needed for richtext as it's a new feature
        }

    def wiki_to_adf(self, wiki_text: str) -> dict:
        """
        Convert wiki markup to Atlassian Document Format (ADF)
        
        Deprecated in favor of convert_wiki_to_adf
        
        :param wiki_text: Text in wiki markup format
        :return: ADF document as dictionary
        """
        warnings.warn(
            "Method wiki_to_adf is deprecated, use convert_wiki_to_adf instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.convert_wiki_to_adf(wiki_text)

    def text_to_adf(self, text: str) -> dict:
        """
        Convert plain text to Atlassian Document Format (ADF)
        
        Deprecated in favor of convert_text_to_adf
        
        :param text: Plain text
        :return: ADF document as dictionary
        """
        warnings.warn(
            "Method text_to_adf is deprecated, use convert_text_to_adf instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.convert_text_to_adf(text)

    def add_comment(self, issue: str, comment: str, adf: bool = False) -> dict:
        """
        Add comment to an issue with option to use ADF format
        
        This is a compatibility method that supports both plain text and ADF
        
        :param issue: Issue key or ID
        :param comment: Comment text or ADF document
        :param adf: Whether comment is already in ADF format
        :return: Created comment
        """
        if adf:
            return self.add_comment_with_adf(issue, comment)
        else:
            # Convert text to ADF first
            adf_document = self.convert_text_to_adf(comment)
            return self.add_comment_with_adf(issue, adf_document)

    def update_comment(self, issue: str, comment_id: str, comment: str, adf: bool = False) -> dict:
        """
        Update comment with option to use ADF format
        
        This is a compatibility method that supports both plain text and ADF
        
        :param issue: Issue key or ID
        :param comment_id: Comment ID
        :param comment: Comment text or ADF document
        :param adf: Whether comment is already in ADF format
        :return: Updated comment
        """
        if adf:
            return self.update_comment_with_adf(issue, comment_id, comment)
        else:
            # Convert text to ADF first
            adf_document = self.convert_text_to_adf(comment)
            return self.update_comment_with_adf(issue, comment_id, adf_document)

    def create_issue(self, fields: dict, is_adf: bool = False) -> dict:
        """
        Create an issue with option to use ADF for rich text fields
        
        This is a compatibility method that supports both plain text and ADF
        
        :param fields: Issue fields
        :param is_adf: Whether the description and other text fields are already in ADF format
        :return: Created issue
        """
        if is_adf:
            return self.create_issue_with_adf(fields)
        else:
            # Convert description to ADF if it exists
            if "description" in fields and isinstance(fields["description"], str):
                fields["description"] = self.convert_text_to_adf(fields["description"])
                
            return self.create_issue_with_adf(fields) 