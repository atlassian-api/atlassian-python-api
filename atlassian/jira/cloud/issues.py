"""
Jira Cloud API for working with issues
"""

import logging
from typing import Any, Dict, Generator, List, Optional, Union

from atlassian.jira.cloud.cloud import CloudJira

log = logging.getLogger(__name__)


class IssuesJira(CloudJira):
    """
    Jira Cloud API for working with issues
    """

    def get_issue(self, issue_id_or_key: str, fields: str = None, expand: str = None) -> Dict[str, Any]:
        """
        Get an issue by ID or key.

        Args:
            issue_id_or_key: Issue ID or key
            fields: Comma-separated list of field names to include
            expand: Expand options to retrieve additional information

        Returns:
            Dictionary containing the issue data
        """
        issue_id_or_key = self.validate_id_or_key(issue_id_or_key, "issue_id_or_key")
        
        endpoint = f"rest/api/3/issue/{issue_id_or_key}"
        params = self.validate_params(fields=fields, expand=expand)
            
        try:
            return self.get(endpoint, params=params)
        except Exception as e:
            log.error(f"Failed to retrieve issue {issue_id_or_key}: {e}")
            raise
    
    def get_create_meta(self, project_keys: str = None, project_ids: str = None, issue_type_ids: str = None, 
                        issue_type_names: str = None, expand: str = None) -> Dict[str, Any]:
        """
        Get metadata for creating issues.
        
        Args:
            project_keys: Comma-separated list of project keys
            project_ids: Comma-separated list of project IDs
            issue_type_ids: Comma-separated list of issue type IDs
            issue_type_names: Comma-separated list of issue type names
            expand: Additional fields to expand in the response
            
        Returns:
            Dictionary containing the issue creation metadata
        """
        endpoint = "rest/api/3/issue/createmeta"
        params = {}
        
        if project_keys:
            params["projectKeys"] = project_keys
        if project_ids:
            params["projectIds"] = project_ids
        if issue_type_ids:
            params["issuetypeIds"] = issue_type_ids
        if issue_type_names:
            params["issuetypeNames"] = issue_type_names
        if expand:
            params["expand"] = expand
        
        return self.get(endpoint, params=params)

    def create_issue(self, fields: Dict[str, Any], update: Dict[str, Any] = None, 
                     transition: Dict[str, Any] = None, update_history: bool = False) -> Dict[str, Any]:
        """
        Create a new issue.

        Args:
            fields: Issue fields
            update: Issue update operations
            transition: Initial transition for the issue
            update_history: Whether to update issue view history

        Returns:
            Dictionary containing the created issue
        """
        endpoint = "rest/api/3/issue"
        data = {"fields": fields}
        
        if update:
            data["update"] = update
        if transition:
            data["transition"] = transition
            
        params = {}
        if update_history:
            params["updateHistory"] = "true"
            
        return self.post(endpoint, data=data, params=params) 