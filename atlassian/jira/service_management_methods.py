# coding=utf-8
# Generated from the supplied Jira Cloud API descriptions; do not edit manually.


class JiraServiceManagementMethods:
    """Concrete methods for every supplied service management API operation."""

    def get_assets_workspaces(self, start=None, limit=None, data=None, **request_kwargs):
        """Get assets workspaces.

        Args:
            start: API path or query parameter.
            limit: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/servicedeskapi/assets/workspace"
        params = {"start": start, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_customer_customer_post(self, strict_conflict_status_code=None, data=None, **request_kwargs):
        """Create customer.

        Args:
            strict_conflict_status_code: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/servicedeskapi/customer"
        params = {"strictConflictStatusCode": strict_conflict_status_code}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def create_customer_customer_skip_permission_check_post(
        self, strict_conflict_status_code=None, data=None, **request_kwargs
    ):
        """Create customer.

        Args:
            strict_conflict_status_code: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/servicedeskapi/customer/skip-permission-check"
        params = {"strictConflictStatusCode": strict_conflict_status_code}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def revoke_portal_only_access_for_user(self, account_id, data=None, **request_kwargs):
        """Revoke portal only access for user.

        Args:
            account_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/customer/user/{account_id}/revoke-portal-only-access"
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_info(self, data=None, **request_kwargs):
        """Get info.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/servicedeskapi/info"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_insight_workspaces(self, start=None, limit=None, data=None, **request_kwargs):
        """Get insight workspaces.

        Args:
            start: API path or query parameter.
            limit: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/servicedeskapi/insight/workspace"
        params = {"start": start, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_articles_knowledgebase_article_get(
        self, query=None, highlight=None, start=None, limit=None, cursor=None, prev=None, data=None, **request_kwargs
    ):
        """Get articles.

        Args:
            query: API path or query parameter.
            highlight: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            cursor: API path or query parameter.
            prev: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/servicedeskapi/knowledgebase/article"
        params = {
            "query": query,
            "highlight": highlight,
            "start": start,
            "limit": limit,
            "cursor": cursor,
            "prev": prev,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def view_article(self, page_id, data=None, **request_kwargs):
        """View knowledge base article.

        Args:
            page_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/knowledgebase/article/view/{page_id}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_organizations_organization_get(self, start=None, limit=None, account_id=None, data=None, **request_kwargs):
        """Get organizations.

        Args:
            start: API path or query parameter.
            limit: API path or query parameter.
            account_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/servicedeskapi/organization"
        params = {"start": start, "limit": limit, "accountId": account_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_organization(self, data=None, **request_kwargs):
        """Create organization.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/servicedeskapi/organization"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_organization(self, organization_id, data=None, **request_kwargs):
        """Delete organization.

        Args:
            organization_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/organization/{organization_id}"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_organization(self, organization_id, data=None, **request_kwargs):
        """Get organization.

        Args:
            organization_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/organization/{organization_id}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_properties_keys_organization_organization_id_property_get(
        self, organization_id, data=None, **request_kwargs
    ):
        """Get properties keys.

        Args:
            organization_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/organization/{organization_id}/property"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_property_organization_organization_id_property_property_key_delete(
        self, organization_id, property_key, data=None, **request_kwargs
    ):
        """Delete property.

        Args:
            organization_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/organization/{organization_id}/property/{property_key}"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_property_organization_organization_id_property_property_key_get(
        self, organization_id, property_key, data=None, **request_kwargs
    ):
        """Get property.

        Args:
            organization_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/organization/{organization_id}/property/{property_key}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_property_organization_organization_id_property_property_key_put(
        self, organization_id, property_key, data=None, **request_kwargs
    ):
        """Set property.

        Args:
            organization_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/organization/{organization_id}/property/{property_key}"
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def remove_users_from_organization(self, organization_id, data=None, **request_kwargs):
        """Remove users from organization.

        Args:
            organization_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/organization/{organization_id}/user"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_users_in_organization(self, organization_id, start=None, limit=None, data=None, **request_kwargs):
        """Get users in organization.

        Args:
            organization_id: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/organization/{organization_id}/user"
        params = {"start": start, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def add_users_to_organization(self, organization_id, data=None, **request_kwargs):
        """Add users to organization.

        Args:
            organization_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/organization/{organization_id}/user"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_customer_requests(
        self,
        search_term=None,
        request_ownership=None,
        request_status=None,
        approval_status=None,
        organization_id=None,
        service_desk_id=None,
        request_type_id=None,
        expand=None,
        start=None,
        limit=None,
        data=None,
        **request_kwargs,
    ):
        """Get customer requests.

        Args:
            search_term: API path or query parameter.
            request_ownership: API path or query parameter.
            request_status: API path or query parameter.
            approval_status: API path or query parameter.
            organization_id: API path or query parameter.
            service_desk_id: API path or query parameter.
            request_type_id: API path or query parameter.
            expand: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/servicedeskapi/request"
        params = {
            "searchTerm": search_term,
            "requestOwnership": request_ownership,
            "requestStatus": request_status,
            "approvalStatus": approval_status,
            "organizationId": organization_id,
            "serviceDeskId": service_desk_id,
            "requestTypeId": request_type_id,
            "expand": expand,
            "start": start,
            "limit": limit,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_customer_request(self, data=None, **request_kwargs):
        """Create customer request.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/servicedeskapi/request"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def validate_customer_request(self, data=None, **request_kwargs):
        """Validate customer request.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/servicedeskapi/request/validate"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_customer_request_by_id_or_key(self, issue_id_or_key, expand=None, data=None, **request_kwargs):
        """Get customer request by id or key.

        Args:
            issue_id_or_key: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}"
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_approvals(self, issue_id_or_key, start=None, limit=None, data=None, **request_kwargs):
        """Get approvals.

        Args:
            issue_id_or_key: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/approval"
        params = {"start": start, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_approval_by_id(self, issue_id_or_key, approval_id, data=None, **request_kwargs):
        """Get approval by id.

        Args:
            issue_id_or_key: API path or query parameter.
            approval_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/approval/{approval_id}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def answer_approval(self, issue_id_or_key, approval_id, data=None, **request_kwargs):
        """Answer approval.

        Args:
            issue_id_or_key: API path or query parameter.
            approval_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/approval/{approval_id}"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_attachments_for_request(self, issue_id_or_key, start=None, limit=None, data=None, **request_kwargs):
        """Get attachments for request.

        Args:
            issue_id_or_key: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/attachment"
        params = {"start": start, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_comment_with_attachment(self, issue_id_or_key, data=None, **request_kwargs):
        """Create comment with attachment.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/attachment"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_attachment_content(self, issue_id_or_key, attachment_id, data=None, **request_kwargs):
        """Get attachment content.

        Args:
            issue_id_or_key: API path or query parameter.
            attachment_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/attachment/{attachment_id}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_attachment_thumbnail(self, issue_id_or_key, attachment_id, data=None, **request_kwargs):
        """Get attachment thumbnail.

        Args:
            issue_id_or_key: API path or query parameter.
            attachment_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/attachment/{attachment_id}/thumbnail"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_request_comments(
        self,
        issue_id_or_key,
        public=None,
        internal=None,
        expand=None,
        start=None,
        limit=None,
        data=None,
        **request_kwargs,
    ):
        """Get request comments.

        Args:
            issue_id_or_key: API path or query parameter.
            public: API path or query parameter.
            internal: API path or query parameter.
            expand: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/comment"
        params = {"public": public, "internal": internal, "expand": expand, "start": start, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_request_comment(self, issue_id_or_key, data=None, **request_kwargs):
        """Create request comment.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/comment"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_request_comment_by_id(self, issue_id_or_key, comment_id, expand=None, data=None, **request_kwargs):
        """Get request comment by id.

        Args:
            issue_id_or_key: API path or query parameter.
            comment_id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/comment/{comment_id}"
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_comment_attachments(self, issue_id_or_key, comment_id, start=None, limit=None, data=None, **request_kwargs):
        """Get comment attachments.

        Args:
            issue_id_or_key: API path or query parameter.
            comment_id: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/comment/{comment_id}/attachment"
        params = {"start": start, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def unsubscribe(self, issue_id_or_key, data=None, **request_kwargs):
        """Unsubscribe.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/notification"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_subscription_status(self, issue_id_or_key, data=None, **request_kwargs):
        """Get subscription status.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/notification"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def subscribe(self, issue_id_or_key, data=None, **request_kwargs):
        """Subscribe.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/notification"
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def remove_request_participants(self, issue_id_or_key, data=None, **request_kwargs):
        """Remove request participants.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/participant"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_request_participants(self, issue_id_or_key, start=None, limit=None, data=None, **request_kwargs):
        """Get request participants.

        Args:
            issue_id_or_key: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/participant"
        params = {"start": start, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def add_request_participants(self, issue_id_or_key, data=None, **request_kwargs):
        """Add request participants.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/participant"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_sla_information(self, issue_id_or_key, start=None, limit=None, data=None, **request_kwargs):
        """Get sla information.

        Args:
            issue_id_or_key: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/sla"
        params = {"start": start, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_sla_information_by_id(self, issue_id_or_key, sla_metric_id, data=None, **request_kwargs):
        """Get sla information by id.

        Args:
            issue_id_or_key: API path or query parameter.
            sla_metric_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/sla/{sla_metric_id}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_customer_request_status(self, issue_id_or_key, start=None, limit=None, data=None, **request_kwargs):
        """Get customer request status.

        Args:
            issue_id_or_key: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/status"
        params = {"start": start, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_customer_transitions(self, issue_id_or_key, start=None, limit=None, data=None, **request_kwargs):
        """Get customer transitions.

        Args:
            issue_id_or_key: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/transition"
        params = {"start": start, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def perform_customer_transition(self, issue_id_or_key, data=None, **request_kwargs):
        """Perform customer transition.

        Args:
            issue_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{issue_id_or_key}/transition"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_feedback(self, request_id_or_key, data=None, **request_kwargs):
        """Delete feedback.

        Args:
            request_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{request_id_or_key}/feedback"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_feedback(self, request_id_or_key, data=None, **request_kwargs):
        """Get feedback.

        Args:
            request_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{request_id_or_key}/feedback"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def post_feedback(self, request_id_or_key, data=None, **request_kwargs):
        """Post feedback.

        Args:
            request_id_or_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/request/{request_id_or_key}/feedback"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_all_request_types(
        self,
        search_query=None,
        service_desk_id=None,
        start=None,
        limit=None,
        expand=None,
        include_hidden_request_types_in_search=None,
        restriction_status=None,
        data=None,
        **request_kwargs,
    ):
        """Get all request types.

        Args:
            search_query: API path or query parameter.
            service_desk_id: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            expand: API path or query parameter.
            include_hidden_request_types_in_search: API path or query parameter.
            restriction_status: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/servicedeskapi/requesttype"
        params = {
            "searchQuery": search_query,
            "serviceDeskId": service_desk_id,
            "start": start,
            "limit": limit,
            "expand": expand,
            "includeHiddenRequestTypesInSearch": include_hidden_request_types_in_search,
            "restrictionStatus": restriction_status,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_service_desks(self, start=None, limit=None, data=None, **request_kwargs):
        """Get service desks.

        Args:
            start: API path or query parameter.
            limit: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = "rest/servicedeskapi/servicedesk"
        params = {"start": start, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_service_desk_by_id(self, service_desk_id, data=None, **request_kwargs):
        """Get service desk by id.

        Args:
            service_desk_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def attach_temporary_file(self, service_desk_id, data=None, **request_kwargs):
        """Attach temporary file.

        Args:
            service_desk_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/attachTemporaryFile"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def remove_customers(self, service_desk_id, data=None, **request_kwargs):
        """Remove customers.

        Args:
            service_desk_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/customer"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_customers(self, service_desk_id, query=None, start=None, limit=None, data=None, **request_kwargs):
        """Get customers.

        Args:
            service_desk_id: API path or query parameter.
            query: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/customer"
        params = {"query": query, "start": start, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def add_customers_servicedesk_service_desk_id_customer_post(self, service_desk_id, data=None, **request_kwargs):
        """Add customers.

        Args:
            service_desk_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/customer"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def invite_customer(self, service_desk_id, strict_conflict_status_code=None, data=None, **request_kwargs):
        """Invite customer.

        Args:
            service_desk_id: API path or query parameter.
            strict_conflict_status_code: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/customer/invite"
        params = {"strictConflictStatusCode": strict_conflict_status_code}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(url, params=params, data=data, **request_kwargs)

    def add_customers_servicedesk_service_desk_id_customer_skip_permission_check_post(
        self, service_desk_id, data=None, **request_kwargs
    ):
        """Add customers.

        Args:
            service_desk_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/customer/skip-permission-check"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_articles_servicedesk_service_desk_id_knowledgebase_article_get(
        self,
        service_desk_id,
        query=None,
        highlight=None,
        start=None,
        limit=None,
        cursor=None,
        prev=None,
        data=None,
        **request_kwargs,
    ):
        """Get articles.

        Args:
            service_desk_id: API path or query parameter.
            query: API path or query parameter.
            highlight: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            cursor: API path or query parameter.
            prev: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/knowledgebase/article"
        params = {
            "query": query,
            "highlight": highlight,
            "start": start,
            "limit": limit,
            "cursor": cursor,
            "prev": prev,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def remove_organization(self, service_desk_id, data=None, **request_kwargs):
        """Remove organization.

        Args:
            service_desk_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/organization"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_organizations_servicedesk_service_desk_id_organization_get(
        self, service_desk_id, start=None, limit=None, account_id=None, data=None, **request_kwargs
    ):
        """Get organizations.

        Args:
            service_desk_id: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            account_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/organization"
        params = {"start": start, "limit": limit, "accountId": account_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def add_organization(self, service_desk_id, data=None, **request_kwargs):
        """Add organization.

        Args:
            service_desk_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/organization"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def get_queues(self, service_desk_id, include_count=None, start=None, limit=None, data=None, **request_kwargs):
        """Get queues.

        Args:
            service_desk_id: API path or query parameter.
            include_count: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/queue"
        params = {"includeCount": include_count, "start": start, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_queue(self, service_desk_id, queue_id, include_count=None, data=None, **request_kwargs):
        """Get queue.

        Args:
            service_desk_id: API path or query parameter.
            queue_id: API path or query parameter.
            include_count: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/queue/{queue_id}"
        params = {"includeCount": include_count}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_issues_in_queue(self, service_desk_id, queue_id, start=None, limit=None, data=None, **request_kwargs):
        """Get issues in queue.

        Args:
            service_desk_id: API path or query parameter.
            queue_id: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/queue/{queue_id}/issue"
        params = {"start": start, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_request_types(
        self,
        service_desk_id,
        group_id=None,
        expand=None,
        search_query=None,
        start=None,
        limit=None,
        include_hidden_request_types_in_search=None,
        restriction_status=None,
        data=None,
        **request_kwargs,
    ):
        """Get request types.

        Args:
            service_desk_id: API path or query parameter.
            group_id: API path or query parameter.
            expand: API path or query parameter.
            search_query: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            include_hidden_request_types_in_search: API path or query parameter.
            restriction_status: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/requesttype"
        params = {
            "groupId": group_id,
            "expand": expand,
            "searchQuery": search_query,
            "start": start,
            "limit": limit,
            "includeHiddenRequestTypesInSearch": include_hidden_request_types_in_search,
            "restrictionStatus": restriction_status,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def create_request_type(self, service_desk_id, data=None, **request_kwargs):
        """Create request type.

        Args:
            service_desk_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/requesttype"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def check_request_type_permissions(self, service_desk_id, data=None, **request_kwargs):
        """Check request type permissions.

        Args:
            service_desk_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/requesttype/permissions/check"
        params = None
        return self.post(url, params=params, data=data, **request_kwargs)

    def delete_request_type(self, service_desk_id, request_type_id, data=None, **request_kwargs):
        """Delete request type.

        Args:
            service_desk_id: API path or query parameter.
            request_type_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/requesttype/{request_type_id}"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_request_type_by_id(self, service_desk_id, request_type_id, expand=None, data=None, **request_kwargs):
        """Get request type by id.

        Args:
            service_desk_id: API path or query parameter.
            request_type_id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/requesttype/{request_type_id}"
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_request_type_fields(self, service_desk_id, request_type_id, expand=None, data=None, **request_kwargs):
        """Get request type fields.

        Args:
            service_desk_id: API path or query parameter.
            request_type_id: API path or query parameter.
            expand: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/requesttype/{request_type_id}/field"
        params = {"expand": expand}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)

    def get_properties_keys_servicedesk_service_desk_id_requesttype_request_type_id_property_get(
        self, request_type_id, service_desk_id, data=None, **request_kwargs
    ):
        """Get properties keys.

        Args:
            request_type_id: API path or query parameter.
            service_desk_id: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/requesttype/{request_type_id}/property"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def delete_property_servicedesk_service_desk_id_requesttype_request_type_id_property_property_key_delete(
        self, service_desk_id, request_type_id, property_key, data=None, **request_kwargs
    ):
        """Delete property.

        Args:
            service_desk_id: API path or query parameter.
            request_type_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/requesttype/{request_type_id}/property/{property_key}"
        params = None
        return self.delete(url, params=params, data=data, **request_kwargs)

    def get_property_servicedesk_service_desk_id_requesttype_request_type_id_property_property_key_get(
        self, service_desk_id, request_type_id, property_key, data=None, **request_kwargs
    ):
        """Get property.

        Args:
            service_desk_id: API path or query parameter.
            request_type_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/requesttype/{request_type_id}/property/{property_key}"
        params = None
        return self.get(url, params=params, data=data, **request_kwargs)

    def set_property_servicedesk_service_desk_id_requesttype_request_type_id_property_property_key_put(
        self, service_desk_id, request_type_id, property_key, data=None, **request_kwargs
    ):
        """Set property.

        Args:
            service_desk_id: API path or query parameter.
            request_type_id: API path or query parameter.
            property_key: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/requesttype/{request_type_id}/property/{property_key}"
        params = None
        return self.put(url, params=params, data=data, **request_kwargs)

    def get_request_type_groups(self, service_desk_id, start=None, limit=None, data=None, **request_kwargs):
        """Get request type groups.

        Args:
            service_desk_id: API path or query parameter.
            start: API path or query parameter.
            limit: API path or query parameter.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Jira REST response.
        """
        url = f"rest/servicedeskapi/servicedesk/{service_desk_id}/requesttypegroup"
        params = {"start": start, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(url, params=params, data=data, **request_kwargs)
