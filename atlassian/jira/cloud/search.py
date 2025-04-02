"""
Jira Cloud API for advanced search capabilities
"""

from atlassian.jira.cloud.cloud_base import CloudJira


class SearchJira(CloudJira):
    """
    Jira Cloud API for advanced search capabilities
    """

    def search_issues(self, jql, start_at=0, max_results=50, fields=None, expand=None, 
                    validate_query=None, validate_query_type="strict"):
        """
        Search for issues using JQL

        :param jql: JQL query string
        :param start_at: Index of the first issue to return
        :param max_results: Maximum number of issues to return (max 1000)
        :param fields: List of fields to return for each issue (default: return all fields)
        :param expand: List of parameters to expand (e.g. "renderedFields", "names", "changelog")
        :param validate_query: Whether to validate the JQL query
        :param validate_query_type: Validation type - must be one of "strict", "warn", "none"
        :return: Search results containing issues that match the query
        """
        url = "rest/api/3/search"
        data = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results
        }
        
        if fields:
            if isinstance(fields, list):
                data["fields"] = fields
            else:
                data["fields"] = [fields]
        
        if expand:
            if isinstance(expand, list):
                data["expand"] = expand
            else:
                data["expand"] = [expand]
        
        if validate_query is not None:
            data["validateQuery"] = validate_query
        
        if validate_query_type:
            data["validateQueryType"] = validate_query_type
        
        return self.post(url, data=data)

    def search_users(self, query, start_at=0, max_results=50, include_inactive=False, 
                    include_active=True):
        """
        Search for users

        :param query: Search query
        :param start_at: Index of the first user to return
        :param max_results: Maximum number of users to return
        :param include_inactive: Whether to include inactive users
        :param include_active: Whether to include active users
        :return: List of users matching the query
        """
        url = "rest/api/3/user/search"
        params = {
            "query": query,
            "startAt": start_at,
            "maxResults": max_results,
            "includeInactive": include_inactive,
            "includeActive": include_active
        }
        
        return self.get(url, params=params)

    def get_issue_search_metadata(self, jql_queries=None):
        """
        Get metadata for JQL search

        :param jql_queries: List of JQL queries or single JQL query for which metadata is requested
        :return: Metadata for the JQL search
        """
        url = "rest/api/3/jql/parse"
        
        data = {}
        if jql_queries:
            if isinstance(jql_queries, list):
                data["queries"] = jql_queries
            else:
                data["queries"] = [jql_queries]
        
        return self.post(url, data=data)

    def get_field_reference_data(self):
        """
        Get reference data for fields used in JQL queries

        :return: Field reference data
        """
        url = "rest/api/3/jql/autocompletedata"
        return self.get(url)

    def get_field_auto_complete_suggestions(self, field_name, field_value=None):
        """
        Get autocompletion suggestions for field values

        :param field_name: Field name
        :param field_value: Partial field value for which suggestions are requested
        :return: Autocompletion suggestions
        """
        url = "rest/api/3/jql/autocompletedata/suggestions"
        params = {
            "fieldName": field_name
        }
        
        if field_value:
            params["fieldValue"] = field_value
        
        return self.get(url, params=params)

    def parse_jql_queries(self, queries, validation_level="strict"):
        """
        Parse JQL queries and validate them

        :param queries: List of JQL queries to parse
        :param validation_level: Validation level (strict, warn, none)
        :return: Parse results
        """
        url = "rest/api/3/jql/parse"
        
        data = {
            "queries": queries,
            "validation": validation_level
        }
        
        return self.post(url, data=data)

    def convert_user_identifiers(self, query, start_at=0, max_results=100, username=True, 
                               account_id=True, query_filter=None):
        """
        Find users based on various identifiers

        :param query: User identifier (username, key, name, or account ID)
        :param start_at: Index of the first user to return
        :param max_results: Maximum number of users to return
        :param username: Whether to include username in the response
        :param account_id: Whether to include account ID in the response
        :param query_filter: Query filter (all, actionable, my-actionable)
        :return: List of users matching the query
        """
        url = "rest/api/3/user/search/query"
        params = {
            "query": query,
            "startAt": start_at,
            "maxResults": max_results,
            "includeUsername": username,
            "includeAccountId": account_id
        }
        
        if query_filter:
            params["filter"] = query_filter
        
        return self.get(url, params=params)

    def find_users_with_permissions(self, permissions, project_key=None, issue_key=None, 
                                  start_at=0, max_results=50, query=None):
        """
        Find users with specified permissions

        :param permissions: List of permissions (e.g. ["BROWSE_PROJECTS", "EDIT_ISSUES"])
        :param project_key: Optional project key
        :param issue_key: Optional issue key
        :param start_at: Index of the first user to return
        :param max_results: Maximum number of users to return
        :param query: Optional query to filter users by name or email
        :return: List of users with the specified permissions
        """
        url = "rest/api/3/user/permission/search"
        params = {
            "startAt": start_at,
            "maxResults": max_results
        }
        
        data = {"permissions": permissions}
        
        if project_key:
            data["projectKey"] = project_key
        
        if issue_key:
            data["issueKey"] = issue_key
        
        if query:
            data["query"] = query
        
        return self.post(url, data=data, params=params)

    def find_assignable_users(self, query, project_key=None, issue_key=None, max_results=50, 
                             username=False, account_id=True, start_at=0):
        """
        Find users assignable to issues

        :param query: User name or email query
        :param project_key: Optional project key
        :param issue_key: Optional issue key
        :param max_results: Maximum number of users to return
        :param username: Whether to include username in the response
        :param account_id: Whether to include account ID in the response
        :param start_at: Index of the first user to return
        :return: List of assignable users
        """
        url = "rest/api/3/user/assignable/search"
        params = {
            "query": query,
            "maxResults": max_results,
            "includeUsername": username,
            "includeAccountId": account_id,
            "startAt": start_at
        }
        
        if project_key:
            params["project"] = project_key
        
        if issue_key:
            params["issueKey"] = issue_key
        
        return self.get(url, params=params)

    def find_users_for_picker(self, query, max_results=50, show_avatar=True, exclude_account_ids=None, 
                            exclude_project_roles=None, project_key=None, 
                            exclude_connected_accounts=None):
        """
        Find users for the user picker

        :param query: User name query or email query
        :param max_results: Maximum number of users to return
        :param show_avatar: Whether to include avatar details in the response
        :param exclude_account_ids: List of account IDs to exclude
        :param exclude_project_roles: List of project roles to exclude
        :param project_key: Optional project key
        :param exclude_connected_accounts: Whether to exclude connected accounts
        :return: List of users for the picker
        """
        url = "rest/api/3/user/picker"
        params = {
            "query": query,
            "maxResults": max_results,
            "showAvatar": show_avatar
        }
        
        if exclude_account_ids:
            if isinstance(exclude_account_ids, list):
                params["excludeAccountIds"] = ",".join(exclude_account_ids)
            else:
                params["excludeAccountIds"] = exclude_account_ids
        
        if exclude_project_roles:
            if isinstance(exclude_project_roles, list):
                params["excludeProjectRoles"] = ",".join(map(str, exclude_project_roles))
            else:
                params["excludeProjectRoles"] = exclude_project_roles
        
        if project_key:
            params["projectKey"] = project_key
        
        if exclude_connected_accounts is not None:
            params["excludeConnectUsers"] = exclude_connected_accounts
        
        return self.get(url, params=params)

    def find_users_by_query(self, query=None, account_id=None, property_key=None, 
                          property_value=None, start_at=0, max_results=50, exclude=None):
        """
        Find users by query

        :param query: Optional query to filter users
        :param account_id: Optional account ID
        :param property_key: Optional user property key
        :param property_value: Optional user property value
        :param start_at: Index of the first user to return
        :param max_results: Maximum number of users to return
        :param exclude: Optional comma-separated list of usernames to exclude
        :return: List of users matching the query
        """
        url = "rest/api/3/user/search"
        params = {
            "startAt": start_at,
            "maxResults": max_results
        }
        
        if query:
            params["query"] = query
        
        if account_id:
            params["accountId"] = account_id
        
        if property_key:
            params["propertyKey"] = property_key
        
        if property_value:
            params["propertyValue"] = property_value
        
        if exclude:
            if isinstance(exclude, list):
                params["exclude"] = ",".join(exclude)
            else:
                params["exclude"] = exclude
        
        return self.get(url, params=params)

    def validate_jql(self, jql_queries, validation_level="strict"):
        """
        Validate JQL queries

        :param jql_queries: List of JQL queries to validate
        :param validation_level: Validation level (strict, warn, none)
        :return: Validation results
        """
        url = "rest/api/3/jql/parse"
        
        data = {
            "queries": jql_queries,
            "validation": validation_level
        }
        
        return self.post(url, data=data)

    def get_visible_issue_types_for_project(self, project_id_or_key):
        """
        Get visible issue types for a project

        :param project_id_or_key: Project ID or key
        :return: List of visible issue types
        """
        url = f"rest/api/3/project/{project_id_or_key}/statuses"
        return self.get(url) 