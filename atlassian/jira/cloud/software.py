"""
Jira Software Cloud API implementation for Jira API v3
This module provides Jira Software specific functionality like boards, sprints, and backlogs
"""

import logging
from typing import Any, Dict, Generator, List, Optional, Union

from atlassian.jira.cloud.cloud import Jira as CloudJira

log = logging.getLogger(__name__)


class SoftwareJira(CloudJira):
    """
    Jira Software Cloud API implementation with software-specific features
    """

    def __init__(self, url: str, username: str = None, password: str = None, **kwargs):
        """
        Initialize a Jira Software Cloud instance.

        Args:
            url: Jira Cloud URL
            username: Username for authentication
            password: Password or API token for authentication
            kwargs: Additional arguments to pass to the CloudJira constructor
        """
        super(SoftwareJira, self).__init__(url, username, password, **kwargs)
        
    # Board operations
    
    def get_all_boards(
        self, 
        start_at: int = 0, 
        max_results: int = 50, 
        board_type: str = None, 
        name: str = None, 
        project_key_or_id: str = None
    ) -> Dict[str, Any]:
        """
        Get all boards visible to the user.
        
        Args:
            start_at: Index of the first board to return
            max_results: Maximum number of boards to return
            board_type: Filter by board type (scrum, kanban)
            name: Filter by board name
            project_key_or_id: Filter by project key or ID
            
        Returns:
            Dictionary containing boards information
        """
        params = {
            "startAt": start_at,
            "maxResults": max_results
        }
        
        if board_type:
            params["type"] = board_type
        if name:
            params["name"] = name
        if project_key_or_id:
            params["projectKeyOrId"] = project_key_or_id
            
        return self.get("rest/agile/1.0/board", params=params)
    
    def create_board(
        self, 
        name: str, 
        board_type: str, 
        filter_id: int
    ) -> Dict[str, Any]:
        """
        Create a new board.
        
        Args:
            name: Board name
            board_type: Board type (scrum, kanban)
            filter_id: ID of the filter to use for the board
            
        Returns:
            Dictionary containing created board information
        """
        data = {
            "name": name,
            "type": board_type,
            "filterId": filter_id
        }
        
        return self.post("rest/agile/1.0/board", data=data)
    
    def get_board(self, board_id: int) -> Dict[str, Any]:
        """
        Get a specific board.
        
        Args:
            board_id: Board ID
            
        Returns:
            Dictionary containing board information
        """
        board_id = self.validate_id_or_key(str(board_id), "board_id")
        return self.get(f"rest/agile/1.0/board/{board_id}")
    
    def delete_board(self, board_id: int) -> None:
        """
        Delete a board.
        
        Args:
            board_id: Board ID
        """
        board_id = self.validate_id_or_key(str(board_id), "board_id")
        return self.delete(f"rest/agile/1.0/board/{board_id}")
    
    def get_board_configuration(self, board_id: int) -> Dict[str, Any]:
        """
        Get a board's configuration.
        
        Args:
            board_id: Board ID
            
        Returns:
            Dictionary containing board configuration
        """
        board_id = self.validate_id_or_key(str(board_id), "board_id")
        return self.get(f"rest/agile/1.0/board/{board_id}/configuration")
    
    def get_board_issues(
        self, 
        board_id: int, 
        jql: str = None, 
        start_at: int = 0, 
        max_results: int = 50, 
        validate_query: bool = True,
        fields: List[str] = None,
        expand: str = None
    ) -> Dict[str, Any]:
        """
        Get issues from a board.
        
        Args:
            board_id: Board ID
            jql: JQL query to filter issues
            start_at: Index of the first issue to return
            max_results: Maximum number of issues to return
            validate_query: Whether to validate the JQL query
            fields: Fields to include in the response
            expand: Expand options to retrieve additional information
            
        Returns:
            Dictionary containing issues information
        """
        board_id = self.validate_id_or_key(str(board_id), "board_id")
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "validateQuery": str(validate_query).lower()
        }
        
        if jql:
            params["jql"] = jql
            
        if fields:
            params["fields"] = ",".join(fields) if isinstance(fields, list) else fields
            
        if expand:
            params["expand"] = expand
            
        return self.get(f"rest/agile/1.0/board/{board_id}/issue", params=params)
    
    # Sprint operations
    
    def get_all_sprints(
        self, 
        board_id: int, 
        start_at: int = 0, 
        max_results: int = 50, 
        state: str = None
    ) -> Dict[str, Any]:
        """
        Get all sprints for a board.
        
        Args:
            board_id: Board ID
            start_at: Index of the first sprint to return
            max_results: Maximum number of sprints to return
            state: Filter by sprint state (future, active, closed)
            
        Returns:
            Dictionary containing sprints information
        """
        board_id = self.validate_id_or_key(str(board_id), "board_id")
        params = {
            "startAt": start_at,
            "maxResults": max_results
        }
        
        if state:
            params["state"] = state
            
        return self.get(f"rest/agile/1.0/board/{board_id}/sprint", params=params)
    
    def create_sprint(
        self, 
        name: str, 
        board_id: int, 
        start_date: str = None, 
        end_date: str = None,
        goal: str = None
    ) -> Dict[str, Any]:
        """
        Create a new sprint.
        
        Args:
            name: Sprint name
            board_id: ID of the board the sprint belongs to
            start_date: Start date in format YYYY-MM-DD
            end_date: End date in format YYYY-MM-DD
            goal: Sprint goal
            
        Returns:
            Dictionary containing created sprint information
        """
        data = {
            "name": name,
            "originBoardId": board_id
        }
        
        if start_date:
            data["startDate"] = start_date
            
        if end_date:
            data["endDate"] = end_date
            
        if goal:
            data["goal"] = goal
            
        return self.post("rest/agile/1.0/sprint", data=data)
    
    def get_sprint(self, sprint_id: int) -> Dict[str, Any]:
        """
        Get a specific sprint.
        
        Args:
            sprint_id: Sprint ID
            
        Returns:
            Dictionary containing sprint information
        """
        sprint_id = self.validate_id_or_key(str(sprint_id), "sprint_id")
        return self.get(f"rest/agile/1.0/sprint/{sprint_id}")
    
    def update_sprint(
        self, 
        sprint_id: int, 
        name: str = None, 
        start_date: str = None, 
        end_date: str = None,
        state: str = None,
        goal: str = None
    ) -> Dict[str, Any]:
        """
        Update a sprint.
        
        Args:
            sprint_id: Sprint ID
            name: Sprint name
            start_date: Start date in format YYYY-MM-DD
            end_date: End date in format YYYY-MM-DD
            state: Sprint state (future, active, closed)
            goal: Sprint goal
            
        Returns:
            Dictionary containing updated sprint information
        """
        sprint_id = self.validate_id_or_key(str(sprint_id), "sprint_id")
        data = {}
        
        if name:
            data["name"] = name
            
        if start_date:
            data["startDate"] = start_date
            
        if end_date:
            data["endDate"] = end_date
            
        if state:
            data["state"] = state
            
        if goal:
            data["goal"] = goal
            
        return self.put(f"rest/agile/1.0/sprint/{sprint_id}", data=data)
    
    def delete_sprint(self, sprint_id: int) -> None:
        """
        Delete a sprint.
        
        Args:
            sprint_id: Sprint ID
        """
        sprint_id = self.validate_id_or_key(str(sprint_id), "sprint_id")
        return self.delete(f"rest/agile/1.0/sprint/{sprint_id}")
    
    def get_sprint_issues(
        self, 
        sprint_id: int, 
        start_at: int = 0, 
        max_results: int = 50, 
        jql: str = None,
        validate_query: bool = True,
        fields: List[str] = None,
        expand: str = None
    ) -> Dict[str, Any]:
        """
        Get issues for a sprint.
        
        Args:
            sprint_id: Sprint ID
            start_at: Index of the first issue to return
            max_results: Maximum number of issues to return
            jql: JQL query to filter issues
            validate_query: Whether to validate the JQL query
            fields: Fields to include in the response
            expand: Expand options to retrieve additional information
            
        Returns:
            Dictionary containing issues information
        """
        sprint_id = self.validate_id_or_key(str(sprint_id), "sprint_id")
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "validateQuery": str(validate_query).lower()
        }
        
        if jql:
            params["jql"] = jql
            
        if fields:
            params["fields"] = ",".join(fields) if isinstance(fields, list) else fields
            
        if expand:
            params["expand"] = expand
            
        return self.get(f"rest/agile/1.0/sprint/{sprint_id}/issue", params=params)
    
    def move_issues_to_sprint(self, sprint_id: int, issue_keys: List[str]) -> Dict[str, Any]:
        """
        Move issues to a sprint.
        
        Args:
            sprint_id: Sprint ID
            issue_keys: List of issue keys to move
            
        Returns:
            Dictionary containing response information
        """
        sprint_id = self.validate_id_or_key(str(sprint_id), "sprint_id")
        data = {"issues": issue_keys}
        return self.post(f"rest/agile/1.0/sprint/{sprint_id}/issue", data=data)
    
    # Backlog operations
    
    def get_backlog_issues(
        self, 
        board_id: int, 
        start_at: int = 0, 
        max_results: int = 50, 
        jql: str = None,
        validate_query: bool = True,
        fields: List[str] = None,
        expand: str = None
    ) -> Dict[str, Any]:
        """
        Get issues from the backlog.
        
        Args:
            board_id: Board ID
            start_at: Index of the first issue to return
            max_results: Maximum number of issues to return
            jql: JQL query to filter issues
            validate_query: Whether to validate the JQL query
            fields: Fields to include in the response
            expand: Expand options to retrieve additional information
            
        Returns:
            Dictionary containing issues information
        """
        board_id = self.validate_id_or_key(str(board_id), "board_id")
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "validateQuery": str(validate_query).lower()
        }
        
        if jql:
            params["jql"] = jql
            
        if fields:
            params["fields"] = ",".join(fields) if isinstance(fields, list) else fields
            
        if expand:
            params["expand"] = expand
            
        return self.get(f"rest/agile/1.0/board/{board_id}/backlog", params=params)
    
    def move_issues_to_backlog(self, issue_keys: List[str]) -> Dict[str, Any]:
        """
        Move issues to the backlog (remove from all sprints).
        
        Args:
            issue_keys: List of issue keys to move
            
        Returns:
            Dictionary containing response information
        """
        data = {"issues": issue_keys}
        return self.post("rest/agile/1.0/backlog/issue", data=data)
    
    # Epic operations
    
    def get_epics(
        self, 
        board_id: int, 
        start_at: int = 0, 
        max_results: int = 50, 
        done: bool = None
    ) -> Dict[str, Any]:
        """
        Get epics from a board.
        
        Args:
            board_id: Board ID
            start_at: Index of the first epic to return
            max_results: Maximum number of epics to return
            done: Filter by epic status (done or not done)
            
        Returns:
            Dictionary containing epics information
        """
        board_id = self.validate_id_or_key(str(board_id), "board_id")
        params = {
            "startAt": start_at,
            "maxResults": max_results
        }
        
        if done is not None:
            params["done"] = str(done).lower()
            
        return self.get(f"rest/agile/1.0/board/{board_id}/epic", params=params)
    
    def get_issues_without_epic(
        self, 
        board_id: int, 
        start_at: int = 0, 
        max_results: int = 50, 
        jql: str = None,
        validate_query: bool = True,
        fields: List[str] = None,
        expand: str = None
    ) -> Dict[str, Any]:
        """
        Get issues that do not belong to any epic.
        
        Args:
            board_id: Board ID
            start_at: Index of the first issue to return
            max_results: Maximum number of issues to return
            jql: JQL query to filter issues
            validate_query: Whether to validate the JQL query
            fields: Fields to include in the response
            expand: Expand options to retrieve additional information
            
        Returns:
            Dictionary containing issues information
        """
        board_id = self.validate_id_or_key(str(board_id), "board_id")
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "validateQuery": str(validate_query).lower()
        }
        
        if jql:
            params["jql"] = jql
            
        if fields:
            params["fields"] = ",".join(fields) if isinstance(fields, list) else fields
            
        if expand:
            params["expand"] = expand
            
        return self.get(f"rest/agile/1.0/board/{board_id}/epic/none/issue", params=params)
    
    def get_issues_for_epic(
        self, 
        board_id: int, 
        epic_id: str,
        start_at: int = 0, 
        max_results: int = 50, 
        jql: str = None,
        validate_query: bool = True,
        fields: List[str] = None,
        expand: str = None
    ) -> Dict[str, Any]:
        """
        Get issues that belong to an epic.
        
        Args:
            board_id: Board ID
            epic_id: Epic ID
            start_at: Index of the first issue to return
            max_results: Maximum number of issues to return
            jql: JQL query to filter issues
            validate_query: Whether to validate the JQL query
            fields: Fields to include in the response
            expand: Expand options to retrieve additional information
            
        Returns:
            Dictionary containing issues information
        """
        board_id = self.validate_id_or_key(str(board_id), "board_id")
        epic_id = self.validate_id_or_key(epic_id, "epic_id")
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "validateQuery": str(validate_query).lower()
        }
        
        if jql:
            params["jql"] = jql
            
        if fields:
            params["fields"] = ",".join(fields) if isinstance(fields, list) else fields
            
        if expand:
            params["expand"] = expand
            
        return self.get(f"rest/agile/1.0/board/{board_id}/epic/{epic_id}/issue", params=params)
    
    # Rank operations
    
    def rank_issues(self, issue_keys: List[str], rank_before: str = None, rank_after: str = None) -> Dict[str, Any]:
        """
        Rank issues (change their order).
        
        Args:
            issue_keys: List of issue keys to rank
            rank_before: Issue key to rank the issues before (higher rank)
            rank_after: Issue key to rank the issues after (lower rank)
            
        Returns:
            Dictionary containing response information
        """
        if not (rank_before or rank_after):
            raise ValueError("Either rank_before or rank_after must be specified")
            
        data = {"issues": issue_keys}
        
        if rank_before:
            data["rankBeforeIssue"] = rank_before
        else:
            data["rankAfterIssue"] = rank_after
            
        return self.put("rest/agile/1.0/issue/rank", data=data)
    
    # Advanced webhook management
    
    def register_webhook(
        self, 
        url: str, 
        events: List[str], 
        jql_filter: str = None, 
        exclude_body: bool = False
    ) -> Dict[str, Any]:
        """
        Register a webhook.
        
        Args:
            url: URL to receive webhook events
            events: List of events to subscribe to
            jql_filter: JQL query to filter issues
            exclude_body: Whether to exclude the issue body from the webhook
            
        Returns:
            Dictionary containing created webhook information
        """
        data = {
            "url": url,
            "events": events,
            "excludeBody": exclude_body
        }
        
        if jql_filter:
            data["jqlFilter"] = jql_filter
            
        return self.post("rest/webhooks/1.0/webhook", data=data)
    
    def get_webhook(self, webhook_id: int) -> Dict[str, Any]:
        """
        Get a specific webhook.
        
        Args:
            webhook_id: Webhook ID
            
        Returns:
            Dictionary containing webhook information
        """
        webhook_id = self.validate_id_or_key(str(webhook_id), "webhook_id")
        return self.get(f"rest/webhooks/1.0/webhook/{webhook_id}")
    
    def get_all_webhooks(self) -> List[Dict[str, Any]]:
        """
        Get all webhooks.
        
        Returns:
            List of dictionaries containing webhook information
        """
        return self.get("rest/webhooks/1.0/webhook")
    
    def delete_webhook(self, webhook_id: int) -> None:
        """
        Delete a webhook.
        
        Args:
            webhook_id: Webhook ID
        """
        webhook_id = self.validate_id_or_key(str(webhook_id), "webhook_id")
        return self.delete(f"rest/webhooks/1.0/webhook/{webhook_id}")
    
    # Jira Software Dashboard and Filter operations
    
    def get_dashboards(
        self, 
        start_at: int = 0, 
        max_results: int = 50, 
        filter: str = None
    ) -> Dict[str, Any]:
        """
        Get dashboards.
        
        Args:
            start_at: Index of the first dashboard to return
            max_results: Maximum number of dashboards to return
            filter: Text filter
            
        Returns:
            Dictionary containing dashboards information
        """
        params = {
            "startAt": start_at,
            "maxResults": max_results
        }
        
        if filter:
            params["filter"] = filter
            
        return self.get("rest/api/3/dashboard", params=params)
    
    def create_filter(
        self, 
        name: str, 
        jql: str, 
        description: str = None, 
        favorite: bool = False
    ) -> Dict[str, Any]:
        """
        Create a filter.
        
        Args:
            name: Filter name
            jql: JQL query
            description: Filter description
            favorite: Whether the filter should be favorited
            
        Returns:
            Dictionary containing created filter information
        """
        data = {
            "name": name,
            "jql": jql,
            "favourite": favorite
        }
        
        if description:
            data["description"] = description
            
        return self.post("rest/api/3/filter", data=data)
    
    def get_filter(self, filter_id: int) -> Dict[str, Any]:
        """
        Get a specific filter.
        
        Args:
            filter_id: Filter ID
            
        Returns:
            Dictionary containing filter information
        """
        filter_id = self.validate_id_or_key(str(filter_id), "filter_id")
        return self.get(f"rest/api/3/filter/{filter_id}")
    
    def get_favorite_filters(self) -> List[Dict[str, Any]]:
        """
        Get favorite filters.
        
        Returns:
            List of dictionaries containing filter information
        """
        return self.get("rest/api/3/filter/favourite")
    
    # Advanced JQL capabilities
    
    def get_field_reference_data(self) -> Dict[str, Any]:
        """
        Get reference data for JQL searches, including fields, functions, and operators.
        
        Returns:
            Dictionary containing JQL reference data
        """
        return self.get("rest/api/3/jql/autocompletedata")
    
    def parse_jql(self, jql: str, validate_query: bool = True) -> Dict[str, Any]:
        """
        Parse a JQL query.
        
        Args:
            jql: JQL query
            validate_query: Whether to validate the JQL query
            
        Returns:
            Dictionary containing parsed query information
        """
        data = {
            "queries": [
                {
                    "query": jql,
                    "validation": "strict" if validate_query else "none"
                }
            ]
        }
        
        return self.post("rest/api/3/jql/parse", data=data) 