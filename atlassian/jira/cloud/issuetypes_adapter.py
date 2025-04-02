"""
Adapter for Jira Issue Types and Field Configurations providing backward compatibility
with the original Jira client
"""

import logging
import warnings
from typing import Optional, List, Dict, Any, Union

from atlassian.jira.cloud.issuetypes import IssueTypesJira


class IssueTypesJiraAdapter(IssueTypesJira):
    """
    Adapter for Jira Issue Types providing backward compatibility with the original Jira client
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._legacy_method_map = {
            "issue_types": "get_all_issue_types",
            "issue_type": "get_issue_type",
            "issue_type_create": "create_issue_type",
            "issue_type_update": "update_issue_type",
            "issue_type_delete": "delete_issue_type",
            "get_field_config": "get_field_configurations",
            "get_all_custom_fields": "get_all_fields",
            "create_custom_field": "create_custom_field",
        }

    def issue_types(self):
        """
        Get all issue types

        Deprecated in favor of get_all_issue_types
        
        :return: List of issue types
        """
        warnings.warn(
            "Method issue_types is deprecated, use get_all_issue_types instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_all_issue_types()

    def issue_type(self, issue_type_id):
        """
        Get issue type by ID

        Deprecated in favor of get_issue_type
        
        :param issue_type_id: Issue type ID
        :return: Issue type details
        """
        warnings.warn(
            "Method issue_type is deprecated, use get_issue_type instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_issue_type(issue_type_id)

    def issue_type_create(self, name, description=None, type="standard"):
        """
        Create a new issue type

        Deprecated in favor of create_issue_type
        
        :param name: Name of the issue type
        :param description: Description of the issue type
        :param type: Type of the issue type (standard, subtask)
        :return: Created issue type
        """
        warnings.warn(
            "Method issue_type_create is deprecated, use create_issue_type instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.create_issue_type(name, description, type)

    def issue_type_update(self, issue_type_id, name=None, description=None):
        """
        Update an issue type

        Deprecated in favor of update_issue_type
        
        :param issue_type_id: Issue type ID
        :param name: New name for the issue type
        :param description: New description for the issue type
        :return: Updated issue type
        """
        warnings.warn(
            "Method issue_type_update is deprecated, use update_issue_type instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.update_issue_type(issue_type_id, name, description)

    def issue_type_delete(self, issue_type_id):
        """
        Delete an issue type

        Deprecated in favor of delete_issue_type
        
        :param issue_type_id: ID of the issue type to delete
        :return: None
        """
        warnings.warn(
            "Method issue_type_delete is deprecated, use delete_issue_type instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.delete_issue_type(issue_type_id)

    def get_field_config(self, config_id=None):
        """
        Get field configurations

        Deprecated in favor of get_field_configurations
        
        :param config_id: Field configuration ID
        :return: Field configuration details
        """
        warnings.warn(
            "Method get_field_config is deprecated, use get_field_configurations instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_field_configurations(ids=config_id)

    def get_all_custom_fields(self):
        """
        Get all custom fields

        Deprecated in favor of get_all_fields with include_system=False
        
        :return: List of custom fields
        """
        warnings.warn(
            "Method get_all_custom_fields is deprecated, use get_all_fields with include_system=False instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_all_fields(include_system=False)

    def projecttype(self, key):
        """
        Get project type by key
        
        Legacy method, not directly mapped to new API
        
        :param key: Project type key
        :return: Project type details
        """
        warnings.warn(
            "Method projecttype is deprecated and may not work as expected in V3 API",
            DeprecationWarning,
            stacklevel=2,
        )
        url = f"rest/api/3/project/type/{key}"
        return self.get(url) 