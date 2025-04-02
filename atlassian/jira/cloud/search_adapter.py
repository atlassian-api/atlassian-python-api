"""
Adapter for Jira Search providing backward compatibility with the original Jira client
"""

import logging
import warnings
from typing import Optional, List, Dict, Any, Union

from atlassian.jira.cloud.search import SearchJira


class SearchJiraAdapter(SearchJira):
    """
    Adapter for Jira Search providing backward compatibility with the original Jira client
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._legacy_method_map = {
            "jql": "search_issues",
            "jql_get": "search_issues",
            "user_find_by_user_string": "find_users_for_picker",
            "user_find": "search_users",
            "user_assignable_search": "find_assignable_users",
            "get_jql_autocomplete_data": "get_field_reference_data",
            "jql_parse": "parse_jql_queries",
            "jql_validators": "get_jql_autocomplete_data",
        }

    def jql(self, jql, fields='*all', start=0, limit=50, expand=None, validate_query=None):
        """
        Search using JQL (POST method)

        Deprecated in favor of search_issues
        
        :param jql: JQL query string
        :param fields: Fields to return
        :param start: Index of the first issue to return
        :param limit: Maximum number of issues to return
        :param expand: List of fields to expand
        :param validate_query: Whether to validate the JQL query
        :return: Search results
        """
        warnings.warn(
            "Method jql is deprecated, use search_issues instead",
            DeprecationWarning,
            stacklevel=2,
        )
        
        if fields == '*all':
            fields = None
        
        return self.search_issues(
            jql=jql, 
            start_at=start, 
            max_results=limit, 
            fields=fields, 
            expand=expand, 
            validate_query=validate_query
        )

    def jql_get(self, jql, fields='*all', start=0, limit=50, expand=None, validate_query=None):
        """
        Search using JQL (GET method)

        Deprecated in favor of search_issues
        
        :param jql: JQL query string
        :param fields: Fields to return
        :param start: Index of the first issue to return
        :param limit: Maximum number of issues to return
        :param expand: List of fields to expand
        :param validate_query: Whether to validate the JQL query
        :return: Search results
        """
        warnings.warn(
            "Method jql_get is deprecated, use search_issues instead",
            DeprecationWarning,
            stacklevel=2,
        )
        
        if fields == '*all':
            fields = None
        
        return self.search_issues(
            jql=jql, 
            start_at=start, 
            max_results=limit, 
            fields=fields, 
            expand=expand, 
            validate_query=validate_query
        )

    def user_find_by_user_string(self, query, start=0, limit=50, include_inactive=False):
        """
        Find users by username, name, or email

        Deprecated in favor of find_users_for_picker
        
        :param query: User string to search
        :param start: Index of the first user to return
        :param limit: Maximum number of users to return
        :param include_inactive: Whether to include inactive users
        :return: List of users
        """
        warnings.warn(
            "Method user_find_by_user_string is deprecated, use find_users_for_picker instead",
            DeprecationWarning,
            stacklevel=2,
        )
        
        return self.find_users_for_picker(
            query=query, 
            max_results=limit
        )

    def user_find(self, query, start=0, limit=50, include_inactive=False):
        """
        Find users by query

        Deprecated in favor of search_users
        
        :param query: User query to search
        :param start: Index of the first user to return
        :param limit: Maximum number of users to return
        :param include_inactive: Whether to include inactive users
        :return: List of users
        """
        warnings.warn(
            "Method user_find is deprecated, use search_users instead",
            DeprecationWarning,
            stacklevel=2,
        )
        
        return self.search_users(
            query=query, 
            start_at=start, 
            max_results=limit, 
            include_inactive=include_inactive
        )

    def user_assignable_search(self, username, project_key=None, issue_key=None, start=0, limit=50):
        """
        Find users assignable to issues

        Deprecated in favor of find_assignable_users
        
        :param username: Username to search
        :param project_key: Optional project key
        :param issue_key: Optional issue key
        :param start: Index of the first user to return
        :param limit: Maximum number of users to return
        :return: List of assignable users
        """
        warnings.warn(
            "Method user_assignable_search is deprecated, use find_assignable_users instead",
            DeprecationWarning,
            stacklevel=2,
        )
        
        return self.find_assignable_users(
            query=username, 
            project_key=project_key, 
            issue_key=issue_key, 
            max_results=limit, 
            start_at=start
        )

    def get_jql_autocomplete_data(self):
        """
        Get JQL autocomplete data

        Deprecated in favor of get_field_reference_data
        
        :return: JQL autocomplete data
        """
        warnings.warn(
            "Method get_jql_autocomplete_data is deprecated, use get_field_reference_data instead",
            DeprecationWarning,
            stacklevel=2,
        )
        
        return self.get_field_reference_data()

    def jql_parse(self, jql_queries, validation_level="strict"):
        """
        Parse JQL queries

        Deprecated in favor of parse_jql_queries
        
        :param jql_queries: List of JQL queries to parse
        :param validation_level: Validation level
        :return: Parse results
        """
        warnings.warn(
            "Method jql_parse is deprecated, use parse_jql_queries instead",
            DeprecationWarning,
            stacklevel=2,
        )
        
        return self.parse_jql_queries(jql_queries, validation_level)

    def jql_validators(self):
        """
        Get JQL validators

        Deprecated in favor of get_field_reference_data
        
        :return: JQL validators
        """
        warnings.warn(
            "Method jql_validators is deprecated, use get_field_reference_data instead",
            DeprecationWarning,
            stacklevel=2,
        )
        
        data = self.get_field_reference_data()
        # Try to maintain format similar to old method's return value
        if "visibleFieldNames" in data:
            return data["visibleFieldNames"]
        return data 