# coding=utf-8
# Generated from the supplied Jira Cloud API descriptions; do not edit manually.


class JiraCloudCoreMethods:
    """Concrete methods for every supplied core API operation."""

    def get_banner(self, data=None, **request_kwargs):
        """Get announcement banner configuration.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("announcementBanner", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_banner(self, data=None, **request_kwargs):
        """Update announcement banner configuration.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("announcementBanner", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_custom_fields_configurations(
        self,
        id=None,
        field_context_id=None,
        issue_id=None,
        project_key_or_id=None,
        issue_type_id=None,
        start_at=None,
        max_results=None,
        data=None,
        **request_kwargs,
    ):
        """Bulk get custom field configurations.

        Args:
            id: API path or query parameter.
            field_context_id: API path or query parameter.
            issue_id: API path or query parameter.
            project_key_or_id: API path or query parameter.
            issue_type_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            "app/field/context/configuration/list", api_root="rest/api", api_version=self.api_version
        )
        params = {
            "id": id,
            "fieldContextId": field_context_id,
            "issueId": issue_id,
            "projectKeyOrId": project_key_or_id,
            "issueTypeId": issue_type_id,
            "startAt": start_at,
            "maxResults": max_results,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def update_multiple_custom_field_values(
        self, generate_changelog=None, generate_app_events=None, data=None, **request_kwargs
    ):
        """Update custom fields.

        Args:
            generate_changelog: API path or query parameter.
            generate_app_events: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("app/field/value", api_root="rest/api", api_version=self.api_version)
        params = {"generateChangelog": generate_changelog, "generateAppEvents": generate_app_events}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_custom_field_configuration(
        self,
        field_id_or_key,
        id=None,
        field_context_id=None,
        issue_id=None,
        project_key_or_id=None,
        issue_type_id=None,
        start_at=None,
        max_results=None,
        data=None,
        **request_kwargs,
    ):
        """Get custom field configurations.

        Args:
            field_id_or_key: API path or query parameter.
            id: API path or query parameter.
            field_context_id: API path or query parameter.
            issue_id: API path or query parameter.
            project_key_or_id: API path or query parameter.
            issue_type_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"app/field/{field_id_or_key}/context/configuration", api_root="rest/api", api_version=self.api_version
        )
        params = {
            "id": id,
            "fieldContextId": field_context_id,
            "issueId": issue_id,
            "projectKeyOrId": project_key_or_id,
            "issueTypeId": issue_type_id,
            "startAt": start_at,
            "maxResults": max_results,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_custom_field_configuration(self, field_id_or_key, data=None, **request_kwargs):
        """Update custom field configurations.

        Args:
            field_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"app/field/{field_id_or_key}/context/configuration", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def update_custom_field_value(
        self, field_id_or_key, generate_changelog=None, generate_app_events=None, data=None, **request_kwargs
    ):
        """Update custom field value.

        Args:
            field_id_or_key: API path or query parameter.
            generate_changelog: API path or query parameter.
            generate_app_events: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"app/field/{field_id_or_key}/value", api_root="rest/api", api_version=self.api_version)
        params = {"generateChangelog": generate_changelog, "generateAppEvents": generate_app_events}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_application_property(self, key=None, permission_level=None, key_filter=None, data=None, **request_kwargs):
        """Get application property.

        Args:
            key: API path or query parameter.
            permission_level: API path or query parameter.
            key_filter: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("application-properties", api_root="rest/api", api_version=self.api_version)
        params = {"key": key, "permissionLevel": permission_level, "keyFilter": key_filter}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_advanced_settings(self, data=None, **request_kwargs):
        """Get advanced settings.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            "application-properties/advanced-settings", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_application_property(self, id, data=None, **request_kwargs):
        """Set application property.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"application-properties/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_all_application_roles(self, data=None, **request_kwargs):
        """Get all application roles.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("applicationrole", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_application_role(self, key, data=None, **request_kwargs):
        """Get application role.

        Args:
            key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"applicationrole/{key}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_attachment_content(self, id, redirect=None, data=None, **request_kwargs):
        """Get attachment content.

        Args:
            id: API path or query parameter.
            redirect: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"attachment/content/{id}", api_root="rest/api", api_version=self.api_version)
        params = {"redirect": redirect}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_attachment_meta(self, data=None, **request_kwargs):
        """Get Jira attachment settings.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("attachment/meta", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_attachment_thumbnail(
        self, id, redirect=None, fallback_to_default=None, width=None, height=None, data=None, **request_kwargs
    ):
        """Get attachment thumbnail.

        Args:
            id: API path or query parameter.
            redirect: API path or query parameter.
            fallback_to_default: API path or query parameter.
            width: API path or query parameter.
            height: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"attachment/thumbnail/{id}", api_root="rest/api", api_version=self.api_version)
        params = {"redirect": redirect, "fallbackToDefault": fallback_to_default, "width": width, "height": height}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def remove_attachment(self, id, data=None, **request_kwargs):
        """Delete attachment.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"attachment/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_attachment(self, id, data=None, **request_kwargs):
        """Get attachment metadata.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"attachment/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def expand_attachment_for_humans(self, id, data=None, **request_kwargs):
        """Get all metadata for an expanded attachment.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"attachment/{id}/expand/human", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def expand_attachment_for_machines(self, id, data=None, **request_kwargs):
        """Get contents metadata for an expanded attachment.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"attachment/{id}/expand/raw", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_audit_records(self, offset=None, limit=None, filter=None, from_=None, to=None, data=None, **request_kwargs):
        """Get audit records.

        Args:
            offset: API path or query parameter.
            limit: API path or query parameter.
            filter: API path or query parameter.
            from_: API path or query parameter.
            to: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("auditing/record", api_root="rest/api", api_version=self.api_version)
        params = {"offset": offset, "limit": limit, "filter": filter, "from": from_, "to": to}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_all_system_avatars(self, type, data=None, **request_kwargs):
        """Get system avatars by type.

        Args:
            type: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"avatar/{type}/system", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def submit_bulk_delete(self, data=None, **request_kwargs):
        """Bulk delete issues.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("bulk/issues/delete", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_bulk_editable_fields(
        self,
        issue_ids_or_keys=None,
        search_text=None,
        ending_before=None,
        starting_after=None,
        data=None,
        **request_kwargs,
    ):
        """Get bulk editable fields.

        Args:
            issue_ids_or_keys: API path or query parameter.
            search_text: API path or query parameter.
            ending_before: API path or query parameter.
            starting_after: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("bulk/issues/fields", api_root="rest/api", api_version=self.api_version)
        params = {
            "issueIdsOrKeys": issue_ids_or_keys,
            "searchText": search_text,
            "endingBefore": ending_before,
            "startingAfter": starting_after,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def submit_bulk_edit(self, data=None, **request_kwargs):
        """Bulk edit issues.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("bulk/issues/fields", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def submit_bulk_move(self, data=None, **request_kwargs):
        """Bulk move issues.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("bulk/issues/move", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_available_transitions(
        self, issue_ids_or_keys=None, ending_before=None, starting_after=None, data=None, **request_kwargs
    ):
        """Get available transitions.

        Args:
            issue_ids_or_keys: API path or query parameter.
            ending_before: API path or query parameter.
            starting_after: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("bulk/issues/transition", api_root="rest/api", api_version=self.api_version)
        params = {"issueIdsOrKeys": issue_ids_or_keys, "endingBefore": ending_before, "startingAfter": starting_after}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def submit_bulk_transition(self, data=None, **request_kwargs):
        """Bulk transition issue statuses.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("bulk/issues/transition", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def submit_bulk_unwatch(self, data=None, **request_kwargs):
        """Bulk unwatch issues.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("bulk/issues/unwatch", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def submit_bulk_watch(self, data=None, **request_kwargs):
        """Bulk watch issues.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("bulk/issues/watch", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_bulk_operation_progress(self, task_id, data=None, **request_kwargs):
        """Get bulk issue operation progress.

        Args:
            task_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"bulk/queue/{task_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_bulk_changelogs(self, data=None, **request_kwargs):
        """Bulk fetch changelogs.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("changelog/bulkfetch", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_all_user_data_classification_levels(self, status=None, order_by=None, data=None, **request_kwargs):
        """Get all classification levels.

        Args:
            status: API path or query parameter.
            order_by: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("classification-levels", api_root="rest/api", api_version=self.api_version)
        params = {"status": status, "orderBy": order_by}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_comments_by_ids(self, expand=None, data=None, **request_kwargs):
        """Get comments by IDs.

        Args:
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("comment/list", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_comment_property_keys(self, comment_id, data=None, **request_kwargs):
        """Get comment property keys.

        Args:
            comment_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"comment/{comment_id}/properties", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_comment_property(self, comment_id, property_key, data=None, **request_kwargs):
        """Delete comment property.

        Args:
            comment_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"comment/{comment_id}/properties/{property_key}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_comment_property(self, comment_id, property_key, data=None, **request_kwargs):
        """Get comment property.

        Args:
            comment_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"comment/{comment_id}/properties/{property_key}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_comment_property(self, comment_id, property_key, data=None, **request_kwargs):
        """Set comment property.

        Args:
            comment_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"comment/{comment_id}/properties/{property_key}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def find_components_for_projects(
        self,
        project_ids_or_keys=None,
        start_at=None,
        max_results=None,
        order_by=None,
        query=None,
        data=None,
        **request_kwargs,
    ):
        """Find components for projects.

        Args:
            project_ids_or_keys: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            order_by: API path or query parameter.
            query: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("component", api_root="rest/api", api_version=self.api_version)
        params = {
            "projectIdsOrKeys": project_ids_or_keys,
            "startAt": start_at,
            "maxResults": max_results,
            "orderBy": order_by,
            "query": query,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_component(self, data=None, **request_kwargs):
        """Create component.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("component", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_component(self, id, move_issues_to=None, data=None, **request_kwargs):
        """Delete component.

        Args:
            id: API path or query parameter.
            move_issues_to: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"component/{id}", api_root="rest/api", api_version=self.api_version)
        params = {"moveIssuesTo": move_issues_to}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_component(self, id, data=None, **request_kwargs):
        """Get component.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"component/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_component(self, id, data=None, **request_kwargs):
        """Update component.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"component/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_component_related_issues(self, id, data=None, **request_kwargs):
        """Get component issues count.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"component/{id}/relatedIssueCounts", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_field_association_schemes(
        self, project_id=None, query=None, start_at=None, max_results=None, data=None, **request_kwargs
    ):
        """Get field schemes.

        Args:
            project_id: API path or query parameter.
            query: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("config/fieldschemes", api_root="rest/api", api_version=self.api_version)
        params = {"projectId": project_id, "query": query, "startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_field_association_scheme(self, data=None, **request_kwargs):
        """Create field scheme.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("config/fieldschemes", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def remove_fields_associated_with_schemes(self, data=None, **request_kwargs):
        """Remove fields associated with field schemes.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("config/fieldschemes/fields", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def update_fields_associated_with_schemes(self, data=None, **request_kwargs):
        """Update fields associated with field schemes.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("config/fieldschemes/fields", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def remove_field_association_scheme_item_parameters(self, data=None, **request_kwargs):
        """Remove field parameters.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            "config/fieldschemes/fields/parameters", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def update_field_association_scheme_item_parameters(self, data=None, **request_kwargs):
        """Update field parameters.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            "config/fieldschemes/fields/parameters", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_projects_with_field_schemes(
        self, start_at=None, max_results=None, project_id=None, data=None, **request_kwargs
    ):
        """Get projects with field schemes.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            project_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("config/fieldschemes/projects", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results, "projectId": project_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def associate_projects_to_field_association_schemes(self, data=None, **request_kwargs):
        """Associate projects to field schemes.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("config/fieldschemes/projects", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_field_association_scheme(self, id, data=None, **request_kwargs):
        """Delete a field scheme.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"config/fieldschemes/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_field_association_scheme_by_id(self, id, data=None, **request_kwargs):
        """Get field scheme.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"config/fieldschemes/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_field_association_scheme(self, id, data=None, **request_kwargs):
        """Update field scheme.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"config/fieldschemes/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def clone_field_association_scheme(self, id, data=None, **request_kwargs):
        """Clone field scheme.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"config/fieldschemes/{id}/clone", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def search_field_association_scheme_fields(
        self, id, start_at=None, max_results=None, field_id=None, data=None, **request_kwargs
    ):
        """Search field scheme fields.

        Args:
            id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            field_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"config/fieldschemes/{id}/fields", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results, "fieldId": field_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_field_association_scheme_item_parameters(self, id, field_id, data=None, **request_kwargs):
        """Get field parameters.

        Args:
            id: API path or query parameter.
            field_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"config/fieldschemes/{id}/fields/{field_id}/parameters", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def search_field_association_scheme_projects(
        self, id, start_at=None, max_results=None, project_id=None, data=None, **request_kwargs
    ):
        """Search field scheme projects.

        Args:
            id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            project_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"config/fieldschemes/{id}/projects", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results, "projectId": project_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_configuration(self, data=None, **request_kwargs):
        """Get global settings.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("configuration", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_selected_time_tracking_implementation(self, data=None, **request_kwargs):
        """Get selected time tracking provider.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("configuration/timetracking", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def select_time_tracking_implementation(self, data=None, **request_kwargs):
        """Select time tracking provider.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("configuration/timetracking", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_available_time_tracking_implementations(self, data=None, **request_kwargs):
        """Get all time tracking providers.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("configuration/timetracking/list", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_shared_time_tracking_configuration(self, data=None, **request_kwargs):
        """Get time tracking settings.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("configuration/timetracking/options", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_shared_time_tracking_configuration(self, data=None, **request_kwargs):
        """Set time tracking settings.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("configuration/timetracking/options", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_custom_field_option(self, id, data=None, **request_kwargs):
        """Get custom field option.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"customFieldOption/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_all_dashboards(self, filter=None, start_at=None, max_results=None, data=None, **request_kwargs):
        """Get all dashboards.

        Args:
            filter: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("dashboard", api_root="rest/api", api_version=self.api_version)
        params = {"filter": filter, "startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_dashboard(self, extend_admin_permissions=None, data=None, **request_kwargs):
        """Create dashboard.

        Args:
            extend_admin_permissions: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("dashboard", api_root="rest/api", api_version=self.api_version)
        params = {"extendAdminPermissions": extend_admin_permissions}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def bulk_edit_dashboards(self, data=None, **request_kwargs):
        """Bulk edit dashboards.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("dashboard/bulk/edit", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_all_available_dashboard_gadgets(self, data=None, **request_kwargs):
        """Get available gadgets.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("dashboard/gadgets", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_dashboards_paginated(
        self,
        dashboard_name=None,
        account_id=None,
        owner=None,
        groupname=None,
        group_id=None,
        project_id=None,
        order_by=None,
        start_at=None,
        max_results=None,
        status=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Search for dashboards.

        Args:
            dashboard_name: API path or query parameter.
            account_id: API path or query parameter.
            owner: API path or query parameter.
            groupname: API path or query parameter.
            group_id: API path or query parameter.
            project_id: API path or query parameter.
            order_by: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            status: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("dashboard/search", api_root="rest/api", api_version=self.api_version)
        params = {
            "dashboardName": dashboard_name,
            "accountId": account_id,
            "owner": owner,
            "groupname": groupname,
            "groupId": group_id,
            "projectId": project_id,
            "orderBy": order_by,
            "startAt": start_at,
            "maxResults": max_results,
            "status": status,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_all_gadgets(self, dashboard_id, module_key=None, uri=None, gadget_id=None, data=None, **request_kwargs):
        """Get gadgets.

        Args:
            dashboard_id: API path or query parameter.
            module_key: API path or query parameter.
            uri: API path or query parameter.
            gadget_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"dashboard/{dashboard_id}/gadget", api_root="rest/api", api_version=self.api_version)
        params = {"moduleKey": module_key, "uri": uri, "gadgetId": gadget_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def add_gadget(self, dashboard_id, data=None, **request_kwargs):
        """Add gadget to dashboard.

        Args:
            dashboard_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"dashboard/{dashboard_id}/gadget", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def remove_gadget(self, dashboard_id, gadget_id, data=None, **request_kwargs):
        """Remove gadget from dashboard.

        Args:
            dashboard_id: API path or query parameter.
            gadget_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"dashboard/{dashboard_id}/gadget/{gadget_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def update_gadget(self, dashboard_id, gadget_id, data=None, **request_kwargs):
        """Update gadget on dashboard.

        Args:
            dashboard_id: API path or query parameter.
            gadget_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"dashboard/{dashboard_id}/gadget/{gadget_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_dashboard_item_property_keys(self, dashboard_id, item_id, data=None, **request_kwargs):
        """Get dashboard item property keys.

        Args:
            dashboard_id: API path or query parameter.
            item_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"dashboard/{dashboard_id}/items/{item_id}/properties", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_dashboard_item_property(self, dashboard_id, item_id, property_key, data=None, **request_kwargs):
        """Delete dashboard item property.

        Args:
            dashboard_id: API path or query parameter.
            item_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"dashboard/{dashboard_id}/items/{item_id}/properties/{property_key}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_dashboard_item_property(self, dashboard_id, item_id, property_key, data=None, **request_kwargs):
        """Get dashboard item property.

        Args:
            dashboard_id: API path or query parameter.
            item_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"dashboard/{dashboard_id}/items/{item_id}/properties/{property_key}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_dashboard_item_property(self, dashboard_id, item_id, property_key, data=None, **request_kwargs):
        """Set dashboard item property.

        Args:
            dashboard_id: API path or query parameter.
            item_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"dashboard/{dashboard_id}/items/{item_id}/properties/{property_key}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_dashboard(self, id, data=None, **request_kwargs):
        """Delete dashboard.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"dashboard/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_dashboard(self, id, data=None, **request_kwargs):
        """Get dashboard.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"dashboard/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_dashboard(self, id, extend_admin_permissions=None, data=None, **request_kwargs):
        """Update dashboard.

        Args:
            id: API path or query parameter.
            extend_admin_permissions: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"dashboard/{id}", api_root="rest/api", api_version=self.api_version)
        params = {"extendAdminPermissions": extend_admin_permissions}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(url, params=params, data=data, **request_kwargs)

    def copy_dashboard(self, id, extend_admin_permissions=None, data=None, **request_kwargs):
        """Copy dashboard.

        Args:
            id: API path or query parameter.
            extend_admin_permissions: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"dashboard/{id}/copy", api_root="rest/api", api_version=self.api_version)
        params = {"extendAdminPermissions": extend_admin_permissions}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_policy(self, data=None, **request_kwargs):
        """Get data policy for the workspace.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("data-policy", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_policies(self, ids=None, data=None, **request_kwargs):
        """Get data policy for projects.

        Args:
            ids: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("data-policy/project", api_root="rest/api", api_version=self.api_version)
        params = {"ids": ids}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_events(self, data=None, **request_kwargs):
        """Get events.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("events", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def analyse_expression(self, check=None, data=None, **request_kwargs):
        """Analyse Jira expression.

        Args:
            check: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("expression/analyse", api_root="rest/api", api_version=self.api_version)
        params = {"check": check}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def evaluate_jira_expression(self, expand=None, data=None, **request_kwargs):
        """Currently being removed. Evaluate Jira expression.

        Args:
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("expression/eval", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def evaluate_jsisjira_expression(self, expand=None, data=None, **request_kwargs):
        """Evaluate Jira expression using enhanced search API.

        Args:
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("expression/evaluate", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_fields(self, data=None, **request_kwargs):
        """Get fields.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("field", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_custom_field(self, data=None, **request_kwargs):
        """Create custom field.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("field", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def remove_associations(self, data=None, **request_kwargs):
        """Remove associations.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("field/association", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def create_associations(self, data=None, **request_kwargs):
        """Create associations.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("field/association", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_fields_paginated(
        self,
        start_at=None,
        max_results=None,
        type=None,
        id=None,
        query=None,
        order_by=None,
        expand=None,
        project_ids=None,
        data=None,
        **request_kwargs,
    ):
        """Get fields paginated.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            type: API path or query parameter.
            id: API path or query parameter.
            query: API path or query parameter.
            order_by: API path or query parameter.
            expand: API path or query parameter.
            project_ids: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("field/search", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "type": type,
            "id": id,
            "query": query,
            "orderBy": order_by,
            "expand": expand,
            "projectIds": project_ids,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_trashed_fields_paginated(
        self,
        start_at=None,
        max_results=None,
        id=None,
        query=None,
        expand=None,
        order_by=None,
        data=None,
        **request_kwargs,
    ):
        """Get fields in trash paginated.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            id: API path or query parameter.
            query: API path or query parameter.
            expand: API path or query parameter.
            order_by: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("field/search/trashed", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "id": id,
            "query": query,
            "expand": expand,
            "orderBy": order_by,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_custom_field(self, field_id, data=None, **request_kwargs):
        """Update custom field.

        Args:
            field_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"field/{field_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_field_project_associations(self, field_id, start_at=None, max_results=None, data=None, **request_kwargs):
        """Get field project associations.

        Args:
            field_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/association/project", api_root="rest/api", api_version=self.api_version
        )
        params = {"startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_contexts_for_field(
        self,
        field_id,
        is_any_issue_type=None,
        is_global_context=None,
        context_id=None,
        start_at=None,
        max_results=None,
        data=None,
        **request_kwargs,
    ):
        """Get custom field contexts.

        Args:
            field_id: API path or query parameter.
            is_any_issue_type: API path or query parameter.
            is_global_context: API path or query parameter.
            context_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"field/{field_id}/context", api_root="rest/api", api_version=self.api_version)
        params = {
            "isAnyIssueType": is_any_issue_type,
            "isGlobalContext": is_global_context,
            "contextId": context_id,
            "startAt": start_at,
            "maxResults": max_results,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_custom_field_context(self, field_id, data=None, **request_kwargs):
        """Create custom field context.

        Args:
            field_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"field/{field_id}/context", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_default_values(
        self, field_id, context_id=None, start_at=None, max_results=None, data=None, **request_kwargs
    ):
        """Get custom field contexts default values.

        Args:
            field_id: API path or query parameter.
            context_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/context/defaultValue", api_root="rest/api", api_version=self.api_version
        )
        params = {"contextId": context_id, "startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_default_values(self, field_id, data=None, **request_kwargs):
        """Set custom field contexts default values.

        Args:
            field_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/context/defaultValue", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_context_default_values(
        self,
        field_id,
        context_id=None,
        issue_type_id=None,
        start_at=None,
        max_results=None,
        data=None,
        **request_kwargs,
    ):
        """Get default values for a custom field grouped by context and issue type.

        Args:
            field_id: API path or query parameter.
            context_id: API path or query parameter.
            issue_type_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/context/defaultValues", api_root="rest/api", api_version=self.api_version
        )
        params = {"contextId": context_id, "issueTypeId": issue_type_id, "startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_issue_type_mappings_for_contexts(
        self, field_id, context_id=None, start_at=None, max_results=None, data=None, **request_kwargs
    ):
        """Get issue types for custom field context.

        Args:
            field_id: API path or query parameter.
            context_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/context/issuetypemapping", api_root="rest/api", api_version=self.api_version
        )
        params = {"contextId": context_id, "startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_custom_field_contexts_for_projects_and_issue_types(
        self, field_id, start_at=None, max_results=None, data=None, **request_kwargs
    ):
        """Get custom field contexts for projects and issue types.

        Args:
            field_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"field/{field_id}/context/mapping", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_project_context_mapping(
        self, field_id, context_id=None, start_at=None, max_results=None, data=None, **request_kwargs
    ):
        """Get project mappings for custom field context.

        Args:
            field_id: API path or query parameter.
            context_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/context/projectmapping", api_root="rest/api", api_version=self.api_version
        )
        params = {"contextId": context_id, "startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_custom_field_context(self, field_id, context_id, data=None, **request_kwargs):
        """Delete custom field context.

        Args:
            field_id: API path or query parameter.
            context_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/context/{context_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def update_custom_field_context(self, field_id, context_id, data=None, **request_kwargs):
        """Update custom field context.

        Args:
            field_id: API path or query parameter.
            context_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/context/{context_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def add_issue_types_to_context(self, field_id, context_id, data=None, **request_kwargs):
        """Add issue types to context.

        Args:
            field_id: API path or query parameter.
            context_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/context/{context_id}/issuetype", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def remove_issue_types_from_context(self, field_id, context_id, data=None, **request_kwargs):
        """Remove issue types from context.

        Args:
            field_id: API path or query parameter.
            context_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/context/{context_id}/issuetype/remove", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_options_for_context(
        self,
        field_id,
        context_id,
        option_id=None,
        only_options=None,
        start_at=None,
        max_results=None,
        data=None,
        **request_kwargs,
    ):
        """Get custom field options (context).

        Args:
            field_id: API path or query parameter.
            context_id: API path or query parameter.
            option_id: API path or query parameter.
            only_options: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/context/{context_id}/option", api_root="rest/api", api_version=self.api_version
        )
        params = {"optionId": option_id, "onlyOptions": only_options, "startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_custom_field_option(self, field_id, context_id, data=None, **request_kwargs):
        """Create custom field options (context).

        Args:
            field_id: API path or query parameter.
            context_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/context/{context_id}/option", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def update_custom_field_option(self, field_id, context_id, data=None, **request_kwargs):
        """Update custom field options (context).

        Args:
            field_id: API path or query parameter.
            context_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/context/{context_id}/option", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def reorder_custom_field_options(self, field_id, context_id, data=None, **request_kwargs):
        """Reorder custom field options (context).

        Args:
            field_id: API path or query parameter.
            context_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/context/{context_id}/option/move", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_custom_field_option(self, field_id, context_id, option_id, data=None, **request_kwargs):
        """Delete custom field options (context).

        Args:
            field_id: API path or query parameter.
            context_id: API path or query parameter.
            option_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/context/{context_id}/option/{option_id}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def replace_custom_field_option(
        self, field_id, option_id, context_id, replace_with=None, jql=None, data=None, **request_kwargs
    ):
        """Replace custom field options.

        Args:
            field_id: API path or query parameter.
            option_id: API path or query parameter.
            context_id: API path or query parameter.
            replace_with: API path or query parameter.
            jql: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/context/{context_id}/option/{option_id}/issue",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = {"replaceWith": replace_with, "jql": jql}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def assign_projects_to_custom_field_context(self, field_id, context_id, data=None, **request_kwargs):
        """Assign custom field context to projects.

        Args:
            field_id: API path or query parameter.
            context_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/context/{context_id}/project", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def remove_custom_field_context_from_projects(self, field_id, context_id, data=None, **request_kwargs):
        """Remove custom field context from projects.

        Args:
            field_id: API path or query parameter.
            context_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_id}/context/{context_id}/project/remove", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_contexts_for_field_deprecated(self, field_id, start_at=None, max_results=None, data=None, **request_kwargs):
        """Get contexts for a field.

        Args:
            field_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"field/{field_id}/contexts", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_screens_for_field(
        self, field_id, start_at=None, max_results=None, expand=None, data=None, **request_kwargs
    ):
        """Get screens for a field.

        Args:
            field_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"field/{field_id}/screens", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results, "expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_all_issue_field_options(self, field_key, start_at=None, max_results=None, data=None, **request_kwargs):
        """Get all issue field options.

        Args:
            field_key: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"field/{field_key}/option", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_issue_field_option(self, field_key, data=None, **request_kwargs):
        """Create issue field option.

        Args:
            field_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"field/{field_key}/option", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_selectable_issue_field_options(
        self, field_key, start_at=None, max_results=None, project_id=None, data=None, **request_kwargs
    ):
        """Get selectable issue field options.

        Args:
            field_key: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            project_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_key}/option/suggestions/edit", api_root="rest/api", api_version=self.api_version
        )
        params = {"startAt": start_at, "maxResults": max_results, "projectId": project_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_visible_issue_field_options(
        self, field_key, start_at=None, max_results=None, project_id=None, data=None, **request_kwargs
    ):
        """Get visible issue field options.

        Args:
            field_key: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            project_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_key}/option/suggestions/search", api_root="rest/api", api_version=self.api_version
        )
        params = {"startAt": start_at, "maxResults": max_results, "projectId": project_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_issue_field_option(self, field_key, option_id, data=None, **request_kwargs):
        """Delete issue field option.

        Args:
            field_key: API path or query parameter.
            option_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_key}/option/{option_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_issue_field_option(self, field_key, option_id, data=None, **request_kwargs):
        """Get issue field option.

        Args:
            field_key: API path or query parameter.
            option_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_key}/option/{option_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_issue_field_option(self, field_key, option_id, data=None, **request_kwargs):
        """Update issue field option.

        Args:
            field_key: API path or query parameter.
            option_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_key}/option/{option_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def replace_issue_field_option(
        self,
        field_key,
        option_id,
        replace_with=None,
        jql=None,
        override_screen_security=None,
        override_editable_flag=None,
        data=None,
        **request_kwargs,
    ):
        """Replace issue field option.

        Args:
            field_key: API path or query parameter.
            option_id: API path or query parameter.
            replace_with: API path or query parameter.
            jql: API path or query parameter.
            override_screen_security: API path or query parameter.
            override_editable_flag: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"field/{field_key}/option/{option_id}/issue", api_root="rest/api", api_version=self.api_version
        )
        params = {
            "replaceWith": replace_with,
            "jql": jql,
            "overrideScreenSecurity": override_screen_security,
            "overrideEditableFlag": override_editable_flag,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def delete_custom_field(self, id, data=None, **request_kwargs):
        """Delete custom field.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"field/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def restore_custom_field(self, id, data=None, **request_kwargs):
        """Restore custom field from trash.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"field/{id}/restore", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def trash_custom_field(self, id, data=None, **request_kwargs):
        """Move custom field to trash.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"field/{id}/trash", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_all_field_configurations(
        self, start_at=None, max_results=None, id=None, is_default=None, query=None, data=None, **request_kwargs
    ):
        """Get all field configurations.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            id: API path or query parameter.
            is_default: API path or query parameter.
            query: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("fieldconfiguration", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results, "id": id, "isDefault": is_default, "query": query}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_field_configuration(self, data=None, **request_kwargs):
        """Create field configuration.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("fieldconfiguration", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_field_configuration(self, id, data=None, **request_kwargs):
        """Delete field configuration.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"fieldconfiguration/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def update_field_configuration(self, id, data=None, **request_kwargs):
        """Update field configuration.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"fieldconfiguration/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_field_configuration_items(self, id, start_at=None, max_results=None, data=None, **request_kwargs):
        """Get field configuration items.

        Args:
            id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"fieldconfiguration/{id}/fields", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_field_configuration_items(self, id, data=None, **request_kwargs):
        """Update field configuration items.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"fieldconfiguration/{id}/fields", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_all_field_configuration_schemes(
        self, start_at=None, max_results=None, id=None, data=None, **request_kwargs
    ):
        """Get all field configuration schemes.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("fieldconfigurationscheme", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results, "id": id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_field_configuration_scheme(self, data=None, **request_kwargs):
        """Create field configuration scheme.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("fieldconfigurationscheme", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_field_configuration_scheme_mappings(
        self, start_at=None, max_results=None, field_configuration_scheme_id=None, data=None, **request_kwargs
    ):
        """Get field configuration issue type items.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            field_configuration_scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("fieldconfigurationscheme/mapping", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "fieldConfigurationSchemeId": field_configuration_scheme_id,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_field_configuration_scheme_project_mapping(
        self, start_at=None, max_results=None, project_id=None, data=None, **request_kwargs
    ):
        """Get field configuration schemes for projects.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            project_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("fieldconfigurationscheme/project", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results, "projectId": project_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def assign_field_configuration_scheme_to_project(self, data=None, **request_kwargs):
        """Assign field configuration scheme to project.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("fieldconfigurationscheme/project", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_field_configuration_scheme(self, id, data=None, **request_kwargs):
        """Delete field configuration scheme.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"fieldconfigurationscheme/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def update_field_configuration_scheme(self, id, data=None, **request_kwargs):
        """Update field configuration scheme.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"fieldconfigurationscheme/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def set_field_configuration_scheme_mapping(self, id, data=None, **request_kwargs):
        """Assign issue types to field configurations.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"fieldconfigurationscheme/{id}/mapping", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def remove_issue_types_from_global_field_configuration_scheme(self, id, data=None, **request_kwargs):
        """Remove issue types from field configuration scheme.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"fieldconfigurationscheme/{id}/mapping/delete", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def create_filter(self, expand=None, override_share_permissions=None, data=None, **request_kwargs):
        """Create filter.

        Args:
            expand: API path or query parameter.
            override_share_permissions: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("filter", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand, "overrideSharePermissions": override_share_permissions}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_default_share_scope(self, data=None, **request_kwargs):
        """Get default share scope.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("filter/defaultShareScope", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_default_share_scope(self, data=None, **request_kwargs):
        """Set default share scope.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("filter/defaultShareScope", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_favourite_filters(self, expand=None, data=None, **request_kwargs):
        """Get favorite filters.

        Args:
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("filter/favourite", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_my_filters(self, expand=None, include_favourites=None, data=None, **request_kwargs):
        """Get my filters.

        Args:
            expand: API path or query parameter.
            include_favourites: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("filter/my", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand, "includeFavourites": include_favourites}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_filters_paginated(
        self,
        filter_name=None,
        account_id=None,
        owner=None,
        groupname=None,
        group_id=None,
        project_id=None,
        id=None,
        order_by=None,
        start_at=None,
        max_results=None,
        expand=None,
        override_share_permissions=None,
        is_substring_match=None,
        data=None,
        **request_kwargs,
    ):
        """Search for filters.

        Args:
            filter_name: API path or query parameter.
            account_id: API path or query parameter.
            owner: API path or query parameter.
            groupname: API path or query parameter.
            group_id: API path or query parameter.
            project_id: API path or query parameter.
            id: API path or query parameter.
            order_by: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            expand: API path or query parameter.
            override_share_permissions: API path or query parameter.
            is_substring_match: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("filter/search", api_root="rest/api", api_version=self.api_version)
        params = {
            "filterName": filter_name,
            "accountId": account_id,
            "owner": owner,
            "groupname": groupname,
            "groupId": group_id,
            "projectId": project_id,
            "id": id,
            "orderBy": order_by,
            "startAt": start_at,
            "maxResults": max_results,
            "expand": expand,
            "overrideSharePermissions": override_share_permissions,
            "isSubstringMatch": is_substring_match,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_filter(self, id, data=None, **request_kwargs):
        """Delete filter.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"filter/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_filter(self, id, expand=None, override_share_permissions=None, data=None, **request_kwargs):
        """Get filter.

        Args:
            id: API path or query parameter.
            expand: API path or query parameter.
            override_share_permissions: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"filter/{id}", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand, "overrideSharePermissions": override_share_permissions}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_filter(self, id, expand=None, override_share_permissions=None, data=None, **request_kwargs):
        """Update filter.

        Args:
            id: API path or query parameter.
            expand: API path or query parameter.
            override_share_permissions: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"filter/{id}", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand, "overrideSharePermissions": override_share_permissions}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(url, params=params, data=data, **request_kwargs)

    def reset_columns(self, id, data=None, **request_kwargs):
        """Reset columns.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"filter/{id}/columns", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_columns(self, id, data=None, **request_kwargs):
        """Get columns.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"filter/{id}/columns", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_columns(self, id, data=None, **request_kwargs):
        """Set columns.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"filter/{id}/columns", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_favourite_for_filter(self, id, expand=None, data=None, **request_kwargs):
        """Remove filter as favorite.

        Args:
            id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"filter/{id}/favourite", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def set_favourite_for_filter(self, id, expand=None, data=None, **request_kwargs):
        """Add filter as favorite.

        Args:
            id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"filter/{id}/favourite", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(url, params=params, data=data, **request_kwargs)

    def change_filter_owner(self, id, data=None, **request_kwargs):
        """Change filter owner.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"filter/{id}/owner", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_share_permissions(self, id, data=None, **request_kwargs):
        """Get share permissions.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"filter/{id}/permission", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def add_share_permission(self, id, data=None, **request_kwargs):
        """Add share permission.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"filter/{id}/permission", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_share_permission(self, id, permission_id, data=None, **request_kwargs):
        """Delete share permission.

        Args:
            id: API path or query parameter.
            permission_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"filter/{id}/permission/{permission_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_share_permission(self, id, permission_id, data=None, **request_kwargs):
        """Get share permission.

        Args:
            id: API path or query parameter.
            permission_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"filter/{id}/permission/{permission_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def bulk_pin_unpin_projects_async(self, data=None, **request_kwargs):
        """Bulk pin or unpin issue panel to projects.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("forge/panel/action/bulk/async", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def remove_group(
        self, groupname=None, group_id=None, swap_group=None, swap_group_id=None, data=None, **request_kwargs
    ):
        """Remove group.

        Args:
            groupname: API path or query parameter.
            group_id: API path or query parameter.
            swap_group: API path or query parameter.
            swap_group_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("group", api_root="rest/api", api_version=self.api_version)
        params = {"groupname": groupname, "groupId": group_id, "swapGroup": swap_group, "swapGroupId": swap_group_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_group(self, groupname=None, group_id=None, expand=None, data=None, **request_kwargs):
        """Get group.

        Args:
            groupname: API path or query parameter.
            group_id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("group", api_root="rest/api", api_version=self.api_version)
        params = {"groupname": groupname, "groupId": group_id, "expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_group(self, data=None, **request_kwargs):
        """Create group.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("group", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def bulk_get_groups(
        self,
        start_at=None,
        max_results=None,
        group_id=None,
        group_name=None,
        access_type=None,
        application_key=None,
        data=None,
        **request_kwargs,
    ):
        """Bulk get groups.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            group_id: API path or query parameter.
            group_name: API path or query parameter.
            access_type: API path or query parameter.
            application_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("group/bulk", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "groupId": group_id,
            "groupName": group_name,
            "accessType": access_type,
            "applicationKey": application_key,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_users_from_group(
        self,
        groupname=None,
        group_id=None,
        include_inactive_users=None,
        start_at=None,
        max_results=None,
        data=None,
        **request_kwargs,
    ):
        """Get users from group.

        Args:
            groupname: API path or query parameter.
            group_id: API path or query parameter.
            include_inactive_users: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("group/member", api_root="rest/api", api_version=self.api_version)
        params = {
            "groupname": groupname,
            "groupId": group_id,
            "includeInactiveUsers": include_inactive_users,
            "startAt": start_at,
            "maxResults": max_results,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def remove_user_from_group(
        self, groupname=None, group_id=None, username=None, account_id=None, data=None, **request_kwargs
    ):
        """Remove user from group.

        Args:
            groupname: API path or query parameter.
            group_id: API path or query parameter.
            username: API path or query parameter.
            account_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("group/user", api_root="rest/api", api_version=self.api_version)
        params = {"groupname": groupname, "groupId": group_id, "username": username, "accountId": account_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def add_user_to_group(self, groupname=None, group_id=None, data=None, **request_kwargs):
        """Add user to group.

        Args:
            groupname: API path or query parameter.
            group_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("group/user", api_root="rest/api", api_version=self.api_version)
        params = {"groupname": groupname, "groupId": group_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def find_groups(
        self,
        account_id=None,
        query=None,
        exclude=None,
        exclude_id=None,
        max_results=None,
        case_insensitive=None,
        user_name=None,
        data=None,
        **request_kwargs,
    ):
        """Find groups.

        Args:
            account_id: API path or query parameter.
            query: API path or query parameter.
            exclude: API path or query parameter.
            exclude_id: API path or query parameter.
            max_results: API path or query parameter.
            case_insensitive: API path or query parameter.
            user_name: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("groups/picker", api_root="rest/api", api_version=self.api_version)
        params = {
            "accountId": account_id,
            "query": query,
            "exclude": exclude,
            "excludeId": exclude_id,
            "maxResults": max_results,
            "caseInsensitive": case_insensitive,
            "userName": user_name,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def find_users_and_groups(
        self,
        query=None,
        max_results=None,
        show_avatar=None,
        field_id=None,
        project_id=None,
        issue_type_id=None,
        avatar_size=None,
        case_insensitive=None,
        exclude_connect_addons=None,
        include_ai_agents=None,
        data=None,
        **request_kwargs,
    ):
        """Find users and groups.

        Args:
            query: API path or query parameter.
            max_results: API path or query parameter.
            show_avatar: API path or query parameter.
            field_id: API path or query parameter.
            project_id: API path or query parameter.
            issue_type_id: API path or query parameter.
            avatar_size: API path or query parameter.
            case_insensitive: API path or query parameter.
            exclude_connect_addons: API path or query parameter.
            include_ai_agents: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("groupuserpicker", api_root="rest/api", api_version=self.api_version)
        params = {
            "query": query,
            "maxResults": max_results,
            "showAvatar": show_avatar,
            "fieldId": field_id,
            "projectId": project_id,
            "issueTypeId": issue_type_id,
            "avatarSize": avatar_size,
            "caseInsensitive": case_insensitive,
            "excludeConnectAddons": exclude_connect_addons,
            "includeAiAgents": include_ai_agents,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_license(self, data=None, **request_kwargs):
        """Get license.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("instance/license", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_issue(self, update_history=None, data=None, **request_kwargs):
        """Create issue.

        Args:
            update_history: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issue", api_root="rest/api", api_version=self.api_version)
        params = {"updateHistory": update_history}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def archive_issues_async(self, data=None, **request_kwargs):
        """Archive issue(s) by JQL.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issue/archive", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def archive_issues(self, data=None, **request_kwargs):
        """Archive issue(s) by issue ID/key.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issue/archive", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def create_issues(self, data=None, **request_kwargs):
        """Bulk create issue.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issue/bulk", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def bulk_fetch_issues(self, data=None, **request_kwargs):
        """Bulk fetch issues.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issue/bulkfetch", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_create_issue_meta(
        self,
        project_ids=None,
        project_keys=None,
        issuetype_ids=None,
        issuetype_names=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get create issue metadata.

        Args:
            project_ids: API path or query parameter.
            project_keys: API path or query parameter.
            issuetype_ids: API path or query parameter.
            issuetype_names: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issue/createmeta", api_root="rest/api", api_version=self.api_version)
        params = {
            "projectIds": project_ids,
            "projectKeys": project_keys,
            "issuetypeIds": issuetype_ids,
            "issuetypeNames": issuetype_names,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_create_issue_meta_issue_types(
        self, project_id_or_key, start_at=None, max_results=None, data=None, **request_kwargs
    ):
        """Get create metadata issue types for a project.

        Args:
            project_id_or_key: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/createmeta/{project_id_or_key}/issuetypes", api_root="rest/api", api_version=self.api_version
        )
        params = {"startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_create_issue_meta_issue_type_id(
        self, project_id_or_key, issue_type_id, start_at=None, max_results=None, data=None, **request_kwargs
    ):
        """Get create field metadata for a project and issue type id.

        Args:
            project_id_or_key: API path or query parameter.
            issue_type_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/createmeta/{project_id_or_key}/issuetypes/{issue_type_id}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = {"startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_issue_adf_limit_report(self, is_returning_keys=None, field_type=None, data=None, **request_kwargs):
        """Get issue adf limit report.

        Args:
            is_returning_keys: API path or query parameter.
            field_type: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issue/limit/adf/report", api_root="rest/api", api_version=self.api_version)
        params = {"isReturningKeys": is_returning_keys, "fieldType": field_type}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_issue_limit_report(self, is_returning_keys=None, data=None, **request_kwargs):
        """Get issue limit report.

        Args:
            is_returning_keys: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issue/limit/report", api_root="rest/api", api_version=self.api_version)
        params = {"isReturningKeys": is_returning_keys}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_issue_picker_resource(
        self,
        query=None,
        current_jql=None,
        current_issue_key=None,
        current_project_id=None,
        show_sub_tasks=None,
        show_sub_task_parent=None,
        data=None,
        **request_kwargs,
    ):
        """Get issue picker suggestions.

        Args:
            query: API path or query parameter.
            current_jql: API path or query parameter.
            current_issue_key: API path or query parameter.
            current_project_id: API path or query parameter.
            show_sub_tasks: API path or query parameter.
            show_sub_task_parent: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issue/picker", api_root="rest/api", api_version=self.api_version)
        params = {
            "query": query,
            "currentJQL": current_jql,
            "currentIssueKey": current_issue_key,
            "currentProjectId": current_project_id,
            "showSubTasks": show_sub_tasks,
            "showSubTaskParent": show_sub_task_parent,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def bulk_set_issues_properties_list(self, data=None, **request_kwargs):
        """Bulk set issues properties by list.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issue/properties", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def bulk_set_issue_properties_by_issue(self, data=None, **request_kwargs):
        """Bulk set issue properties by issue.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issue/properties/multi", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def bulk_delete_issue_property(self, property_key, data=None, **request_kwargs):
        """Bulk delete issue property.

        Args:
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/properties/{property_key}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def bulk_set_issue_property(self, property_key, data=None, **request_kwargs):
        """Bulk set issue property.

        Args:
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/properties/{property_key}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def unarchive_issues(self, data=None, **request_kwargs):
        """Unarchive issue(s) by issue keys/ID.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issue/unarchive", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_is_watching_issue_bulk(self, data=None, **request_kwargs):
        """Get is watching issue bulk.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issue/watching", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_issue(self, issue_id_or_key, delete_subtasks=None, data=None, **request_kwargs):
        """Delete issue.

        Args:
            issue_id_or_key: API path or query parameter.
            delete_subtasks: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}", api_root="rest/api", api_version=self.api_version)
        params = {"deleteSubtasks": delete_subtasks}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_issue(
        self,
        issue_id_or_key,
        fields=None,
        fields_by_keys=None,
        expand=None,
        properties=None,
        update_history=None,
        fail_fast=None,
        data=None,
        **request_kwargs,
    ):
        """Get issue.

        Args:
            issue_id_or_key: API path or query parameter.
            fields: API path or query parameter.
            fields_by_keys: API path or query parameter.
            expand: API path or query parameter.
            properties: API path or query parameter.
            update_history: API path or query parameter.
            fail_fast: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}", api_root="rest/api", api_version=self.api_version)
        params = {
            "fields": fields,
            "fieldsByKeys": fields_by_keys,
            "expand": expand,
            "properties": properties,
            "updateHistory": update_history,
            "failFast": fail_fast,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def edit_issue(
        self,
        issue_id_or_key,
        notify_users=None,
        override_screen_security=None,
        override_editable_flag=None,
        return_issue=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Edit issue.

        Args:
            issue_id_or_key: API path or query parameter.
            notify_users: API path or query parameter.
            override_screen_security: API path or query parameter.
            override_editable_flag: API path or query parameter.
            return_issue: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}", api_root="rest/api", api_version=self.api_version)
        params = {
            "notifyUsers": notify_users,
            "overrideScreenSecurity": override_screen_security,
            "overrideEditableFlag": override_editable_flag,
            "returnIssue": return_issue,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(url, params=params, data=data, **request_kwargs)

    def assign_issue(self, issue_id_or_key, data=None, **request_kwargs):
        """Assign issue.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}/assignee", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def add_attachment(self, issue_id_or_key, data=None, **request_kwargs):
        """Add attachment.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/attachments", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_change_logs(self, issue_id_or_key, start_at=None, max_results=None, data=None, **request_kwargs):
        """Get changelogs.

        Args:
            issue_id_or_key: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}/changelog", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_change_logs_by_ids(self, issue_id_or_key, data=None, **request_kwargs):
        """Get changelogs by IDs.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/changelog/list", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_comments(
        self, issue_id_or_key, start_at=None, max_results=None, order_by=None, expand=None, data=None, **request_kwargs
    ):
        """Get comments.

        Args:
            issue_id_or_key: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            order_by: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}/comment", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results, "orderBy": order_by, "expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def add_comment(self, issue_id_or_key, expand=None, data=None, **request_kwargs):
        """Add comment.

        Args:
            issue_id_or_key: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}/comment", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_comment(self, issue_id_or_key, id, data=None, **request_kwargs):
        """Delete comment.

        Args:
            issue_id_or_key: API path or query parameter.
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/comment/{id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_comment(self, issue_id_or_key, id, expand=None, data=None, **request_kwargs):
        """Get comment.

        Args:
            issue_id_or_key: API path or query parameter.
            id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/comment/{id}", api_root="rest/api", api_version=self.api_version
        )
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_comment(
        self,
        issue_id_or_key,
        id,
        notify_users=None,
        override_editable_flag=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Update comment.

        Args:
            issue_id_or_key: API path or query parameter.
            id: API path or query parameter.
            notify_users: API path or query parameter.
            override_editable_flag: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/comment/{id}", api_root="rest/api", api_version=self.api_version
        )
        params = {"notifyUsers": notify_users, "overrideEditableFlag": override_editable_flag, "expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_edit_issue_meta(
        self, issue_id_or_key, override_screen_security=None, override_editable_flag=None, data=None, **request_kwargs
    ):
        """Get edit issue metadata.

        Args:
            issue_id_or_key: API path or query parameter.
            override_screen_security: API path or query parameter.
            override_editable_flag: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}/editmeta", api_root="rest/api", api_version=self.api_version)
        params = {"overrideScreenSecurity": override_screen_security, "overrideEditableFlag": override_editable_flag}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def notify(self, issue_id_or_key, data=None, **request_kwargs):
        """Send notification for issue.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}/notify", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_issue_property_keys(self, issue_id_or_key, data=None, **request_kwargs):
        """Get issue property keys.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/properties", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_issue_property(self, issue_id_or_key, property_key, data=None, **request_kwargs):
        """Delete issue property.

        Args:
            issue_id_or_key: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/properties/{property_key}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_issue_property(self, issue_id_or_key, property_key, data=None, **request_kwargs):
        """Get issue property.

        Args:
            issue_id_or_key: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/properties/{property_key}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_issue_property(self, issue_id_or_key, property_key, data=None, **request_kwargs):
        """Set issue property.

        Args:
            issue_id_or_key: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/properties/{property_key}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_remote_issue_link_by_global_id(self, issue_id_or_key, global_id=None, data=None, **request_kwargs):
        """Delete remote issue link by global ID.

        Args:
            issue_id_or_key: API path or query parameter.
            global_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/remotelink", api_root="rest/api", api_version=self.api_version
        )
        params = {"globalId": global_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_remote_issue_links(self, issue_id_or_key, global_id=None, data=None, **request_kwargs):
        """Get remote issue links.

        Args:
            issue_id_or_key: API path or query parameter.
            global_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/remotelink", api_root="rest/api", api_version=self.api_version
        )
        params = {"globalId": global_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_or_update_remote_issue_link(self, issue_id_or_key, data=None, **request_kwargs):
        """Create or update remote issue link.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/remotelink", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_remote_issue_link_by_id(self, issue_id_or_key, link_id, data=None, **request_kwargs):
        """Delete remote issue link by ID.

        Args:
            issue_id_or_key: API path or query parameter.
            link_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/remotelink/{link_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_remote_issue_link_by_id(self, issue_id_or_key, link_id, data=None, **request_kwargs):
        """Get remote issue link by ID.

        Args:
            issue_id_or_key: API path or query parameter.
            link_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/remotelink/{link_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_remote_issue_link(self, issue_id_or_key, link_id, data=None, **request_kwargs):
        """Update remote issue link by ID.

        Args:
            issue_id_or_key: API path or query parameter.
            link_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/remotelink/{link_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_transitions(
        self,
        issue_id_or_key,
        expand=None,
        transition_id=None,
        skip_remote_only_condition=None,
        include_unavailable_transitions=None,
        sort_by_ops_bar_and_status=None,
        data=None,
        **request_kwargs,
    ):
        """Get transitions.

        Args:
            issue_id_or_key: API path or query parameter.
            expand: API path or query parameter.
            transition_id: API path or query parameter.
            skip_remote_only_condition: API path or query parameter.
            include_unavailable_transitions: API path or query parameter.
            sort_by_ops_bar_and_status: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/transitions", api_root="rest/api", api_version=self.api_version
        )
        params = {
            "expand": expand,
            "transitionId": transition_id,
            "skipRemoteOnlyCondition": skip_remote_only_condition,
            "includeUnavailableTransitions": include_unavailable_transitions,
            "sortByOpsBarAndStatus": sort_by_ops_bar_and_status,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def do_transition(self, issue_id_or_key, data=None, **request_kwargs):
        """Transition issue.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/transitions", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def remove_vote(self, issue_id_or_key, data=None, **request_kwargs):
        """Delete vote.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}/votes", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_votes(self, issue_id_or_key, data=None, **request_kwargs):
        """Get votes.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}/votes", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def add_vote(self, issue_id_or_key, data=None, **request_kwargs):
        """Add vote.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}/votes", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def remove_watcher(self, issue_id_or_key, username=None, account_id=None, data=None, **request_kwargs):
        """Delete watcher.

        Args:
            issue_id_or_key: API path or query parameter.
            username: API path or query parameter.
            account_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}/watchers", api_root="rest/api", api_version=self.api_version)
        params = {"username": username, "accountId": account_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_issue_watchers(self, issue_id_or_key, data=None, **request_kwargs):
        """Get issue watchers.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}/watchers", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def add_watcher(self, issue_id_or_key, data=None, **request_kwargs):
        """Add watcher.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}/watchers", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def bulk_delete_worklogs(
        self, issue_id_or_key, adjust_estimate=None, override_editable_flag=None, data=None, **request_kwargs
    ):
        """Bulk delete worklogs.

        Args:
            issue_id_or_key: API path or query parameter.
            adjust_estimate: API path or query parameter.
            override_editable_flag: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}/worklog", api_root="rest/api", api_version=self.api_version)
        params = {"adjustEstimate": adjust_estimate, "overrideEditableFlag": override_editable_flag}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_issue_worklog(
        self,
        issue_id_or_key,
        start_at=None,
        max_results=None,
        started_after=None,
        started_before=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get issue worklogs.

        Args:
            issue_id_or_key: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            started_after: API path or query parameter.
            started_before: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}/worklog", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "startedAfter": started_after,
            "startedBefore": started_before,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def add_worklog(
        self,
        issue_id_or_key,
        notify_users=None,
        adjust_estimate=None,
        new_estimate=None,
        reduce_by=None,
        expand=None,
        override_editable_flag=None,
        data=None,
        **request_kwargs,
    ):
        """Add worklog.

        Args:
            issue_id_or_key: API path or query parameter.
            notify_users: API path or query parameter.
            adjust_estimate: API path or query parameter.
            new_estimate: API path or query parameter.
            reduce_by: API path or query parameter.
            expand: API path or query parameter.
            override_editable_flag: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issue/{issue_id_or_key}/worklog", api_root="rest/api", api_version=self.api_version)
        params = {
            "notifyUsers": notify_users,
            "adjustEstimate": adjust_estimate,
            "newEstimate": new_estimate,
            "reduceBy": reduce_by,
            "expand": expand,
            "overrideEditableFlag": override_editable_flag,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def bulk_move_worklogs(
        self, issue_id_or_key, adjust_estimate=None, override_editable_flag=None, data=None, **request_kwargs
    ):
        """Bulk move worklogs.

        Args:
            issue_id_or_key: API path or query parameter.
            adjust_estimate: API path or query parameter.
            override_editable_flag: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/worklog/move", api_root="rest/api", api_version=self.api_version
        )
        params = {"adjustEstimate": adjust_estimate, "overrideEditableFlag": override_editable_flag}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_worklog(
        self,
        issue_id_or_key,
        id,
        notify_users=None,
        adjust_estimate=None,
        new_estimate=None,
        increase_by=None,
        override_editable_flag=None,
        data=None,
        **request_kwargs,
    ):
        """Delete worklog.

        Args:
            issue_id_or_key: API path or query parameter.
            id: API path or query parameter.
            notify_users: API path or query parameter.
            adjust_estimate: API path or query parameter.
            new_estimate: API path or query parameter.
            increase_by: API path or query parameter.
            override_editable_flag: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/worklog/{id}", api_root="rest/api", api_version=self.api_version
        )
        params = {
            "notifyUsers": notify_users,
            "adjustEstimate": adjust_estimate,
            "newEstimate": new_estimate,
            "increaseBy": increase_by,
            "overrideEditableFlag": override_editable_flag,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_worklog(self, issue_id_or_key, id, expand=None, data=None, **request_kwargs):
        """Get worklog.

        Args:
            issue_id_or_key: API path or query parameter.
            id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/worklog/{id}", api_root="rest/api", api_version=self.api_version
        )
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_worklog(
        self,
        issue_id_or_key,
        id,
        notify_users=None,
        adjust_estimate=None,
        new_estimate=None,
        expand=None,
        override_editable_flag=None,
        data=None,
        **request_kwargs,
    ):
        """Update worklog.

        Args:
            issue_id_or_key: API path or query parameter.
            id: API path or query parameter.
            notify_users: API path or query parameter.
            adjust_estimate: API path or query parameter.
            new_estimate: API path or query parameter.
            expand: API path or query parameter.
            override_editable_flag: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/worklog/{id}", api_root="rest/api", api_version=self.api_version
        )
        params = {
            "notifyUsers": notify_users,
            "adjustEstimate": adjust_estimate,
            "newEstimate": new_estimate,
            "expand": expand,
            "overrideEditableFlag": override_editable_flag,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_worklog_property_keys(self, issue_id_or_key, worklog_id, data=None, **request_kwargs):
        """Get worklog property keys.

        Args:
            issue_id_or_key: API path or query parameter.
            worklog_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/worklog/{worklog_id}/properties",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_worklog_property(self, issue_id_or_key, worklog_id, property_key, data=None, **request_kwargs):
        """Delete worklog property.

        Args:
            issue_id_or_key: API path or query parameter.
            worklog_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/worklog/{worklog_id}/properties/{property_key}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_worklog_property(self, issue_id_or_key, worklog_id, property_key, data=None, **request_kwargs):
        """Get worklog property.

        Args:
            issue_id_or_key: API path or query parameter.
            worklog_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/worklog/{worklog_id}/properties/{property_key}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_worklog_property(self, issue_id_or_key, worklog_id, property_key, data=None, **request_kwargs):
        """Set worklog property.

        Args:
            issue_id_or_key: API path or query parameter.
            worklog_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issue/{issue_id_or_key}/worklog/{worklog_id}/properties/{property_key}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def link_issues(self, data=None, **request_kwargs):
        """Create issue link.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issueLink", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_issue_link(self, link_id, data=None, **request_kwargs):
        """Delete issue link.

        Args:
            link_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issueLink/{link_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_issue_link(self, link_id, data=None, **request_kwargs):
        """Get issue link.

        Args:
            link_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issueLink/{link_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_issue_link_types(self, data=None, **request_kwargs):
        """Get issue link types.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issueLinkType", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_issue_link_type(self, data=None, **request_kwargs):
        """Create issue link type.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issueLinkType", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_issue_link_type(self, issue_link_type_id, data=None, **request_kwargs):
        """Delete issue link type.

        Args:
            issue_link_type_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issueLinkType/{issue_link_type_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_issue_link_type(self, issue_link_type_id, data=None, **request_kwargs):
        """Get issue link type.

        Args:
            issue_link_type_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issueLinkType/{issue_link_type_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_issue_link_type(self, issue_link_type_id, data=None, **request_kwargs):
        """Update issue link type.

        Args:
            issue_link_type_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issueLinkType/{issue_link_type_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def export_archived_issues(self, data=None, **request_kwargs):
        """Export archived issue(s).

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issues/archive/export", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_issue_security_schemes(self, data=None, **request_kwargs):
        """Get issue security schemes.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuesecurityschemes", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_issue_security_scheme(self, data=None, **request_kwargs):
        """Create issue security scheme.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuesecurityschemes", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_security_levels(
        self, start_at=None, max_results=None, id=None, scheme_id=None, only_default=None, data=None, **request_kwargs
    ):
        """Get issue security levels.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            id: API path or query parameter.
            scheme_id: API path or query parameter.
            only_default: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuesecurityschemes/level", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "id": id,
            "schemeId": scheme_id,
            "onlyDefault": only_default,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_default_levels(self, data=None, **request_kwargs):
        """Set default issue security levels.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuesecurityschemes/level/default", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_security_level_members(
        self,
        start_at=None,
        max_results=None,
        id=None,
        scheme_id=None,
        level_id=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get issue security level members.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            id: API path or query parameter.
            scheme_id: API path or query parameter.
            level_id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuesecurityschemes/level/member", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "id": id,
            "schemeId": scheme_id,
            "levelId": level_id,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def search_projects_using_security_schemes(
        self,
        start_at=None,
        max_results=None,
        issue_security_scheme_id=None,
        project_id=None,
        data=None,
        **request_kwargs,
    ):
        """Get projects using issue security schemes.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            issue_security_scheme_id: API path or query parameter.
            project_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuesecurityschemes/project", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "issueSecuritySchemeId": issue_security_scheme_id,
            "projectId": project_id,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def associate_schemes_to_projects(self, data=None, **request_kwargs):
        """Associate security scheme to project.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuesecurityschemes/project", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def search_security_schemes(
        self, start_at=None, max_results=None, id=None, project_id=None, data=None, **request_kwargs
    ):
        """Search issue security schemes.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            id: API path or query parameter.
            project_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuesecurityschemes/search", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results, "id": id, "projectId": project_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_issue_security_scheme(self, id, data=None, **request_kwargs):
        """Get issue security scheme.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issuesecurityschemes/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_issue_security_scheme(self, id, data=None, **request_kwargs):
        """Update issue security scheme.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issuesecurityschemes/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_issue_security_level_members(
        self,
        issue_security_scheme_id,
        start_at=None,
        max_results=None,
        issue_security_level_id=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get issue security level members by issue security scheme.

        Args:
            issue_security_scheme_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            issue_security_level_id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuesecurityschemes/{issue_security_scheme_id}/members",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "issueSecurityLevelId": issue_security_level_id,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_security_scheme(self, scheme_id, data=None, **request_kwargs):
        """Delete issue security scheme.

        Args:
            scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issuesecurityschemes/{scheme_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def add_security_level(self, scheme_id, data=None, **request_kwargs):
        """Add issue security levels.

        Args:
            scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuesecurityschemes/{scheme_id}/level", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def remove_level(self, scheme_id, level_id, replace_with=None, data=None, **request_kwargs):
        """Remove issue security level.

        Args:
            scheme_id: API path or query parameter.
            level_id: API path or query parameter.
            replace_with: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuesecurityschemes/{scheme_id}/level/{level_id}", api_root="rest/api", api_version=self.api_version
        )
        params = {"replaceWith": replace_with}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def update_security_level(self, scheme_id, level_id, data=None, **request_kwargs):
        """Update issue security level.

        Args:
            scheme_id: API path or query parameter.
            level_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuesecurityschemes/{scheme_id}/level/{level_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def add_security_level_members(self, scheme_id, level_id, data=None, **request_kwargs):
        """Add issue security level members.

        Args:
            scheme_id: API path or query parameter.
            level_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuesecurityschemes/{scheme_id}/level/{level_id}/member",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def remove_member_from_security_level(self, scheme_id, level_id, member_id, data=None, **request_kwargs):
        """Remove member from issue security level.

        Args:
            scheme_id: API path or query parameter.
            level_id: API path or query parameter.
            member_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuesecurityschemes/{scheme_id}/level/{level_id}/member/{member_id}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_issue_all_types(self, data=None, **request_kwargs):
        """Get all issue types for user.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuetype", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_issue_type(self, data=None, **request_kwargs):
        """Create issue type.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuetype", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_issue_types_for_project(self, project_id=None, level=None, data=None, **request_kwargs):
        """Get issue types for project.

        Args:
            project_id: API path or query parameter.
            level: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuetype/project", api_root="rest/api", api_version=self.api_version)
        params = {"projectId": project_id, "level": level}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_issue_type(self, id, alternative_issue_type_id=None, data=None, **request_kwargs):
        """Delete issue type.

        Args:
            id: API path or query parameter.
            alternative_issue_type_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issuetype/{id}", api_root="rest/api", api_version=self.api_version)
        params = {"alternativeIssueTypeId": alternative_issue_type_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_issue_type(self, id, data=None, **request_kwargs):
        """Get issue type.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issuetype/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_issue_type(self, id, data=None, **request_kwargs):
        """Update issue type.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issuetype/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_alternative_issue_types(self, id, data=None, **request_kwargs):
        """Get alternative issue types.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issuetype/{id}/alternatives", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_issue_type_avatar(self, id, x=None, y=None, size=None, data=None, **request_kwargs):
        """Load issue type avatar.

        Args:
            id: API path or query parameter.
            x: API path or query parameter.
            y: API path or query parameter.
            size: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"issuetype/{id}/avatar2", api_root="rest/api", api_version=self.api_version)
        params = {"x": x, "y": y, "size": size}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_issue_type_property_keys(self, issue_type_id, data=None, **request_kwargs):
        """Get issue type property keys.

        Args:
            issue_type_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuetype/{issue_type_id}/properties", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_issue_type_property(self, issue_type_id, property_key, data=None, **request_kwargs):
        """Delete issue type property.

        Args:
            issue_type_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuetype/{issue_type_id}/properties/{property_key}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_issue_type_property(self, issue_type_id, property_key, data=None, **request_kwargs):
        """Get issue type property.

        Args:
            issue_type_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuetype/{issue_type_id}/properties/{property_key}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_issue_type_property(self, issue_type_id, property_key, data=None, **request_kwargs):
        """Set issue type property.

        Args:
            issue_type_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuetype/{issue_type_id}/properties/{property_key}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_all_issue_type_schemes(
        self,
        start_at=None,
        max_results=None,
        id=None,
        order_by=None,
        expand=None,
        query_string=None,
        data=None,
        **request_kwargs,
    ):
        """Get all issue type schemes.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            id: API path or query parameter.
            order_by: API path or query parameter.
            expand: API path or query parameter.
            query_string: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuetypescheme", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "id": id,
            "orderBy": order_by,
            "expand": expand,
            "queryString": query_string,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_issue_type_scheme(self, data=None, **request_kwargs):
        """Create issue type scheme.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuetypescheme", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_issue_type_schemes_mapping(
        self, start_at=None, max_results=None, issue_type_scheme_id=None, data=None, **request_kwargs
    ):
        """Get issue type scheme items.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            issue_type_scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuetypescheme/mapping", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results, "issueTypeSchemeId": issue_type_scheme_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_issue_type_scheme_for_projects(
        self, start_at=None, max_results=None, project_id=None, data=None, **request_kwargs
    ):
        """Get issue type schemes for projects.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            project_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuetypescheme/project", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results, "projectId": project_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def assign_issue_type_scheme_to_project(self, data=None, **request_kwargs):
        """Assign issue type scheme to project.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuetypescheme/project", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_issue_type_scheme(self, issue_type_scheme_id, data=None, **request_kwargs):
        """Delete issue type scheme.

        Args:
            issue_type_scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuetypescheme/{issue_type_scheme_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def update_issue_type_scheme(self, issue_type_scheme_id, data=None, **request_kwargs):
        """Update issue type scheme.

        Args:
            issue_type_scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuetypescheme/{issue_type_scheme_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def add_issue_types_to_issue_type_scheme(self, issue_type_scheme_id, data=None, **request_kwargs):
        """Add issue types to issue type scheme.

        Args:
            issue_type_scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuetypescheme/{issue_type_scheme_id}/issuetype", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def reorder_issue_types_in_issue_type_scheme(self, issue_type_scheme_id, data=None, **request_kwargs):
        """Change order of issue types.

        Args:
            issue_type_scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuetypescheme/{issue_type_scheme_id}/issuetype/move", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def remove_issue_type_from_issue_type_scheme(
        self, issue_type_scheme_id, issue_type_id, data=None, **request_kwargs
    ):
        """Remove issue type from issue type scheme.

        Args:
            issue_type_scheme_id: API path or query parameter.
            issue_type_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuetypescheme/{issue_type_scheme_id}/issuetype/{issue_type_id}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_issue_type_screen_schemes(
        self,
        start_at=None,
        max_results=None,
        id=None,
        query_string=None,
        order_by=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get issue type screen schemes.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            id: API path or query parameter.
            query_string: API path or query parameter.
            order_by: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuetypescreenscheme", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "id": id,
            "queryString": query_string,
            "orderBy": order_by,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_issue_type_screen_scheme(self, data=None, **request_kwargs):
        """Create issue type screen scheme.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuetypescreenscheme", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_issue_type_screen_scheme_mappings(
        self, start_at=None, max_results=None, issue_type_screen_scheme_id=None, data=None, **request_kwargs
    ):
        """Get issue type screen scheme items.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            issue_type_screen_scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuetypescreenscheme/mapping", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "issueTypeScreenSchemeId": issue_type_screen_scheme_id,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_issue_type_screen_scheme_project_associations(
        self, start_at=None, max_results=None, project_id=None, data=None, **request_kwargs
    ):
        """Get issue type screen schemes for projects.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            project_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuetypescreenscheme/project", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results, "projectId": project_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def assign_issue_type_screen_scheme_to_project(self, data=None, **request_kwargs):
        """Assign issue type screen scheme to project.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("issuetypescreenscheme/project", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_issue_type_screen_scheme(self, issue_type_screen_scheme_id, data=None, **request_kwargs):
        """Delete issue type screen scheme.

        Args:
            issue_type_screen_scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuetypescreenscheme/{issue_type_screen_scheme_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def update_issue_type_screen_scheme(self, issue_type_screen_scheme_id, data=None, **request_kwargs):
        """Update issue type screen scheme.

        Args:
            issue_type_screen_scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuetypescreenscheme/{issue_type_screen_scheme_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def append_mappings_for_issue_type_screen_scheme(self, issue_type_screen_scheme_id, data=None, **request_kwargs):
        """Append mappings to issue type screen scheme.

        Args:
            issue_type_screen_scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuetypescreenscheme/{issue_type_screen_scheme_id}/mapping",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def update_default_screen_scheme(self, issue_type_screen_scheme_id, data=None, **request_kwargs):
        """Update issue type screen scheme default screen scheme.

        Args:
            issue_type_screen_scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuetypescreenscheme/{issue_type_screen_scheme_id}/mapping/default",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def remove_mappings_from_issue_type_screen_scheme(self, issue_type_screen_scheme_id, data=None, **request_kwargs):
        """Remove mappings from issue type screen scheme.

        Args:
            issue_type_screen_scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuetypescreenscheme/{issue_type_screen_scheme_id}/mapping/remove",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_projects_for_issue_type_screen_scheme(
        self, issue_type_screen_scheme_id, start_at=None, max_results=None, query=None, data=None, **request_kwargs
    ):
        """Get issue type screen scheme projects.

        Args:
            issue_type_screen_scheme_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            query: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"issuetypescreenscheme/{issue_type_screen_scheme_id}/project",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = {"startAt": start_at, "maxResults": max_results, "query": query}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_auto_complete(self, data=None, **request_kwargs):
        """Get field reference data (GET).

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("jql/autocompletedata", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_auto_complete_post(self, data=None, **request_kwargs):
        """Get field reference data (POST).

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("jql/autocompletedata", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_field_auto_complete_for_query_string(
        self, field_name=None, field_value=None, predicate_name=None, predicate_value=None, data=None, **request_kwargs
    ):
        """Get field auto complete suggestions.

        Args:
            field_name: API path or query parameter.
            field_value: API path or query parameter.
            predicate_name: API path or query parameter.
            predicate_value: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("jql/autocompletedata/suggestions", api_root="rest/api", api_version=self.api_version)
        params = {
            "fieldName": field_name,
            "fieldValue": field_value,
            "predicateName": predicate_name,
            "predicateValue": predicate_value,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_precomputations(
        self, function_key=None, start_at=None, max_results=None, order_by=None, data=None, **request_kwargs
    ):
        """Get precomputations (apps).

        Args:
            function_key: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            order_by: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("jql/function/computation", api_root="rest/api", api_version=self.api_version)
        params = {"functionKey": function_key, "startAt": start_at, "maxResults": max_results, "orderBy": order_by}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_precomputations(self, skip_not_found_precomputations=None, data=None, **request_kwargs):
        """Update precomputations (apps).

        Args:
            skip_not_found_precomputations: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("jql/function/computation", api_root="rest/api", api_version=self.api_version)
        params = {"skipNotFoundPrecomputations": skip_not_found_precomputations}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_precomputations_by_id(self, order_by=None, data=None, **request_kwargs):
        """Get precomputations by ID (apps).

        Args:
            order_by: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("jql/function/computation/search", api_root="rest/api", api_version=self.api_version)
        params = {"orderBy": order_by}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def match_issues(self, data=None, **request_kwargs):
        """Check issues against JQL.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("jql/match", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def parse_jql_queries(self, validation=None, data=None, **request_kwargs):
        """Parse JQL query.

        Args:
            validation: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("jql/parse", api_root="rest/api", api_version=self.api_version)
        params = {"validation": validation}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def migrate_queries(self, data=None, **request_kwargs):
        """Convert user identifiers to account IDs in JQL queries.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("jql/pdcleaner", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def sanitise_jql_queries(self, data=None, **request_kwargs):
        """Sanitize JQL queries.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("jql/sanitize", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_all_labels(self, start_at=None, max_results=None, data=None, **request_kwargs):
        """Get all labels.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("label", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_approximate_license_count(self, data=None, **request_kwargs):
        """Get approximate license count.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("license/approximateLicenseCount", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_approximate_application_license_count(self, application_key, data=None, **request_kwargs):
        """Get approximate application license count.

        Args:
            application_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"license/approximateLicenseCount/product/{application_key}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_my_permissions(
        self,
        project_key=None,
        project_id=None,
        issue_key=None,
        issue_id=None,
        permissions=None,
        project_uuid=None,
        project_configuration_uuid=None,
        comment_id=None,
        data=None,
        **request_kwargs,
    ):
        """Get my permissions.

        Args:
            project_key: API path or query parameter.
            project_id: API path or query parameter.
            issue_key: API path or query parameter.
            issue_id: API path or query parameter.
            permissions: API path or query parameter.
            project_uuid: API path or query parameter.
            project_configuration_uuid: API path or query parameter.
            comment_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("mypermissions", api_root="rest/api", api_version=self.api_version)
        params = {
            "projectKey": project_key,
            "projectId": project_id,
            "issueKey": issue_key,
            "issueId": issue_id,
            "permissions": permissions,
            "projectUuid": project_uuid,
            "projectConfigurationUuid": project_configuration_uuid,
            "commentId": comment_id,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def remove_preference(self, key=None, data=None, **request_kwargs):
        """Delete preference.

        Args:
            key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("mypreferences", api_root="rest/api", api_version=self.api_version)
        params = {"key": key}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_preference(self, key=None, data=None, **request_kwargs):
        """Get preference.

        Args:
            key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("mypreferences", api_root="rest/api", api_version=self.api_version)
        params = {"key": key}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_preference(self, key=None, data=None, **request_kwargs):
        """Set preference.

        Args:
            key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("mypreferences", api_root="rest/api", api_version=self.api_version)
        params = {"key": key}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_locale(self, data=None, **request_kwargs):
        """Get locale.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("mypreferences/locale", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_locale(self, data=None, **request_kwargs):
        """Set locale.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("mypreferences/locale", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_current_user(self, expand=None, data=None, **request_kwargs):
        """Get current user.

        Args:
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("myself", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_notification_schemes(
        self,
        start_at=None,
        max_results=None,
        id=None,
        project_id=None,
        only_default=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get notification schemes paginated.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            id: API path or query parameter.
            project_id: API path or query parameter.
            only_default: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("notificationscheme", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "id": id,
            "projectId": project_id,
            "onlyDefault": only_default,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_notification_scheme(self, data=None, **request_kwargs):
        """Create notification scheme.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("notificationscheme", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_notification_scheme_to_project_mappings(
        self, start_at=None, max_results=None, notification_scheme_id=None, project_id=None, data=None, **request_kwargs
    ):
        """Get projects using notification schemes paginated.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            notification_scheme_id: API path or query parameter.
            project_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("notificationscheme/project", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "notificationSchemeId": notification_scheme_id,
            "projectId": project_id,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_notification_scheme(self, id, expand=None, data=None, **request_kwargs):
        """Get notification scheme.

        Args:
            id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"notificationscheme/{id}", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_notification_scheme(self, id, data=None, **request_kwargs):
        """Update notification scheme.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"notificationscheme/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def add_notifications(self, id, data=None, **request_kwargs):
        """Add notifications to notification scheme.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"notificationscheme/{id}/notification", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_notification_scheme(self, notification_scheme_id, data=None, **request_kwargs):
        """Delete notification scheme.

        Args:
            notification_scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"notificationscheme/{notification_scheme_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def remove_notification_from_notification_scheme(
        self, notification_scheme_id, notification_id, data=None, **request_kwargs
    ):
        """Remove notification from notification scheme.

        Args:
            notification_scheme_id: API path or query parameter.
            notification_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"notificationscheme/{notification_scheme_id}/notification/{notification_id}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_all_permissions(self, data=None, **request_kwargs):
        """Get all permissions.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("permissions", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_bulk_permissions(self, data=None, **request_kwargs):
        """Get bulk permissions.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("permissions/check", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_permitted_projects(self, data=None, **request_kwargs):
        """Get permitted projects.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("permissions/project", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_all_permission_schemes(self, expand=None, data=None, **request_kwargs):
        """Get all permission schemes.

        Args:
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("permissionscheme", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_permission_scheme(self, expand=None, data=None, **request_kwargs):
        """Create permission scheme.

        Args:
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("permissionscheme", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_permission_scheme(self, scheme_id, data=None, **request_kwargs):
        """Delete permission scheme.

        Args:
            scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"permissionscheme/{scheme_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_permission_scheme(self, scheme_id, expand=None, data=None, **request_kwargs):
        """Get permission scheme.

        Args:
            scheme_id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"permissionscheme/{scheme_id}", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_permission_scheme(self, scheme_id, expand=None, data=None, **request_kwargs):
        """Update permission scheme.

        Args:
            scheme_id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"permissionscheme/{scheme_id}", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_permission_scheme_grants(self, scheme_id, expand=None, data=None, **request_kwargs):
        """Get permission scheme grants.

        Args:
            scheme_id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"permissionscheme/{scheme_id}/permission", api_root="rest/api", api_version=self.api_version
        )
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_permission_grant(self, scheme_id, expand=None, data=None, **request_kwargs):
        """Create permission grant.

        Args:
            scheme_id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"permissionscheme/{scheme_id}/permission", api_root="rest/api", api_version=self.api_version
        )
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_permission_scheme_entity(self, scheme_id, permission_id, data=None, **request_kwargs):
        """Delete permission scheme grant.

        Args:
            scheme_id: API path or query parameter.
            permission_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"permissionscheme/{scheme_id}/permission/{permission_id}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_permission_scheme_grant(self, scheme_id, permission_id, expand=None, data=None, **request_kwargs):
        """Get permission scheme grant.

        Args:
            scheme_id: API path or query parameter.
            permission_id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"permissionscheme/{scheme_id}/permission/{permission_id}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_plans(
        self, include_trashed=None, include_archived=None, cursor=None, max_results=None, data=None, **request_kwargs
    ):
        """Get plans paginated.

        Args:
            include_trashed: API path or query parameter.
            include_archived: API path or query parameter.
            cursor: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("plans/plan", api_root="rest/api", api_version=self.api_version)
        params = {
            "includeTrashed": include_trashed,
            "includeArchived": include_archived,
            "cursor": cursor,
            "maxResults": max_results,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_plan(self, use_group_id=None, data=None, **request_kwargs):
        """Create plan.

        Args:
            use_group_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("plans/plan", api_root="rest/api", api_version=self.api_version)
        params = {"useGroupId": use_group_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_plan(self, plan_id, use_group_id=None, data=None, **request_kwargs):
        """Get plan.

        Args:
            plan_id: API path or query parameter.
            use_group_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"plans/plan/{plan_id}", api_root="rest/api", api_version=self.api_version)
        params = {"useGroupId": use_group_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_plan(self, plan_id, use_group_id=None, data=None, **request_kwargs):
        """Update plan.

        Args:
            plan_id: API path or query parameter.
            use_group_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"plans/plan/{plan_id}", api_root="rest/api", api_version=self.api_version)
        params = {"useGroupId": use_group_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(url, params=params, data=data, **request_kwargs)

    def archive_plan(self, plan_id, data=None, **request_kwargs):
        """Archive plan.

        Args:
            plan_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"plans/plan/{plan_id}/archive", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def duplicate_plan(self, plan_id, data=None, **request_kwargs):
        """Duplicate plan.

        Args:
            plan_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"plans/plan/{plan_id}/duplicate", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_teams(self, plan_id, cursor=None, max_results=None, data=None, **request_kwargs):
        """Get teams in plan paginated.

        Args:
            plan_id: API path or query parameter.
            cursor: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"plans/plan/{plan_id}/team", api_root="rest/api", api_version=self.api_version)
        params = {"cursor": cursor, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def add_atlassian_team(self, plan_id, data=None, **request_kwargs):
        """Add Atlassian team to plan.

        Args:
            plan_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"plans/plan/{plan_id}/team/atlassian", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def remove_atlassian_team(self, plan_id, atlassian_team_id, data=None, **request_kwargs):
        """Remove Atlassian team from plan.

        Args:
            plan_id: API path or query parameter.
            atlassian_team_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"plans/plan/{plan_id}/team/atlassian/{atlassian_team_id}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_atlassian_team(self, plan_id, atlassian_team_id, data=None, **request_kwargs):
        """Get Atlassian team in plan.

        Args:
            plan_id: API path or query parameter.
            atlassian_team_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"plans/plan/{plan_id}/team/atlassian/{atlassian_team_id}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_atlassian_team(self, plan_id, atlassian_team_id, data=None, **request_kwargs):
        """Update Atlassian team in plan.

        Args:
            plan_id: API path or query parameter.
            atlassian_team_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"plans/plan/{plan_id}/team/atlassian/{atlassian_team_id}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def create_plan_only_team(self, plan_id, data=None, **request_kwargs):
        """Create plan-only team.

        Args:
            plan_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"plans/plan/{plan_id}/team/planonly", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_plan_only_team(self, plan_id, plan_only_team_id, data=None, **request_kwargs):
        """Delete plan-only team.

        Args:
            plan_id: API path or query parameter.
            plan_only_team_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"plans/plan/{plan_id}/team/planonly/{plan_only_team_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_plan_only_team(self, plan_id, plan_only_team_id, data=None, **request_kwargs):
        """Get plan-only team.

        Args:
            plan_id: API path or query parameter.
            plan_only_team_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"plans/plan/{plan_id}/team/planonly/{plan_only_team_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_plan_only_team(self, plan_id, plan_only_team_id, data=None, **request_kwargs):
        """Update plan-only team.

        Args:
            plan_id: API path or query parameter.
            plan_only_team_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"plans/plan/{plan_id}/team/planonly/{plan_only_team_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def trash_plan(self, plan_id, data=None, **request_kwargs):
        """Trash plan.

        Args:
            plan_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"plans/plan/{plan_id}/trash", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_priorities(self, data=None, **request_kwargs):
        """Get priorities.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("priority", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_priority(self, data=None, **request_kwargs):
        """Create priority.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("priority", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def set_default_priority(self, data=None, **request_kwargs):
        """Set default priority.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("priority/default", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def move_priorities(self, data=None, **request_kwargs):
        """Move priorities.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("priority/move", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def search_priorities(
        self,
        start_at=None,
        max_results=None,
        id=None,
        project_id=None,
        priority_name=None,
        only_default=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Search priorities.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            id: API path or query parameter.
            project_id: API path or query parameter.
            priority_name: API path or query parameter.
            only_default: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("priority/search", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "id": id,
            "projectId": project_id,
            "priorityName": priority_name,
            "onlyDefault": only_default,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_priority(self, id, data=None, **request_kwargs):
        """Delete priority.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"priority/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_priority(self, id, data=None, **request_kwargs):
        """Get priority.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"priority/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_priority(self, id, data=None, **request_kwargs):
        """Update priority.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"priority/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_priority_schemes(
        self,
        start_at=None,
        max_results=None,
        priority_id=None,
        scheme_id=None,
        scheme_name=None,
        only_default=None,
        order_by=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get priority schemes.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            priority_id: API path or query parameter.
            scheme_id: API path or query parameter.
            scheme_name: API path or query parameter.
            only_default: API path or query parameter.
            order_by: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("priorityscheme", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "priorityId": priority_id,
            "schemeId": scheme_id,
            "schemeName": scheme_name,
            "onlyDefault": only_default,
            "orderBy": order_by,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_priority_scheme(self, data=None, **request_kwargs):
        """Create priority scheme.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("priorityscheme", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def suggested_priorities_for_mappings(self, data=None, **request_kwargs):
        """Suggested priorities for mappings.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("priorityscheme/mappings", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_available_priorities_by_priority_scheme(
        self, start_at=None, max_results=None, query=None, scheme_id=None, exclude=None, data=None, **request_kwargs
    ):
        """Get available priorities by priority scheme.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            query: API path or query parameter.
            scheme_id: API path or query parameter.
            exclude: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            "priorityscheme/priorities/available", api_root="rest/api", api_version=self.api_version
        )
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "query": query,
            "schemeId": scheme_id,
            "exclude": exclude,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_priority_scheme(self, scheme_id, data=None, **request_kwargs):
        """Delete priority scheme.

        Args:
            scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"priorityscheme/{scheme_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def update_priority_scheme(self, scheme_id, data=None, **request_kwargs):
        """Update priority scheme.

        Args:
            scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"priorityscheme/{scheme_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_priorities_by_priority_scheme(
        self, scheme_id, start_at=None, max_results=None, data=None, **request_kwargs
    ):
        """Get priorities by priority scheme.

        Args:
            scheme_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"priorityscheme/{scheme_id}/priorities", api_root="rest/api", api_version=self.api_version
        )
        params = {"startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_projects_by_priority_scheme(
        self, scheme_id, start_at=None, max_results=None, project_id=None, query=None, data=None, **request_kwargs
    ):
        """Get projects by priority scheme.

        Args:
            scheme_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            project_id: API path or query parameter.
            query: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"priorityscheme/{scheme_id}/projects", api_root="rest/api", api_version=self.api_version
        )
        params = {"startAt": start_at, "maxResults": max_results, "projectId": project_id, "query": query}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_all_projects(self, expand=None, recent=None, properties=None, data=None, **request_kwargs):
        """Get all projects.

        Args:
            expand: API path or query parameter.
            recent: API path or query parameter.
            properties: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("project", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand, "recent": recent, "properties": properties}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_project(self, data=None, **request_kwargs):
        """Create project.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("project", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def create_project_with_custom_template(self, data=None, **request_kwargs):
        """Create custom project.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("project-template", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def edit_template(self, data=None, **request_kwargs):
        """Edit a custom project template.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("project-template/edit-template", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def live_template(self, project_id=None, template_key=None, data=None, **request_kwargs):
        """Gets a custom project template.

        Args:
            project_id: API path or query parameter.
            template_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("project-template/live-template", api_root="rest/api", api_version=self.api_version)
        params = {"projectId": project_id, "templateKey": template_key}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def remove_template(self, template_key=None, data=None, **request_kwargs):
        """Deletes a custom project template.

        Args:
            template_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("project-template/remove-template", api_root="rest/api", api_version=self.api_version)
        params = {"templateKey": template_key}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def save_template(self, data=None, **request_kwargs):
        """Save a custom project template.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("project-template/save-template", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_recent(self, expand=None, properties=None, data=None, **request_kwargs):
        """Get recent projects.

        Args:
            expand: API path or query parameter.
            properties: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("project/recent", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand, "properties": properties}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def search_projects(
        self,
        start_at=None,
        max_results=None,
        order_by=None,
        id=None,
        keys=None,
        query=None,
        type_key=None,
        category_id=None,
        action=None,
        expand=None,
        status=None,
        properties=None,
        property_query=None,
        data=None,
        **request_kwargs,
    ):
        """Get projects paginated.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            order_by: API path or query parameter.
            id: API path or query parameter.
            keys: API path or query parameter.
            query: API path or query parameter.
            type_key: API path or query parameter.
            category_id: API path or query parameter.
            action: API path or query parameter.
            expand: API path or query parameter.
            status: API path or query parameter.
            properties: API path or query parameter.
            property_query: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("project/search", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "orderBy": order_by,
            "id": id,
            "keys": keys,
            "query": query,
            "typeKey": type_key,
            "categoryId": category_id,
            "action": action,
            "expand": expand,
            "status": status,
            "properties": properties,
            "propertyQuery": property_query,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_all_project_types(self, data=None, **request_kwargs):
        """Get all project types.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("project/type", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_all_accessible_project_types(self, data=None, **request_kwargs):
        """Get licensed project types.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("project/type/accessible", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_project_type_by_key(self, project_type_key, data=None, **request_kwargs):
        """Get project type by key.

        Args:
            project_type_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"project/type/{project_type_key}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_accessible_project_type_by_key(self, project_type_key, data=None, **request_kwargs):
        """Get accessible project type by key.

        Args:
            project_type_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/type/{project_type_key}/accessible", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_project(self, project_id_or_key, enable_undo=None, data=None, **request_kwargs):
        """Delete project.

        Args:
            project_id_or_key: API path or query parameter.
            enable_undo: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"project/{project_id_or_key}", api_root="rest/api", api_version=self.api_version)
        params = {"enableUndo": enable_undo}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_project(self, project_id_or_key, expand=None, properties=None, data=None, **request_kwargs):
        """Get project.

        Args:
            project_id_or_key: API path or query parameter.
            expand: API path or query parameter.
            properties: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"project/{project_id_or_key}", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand, "properties": properties}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_project(self, project_id_or_key, expand=None, data=None, **request_kwargs):
        """Update project.

        Args:
            project_id_or_key: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"project/{project_id_or_key}", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(url, params=params, data=data, **request_kwargs)

    def archive_project(self, project_id_or_key, data=None, **request_kwargs):
        """Archive project.

        Args:
            project_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/archive", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def update_project_avatar(self, project_id_or_key, data=None, **request_kwargs):
        """Set project avatar.

        Args:
            project_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/avatar", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_project_avatar(self, project_id_or_key, id, data=None, **request_kwargs):
        """Delete project avatar.

        Args:
            project_id_or_key: API path or query parameter.
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/avatar/{id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def create_project_avatar(self, project_id_or_key, x=None, y=None, size=None, data=None, **request_kwargs):
        """Load project avatar.

        Args:
            project_id_or_key: API path or query parameter.
            x: API path or query parameter.
            y: API path or query parameter.
            size: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/avatar2", api_root="rest/api", api_version=self.api_version
        )
        params = {"x": x, "y": y, "size": size}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_all_project_avatars(self, project_id_or_key, data=None, **request_kwargs):
        """Get all project avatars.

        Args:
            project_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/avatars", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_project_classification_config(self, project_id_or_key, data=None, **request_kwargs):
        """Get the classification configuration for a project.

        Args:
            project_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/classification-config", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def remove_default_project_classification(self, project_id_or_key, data=None, **request_kwargs):
        """Remove the default data classification level from a project.

        Args:
            project_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/classification-level/default",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_default_project_classification(self, project_id_or_key, data=None, **request_kwargs):
        """Get the default data classification level of a project.

        Args:
            project_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/classification-level/default",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_default_project_classification(self, project_id_or_key, data=None, **request_kwargs):
        """Update the default data classification level of a project.

        Args:
            project_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/classification-level/default",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_project_components_paginated(
        self,
        project_id_or_key,
        start_at=None,
        max_results=None,
        order_by=None,
        component_source=None,
        query=None,
        data=None,
        **request_kwargs,
    ):
        """Get project components paginated.

        Args:
            project_id_or_key: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            order_by: API path or query parameter.
            component_source: API path or query parameter.
            query: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/component", api_root="rest/api", api_version=self.api_version
        )
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "orderBy": order_by,
            "componentSource": component_source,
            "query": query,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_project_components(self, project_id_or_key, component_source=None, data=None, **request_kwargs):
        """Get project components.

        Args:
            project_id_or_key: API path or query parameter.
            component_source: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/components", api_root="rest/api", api_version=self.api_version
        )
        params = {"componentSource": component_source}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_project_asynchronously(self, project_id_or_key, data=None, **request_kwargs):
        """Delete project asynchronously.

        Args:
            project_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/delete", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_features_for_project(self, project_id_or_key, data=None, **request_kwargs):
        """Get project features.

        Args:
            project_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/features", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def toggle_feature_for_project(self, project_id_or_key, feature_key, data=None, **request_kwargs):
        """Set project feature state.

        Args:
            project_id_or_key: API path or query parameter.
            feature_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/features/{feature_key}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_project_property_keys(self, project_id_or_key, data=None, **request_kwargs):
        """Get project property keys.

        Args:
            project_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/properties", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_project_property(self, project_id_or_key, property_key, data=None, **request_kwargs):
        """Delete project property.

        Args:
            project_id_or_key: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/properties/{property_key}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_project_property(self, project_id_or_key, property_key, data=None, **request_kwargs):
        """Get project property.

        Args:
            project_id_or_key: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/properties/{property_key}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_project_property(self, project_id_or_key, property_key, data=None, **request_kwargs):
        """Set project property.

        Args:
            project_id_or_key: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/properties/{property_key}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def restore(self, project_id_or_key, data=None, **request_kwargs):
        """Restore deleted or archived project.

        Args:
            project_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/restore", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_project_roles(self, project_id_or_key, data=None, **request_kwargs):
        """Get project roles for project.

        Args:
            project_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"project/{project_id_or_key}/role", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_actor(self, project_id_or_key, id, user=None, group=None, group_id=None, data=None, **request_kwargs):
        """Delete actors from project role.

        Args:
            project_id_or_key: API path or query parameter.
            id: API path or query parameter.
            user: API path or query parameter.
            group: API path or query parameter.
            group_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/role/{id}", api_root="rest/api", api_version=self.api_version
        )
        params = {"user": user, "group": group, "groupId": group_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_project_role(self, project_id_or_key, id, exclude_inactive_users=None, data=None, **request_kwargs):
        """Get project role for project.

        Args:
            project_id_or_key: API path or query parameter.
            id: API path or query parameter.
            exclude_inactive_users: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/role/{id}", api_root="rest/api", api_version=self.api_version
        )
        params = {"excludeInactiveUsers": exclude_inactive_users}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def add_actor_users(self, project_id_or_key, id, data=None, **request_kwargs):
        """Add actors to project role.

        Args:
            project_id_or_key: API path or query parameter.
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/role/{id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def set_actors(self, project_id_or_key, id, data=None, **request_kwargs):
        """Set actors for project role.

        Args:
            project_id_or_key: API path or query parameter.
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/role/{id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_project_role_details(
        self,
        project_id_or_key,
        current_member=None,
        exclude_connect_addons=None,
        exclude_other_service_roles=None,
        data=None,
        **request_kwargs,
    ):
        """Get project role details.

        Args:
            project_id_or_key: API path or query parameter.
            current_member: API path or query parameter.
            exclude_connect_addons: API path or query parameter.
            exclude_other_service_roles: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/roledetails", api_root="rest/api", api_version=self.api_version
        )
        params = {
            "currentMember": current_member,
            "excludeConnectAddons": exclude_connect_addons,
            "excludeOtherServiceRoles": exclude_other_service_roles,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_all_statuses(self, project_id_or_key, data=None, **request_kwargs):
        """Get all statuses for project.

        Args:
            project_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/statuses", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_project_versions_paginated(
        self,
        project_id_or_key,
        start_at=None,
        max_results=None,
        order_by=None,
        query=None,
        status=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get project versions paginated.

        Args:
            project_id_or_key: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            order_by: API path or query parameter.
            query: API path or query parameter.
            status: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/version", api_root="rest/api", api_version=self.api_version
        )
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "orderBy": order_by,
            "query": query,
            "status": status,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_project_versions(self, project_id_or_key, expand=None, data=None, **request_kwargs):
        """Get project versions.

        Args:
            project_id_or_key: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_id_or_key}/versions", api_root="rest/api", api_version=self.api_version
        )
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_project_email(self, project_id, data=None, **request_kwargs):
        """Get project's sender email.

        Args:
            project_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"project/{project_id}/email", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_project_email(self, project_id, data=None, **request_kwargs):
        """Set project's sender email.

        Args:
            project_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"project/{project_id}/email", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_hierarchy(self, project_id, data=None, **request_kwargs):
        """Get project issue type hierarchy.

        Args:
            project_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"project/{project_id}/hierarchy", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_project_issue_security_scheme(self, project_key_or_id, data=None, **request_kwargs):
        """Get project issue security scheme.

        Args:
            project_key_or_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_key_or_id}/issuesecuritylevelscheme", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_notification_scheme_for_project(self, project_key_or_id, expand=None, data=None, **request_kwargs):
        """Get project notification scheme.

        Args:
            project_key_or_id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_key_or_id}/notificationscheme", api_root="rest/api", api_version=self.api_version
        )
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_assigned_permission_scheme(self, project_key_or_id, expand=None, data=None, **request_kwargs):
        """Get assigned permission scheme.

        Args:
            project_key_or_id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_key_or_id}/permissionscheme", api_root="rest/api", api_version=self.api_version
        )
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def assign_permission_scheme(self, project_key_or_id, expand=None, data=None, **request_kwargs):
        """Assign permission scheme.

        Args:
            project_key_or_id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_key_or_id}/permissionscheme", api_root="rest/api", api_version=self.api_version
        )
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_security_levels_for_project(self, project_key_or_id, data=None, **request_kwargs):
        """Get project issue security levels.

        Args:
            project_key_or_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"project/{project_key_or_id}/securitylevel", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_all_project_categories(self, data=None, **request_kwargs):
        """Get all project categories.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("projectCategory", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_project_category(self, data=None, **request_kwargs):
        """Create project category.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("projectCategory", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def remove_project_category(self, id, data=None, **request_kwargs):
        """Delete project category.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"projectCategory/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_project_category_by_id(self, id, data=None, **request_kwargs):
        """Get project category by ID.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"projectCategory/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_project_category(self, id, data=None, **request_kwargs):
        """Update project category.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"projectCategory/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_project_fields(
        self,
        start_at=None,
        max_results=None,
        project_id=None,
        work_type_id=None,
        field_id=None,
        data=None,
        **request_kwargs,
    ):
        """Get fields for projects.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            project_id: API path or query parameter.
            work_type_id: API path or query parameter.
            field_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("projects/fields", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "projectId": project_id,
            "workTypeId": work_type_id,
            "fieldId": field_id,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def validate_project_key(self, key=None, data=None, **request_kwargs):
        """Validate project key.

        Args:
            key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("projectvalidate/key", api_root="rest/api", api_version=self.api_version)
        params = {"key": key}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_valid_project_key(self, key=None, data=None, **request_kwargs):
        """Get valid project key.

        Args:
            key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("projectvalidate/validProjectKey", api_root="rest/api", api_version=self.api_version)
        params = {"key": key}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_valid_project_name(self, name=None, data=None, **request_kwargs):
        """Get valid project name.

        Args:
            name: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("projectvalidate/validProjectName", api_root="rest/api", api_version=self.api_version)
        params = {"name": name}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def redact(self, data=None, **request_kwargs):
        """Redact.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("redact", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_redaction_status(self, job_id, data=None, **request_kwargs):
        """Get redaction status.

        Args:
            job_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"redact/status/{job_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_resolutions(self, data=None, **request_kwargs):
        """Get resolutions.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("resolution", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_resolution(self, data=None, **request_kwargs):
        """Create resolution.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("resolution", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def set_default_resolution(self, data=None, **request_kwargs):
        """Set default resolution.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("resolution/default", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def move_resolutions(self, data=None, **request_kwargs):
        """Move resolutions.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("resolution/move", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def search_resolutions(
        self, start_at=None, max_results=None, id=None, only_default=None, data=None, **request_kwargs
    ):
        """Search resolutions.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            id: API path or query parameter.
            only_default: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("resolution/search", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results, "id": id, "onlyDefault": only_default}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_resolution(self, id, replace_with=None, data=None, **request_kwargs):
        """Delete resolution.

        Args:
            id: API path or query parameter.
            replace_with: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"resolution/{id}", api_root="rest/api", api_version=self.api_version)
        params = {"replaceWith": replace_with}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_resolution(self, id, data=None, **request_kwargs):
        """Get resolution.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"resolution/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_resolution(self, id, data=None, **request_kwargs):
        """Update resolution.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"resolution/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_all_project_roles(self, data=None, **request_kwargs):
        """Get all project roles.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("role", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_project_role(self, data=None, **request_kwargs):
        """Create project role.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("role", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_project_role(self, id, swap=None, data=None, **request_kwargs):
        """Delete project role.

        Args:
            id: API path or query parameter.
            swap: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"role/{id}", api_root="rest/api", api_version=self.api_version)
        params = {"swap": swap}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_project_role_by_id(self, id, data=None, **request_kwargs):
        """Get project role by ID.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"role/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def partial_update_project_role(self, id, data=None, **request_kwargs):
        """Partial update project role.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"role/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def fully_update_project_role(self, id, data=None, **request_kwargs):
        """Fully update project role.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"role/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_project_role_actors_from_role(
        self, id, user=None, group_id=None, group=None, data=None, **request_kwargs
    ):
        """Delete default actors from project role.

        Args:
            id: API path or query parameter.
            user: API path or query parameter.
            group_id: API path or query parameter.
            group: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"role/{id}/actors", api_root="rest/api", api_version=self.api_version)
        params = {"user": user, "groupId": group_id, "group": group}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_project_role_actors_for_role(self, id, data=None, **request_kwargs):
        """Get default actors for project role.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"role/{id}/actors", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def add_project_role_actors_to_role(self, id, data=None, **request_kwargs):
        """Add default actors to project role.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"role/{id}/actors", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_screens(
        self,
        start_at=None,
        max_results=None,
        id=None,
        query_string=None,
        scope=None,
        order_by=None,
        data=None,
        **request_kwargs,
    ):
        """Get screens.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            id: API path or query parameter.
            query_string: API path or query parameter.
            scope: API path or query parameter.
            order_by: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("screens", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "id": id,
            "queryString": query_string,
            "scope": scope,
            "orderBy": order_by,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_screen(self, data=None, **request_kwargs):
        """Create screen.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("screens", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def add_field_to_default_screen(self, field_id, data=None, **request_kwargs):
        """Add field to default screen.

        Args:
            field_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"screens/addToDefault/{field_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_bulk_screen_tabs(
        self, screen_id=None, tab_id=None, start_at=None, max_result=None, data=None, **request_kwargs
    ):
        """Get bulk screen tabs.

        Args:
            screen_id: API path or query parameter.
            tab_id: API path or query parameter.
            start_at: API path or query parameter.
            max_result: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("screens/tabs", api_root="rest/api", api_version=self.api_version)
        params = {"screenId": screen_id, "tabId": tab_id, "startAt": start_at, "maxResult": max_result}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_screen(self, screen_id, data=None, **request_kwargs):
        """Delete screen.

        Args:
            screen_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"screens/{screen_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def update_screen(self, screen_id, data=None, **request_kwargs):
        """Update screen.

        Args:
            screen_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"screens/{screen_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_available_screen_fields(self, screen_id, data=None, **request_kwargs):
        """Get available screen fields.

        Args:
            screen_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"screens/{screen_id}/availableFields", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_all_screen_tabs(self, screen_id, project_key=None, data=None, **request_kwargs):
        """Get all screen tabs.

        Args:
            screen_id: API path or query parameter.
            project_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"screens/{screen_id}/tabs", api_root="rest/api", api_version=self.api_version)
        params = {"projectKey": project_key}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def add_screen_tab(self, screen_id, data=None, **request_kwargs):
        """Create screen tab.

        Args:
            screen_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"screens/{screen_id}/tabs", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_screen_tab(self, screen_id, tab_id, data=None, **request_kwargs):
        """Delete screen tab.

        Args:
            screen_id: API path or query parameter.
            tab_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"screens/{screen_id}/tabs/{tab_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def rename_screen_tab(self, screen_id, tab_id, data=None, **request_kwargs):
        """Update screen tab.

        Args:
            screen_id: API path or query parameter.
            tab_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"screens/{screen_id}/tabs/{tab_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_all_screen_tab_fields(self, screen_id, tab_id, project_key=None, data=None, **request_kwargs):
        """Get all screen tab fields.

        Args:
            screen_id: API path or query parameter.
            tab_id: API path or query parameter.
            project_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"screens/{screen_id}/tabs/{tab_id}/fields", api_root="rest/api", api_version=self.api_version
        )
        params = {"projectKey": project_key}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def add_screen_tab_field(self, screen_id, tab_id, skip_field_association=None, data=None, **request_kwargs):
        """Add screen tab field.

        Args:
            screen_id: API path or query parameter.
            tab_id: API path or query parameter.
            skip_field_association: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"screens/{screen_id}/tabs/{tab_id}/fields", api_root="rest/api", api_version=self.api_version
        )
        params = {"skipFieldAssociation": skip_field_association}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def remove_screen_tab_field(self, screen_id, tab_id, id, data=None, **request_kwargs):
        """Remove screen tab field.

        Args:
            screen_id: API path or query parameter.
            tab_id: API path or query parameter.
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"screens/{screen_id}/tabs/{tab_id}/fields/{id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def move_screen_tab_field(self, screen_id, tab_id, id, data=None, **request_kwargs):
        """Move screen tab field.

        Args:
            screen_id: API path or query parameter.
            tab_id: API path or query parameter.
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"screens/{screen_id}/tabs/{tab_id}/fields/{id}/move", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def move_screen_tab(self, screen_id, tab_id, pos, data=None, **request_kwargs):
        """Move screen tab.

        Args:
            screen_id: API path or query parameter.
            tab_id: API path or query parameter.
            pos: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"screens/{screen_id}/tabs/{tab_id}/move/{pos}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_screen_schemes(
        self,
        start_at=None,
        max_results=None,
        id=None,
        expand=None,
        query_string=None,
        order_by=None,
        data=None,
        **request_kwargs,
    ):
        """Get screen schemes.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            id: API path or query parameter.
            expand: API path or query parameter.
            query_string: API path or query parameter.
            order_by: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("screenscheme", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "id": id,
            "expand": expand,
            "queryString": query_string,
            "orderBy": order_by,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_screen_scheme(self, data=None, **request_kwargs):
        """Create screen scheme.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("screenscheme", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_screen_scheme(self, screen_scheme_id, data=None, **request_kwargs):
        """Delete screen scheme.

        Args:
            screen_scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"screenscheme/{screen_scheme_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def update_screen_scheme(self, screen_scheme_id, data=None, **request_kwargs):
        """Update screen scheme.

        Args:
            screen_scheme_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"screenscheme/{screen_scheme_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def search_for_issues_using_jql(
        self,
        jql=None,
        start_at=None,
        max_results=None,
        validate_query=None,
        fields=None,
        expand=None,
        properties=None,
        fields_by_keys=None,
        fail_fast=None,
        data=None,
        **request_kwargs,
    ):
        """Currently being removed. Search for issues using JQL (GET).

        Args:
            jql: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            validate_query: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            properties: API path or query parameter.
            fields_by_keys: API path or query parameter.
            fail_fast: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("search", api_root="rest/api", api_version=self.api_version)
        params = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results,
            "validateQuery": validate_query,
            "fields": fields,
            "expand": expand,
            "properties": properties,
            "fieldsByKeys": fields_by_keys,
            "failFast": fail_fast,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def search_for_issues_using_jql_post(self, data=None, **request_kwargs):
        """Currently being removed. Search for issues using JQL (POST).

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("search", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def count_issues(self, data=None, **request_kwargs):
        """Count issues using JQL.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("search/approximate-count", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def search_and_reconsile_issues_using_jql(
        self,
        jql=None,
        next_page_token=None,
        max_results=None,
        fields=None,
        expand=None,
        properties=None,
        fields_by_keys=None,
        fail_fast=None,
        reconcile_issues=None,
        data=None,
        **request_kwargs,
    ):
        """Search for issues using JQL enhanced search (GET).

        Args:
            jql: API path or query parameter.
            next_page_token: API path or query parameter.
            max_results: API path or query parameter.
            fields: API path or query parameter.
            expand: API path or query parameter.
            properties: API path or query parameter.
            fields_by_keys: API path or query parameter.
            fail_fast: API path or query parameter.
            reconcile_issues: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("search/jql", api_root="rest/api", api_version=self.api_version)
        params = {
            "jql": jql,
            "nextPageToken": next_page_token,
            "maxResults": max_results,
            "fields": fields,
            "expand": expand,
            "properties": properties,
            "fieldsByKeys": fields_by_keys,
            "failFast": fail_fast,
            "reconcileIssues": reconcile_issues,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def search_and_reconsile_issues_using_jql_post(self, data=None, **request_kwargs):
        """Search for issues using JQL enhanced search (POST).

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("search/jql", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_issue_security_level(self, id, data=None, **request_kwargs):
        """Get issue security level.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"securitylevel/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_server_info(self, data=None, **request_kwargs):
        """Get Jira instance info.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("serverInfo", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_issue_navigator_default_columns(self, data=None, **request_kwargs):
        """Get issue navigator default columns.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("settings/columns", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_issue_navigator_default_columns(self, data=None, **request_kwargs):
        """Set issue navigator default columns.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("settings/columns", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_statuses(self, data=None, **request_kwargs):
        """Get all statuses.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("status", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_status(self, id_or_name, data=None, **request_kwargs):
        """Get status.

        Args:
            id_or_name: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"status/{id_or_name}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_status_categories(self, data=None, **request_kwargs):
        """Get all status categories.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("statuscategory", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_status_category(self, id_or_key, data=None, **request_kwargs):
        """Get status category.

        Args:
            id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"statuscategory/{id_or_key}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_statuses_by_id(self, id=None, data=None, **request_kwargs):
        """Bulk delete Statuses.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("statuses", api_root="rest/api", api_version=self.api_version)
        params = {"id": id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_statuses_by_id(self, id=None, data=None, **request_kwargs):
        """Bulk get statuses.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("statuses", api_root="rest/api", api_version=self.api_version)
        params = {"id": id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_statuses(self, data=None, **request_kwargs):
        """Bulk create statuses.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("statuses", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def update_statuses(self, data=None, **request_kwargs):
        """Bulk update statuses.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("statuses", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_statuses_by_name(self, name=None, project_id=None, data=None, **request_kwargs):
        """Bulk get statuses by name.

        Args:
            name: API path or query parameter.
            project_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("statuses/byNames", api_root="rest/api", api_version=self.api_version)
        params = {"name": name, "projectId": project_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def search(
        self,
        project_id=None,
        start_at=None,
        max_results=None,
        search_string=None,
        status_category=None,
        include_global_statuses=None,
        data=None,
        **request_kwargs,
    ):
        """Search statuses paginated.

        Args:
            project_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            search_string: API path or query parameter.
            status_category: API path or query parameter.
            include_global_statuses: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("statuses/search", api_root="rest/api", api_version=self.api_version)
        params = {
            "projectId": project_id,
            "startAt": start_at,
            "maxResults": max_results,
            "searchString": search_string,
            "statusCategory": status_category,
            "includeGlobalStatuses": include_global_statuses,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_project_issue_type_usages_for_status(
        self, status_id, project_id, next_page_token=None, max_results=None, data=None, **request_kwargs
    ):
        """Get issue type usages by status and project.

        Args:
            status_id: API path or query parameter.
            project_id: API path or query parameter.
            next_page_token: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"statuses/{status_id}/project/{project_id}/issueTypeUsages",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = {"nextPageToken": next_page_token, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_project_usages_for_status(
        self, status_id, next_page_token=None, max_results=None, data=None, **request_kwargs
    ):
        """Get project usages by status.

        Args:
            status_id: API path or query parameter.
            next_page_token: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"statuses/{status_id}/projectUsages", api_root="rest/api", api_version=self.api_version
        )
        params = {"nextPageToken": next_page_token, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_workflow_usages_for_status(
        self, status_id, next_page_token=None, max_results=None, data=None, **request_kwargs
    ):
        """Get workflow usages by status.

        Args:
            status_id: API path or query parameter.
            next_page_token: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"statuses/{status_id}/workflowUsages", api_root="rest/api", api_version=self.api_version
        )
        params = {"nextPageToken": next_page_token, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_task(self, task_id, data=None, **request_kwargs):
        """Get task.

        Args:
            task_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"task/{task_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def cancel_task(self, task_id, data=None, **request_kwargs):
        """Cancel task.

        Args:
            task_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"task/{task_id}/cancel", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_ui_modifications(self, start_at=None, max_results=None, expand=None, data=None, **request_kwargs):
        """Get UI modifications.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("uiModifications", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results, "expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_ui_modification(self, data=None, **request_kwargs):
        """Create UI modification.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("uiModifications", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_ui_modification(self, ui_modification_id, data=None, **request_kwargs):
        """Delete UI modification.

        Args:
            ui_modification_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"uiModifications/{ui_modification_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def update_ui_modification(self, ui_modification_id, data=None, **request_kwargs):
        """Update UI modification.

        Args:
            ui_modification_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"uiModifications/{ui_modification_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_avatars(self, type, entity_id, data=None, **request_kwargs):
        """Get avatars.

        Args:
            type: API path or query parameter.
            entity_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"universal_avatar/type/{type}/owner/{entity_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def store_avatar(self, type, entity_id, x=None, y=None, size=None, data=None, **request_kwargs):
        """Load avatar.

        Args:
            type: API path or query parameter.
            entity_id: API path or query parameter.
            x: API path or query parameter.
            y: API path or query parameter.
            size: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"universal_avatar/type/{type}/owner/{entity_id}", api_root="rest/api", api_version=self.api_version
        )
        params = {"x": x, "y": y, "size": size}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_avatar(self, type, owning_object_id, id, data=None, **request_kwargs):
        """Delete avatar.

        Args:
            type: API path or query parameter.
            owning_object_id: API path or query parameter.
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"universal_avatar/type/{type}/owner/{owning_object_id}/avatar/{id}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_avatar_image_by_type(self, type, size=None, format=None, data=None, **request_kwargs):
        """Get avatar image by type.

        Args:
            type: API path or query parameter.
            size: API path or query parameter.
            format: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"universal_avatar/view/type/{type}", api_root="rest/api", api_version=self.api_version)
        params = {"size": size, "format": format}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_avatar_image_by_id(self, type, id, size=None, format=None, data=None, **request_kwargs):
        """Get avatar image by ID.

        Args:
            type: API path or query parameter.
            id: API path or query parameter.
            size: API path or query parameter.
            format: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"universal_avatar/view/type/{type}/avatar/{id}", api_root="rest/api", api_version=self.api_version
        )
        params = {"size": size, "format": format}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_avatar_image_by_owner(self, type, entity_id, size=None, format=None, data=None, **request_kwargs):
        """Get avatar image by owner.

        Args:
            type: API path or query parameter.
            entity_id: API path or query parameter.
            size: API path or query parameter.
            format: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"universal_avatar/view/type/{type}/owner/{entity_id}", api_root="rest/api", api_version=self.api_version
        )
        params = {"size": size, "format": format}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def remove_user(self, account_id=None, username=None, key=None, data=None, **request_kwargs):
        """Delete user.

        Args:
            account_id: API path or query parameter.
            username: API path or query parameter.
            key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user", api_root="rest/api", api_version=self.api_version)
        params = {"accountId": account_id, "username": username, "key": key}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_user(self, account_id=None, username=None, key=None, expand=None, data=None, **request_kwargs):
        """Get user.

        Args:
            account_id: API path or query parameter.
            username: API path or query parameter.
            key: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user", api_root="rest/api", api_version=self.api_version)
        params = {"accountId": account_id, "username": username, "key": key, "expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_user(self, data=None, **request_kwargs):
        """Create user.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def find_bulk_assignable_users(
        self,
        query=None,
        username=None,
        account_id=None,
        project_keys=None,
        start_at=None,
        max_results=None,
        data=None,
        **request_kwargs,
    ):
        """Find users assignable to projects.

        Args:
            query: API path or query parameter.
            username: API path or query parameter.
            account_id: API path or query parameter.
            project_keys: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user/assignable/multiProjectSearch", api_root="rest/api", api_version=self.api_version)
        params = {
            "query": query,
            "username": username,
            "accountId": account_id,
            "projectKeys": project_keys,
            "startAt": start_at,
            "maxResults": max_results,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def find_assignable_users(
        self,
        query=None,
        session_id=None,
        username=None,
        account_id=None,
        project=None,
        issue_key=None,
        issue_id=None,
        start_at=None,
        max_results=None,
        action_descriptor_id=None,
        recommend=None,
        account_type=None,
        app_type=None,
        data=None,
        **request_kwargs,
    ):
        """Find users assignable to issues.

        Args:
            query: API path or query parameter.
            session_id: API path or query parameter.
            username: API path or query parameter.
            account_id: API path or query parameter.
            project: API path or query parameter.
            issue_key: API path or query parameter.
            issue_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            action_descriptor_id: API path or query parameter.
            recommend: API path or query parameter.
            account_type: API path or query parameter.
            app_type: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user/assignable/search", api_root="rest/api", api_version=self.api_version)
        params = {
            "query": query,
            "sessionId": session_id,
            "username": username,
            "accountId": account_id,
            "project": project,
            "issueKey": issue_key,
            "issueId": issue_id,
            "startAt": start_at,
            "maxResults": max_results,
            "actionDescriptorId": action_descriptor_id,
            "recommend": recommend,
            "accountType": account_type,
            "appType": app_type,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def bulk_get_users(
        self, start_at=None, max_results=None, username=None, key=None, account_id=None, data=None, **request_kwargs
    ):
        """Bulk get users.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            username: API path or query parameter.
            key: API path or query parameter.
            account_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user/bulk", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "username": username,
            "key": key,
            "accountId": account_id,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def bulk_get_users_migration(
        self, start_at=None, max_results=None, username=None, key=None, data=None, **request_kwargs
    ):
        """Get account IDs for users.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            username: API path or query parameter.
            key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user/bulk/migration", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results, "username": username, "key": key}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def reset_user_columns(self, account_id=None, username=None, data=None, **request_kwargs):
        """Reset user default columns.

        Args:
            account_id: API path or query parameter.
            username: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user/columns", api_root="rest/api", api_version=self.api_version)
        params = {"accountId": account_id, "username": username}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_user_default_columns(self, account_id=None, username=None, data=None, **request_kwargs):
        """Get user default columns.

        Args:
            account_id: API path or query parameter.
            username: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user/columns", api_root="rest/api", api_version=self.api_version)
        params = {"accountId": account_id, "username": username}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_user_columns(self, account_id=None, data=None, **request_kwargs):
        """Set user default columns.

        Args:
            account_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user/columns", api_root="rest/api", api_version=self.api_version)
        params = {"accountId": account_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_user_email(self, account_id=None, data=None, **request_kwargs):
        """Get user email.

        Args:
            account_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user/email", api_root="rest/api", api_version=self.api_version)
        params = {"accountId": account_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_user_email_bulk(self, account_id=None, data=None, **request_kwargs):
        """Get user email bulk.

        Args:
            account_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user/email/bulk", api_root="rest/api", api_version=self.api_version)
        params = {"accountId": account_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_user_groups(self, account_id=None, username=None, key=None, data=None, **request_kwargs):
        """Get user groups.

        Args:
            account_id: API path or query parameter.
            username: API path or query parameter.
            key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user/groups", api_root="rest/api", api_version=self.api_version)
        params = {"accountId": account_id, "username": username, "key": key}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def find_users_with_all_permissions(
        self,
        query=None,
        username=None,
        account_id=None,
        permissions=None,
        issue_key=None,
        project_key=None,
        start_at=None,
        max_results=None,
        data=None,
        **request_kwargs,
    ):
        """Find users with permissions.

        Args:
            query: API path or query parameter.
            username: API path or query parameter.
            account_id: API path or query parameter.
            permissions: API path or query parameter.
            issue_key: API path or query parameter.
            project_key: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user/permission/search", api_root="rest/api", api_version=self.api_version)
        params = {
            "query": query,
            "username": username,
            "accountId": account_id,
            "permissions": permissions,
            "issueKey": issue_key,
            "projectKey": project_key,
            "startAt": start_at,
            "maxResults": max_results,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def find_users_for_picker(
        self,
        query=None,
        max_results=None,
        show_avatar=None,
        exclude=None,
        exclude_account_ids=None,
        avatar_size=None,
        exclude_connect_users=None,
        data=None,
        **request_kwargs,
    ):
        """Find users for picker.

        Args:
            query: API path or query parameter.
            max_results: API path or query parameter.
            show_avatar: API path or query parameter.
            exclude: API path or query parameter.
            exclude_account_ids: API path or query parameter.
            avatar_size: API path or query parameter.
            exclude_connect_users: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user/picker", api_root="rest/api", api_version=self.api_version)
        params = {
            "query": query,
            "maxResults": max_results,
            "showAvatar": show_avatar,
            "exclude": exclude,
            "excludeAccountIds": exclude_account_ids,
            "avatarSize": avatar_size,
            "excludeConnectUsers": exclude_connect_users,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_user_property_keys(self, account_id=None, user_key=None, username=None, data=None, **request_kwargs):
        """Get user property keys.

        Args:
            account_id: API path or query parameter.
            user_key: API path or query parameter.
            username: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user/properties", api_root="rest/api", api_version=self.api_version)
        params = {"accountId": account_id, "userKey": user_key, "username": username}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_user_property(
        self, property_key, account_id=None, user_key=None, username=None, data=None, **request_kwargs
    ):
        """Delete user property.

        Args:
            property_key: API path or query parameter.
            account_id: API path or query parameter.
            user_key: API path or query parameter.
            username: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"user/properties/{property_key}", api_root="rest/api", api_version=self.api_version)
        params = {"accountId": account_id, "userKey": user_key, "username": username}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_user_property(
        self, property_key, account_id=None, user_key=None, username=None, data=None, **request_kwargs
    ):
        """Get user property.

        Args:
            property_key: API path or query parameter.
            account_id: API path or query parameter.
            user_key: API path or query parameter.
            username: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"user/properties/{property_key}", api_root="rest/api", api_version=self.api_version)
        params = {"accountId": account_id, "userKey": user_key, "username": username}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_user_property(
        self, property_key, account_id=None, user_key=None, username=None, data=None, **request_kwargs
    ):
        """Set user property.

        Args:
            property_key: API path or query parameter.
            account_id: API path or query parameter.
            user_key: API path or query parameter.
            username: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"user/properties/{property_key}", api_root="rest/api", api_version=self.api_version)
        params = {"accountId": account_id, "userKey": user_key, "username": username}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(url, params=params, data=data, **request_kwargs)

    def find_users(
        self,
        query=None,
        username=None,
        account_id=None,
        start_at=None,
        max_results=None,
        property=None,
        data=None,
        **request_kwargs,
    ):
        """Find users.

        Args:
            query: API path or query parameter.
            username: API path or query parameter.
            account_id: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            property: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user/search", api_root="rest/api", api_version=self.api_version)
        params = {
            "query": query,
            "username": username,
            "accountId": account_id,
            "startAt": start_at,
            "maxResults": max_results,
            "property": property,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def find_users_by_query(self, query=None, start_at=None, max_results=None, data=None, **request_kwargs):
        """Find users by query.

        Args:
            query: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user/search/query", api_root="rest/api", api_version=self.api_version)
        params = {"query": query, "startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def find_user_keys_by_query(self, query=None, start_at=None, max_result=None, data=None, **request_kwargs):
        """Find user keys by query.

        Args:
            query: API path or query parameter.
            start_at: API path or query parameter.
            max_result: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user/search/query/key", api_root="rest/api", api_version=self.api_version)
        params = {"query": query, "startAt": start_at, "maxResult": max_result}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def find_users_with_browse_permission(
        self,
        query=None,
        username=None,
        account_id=None,
        issue_key=None,
        project_key=None,
        start_at=None,
        max_results=None,
        data=None,
        **request_kwargs,
    ):
        """Find users with browse permission.

        Args:
            query: API path or query parameter.
            username: API path or query parameter.
            account_id: API path or query parameter.
            issue_key: API path or query parameter.
            project_key: API path or query parameter.
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("user/viewissue/search", api_root="rest/api", api_version=self.api_version)
        params = {
            "query": query,
            "username": username,
            "accountId": account_id,
            "issueKey": issue_key,
            "projectKey": project_key,
            "startAt": start_at,
            "maxResults": max_results,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_all_users_default(self, start_at=None, max_results=None, expand=None, data=None, **request_kwargs):
        """Get all users default.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("users", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results, "expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_all_users(self, start_at=None, max_results=None, expand=None, data=None, **request_kwargs):
        """Get all users.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("users/search", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results, "expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_version(self, data=None, **request_kwargs):
        """Create version.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("version", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_version(self, id, move_fix_issues_to=None, move_affected_issues_to=None, data=None, **request_kwargs):
        """Delete version.

        Args:
            id: API path or query parameter.
            move_fix_issues_to: API path or query parameter.
            move_affected_issues_to: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"version/{id}", api_root="rest/api", api_version=self.api_version)
        params = {"moveFixIssuesTo": move_fix_issues_to, "moveAffectedIssuesTo": move_affected_issues_to}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_version(self, id, expand=None, data=None, **request_kwargs):
        """Get version.

        Args:
            id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"version/{id}", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_version(self, id, data=None, **request_kwargs):
        """Update version.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"version/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def merge_versions(self, id, move_issues_to, data=None, **request_kwargs):
        """Merge versions.

        Args:
            id: API path or query parameter.
            move_issues_to: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"version/{id}/mergeto/{move_issues_to}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def move_version(self, id, data=None, **request_kwargs):
        """Move version.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"version/{id}/move", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_version_related_issues(self, id, data=None, **request_kwargs):
        """Get version's related issues count.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"version/{id}/relatedIssueCounts", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_related_work(self, id, data=None, **request_kwargs):
        """Get related work.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"version/{id}/relatedwork", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_related_work(self, id, data=None, **request_kwargs):
        """Create related work.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"version/{id}/relatedwork", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def update_related_work(self, id, data=None, **request_kwargs):
        """Update related work.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"version/{id}/relatedwork", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_and_replace_version(self, id, data=None, **request_kwargs):
        """Delete and replace version.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"version/{id}/removeAndSwap", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_version_unresolved_issues(self, id, data=None, **request_kwargs):
        """Get version's unresolved issues count.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"version/{id}/unresolvedIssueCount", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_related_work(self, version_id, related_work_id, data=None, **request_kwargs):
        """Delete related work.

        Args:
            version_id: API path or query parameter.
            related_work_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"version/{version_id}/relatedwork/{related_work_id}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def delete_webhook_by_id(self, data=None, **request_kwargs):
        """Delete webhooks by ID.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("webhook", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_dynamic_webhooks_for_app(self, start_at=None, max_results=None, data=None, **request_kwargs):
        """Get dynamic webhooks for app.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("webhook", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def register_dynamic_webhooks(self, data=None, **request_kwargs):
        """Register dynamic webhooks.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("webhook", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_failed_webhooks(self, max_results=None, after=None, data=None, **request_kwargs):
        """Get failed webhooks.

        Args:
            max_results: API path or query parameter.
            after: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("webhook/failed", api_root="rest/api", api_version=self.api_version)
        params = {"maxResults": max_results, "after": after}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def refresh_webhooks(self, data=None, **request_kwargs):
        """Extend webhook life.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("webhook/refresh", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def read_workflow_from_history(self, data=None, **request_kwargs):
        """Read workflow version from history.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflow/history", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def list_workflow_history(self, expand=None, data=None, **request_kwargs):
        """List workflow history entries.

        Args:
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflow/history/list", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_workflow_transition_rule_configurations(
        self,
        start_at=None,
        max_results=None,
        types=None,
        keys=None,
        workflow_names=None,
        with_tags=None,
        draft=None,
        expand=None,
        data=None,
        **request_kwargs,
    ):
        """Get workflow transition rule configurations.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            types: API path or query parameter.
            keys: API path or query parameter.
            workflow_names: API path or query parameter.
            with_tags: API path or query parameter.
            draft: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflow/rule/config", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "types": types,
            "keys": keys,
            "workflowNames": workflow_names,
            "withTags": with_tags,
            "draft": draft,
            "expand": expand,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_workflow_transition_rule_configurations(self, data=None, **request_kwargs):
        """Update workflow transition rule configurations.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflow/rule/config", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_workflow_transition_rule_configurations(self, data=None, **request_kwargs):
        """Delete workflow transition rule configurations.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflow/rule/config/delete", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_workflows_paginated(
        self,
        start_at=None,
        max_results=None,
        workflow_name=None,
        expand=None,
        query_string=None,
        order_by=None,
        is_active=None,
        data=None,
        **request_kwargs,
    ):
        """Get workflows paginated.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            workflow_name: API path or query parameter.
            expand: API path or query parameter.
            query_string: API path or query parameter.
            order_by: API path or query parameter.
            is_active: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflow/search", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "workflowName": workflow_name,
            "expand": expand,
            "queryString": query_string,
            "orderBy": order_by,
            "isActive": is_active,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_inactive_workflow(self, entity_id, data=None, **request_kwargs):
        """Delete inactive workflow.

        Args:
            entity_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflow/{entity_id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_workflow_project_issue_type_usages(
        self, workflow_id, project_id, next_page_token=None, max_results=None, data=None, **request_kwargs
    ):
        """Get issue types in a project that are using a given workflow.

        Args:
            workflow_id: API path or query parameter.
            project_id: API path or query parameter.
            next_page_token: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"workflow/{workflow_id}/project/{project_id}/issueTypeUsages",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = {"nextPageToken": next_page_token, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_project_usages_for_workflow(
        self, workflow_id, next_page_token=None, max_results=None, data=None, **request_kwargs
    ):
        """Get projects using a given workflow.

        Args:
            workflow_id: API path or query parameter.
            next_page_token: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"workflow/{workflow_id}/projectUsages", api_root="rest/api", api_version=self.api_version
        )
        params = {"nextPageToken": next_page_token, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_workflow_scheme_usages_for_workflow(
        self, workflow_id, next_page_token=None, max_results=None, data=None, **request_kwargs
    ):
        """Get workflow schemes which are using a given workflow.

        Args:
            workflow_id: API path or query parameter.
            next_page_token: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"workflow/{workflow_id}/workflowSchemes", api_root="rest/api", api_version=self.api_version
        )
        params = {"nextPageToken": next_page_token, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def read_workflows(self, data=None, **request_kwargs):
        """Bulk get workflows.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflows", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def workflow_capabilities(self, workflow_id=None, project_id=None, issue_type_id=None, data=None, **request_kwargs):
        """Get available workflow capabilities.

        Args:
            workflow_id: API path or query parameter.
            project_id: API path or query parameter.
            issue_type_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflows/capabilities", api_root="rest/api", api_version=self.api_version)
        params = {"workflowId": workflow_id, "projectId": project_id, "issueTypeId": issue_type_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_workflows(self, data=None, **request_kwargs):
        """Bulk create workflows.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflows/create", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def validate_create_workflows(self, data=None, **request_kwargs):
        """Validate create workflows.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflows/create/validation", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_default_editor(self, data=None, **request_kwargs):
        """Get the user's default workflow editor.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflows/defaultEditor", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def read_workflow_previews(self, data=None, **request_kwargs):
        """Preview workflow.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflows/preview", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def search_workflows(
        self,
        start_at=None,
        max_results=None,
        expand=None,
        query_string=None,
        order_by=None,
        scope=None,
        is_active=None,
        project_id=None,
        data=None,
        **request_kwargs,
    ):
        """Search workflows.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            expand: API path or query parameter.
            query_string: API path or query parameter.
            order_by: API path or query parameter.
            scope: API path or query parameter.
            is_active: API path or query parameter.
            project_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflows/search", api_root="rest/api", api_version=self.api_version)
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "expand": expand,
            "queryString": query_string,
            "orderBy": order_by,
            "scope": scope,
            "isActive": is_active,
            "projectId": project_id,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_workflows(self, data=None, **request_kwargs):
        """Bulk update workflows.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflows/update", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def validate_update_workflows(self, data=None, **request_kwargs):
        """Validate update workflows.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflows/update/validation", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_all_workflow_schemes(self, start_at=None, max_results=None, data=None, **request_kwargs):
        """Get all workflow schemes.

        Args:
            start_at: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflowscheme", api_root="rest/api", api_version=self.api_version)
        params = {"startAt": start_at, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_workflow_scheme(self, data=None, **request_kwargs):
        """Create workflow scheme.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflowscheme", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_workflow_scheme_project_associations(self, project_id=None, data=None, **request_kwargs):
        """Get workflow scheme project associations.

        Args:
            project_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflowscheme/project", api_root="rest/api", api_version=self.api_version)
        params = {"projectId": project_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def assign_scheme_to_project(self, data=None, **request_kwargs):
        """Assign workflow scheme to project.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflowscheme/project", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def switch_workflow_scheme_for_project(self, data=None, **request_kwargs):
        """Switch workflow scheme for project.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflowscheme/project/switch", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def read_workflow_schemes(self, data=None, **request_kwargs):
        """Bulk get workflow schemes.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflowscheme/read", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def update_schemes(self, data=None, **request_kwargs):
        """Update workflow scheme.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflowscheme/update", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_required_workflow_scheme_mappings(self, data=None, **request_kwargs):
        """Get required status mappings for workflow scheme update.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("workflowscheme/update/mappings", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_workflow_scheme(self, id, data=None, **request_kwargs):
        """Delete workflow scheme.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflowscheme/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_workflow_scheme(self, id, return_draft_if_exists=None, data=None, **request_kwargs):
        """Get workflow scheme.

        Args:
            id: API path or query parameter.
            return_draft_if_exists: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflowscheme/{id}", api_root="rest/api", api_version=self.api_version)
        params = {"returnDraftIfExists": return_draft_if_exists}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_workflow_scheme(self, id, data=None, **request_kwargs):
        """Classic update workflow scheme.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflowscheme/{id}", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def create_workflow_scheme_draft_from_parent(self, id, data=None, **request_kwargs):
        """Create draft workflow scheme.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflowscheme/{id}/createdraft", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_default_workflow(self, id, update_draft_if_needed=None, data=None, **request_kwargs):
        """Delete default workflow.

        Args:
            id: API path or query parameter.
            update_draft_if_needed: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflowscheme/{id}/default", api_root="rest/api", api_version=self.api_version)
        params = {"updateDraftIfNeeded": update_draft_if_needed}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_default_workflow(self, id, return_draft_if_exists=None, data=None, **request_kwargs):
        """Get default workflow.

        Args:
            id: API path or query parameter.
            return_draft_if_exists: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflowscheme/{id}/default", api_root="rest/api", api_version=self.api_version)
        params = {"returnDraftIfExists": return_draft_if_exists}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_default_workflow(self, id, data=None, **request_kwargs):
        """Update default workflow.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflowscheme/{id}/default", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_workflow_scheme_draft(self, id, data=None, **request_kwargs):
        """Delete draft workflow scheme.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflowscheme/{id}/draft", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_workflow_scheme_draft(self, id, data=None, **request_kwargs):
        """Get draft workflow scheme.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflowscheme/{id}/draft", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_workflow_scheme_draft(self, id, data=None, **request_kwargs):
        """Update draft workflow scheme.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflowscheme/{id}/draft", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_draft_default_workflow(self, id, data=None, **request_kwargs):
        """Delete draft default workflow.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflowscheme/{id}/draft/default", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_draft_default_workflow(self, id, data=None, **request_kwargs):
        """Get draft default workflow.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflowscheme/{id}/draft/default", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_draft_default_workflow(self, id, data=None, **request_kwargs):
        """Update draft default workflow.

        Args:
            id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflowscheme/{id}/draft/default", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_workflow_scheme_draft_issue_type(self, id, issue_type, data=None, **request_kwargs):
        """Delete workflow for issue type in draft workflow scheme.

        Args:
            id: API path or query parameter.
            issue_type: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"workflowscheme/{id}/draft/issuetype/{issue_type}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_workflow_scheme_draft_issue_type(self, id, issue_type, data=None, **request_kwargs):
        """Get workflow for issue type in draft workflow scheme.

        Args:
            id: API path or query parameter.
            issue_type: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"workflowscheme/{id}/draft/issuetype/{issue_type}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_workflow_scheme_draft_issue_type(self, id, issue_type, data=None, **request_kwargs):
        """Set workflow for issue type in draft workflow scheme.

        Args:
            id: API path or query parameter.
            issue_type: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"workflowscheme/{id}/draft/issuetype/{issue_type}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def publish_draft_workflow_scheme(self, id, validate_only=None, data=None, **request_kwargs):
        """Publish draft workflow scheme.

        Args:
            id: API path or query parameter.
            validate_only: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflowscheme/{id}/draft/publish", api_root="rest/api", api_version=self.api_version)
        params = {"validateOnly": validate_only}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_draft_workflow_mapping(self, id, workflow_name=None, data=None, **request_kwargs):
        """Delete issue types for workflow in draft workflow scheme.

        Args:
            id: API path or query parameter.
            workflow_name: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"workflowscheme/{id}/draft/workflow", api_root="rest/api", api_version=self.api_version
        )
        params = {"workflowName": workflow_name}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_draft_workflow(self, id, workflow_name=None, data=None, **request_kwargs):
        """Get issue types for workflows in draft workflow scheme.

        Args:
            id: API path or query parameter.
            workflow_name: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"workflowscheme/{id}/draft/workflow", api_root="rest/api", api_version=self.api_version
        )
        params = {"workflowName": workflow_name}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_draft_workflow_mapping(self, id, workflow_name=None, data=None, **request_kwargs):
        """Set issue types for workflow in workflow scheme.

        Args:
            id: API path or query parameter.
            workflow_name: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"workflowscheme/{id}/draft/workflow", api_root="rest/api", api_version=self.api_version
        )
        params = {"workflowName": workflow_name}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_workflow_scheme_issue_type(
        self, id, issue_type, update_draft_if_needed=None, data=None, **request_kwargs
    ):
        """Delete workflow for issue type in workflow scheme.

        Args:
            id: API path or query parameter.
            issue_type: API path or query parameter.
            update_draft_if_needed: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"workflowscheme/{id}/issuetype/{issue_type}", api_root="rest/api", api_version=self.api_version
        )
        params = {"updateDraftIfNeeded": update_draft_if_needed}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_workflow_scheme_issue_type(self, id, issue_type, return_draft_if_exists=None, data=None, **request_kwargs):
        """Get workflow for issue type in workflow scheme.

        Args:
            id: API path or query parameter.
            issue_type: API path or query parameter.
            return_draft_if_exists: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"workflowscheme/{id}/issuetype/{issue_type}", api_root="rest/api", api_version=self.api_version
        )
        params = {"returnDraftIfExists": return_draft_if_exists}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_workflow_scheme_issue_type(self, id, issue_type, data=None, **request_kwargs):
        """Set workflow for issue type in workflow scheme.

        Args:
            id: API path or query parameter.
            issue_type: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"workflowscheme/{id}/issuetype/{issue_type}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def delete_workflow_mapping(self, id, workflow_name=None, update_draft_if_needed=None, data=None, **request_kwargs):
        """Delete issue types for workflow in workflow scheme.

        Args:
            id: API path or query parameter.
            workflow_name: API path or query parameter.
            update_draft_if_needed: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflowscheme/{id}/workflow", api_root="rest/api", api_version=self.api_version)
        params = {"workflowName": workflow_name, "updateDraftIfNeeded": update_draft_if_needed}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_workflow(self, id, workflow_name=None, return_draft_if_exists=None, data=None, **request_kwargs):
        """Get issue types for workflows in workflow scheme.

        Args:
            id: API path or query parameter.
            workflow_name: API path or query parameter.
            return_draft_if_exists: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflowscheme/{id}/workflow", api_root="rest/api", api_version=self.api_version)
        params = {"workflowName": workflow_name, "returnDraftIfExists": return_draft_if_exists}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def update_workflow_mapping(self, id, workflow_name=None, data=None, **request_kwargs):
        """Set issue types for workflow in workflow scheme.

        Args:
            id: API path or query parameter.
            workflow_name: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(f"workflowscheme/{id}/workflow", api_root="rest/api", api_version=self.api_version)
        params = {"workflowName": workflow_name}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_project_usages_for_workflow_scheme(
        self, workflow_scheme_id, next_page_token=None, max_results=None, data=None, **request_kwargs
    ):
        """Get projects which are using a given workflow scheme.

        Args:
            workflow_scheme_id: API path or query parameter.
            next_page_token: API path or query parameter.
            max_results: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"workflowscheme/{workflow_scheme_id}/projectUsages", api_root="rest/api", api_version=self.api_version
        )
        params = {"nextPageToken": next_page_token, "maxResults": max_results}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_ids_of_worklogs_deleted_since(self, since=None, data=None, **request_kwargs):
        """Get IDs of deleted worklogs.

        Args:
            since: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("worklog/deleted", api_root="rest/api", api_version=self.api_version)
        params = {"since": since}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_worklogs_for_ids(self, expand=None, data=None, **request_kwargs):
        """Get worklogs.

        Args:
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("worklog/list", api_root="rest/api", api_version=self.api_version)
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_ids_of_worklogs_modified_since(self, since=None, expand=None, data=None, **request_kwargs):
        """Get IDs of updated worklogs.

        Args:
            since: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("worklog/updated", api_root="rest/api", api_version=self.api_version)
        params = {"since": since, "expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def addon_properties_resource_get_addon_properties_get(self, addon_key, data=None, **request_kwargs):
        """Get app properties.

        Args:
            addon_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"rest/atlassian-connect/1/addons/{addon_key}/properties", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def addon_properties_resource_delete_addon_property_delete(
        self, addon_key, property_key, data=None, **request_kwargs
    ):
        """Delete app property.

        Args:
            addon_key: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"rest/atlassian-connect/1/addons/{addon_key}/properties/{property_key}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def addon_properties_resource_get_addon_property_get(self, addon_key, property_key, data=None, **request_kwargs):
        """Get app property.

        Args:
            addon_key: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"rest/atlassian-connect/1/addons/{addon_key}/properties/{property_key}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def addon_properties_resource_put_addon_property_put(self, addon_key, property_key, data=None, **request_kwargs):
        """Set app property.

        Args:
            addon_key: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"rest/atlassian-connect/1/addons/{addon_key}/properties/{property_key}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def dynamic_modules_resource_remove_modules_delete(self, module_key=None, data=None, **request_kwargs):
        """Remove modules.

        Args:
            module_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            "rest/atlassian-connect/1/app/module/dynamic", api_root="rest/api", api_version=self.api_version
        )
        params = {"moduleKey": module_key}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def dynamic_modules_resource_get_modules_get(self, data=None, **request_kwargs):
        """Get modules.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            "rest/atlassian-connect/1/app/module/dynamic", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def dynamic_modules_resource_register_modules_post(self, data=None, **request_kwargs):
        """Register modules.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            "rest/atlassian-connect/1/app/module/dynamic", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def app_issue_field_value_update_resource_update_issue_fields_put(self, data=None, **request_kwargs):
        """Bulk update custom field value.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            "rest/atlassian-connect/1/migration/field", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def migration_resource_update_entity_properties_value_put(self, entity_type, data=None, **request_kwargs):
        """Bulk update entity properties.

        Args:
            entity_type: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"rest/atlassian-connect/1/migration/properties/{entity_type}",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def migration_resource_workflow_rule_search_post(self, data=None, **request_kwargs):
        """Get workflow transition rule configurations.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            "rest/atlassian-connect/1/migration/workflow/rule/search",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def connect_to_forge_migration_fetch_task_resource_fetch_migration_task_get(
        self, connect_key, jira_issue_fields_key, data=None, **request_kwargs
    ):
        """Get Connect issue field migration task.

        Args:
            connect_key: API path or query parameter.
            jira_issue_fields_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"rest/atlassian-connect/1/migration/{connect_key}/{jira_issue_fields_key}/task",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def connect_to_forge_migration_task_submission_resource_submit_task_post(
        self, connect_key, jira_issue_fields_key, retrigger_completed_migration=None, data=None, **request_kwargs
    ):
        """Submit Connect issue field migration task.

        Args:
            connect_key: API path or query parameter.
            jira_issue_fields_key: API path or query parameter.
            retrigger_completed_migration: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"rest/atlassian-connect/1/migration/{connect_key}/{jira_issue_fields_key}/task",
            api_root="rest/api",
            api_version=self.api_version,
        )
        params = {"retriggerCompletedMigration": retrigger_completed_migration}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def service_registry_resource_services_get(self, service_ids=None, data=None, **request_kwargs):
        """Retrieve the attributes of service registries.

        Args:
            service_ids: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            "rest/atlassian-connect/1/service-registry", api_root="rest/api", api_version=self.api_version
        )
        params = {"serviceIds": service_ids}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_forge_app_property_keys(self, data=None, **request_kwargs):
        """Get app property keys (Forge).

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url("rest/forge/1/app/properties", api_root="rest/api", api_version=self.api_version)
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_forge_app_property(self, property_key, data=None, **request_kwargs):
        """Delete app property (Forge).

        Args:
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"rest/forge/1/app/properties/{property_key}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_forge_app_property(self, property_key, data=None, **request_kwargs):
        """Get app property (Forge).

        Args:
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"rest/forge/1/app/properties/{property_key}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def put_forge_app_property(self, property_key, data=None, **request_kwargs):
        """Set app property (Forge).

        Args:
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            f"rest/forge/1/app/properties/{property_key}", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_worklogs_by_issue_id_and_worklog_id(self, data=None, **request_kwargs):
        """Get worklogs by issue id and worklog id.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = self.resource_url(
            "rest/internal/api/latest/worklog/bulk", api_root="rest/api", api_version=self.api_version
        )
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)
