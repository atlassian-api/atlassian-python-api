"""
Jira Software Cloud API Adapter for backward compatibility
This module provides adapters to maintain backward compatibility with existing code
"""

import logging
import warnings
from typing import Any, Dict, List, Optional, Union

from atlassian.jira.cloud.software import SoftwareJira

log = logging.getLogger(__name__)


class SoftwareJiraAdapter(SoftwareJira):
    """
    Adapter class for Jira Software Cloud API to maintain backward compatibility with the original Jira client.
    This class wraps the new SoftwareJira implementation and provides methods with the same names and signatures
    as in the original client.
    """

    def __init__(self, url: str, username: str = None, password: str = None, **kwargs):
        """
        Initialize a Jira Software Cloud Adapter instance.

        Args:
            url: Jira Cloud URL
            username: Username for authentication
            password: Password or API token for authentication
            kwargs: Additional arguments to pass to the SoftwareJira constructor
        """
        super(SoftwareJiraAdapter, self).__init__(url, username, password, **kwargs)
        
        # Dictionary mapping legacy method names to new method names
        self._legacy_method_map = {
            "boards": "get_all_boards",
            "get_board": "get_board",
            "create_board": "create_board",
            "delete_board": "delete_board",
            "get_board_configuration": "get_board_configuration",
            "get_issues_from_board": "get_board_issues",
            
            "sprints": "get_all_sprints",
            "get_sprint": "get_sprint",
            "create_sprint": "create_sprint",
            "update_sprint": "update_sprint",
            "delete_sprint": "delete_sprint",
            "get_sprint_issues": "get_sprint_issues",
            "add_issues_to_sprint": "move_issues_to_sprint",
            
            "get_backlog_issues": "get_backlog_issues",
            "move_to_backlog": "move_issues_to_backlog",
            
            "epics": "get_epics",
            "get_issues_without_epic": "get_issues_without_epic",
            "get_issues_for_epic": "get_issues_for_epic",
            
            "rank": "rank_issues",
            
            "create_webhook": "register_webhook",
            "webhook": "get_webhook",
            "webhooks": "get_all_webhooks",
            "delete_webhook": "delete_webhook",
            
            "dashboards": "get_dashboards",
            "create_filter": "create_filter",
            "get_filter": "get_filter",
            "favourite_filters": "get_favorite_filters",
        }
    
    # Board operations - legacy methods
    
    def boards(
        self, 
        startAt: int = 0, 
        maxResults: int = 50, 
        type: str = None, 
        name: str = None, 
        projectKeyOrId: str = None
    ) -> Dict[str, Any]:
        """
        Get all boards visible to the user. (Legacy method)
        
        Args:
            startAt: Index of the first board to return
            maxResults: Maximum number of boards to return
            type: Filter by board type (scrum, kanban)
            name: Filter by board name
            projectKeyOrId: Filter by project key or ID
            
        Returns:
            Dictionary containing boards information
        """
        warnings.warn(
            "The 'boards' method is deprecated. Use 'get_all_boards' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.get_all_boards(
            start_at=startAt,
            max_results=maxResults,
            board_type=type,
            name=name,
            project_key_or_id=projectKeyOrId
        )
    
    # Add methods for backward compatibility for each legacy method name
    def get_issues_from_board(
        self, 
        board_id: int, 
        jql_str: str = None, 
        startAt: int = 0, 
        maxResults: int = 50,
        validate_query: bool = True,
        fields: List[str] = None,
        expand: str = None
    ) -> Dict[str, Any]:
        """
        Get issues from a board. (Legacy method)
        
        Args:
            board_id: Board ID
            jql_str: JQL query to filter issues
            startAt: Index of the first issue to return
            maxResults: Maximum number of issues to return
            validate_query: Whether to validate the JQL query
            fields: Fields to include in the response
            expand: Expand options to retrieve additional information
            
        Returns:
            Dictionary containing issues information
        """
        warnings.warn(
            "The 'get_issues_from_board' method is deprecated. Use 'get_board_issues' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.get_board_issues(
            board_id=board_id,
            jql=jql_str,
            start_at=startAt,
            max_results=maxResults,
            validate_query=validate_query,
            fields=fields,
            expand=expand
        )
    
    # Sprint legacy methods
    
    def sprints(
        self, 
        board_id: int, 
        startAt: int = 0, 
        maxResults: int = 50, 
        state: str = None
    ) -> Dict[str, Any]:
        """
        Get all sprints for a board. (Legacy method)
        
        Args:
            board_id: Board ID
            startAt: Index of the first sprint to return
            maxResults: Maximum number of sprints to return
            state: Filter by sprint state (future, active, closed)
            
        Returns:
            Dictionary containing sprints information
        """
        warnings.warn(
            "The 'sprints' method is deprecated. Use 'get_all_sprints' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.get_all_sprints(
            board_id=board_id,
            start_at=startAt,
            max_results=maxResults,
            state=state
        )
    
    def add_issues_to_sprint(self, sprint_id: int, issues: List[str]) -> Dict[str, Any]:
        """
        Move issues to a sprint. (Legacy method)
        
        Args:
            sprint_id: Sprint ID
            issues: List of issue keys to move
            
        Returns:
            Dictionary containing response information
        """
        warnings.warn(
            "The 'add_issues_to_sprint' method is deprecated. Use 'move_issues_to_sprint' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.move_issues_to_sprint(sprint_id=sprint_id, issue_keys=issues)
    
    # Backlog legacy methods
    
    def move_to_backlog(self, issues: List[str]) -> Dict[str, Any]:
        """
        Move issues to the backlog. (Legacy method)
        
        Args:
            issues: List of issue keys to move
            
        Returns:
            Dictionary containing response information
        """
        warnings.warn(
            "The 'move_to_backlog' method is deprecated. Use 'move_issues_to_backlog' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.move_issues_to_backlog(issue_keys=issues)
    
    # Epic legacy methods
    
    def epics(
        self, 
        board_id: int, 
        startAt: int = 0, 
        maxResults: int = 50, 
        done: bool = None
    ) -> Dict[str, Any]:
        """
        Get epics from a board. (Legacy method)
        
        Args:
            board_id: Board ID
            startAt: Index of the first epic to return
            maxResults: Maximum number of epics to return
            done: Filter by epic status (done or not done)
            
        Returns:
            Dictionary containing epics information
        """
        warnings.warn(
            "The 'epics' method is deprecated. Use 'get_epics' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.get_epics(
            board_id=board_id,
            start_at=startAt,
            max_results=maxResults,
            done=done
        )
    
    # Rank legacy methods
    
    def rank(self, issues: List[str], rank_before: str = None, rank_after: str = None) -> Dict[str, Any]:
        """
        Rank issues. (Legacy method)
        
        Args:
            issues: List of issue keys to rank
            rank_before: Issue key to rank the issues before (higher rank)
            rank_after: Issue key to rank the issues after (lower rank)
            
        Returns:
            Dictionary containing response information
        """
        warnings.warn(
            "The 'rank' method is deprecated. Use 'rank_issues' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.rank_issues(
            issue_keys=issues,
            rank_before=rank_before,
            rank_after=rank_after
        )
    
    # Webhook legacy methods
    
    def create_webhook(
        self, 
        url: str, 
        events: List[str], 
        jql_filter: str = None, 
        exclude_body: bool = False
    ) -> Dict[str, Any]:
        """
        Register a webhook. (Legacy method)
        
        Args:
            url: URL to receive webhook events
            events: List of events to subscribe to
            jql_filter: JQL query to filter issues
            exclude_body: Whether to exclude the issue body from the webhook
            
        Returns:
            Dictionary containing created webhook information
        """
        warnings.warn(
            "The 'create_webhook' method is deprecated. Use 'register_webhook' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.register_webhook(
            url=url,
            events=events,
            jql_filter=jql_filter,
            exclude_body=exclude_body
        )
    
    def webhook(self, webhook_id: int) -> Dict[str, Any]:
        """
        Get a specific webhook. (Legacy method)
        
        Args:
            webhook_id: Webhook ID
            
        Returns:
            Dictionary containing webhook information
        """
        warnings.warn(
            "The 'webhook' method is deprecated. Use 'get_webhook' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.get_webhook(webhook_id=webhook_id)
    
    def webhooks(self) -> List[Dict[str, Any]]:
        """
        Get all webhooks. (Legacy method)
        
        Returns:
            List of dictionaries containing webhook information
        """
        warnings.warn(
            "The 'webhooks' method is deprecated. Use 'get_all_webhooks' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.get_all_webhooks()
    
    # Dashboard and Filter legacy methods
    
    def dashboards(
        self, 
        startAt: int = 0, 
        maxResults: int = 50, 
        filter: str = None
    ) -> Dict[str, Any]:
        """
        Get dashboards. (Legacy method)
        
        Args:
            startAt: Index of the first dashboard to return
            maxResults: Maximum number of dashboards to return
            filter: Text filter
            
        Returns:
            Dictionary containing dashboards information
        """
        warnings.warn(
            "The 'dashboards' method is deprecated. Use 'get_dashboards' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.get_dashboards(
            start_at=startAt,
            max_results=maxResults,
            filter=filter
        )
    
    def favourite_filters(self) -> List[Dict[str, Any]]:
        """
        Get favorite filters. (Legacy method)
        
        Returns:
            List of dictionaries containing filter information
        """
        warnings.warn(
            "The 'favourite_filters' method is deprecated. Use 'get_favorite_filters' instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        return self.get_favorite_filters() 