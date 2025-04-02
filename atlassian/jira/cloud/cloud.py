"""
Jira Cloud API implementation.
"""

import logging
from typing import Any, Dict, List, Optional, Union, cast

from atlassian.jira.base import JiraBase

log = logging.getLogger(__name__)


class Jira(JiraBase):
    """
    Jira Cloud API wrapper with support for both v2 and v3 APIs.
    Reference for v3: https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/
    """

    def __init__(self, url: str, *args: Any, **kwargs: Any):
        """
        Initialize the Jira Cloud instance.

        Args:
            url: Jira Cloud URL
            args: Arguments to pass to JiraBase
            kwargs: Keyword arguments to pass to JiraBase
        """
        # Set default version to 2 if not specified
        if "api_version" not in kwargs:
            kwargs["api_version"] = "2"

        super(Jira, self).__init__(url, *args, **kwargs)
        
        # Force cloud flag to True
        self.cloud = True

    # Example of a basic issue method supporting both v2 and v3 API
    def get_issue(self, issue_key: str, fields: Optional[str] = None, expand: Optional[str] = None) -> Dict[str, Any]:
        """
        Get an issue by its key.

        Args:
            issue_key: The issue key (e.g. 'JRA-123')
            fields: Comma-separated list of fields to return
            expand: Expand specific fields

        Returns:
            The issue data
        """
        params = {}
        if fields:
            params["fields"] = fields
        if expand:
            params["expand"] = expand

        url = self.get_endpoint("issue_by_id", id=issue_key)
        return self.get(url, params=params)

    # Implement additional methods in Phase 2 and 3

    # Example implementation of API version-specific method
    def add_comment(self, issue_key: str, comment: Union[str, Dict[str, Any]]):
        """
        Add a comment to an issue.

        Args:
            issue_key: The issue key (e.g. 'JRA-123')
            comment: The comment text or an ADF document for v3 API

        Returns:
            The created comment data
        """
        url = self.get_endpoint("issue_comment", id=issue_key)
        
        # Handle API version-specific formats
        if self.api_version == 2:
            # For v2, comment must be a string
            if isinstance(comment, dict):
                raise ValueError("API v2 only supports string comments. Use api_version=3 for ADF comments.")
            data = {"body": comment}
        else:  # v3
            # For v3, comment can be a string or an ADF document
            if isinstance(comment, str):
                # Convert string to ADF document
                data = {
                    "body": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": comment
                                    }
                                ]
                            }
                        ]
                    }
                }
            else:
                # Assume comment is already an ADF document
                data = {"body": comment}
                
        return self.post(url, data=data)

    # Other methods will be implemented in Phases 2 and 3 