# coding=utf-8
# Generated from the supplied Jira Cloud API descriptions; do not edit manually.


class JiraSoftwareMethods:
    """Concrete methods for every supplied software API operation."""

    def move_issues_to_backlog(self, data=None, **request_kwargs):
        """Move issues to backlog.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/agile/1.0/backlog/issue"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def move_issues_to_backlog_for_board(self, board_id, data=None, **request_kwargs):
        """Move issues to backlog for board.

        Args:
            board_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/backlog/{board_id}/issue"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_all_boards(
        self,
        start_at=None,
        max_results=None,
        type=None,
        name=None,
        project_key_or_id=None,
        account_id_location=None,
        project_location=None,
        include_private=None,
        negate_location_filtering=None,
        order_by=None,
        expand=None,
        project_type_location=None,
        filter_id=None,
        data=None,
        **request_kwargs,
    ):
        """Get all boards.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            type: API path or query parameter.
            name: API path or query parameter.
            project_key_or_id: API path or query parameter.
            account_id_location: API path or query parameter.
            project_location: API path or query parameter.
            include_private: API path or query parameter.
            negate_location_filtering: API path or query parameter.
            order_by: API path or query parameter.
            expand: API path or query parameter.
            project_type_location: API path or query parameter.
            filter_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/agile/1.0/board"
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "type": type,
            "name": name,
            "projectKeyOrId": project_key_or_id,
            "accountIdLocation": account_id_location,
            "projectLocation": project_location,
            "includePrivate": include_private,
            "negateLocationFiltering": negate_location_filtering,
            "orderBy": order_by,
            "expand": expand,
            "projectTypeLocation": project_type_location,
            "filterId": filter_id,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_board(self, data=None, **request_kwargs):
        """Create board.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/agile/1.0/board"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_board_by_filter_id(self, filter_id, start_at=None, max_results=None, data=None, **request_kwargs):
        """Get board by filter id.

        Args:
            filter_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/filter/{filter_id}"
        params = {"startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_board(self, board_id, data=None, **request_kwargs):
        """Delete board.

        Args:
            board_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_board(self, board_id, data=None, **request_kwargs):
        """Get board.

        Args:
            board_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_issues_for_backlog(
        self,
        board_id,
        start_at=None,
        max_results=None,
        jql=None,
        validate_query=None,
        fields=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get issues for backlog.

        Args:
            board_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            jql: API path or query parameter.
            validate_query: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/backlog"
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "jql": jql,
            "validateQuery": validate_query,
            "fields": fields,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_issues_for_backlog_jsis(
        self,
        board_id,
        next_page_token=None,
        max_results=None,
        reconcile_issues=None,
        jql=None,
        validate_query=None,
        fields=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get issues for backlog (enhanced).

        Args:
            board_id: API path or query parameter.
            next_page_token: API path or query parameter.
            max_results: API path or query parameter.
            reconcile_issues: API path or query parameter.
            jql: API path or query parameter.
            validate_query: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/software/1.0/board/{board_id}/backlog"
        params = {
            "nextPageToken": next_page_token,
            "maxResults": max_results,
            "reconcileIssues": reconcile_issues,
            "jql": jql,
            "validateQuery": validate_query,
            "fields": fields,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_approximate_issue_count_for_backlog(self, board_id, jql=None, data=None, **request_kwargs):
        """Get approximate issue count for backlog.

        Args:
            board_id: API path or query parameter.
            jql: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/software/1.0/board/{board_id}/backlog/approximate-count"
        params = {"jql": jql}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_configuration(self, board_id, data=None, **request_kwargs):
        """Get configuration.

        Args:
            board_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/configuration"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_epics(self, board_id, start_at=None, max_results=None, done=None, data=None, **request_kwargs):
        """Get epics.

        Args:
            board_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            done: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/epic"
        params = {"startAt": start_at, "maxResults": max_results, "done": done}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_issues_without_epic_for_board(
        self,
        board_id,
        start_at=None,
        max_results=None,
        jql=None,
        validate_query=None,
        fields=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get issues without epic for board.

        Args:
            board_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            jql: API path or query parameter.
            validate_query: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/epic/none/issue"
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "jql": jql,
            "validateQuery": validate_query,
            "fields": fields,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_issues_without_epic_for_board_jsis(
        self,
        board_id,
        next_page_token=None,
        max_results=None,
        reconcile_issues=None,
        jql=None,
        validate_query=None,
        fields=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get issues without epic for board (enhanced).

        Args:
            board_id: API path or query parameter.
            next_page_token: API path or query parameter.
            max_results: API path or query parameter.
            reconcile_issues: API path or query parameter.
            jql: API path or query parameter.
            validate_query: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/software/1.0/board/{board_id}/epic/none/issue"
        params = {
            "nextPageToken": next_page_token,
            "maxResults": max_results,
            "reconcileIssues": reconcile_issues,
            "jql": jql,
            "validateQuery": validate_query,
            "fields": fields,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_board_issues_for_epic(
        self,
        board_id,
        epic_id,
        start_at=None,
        max_results=None,
        jql=None,
        validate_query=None,
        fields=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get board issues for epic.

        Args:
            board_id: API path or query parameter.
            epic_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            jql: API path or query parameter.
            validate_query: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/epic/{epic_id}/issue"
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "jql": jql,
            "validateQuery": validate_query,
            "fields": fields,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_board_issues_for_epic_jsis(
        self,
        board_id,
        epic_id,
        next_page_token=None,
        max_results=None,
        reconcile_issues=None,
        jql=None,
        validate_query=None,
        fields=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get board issues for epic (enhanced).

        Args:
            board_id: API path or query parameter.
            epic_id: API path or query parameter.
            next_page_token: API path or query parameter.
            max_results: API path or query parameter.
            reconcile_issues: API path or query parameter.
            jql: API path or query parameter.
            validate_query: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/software/1.0/board/{board_id}/epic/{epic_id}/issue"
        params = {
            "nextPageToken": next_page_token,
            "maxResults": max_results,
            "reconcileIssues": reconcile_issues,
            "jql": jql,
            "validateQuery": validate_query,
            "fields": fields,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_features_for_board(self, board_id, data=None, **request_kwargs):
        """Get features for board.

        Args:
            board_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/features"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def toggle_features(self, board_id, data=None, **request_kwargs):
        """Toggle features.

        Args:
            board_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/features"
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_issues_for_board(
        self,
        board_id,
        start_at=None,
        max_results=None,
        jql=None,
        validate_query=None,
        fields=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get issues for board.

        Args:
            board_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            jql: API path or query parameter.
            validate_query: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/issue"
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "jql": jql,
            "validateQuery": validate_query,
            "fields": fields,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def move_issues_to_board(self, board_id, data=None, **request_kwargs):
        """Move issues to board.

        Args:
            board_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/issue"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_issues_for_board_jsis(
        self,
        board_id,
        next_page_token=None,
        max_results=None,
        reconcile_issues=None,
        jql=None,
        validate_query=None,
        fields=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get issues for board (enhanced).

        Args:
            board_id: API path or query parameter.
            next_page_token: API path or query parameter.
            max_results: API path or query parameter.
            reconcile_issues: API path or query parameter.
            jql: API path or query parameter.
            validate_query: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/software/1.0/board/{board_id}/issue"
        params = {
            "nextPageToken": next_page_token,
            "maxResults": max_results,
            "reconcileIssues": reconcile_issues,
            "jql": jql,
            "validateQuery": validate_query,
            "fields": fields,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_approximate_issue_count_for_board(self, board_id, jql=None, data=None, **request_kwargs):
        """Get approximate issue count for board.

        Args:
            board_id: API path or query parameter.
            jql: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/software/1.0/board/{board_id}/issue/approximate-count"
        params = {"jql": jql}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_projects(self, board_id, start_at=None, max_results=None, data=None, **request_kwargs):
        """Get projects.

        Args:
            board_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/project"
        params = {"startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_projects_full(self, board_id, data=None, **request_kwargs):
        """Get projects full.

        Args:
            board_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/project/full"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_board_property_keys(self, board_id, data=None, **request_kwargs):
        """Get board property keys.

        Args:
            board_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/properties"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_board_property(self, board_id, property_key, data=None, **request_kwargs):
        """Delete board property.

        Args:
            board_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/properties/{property_key}"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_board_property(self, board_id, property_key, data=None, **request_kwargs):
        """Get board property.

        Args:
            board_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/properties/{property_key}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_board_property(self, board_id, property_key, data=None, **request_kwargs):
        """Set board property.

        Args:
            board_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/properties/{property_key}"
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_all_quick_filters(self, board_id, start_at=None, max_results=None, data=None, **request_kwargs):
        """Get all quick filters.

        Args:
            board_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/quickfilter"
        params = {"startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_quick_filter(self, board_id, quick_filter_id, data=None, **request_kwargs):
        """Get quick filter.

        Args:
            board_id: API path or query parameter.
            quick_filter_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/quickfilter/{quick_filter_id}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_reports_for_board(self, board_id, data=None, **request_kwargs):
        """Get reports for board.

        Args:
            board_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/reports"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_all_sprints(self, board_id, start_at=None, max_results=None, state=None, data=None, **request_kwargs):
        """Get all sprints.

        Args:
            board_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            state: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/sprint"
        params = {"startAt": start_at, "maxResults": max_results, "state": state}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_board_issues_for_sprint(
        self,
        board_id,
        sprint_id,
        start_at=None,
        max_results=None,
        jql=None,
        validate_query=None,
        fields=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get board issues for sprint.

        Args:
            board_id: API path or query parameter.
            sprint_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            jql: API path or query parameter.
            validate_query: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/sprint/{sprint_id}/issue"
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "jql": jql,
            "validateQuery": validate_query,
            "fields": fields,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_board_issues_for_sprint_jsis(
        self,
        board_id,
        sprint_id,
        next_page_token=None,
        max_results=None,
        reconcile_issues=None,
        jql=None,
        validate_query=None,
        fields=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get board issues for sprint (enhanced).

        Args:
            board_id: API path or query parameter.
            sprint_id: API path or query parameter.
            next_page_token: API path or query parameter.
            max_results: API path or query parameter.
            reconcile_issues: API path or query parameter.
            jql: API path or query parameter.
            validate_query: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/software/1.0/board/{board_id}/sprint/{sprint_id}/issue"
        params = {
            "nextPageToken": next_page_token,
            "maxResults": max_results,
            "reconcileIssues": reconcile_issues,
            "jql": jql,
            "validateQuery": validate_query,
            "fields": fields,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_all_versions(self, board_id, start_at=None, max_results=None, released=None, data=None, **request_kwargs):
        """Get all versions.

        Args:
            board_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            released: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/board/{board_id}/version"
        params = {"startAt": start_at, "maxResults": max_results, "released": released}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_issues_without_epic(
        self,
        start_at=None,
        max_results=None,
        jql=None,
        validate_query=None,
        fields=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get issues without epic.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            jql: API path or query parameter.
            validate_query: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/agile/1.0/epic/none/issue"
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "jql": jql,
            "validateQuery": validate_query,
            "fields": fields,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def remove_issues_from_epic(self, data=None, **request_kwargs):
        """Remove issues from epic.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/agile/1.0/epic/none/issue"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_issues_without_epic_jsis(
        self,
        next_page_token=None,
        max_results=None,
        reconcile_issues=None,
        jql=None,
        validate_query=None,
        fields=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get issues without epic (enhanced).

        Args:
            next_page_token: API path or query parameter.
            max_results: API path or query parameter.
            reconcile_issues: API path or query parameter.
            jql: API path or query parameter.
            validate_query: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/software/1.0/epic/none/issue"
        params = {
            "nextPageToken": next_page_token,
            "maxResults": max_results,
            "reconcileIssues": reconcile_issues,
            "jql": jql,
            "validateQuery": validate_query,
            "fields": fields,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_epic(self, epic_id_or_key, data=None, **request_kwargs):
        """Get epic.

        Args:
            epic_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/epic/{epic_id_or_key}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def partially_update_epic(self, epic_id_or_key, data=None, **request_kwargs):
        """Partially update epic.

        Args:
            epic_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/epic/{epic_id_or_key}"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_issues_for_epic(
        self,
        epic_id_or_key,
        start_at=None,
        max_results=None,
        jql=None,
        validate_query=None,
        fields=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get issues for epic.

        Args:
            epic_id_or_key: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            jql: API path or query parameter.
            validate_query: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/epic/{epic_id_or_key}/issue"
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "jql": jql,
            "validateQuery": validate_query,
            "fields": fields,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def move_issues_to_epic(self, epic_id_or_key, data=None, **request_kwargs):
        """Move issues to epic.

        Args:
            epic_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/epic/{epic_id_or_key}/issue"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_issues_for_epic_jsis(
        self,
        epic_id_or_key,
        next_page_token=None,
        max_results=None,
        reconcile_issues=None,
        jql=None,
        validate_query=None,
        fields=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get issues for epic (enhanced).

        Args:
            epic_id_or_key: API path or query parameter.
            next_page_token: API path or query parameter.
            max_results: API path or query parameter.
            reconcile_issues: API path or query parameter.
            jql: API path or query parameter.
            validate_query: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/software/1.0/epic/{epic_id_or_key}/issue"
        params = {
            "nextPageToken": next_page_token,
            "maxResults": max_results,
            "reconcileIssues": reconcile_issues,
            "jql": jql,
            "validateQuery": validate_query,
            "fields": fields,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def rank_epics(self, epic_id_or_key, data=None, **request_kwargs):
        """Rank epics.

        Args:
            epic_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/epic/{epic_id_or_key}/rank"
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def rank_issues(self, data=None, **request_kwargs):
        """Rank issues.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/agile/1.0/issue/rank"
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_issue(self, issue_id_or_key, fields=None, expand=None, update_history=None, data=None, **request_kwargs):
        """Get issue.

        Args:
            issue_id_or_key: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            update_history: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/issue/{issue_id_or_key}"
        params = {"fields": fields, "expand": expand, "updateHistory": update_history}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_issue_estimation_for_board(self, issue_id_or_key, board_id=None, data=None, **request_kwargs):
        """Get issue estimation for board.

        Args:
            issue_id_or_key: API path or query parameter.
            board_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/issue/{issue_id_or_key}/estimation"
        params = {"boardId": board_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def estimate_issue_for_board(self, issue_id_or_key, board_id=None, data=None, **request_kwargs):
        """Estimate issue for board.

        Args:
            issue_id_or_key: API path or query parameter.
            board_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/issue/{issue_id_or_key}/estimation"
        params = {"boardId": board_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(url, params=params, data=data, **request_kwargs)

    def create_sprint(self, data=None, **request_kwargs):
        """Create sprint.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/agile/1.0/sprint"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_sprint(self, sprint_id, data=None, **request_kwargs):
        """Delete sprint.

        Args:
            sprint_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/sprint/{sprint_id}"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_sprint(self, sprint_id, data=None, **request_kwargs):
        """Get sprint.

        Args:
            sprint_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/sprint/{sprint_id}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def partially_update_sprint(self, sprint_id, data=None, **request_kwargs):
        """Partially update sprint.

        Args:
            sprint_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/sprint/{sprint_id}"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def update_sprint(self, sprint_id, data=None, **request_kwargs):
        """Update sprint.

        Args:
            sprint_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/sprint/{sprint_id}"
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_issues_for_sprint(
        self,
        sprint_id,
        start_at=None,
        max_results=None,
        jql=None,
        validate_query=None,
        fields=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get issues for sprint.

        Args:
            sprint_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            jql: API path or query parameter.
            validate_query: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/sprint/{sprint_id}/issue"
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "jql": jql,
            "validateQuery": validate_query,
            "fields": fields,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def move_issues_to_sprint_and_rank(self, sprint_id, data=None, **request_kwargs):
        """Move issues to sprint and rank.

        Args:
            sprint_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/sprint/{sprint_id}/issue"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_issues_for_sprint_jsis(
        self,
        sprint_id,
        next_page_token=None,
        max_results=None,
        reconcile_issues=None,
        jql=None,
        validate_query=None,
        fields=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get issues for sprint (enhanced).

        Args:
            sprint_id: API path or query parameter.
            next_page_token: API path or query parameter.
            max_results: API path or query parameter.
            reconcile_issues: API path or query parameter.
            jql: API path or query parameter.
            validate_query: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/software/1.0/sprint/{sprint_id}/issue"
        params = {
            "nextPageToken": next_page_token,
            "maxResults": max_results,
            "reconcileIssues": reconcile_issues,
            "jql": jql,
            "validateQuery": validate_query,
            "fields": fields,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_properties_keys(self, sprint_id, data=None, **request_kwargs):
        """Get properties keys.

        Args:
            sprint_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/sprint/{sprint_id}/properties"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_property(self, sprint_id, property_key, data=None, **request_kwargs):
        """Delete property.

        Args:
            sprint_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/sprint/{sprint_id}/properties/{property_key}"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_property(self, sprint_id, property_key, data=None, **request_kwargs):
        """Get property.

        Args:
            sprint_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/sprint/{sprint_id}/properties/{property_key}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_property(self, sprint_id, property_key, data=None, **request_kwargs):
        """Set property.

        Args:
            sprint_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/sprint/{sprint_id}/properties/{property_key}"
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def swap_sprint(self, sprint_id, data=None, **request_kwargs):
        """Swap sprint.

        Args:
            sprint_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/agile/1.0/sprint/{sprint_id}/swap"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def store_development_information(self, data=None, **request_kwargs):
        """Store development information.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/devinfo/0.10/bulk"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_repository(self, repository_id, data=None, **request_kwargs):
        """Get repository.

        Args:
            repository_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/devinfo/0.10/repository/{repository_id}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_repository(self, repository_id, update_sequence_id=None, data=None, **request_kwargs):
        """Delete repository.

        Args:
            repository_id: API path or query parameter.
            update_sequence_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/devinfo/0.10/repository/{repository_id}"
        params = {"_updateSequenceId": update_sequence_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def delete_by_properties(self, update_sequence_id=None, data=None, **request_kwargs):
        """Delete development information by properties.

        Args:
            update_sequence_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/devinfo/0.10/bulkByProperties"
        params = {"_updateSequenceId": update_sequence_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def exists_by_properties(self, update_sequence_id=None, data=None, **request_kwargs):
        """Check if data exists for the supplied properties.

        Args:
            update_sequence_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/devinfo/0.10/existsByProperties"
        params = {"_updateSequenceId": update_sequence_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_entity(
        self, repository_id, entity_type, entity_id, update_sequence_id=None, data=None, **request_kwargs
    ):
        """Delete development information entity.

        Args:
            repository_id: API path or query parameter.
            entity_type: API path or query parameter.
            entity_id: API path or query parameter.
            update_sequence_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/devinfo/0.10/repository/{repository_id}/{entity_type}/{entity_id}"
        params = {"_updateSequenceId": update_sequence_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def submit_feature_flags(self, data=None, **request_kwargs):
        """Submit Feature Flag data.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/featureflags/0.1/bulk"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_feature_flags_by_property(self, update_sequence_id=None, data=None, **request_kwargs):
        """Delete Feature Flags by Property.

        Args:
            update_sequence_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/featureflags/0.1/bulkByProperties"
        params = {"_updateSequenceId": update_sequence_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_feature_flag_by_id(self, feature_flag_id, data=None, **request_kwargs):
        """Get a Feature Flag by ID.

        Args:
            feature_flag_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/featureflags/0.1/flag/{feature_flag_id}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_feature_flag_by_id(self, feature_flag_id, update_sequence_id=None, data=None, **request_kwargs):
        """Delete a Feature Flag by ID.

        Args:
            feature_flag_id: API path or query parameter.
            update_sequence_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/featureflags/0.1/flag/{feature_flag_id}"
        params = {"_updateSequenceId": update_sequence_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def submit_deployments(self, data=None, **request_kwargs):
        """Submit deployment data.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/deployments/0.1/bulk"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_deployments_by_property(self, update_sequence_number=None, data=None, **request_kwargs):
        """Delete deployments by Property.

        Args:
            update_sequence_number: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/deployments/0.1/bulkByProperties"
        params = {"_updateSequenceNumber": update_sequence_number}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_deployment_by_key(
        self, pipeline_id, environment_id, deployment_sequence_number, data=None, **request_kwargs
    ):
        """Get a deployment by key.

        Args:
            pipeline_id: API path or query parameter.
            environment_id: API path or query parameter.
            deployment_sequence_number: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/deployments/0.1/pipelines/{pipeline_id}/environments/{environment_id}/deployments/{deployment_sequence_number}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_deployment_by_key(
        self,
        pipeline_id,
        environment_id,
        deployment_sequence_number,
        update_sequence_number=None,
        data=None,
        **request_kwargs,
    ):
        """Delete a deployment by key.

        Args:
            pipeline_id: API path or query parameter.
            environment_id: API path or query parameter.
            deployment_sequence_number: API path or query parameter.
            update_sequence_number: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/deployments/0.1/pipelines/{pipeline_id}/environments/{environment_id}/deployments/{deployment_sequence_number}"
        params = {"_updateSequenceNumber": update_sequence_number}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_deployment_gating_status_by_key(
        self, pipeline_id, environment_id, deployment_sequence_number, data=None, **request_kwargs
    ):
        """Get deployment gating status by key.

        Args:
            pipeline_id: API path or query parameter.
            environment_id: API path or query parameter.
            deployment_sequence_number: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/deployments/0.1/pipelines/{pipeline_id}/environments/{environment_id}/deployments/{deployment_sequence_number}/gating-status"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def submit_builds(self, data=None, **request_kwargs):
        """Submit build data.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/builds/0.1/bulk"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_builds_by_property(self, update_sequence_number=None, data=None, **request_kwargs):
        """Delete builds by Property.

        Args:
            update_sequence_number: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/builds/0.1/bulkByProperties"
        params = {"_updateSequenceNumber": update_sequence_number}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_build_by_key(self, pipeline_id, build_number, data=None, **request_kwargs):
        """Get a build by key.

        Args:
            pipeline_id: API path or query parameter.
            build_number: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/builds/0.1/pipelines/{pipeline_id}/builds/{build_number}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_build_by_key(self, pipeline_id, build_number, update_sequence_number=None, data=None, **request_kwargs):
        """Delete a build by key.

        Args:
            pipeline_id: API path or query parameter.
            build_number: API path or query parameter.
            update_sequence_number: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/builds/0.1/pipelines/{pipeline_id}/builds/{build_number}"
        params = {"_updateSequenceNumber": update_sequence_number}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def submit_remote_links(self, data=None, **request_kwargs):
        """Submit Remote Link data.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/remotelinks/1.0/bulk"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_remote_links_by_property(self, update_sequence_number=None, params=None, data=None, **request_kwargs):
        """Delete Remote Links by Property.

        Args:
            update_sequence_number: API path or query parameter.
            params: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/remotelinks/1.0/bulkByProperties"
        params = {"_updateSequenceNumber": update_sequence_number, "params": params}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_remote_link_by_id(self, remote_link_id, data=None, **request_kwargs):
        """Get a Remote Link by ID.

        Args:
            remote_link_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/remotelinks/1.0/remotelink/{remote_link_id}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_remote_link_by_id(self, remote_link_id, update_sequence_number=None, data=None, **request_kwargs):
        """Delete a Remote Link by ID.

        Args:
            remote_link_id: API path or query parameter.
            update_sequence_number: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/remotelinks/1.0/remotelink/{remote_link_id}"
        params = {"_updateSequenceNumber": update_sequence_number}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def submit_workspaces(self, data=None, **request_kwargs):
        """Submit Security Workspaces to link.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/security/1.0/linkedWorkspaces/bulk"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_linked_workspaces(self, data=None, **request_kwargs):
        """Delete linked Security Workspaces.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/security/1.0/linkedWorkspaces/bulk"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_linked_workspaces(self, data=None, **request_kwargs):
        """Get linked Security Workspaces.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/security/1.0/linkedWorkspaces"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_linked_workspace_by_id(self, workspace_id, data=None, **request_kwargs):
        """Get a linked Security Workspace by ID.

        Args:
            workspace_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/security/1.0/linkedWorkspaces/{workspace_id}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def submit_vulnerabilities(self, data=None, **request_kwargs):
        """Submit Vulnerability data.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/security/1.0/bulk"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_vulnerabilities_by_property(self, data=None, **request_kwargs):
        """Delete Vulnerabilities by Property.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/security/1.0/bulkByProperties"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_vulnerability_by_id(self, vulnerability_id, data=None, **request_kwargs):
        """Get a Vulnerability by ID.

        Args:
            vulnerability_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/security/1.0/vulnerability/{vulnerability_id}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_vulnerability_by_id(self, vulnerability_id, data=None, **request_kwargs):
        """Delete a Vulnerability by ID.

        Args:
            vulnerability_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/security/1.0/vulnerability/{vulnerability_id}"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def submit_operations_workspaces(self, data=None, **request_kwargs):
        """Submit Operations Workspace Ids.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/operations/1.0/linkedWorkspaces/bulk"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_workspaces(self, data=None, **request_kwargs):
        """Delete Operations Workpaces by Id.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/operations/1.0/linkedWorkspaces/bulk"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_workspaces(self, data=None, **request_kwargs):
        """Get all Operations Workspace IDs or a specific Operations Workspace by ID.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/operations/1.0/linkedWorkspaces"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def submit_entity(self, data=None, **request_kwargs):
        """Submit Incident or Review data.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/operations/1.0/bulk"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_entity_by_property(self, data=None, **request_kwargs):
        """Delete Incidents or Review by Property.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/operations/1.0/bulkByProperties"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_incident_by_id(self, incident_id, data=None, **request_kwargs):
        """Get a Incident by ID.

        Args:
            incident_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/operations/1.0/incidents/{incident_id}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_incident_by_id(self, incident_id, data=None, **request_kwargs):
        """Delete a Incident by ID.

        Args:
            incident_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/operations/1.0/incidents/{incident_id}"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_review_by_id(self, review_id, data=None, **request_kwargs):
        """Get a Review by ID.

        Args:
            review_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/operations/1.0/post-incident-reviews/{review_id}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_review_by_id(self, review_id, data=None, **request_kwargs):
        """Delete a Review by ID.

        Args:
            review_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/operations/1.0/post-incident-reviews/{review_id}"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def submit_components(self, data=None, **request_kwargs):
        """Submit DevOps Components.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/devopscomponents/1.0/bulk"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_components_by_property(self, data=None, **request_kwargs):
        """Delete DevOps Components by Property.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/devopscomponents/1.0/bulkByProperties"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_component_by_id(self, component_id, data=None, **request_kwargs):
        """Get a Component by ID.

        Args:
            component_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/devopscomponents/1.0/devopscomponents/{component_id}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_component_by_id(self, component_id, data=None, **request_kwargs):
        """Delete a Component by ID.

        Args:
            component_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/devopscomponents/1.0/devopscomponents/{component_id}"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)
