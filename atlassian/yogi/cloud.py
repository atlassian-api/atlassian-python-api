"""Concrete Requirement Yogi Cloud REST API methods."""

from .base import YogiBase


class YogiCloud(YogiBase):
    """Requirement Yogi Cloud API client shared by Jira and Confluence."""

    def __init__(self, url="https://api.us.requirementyogi.com/api", *args, **kwargs):
        """Create a Cloud client using the Requirement Yogi API base URL."""
        kwargs.setdefault("cloud", True)
        super(YogiCloud, self).__init__(url, *args, **kwargs)

    def get_organizations(self, **request_kwargs):
        """Finds all the organizations the current user belongs to.

        Args:
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.get("/organizations", **request_kwargs)

    def create_organization(self, data=None, **request_kwargs):
        """Creates an organization.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.post("/organizations", data=data, **request_kwargs)

    def get_applications(self, organization_id, offset=None, limit=None, **request_kwargs):
        """Finds all the applications.

        Args:
            organization_id: Query parameter ``organizationId``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"organizationId": organization_id, "offset": offset, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get("/applications", params=params, **request_kwargs)

    def get_project_containers_in_application(
        self, application_id, offset=None, limit=None, sort=None, **request_kwargs
    ):
        """Finds all containers of level \"project\".

        Args:
            application_id: Path parameter ``applicationId``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            sort: Query parameter ``sort``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"offset": offset, "limit": limit, "sort": sort}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/applications/{application_id}/projects", params=params, **request_kwargs)

    def get_variants_in_container(
        self, application_id, project_id, name=None, offset=None, limit=None, sort=None, **request_kwargs
    ):
        """Finds all the variants in a project.

        Args:
            application_id: Path parameter ``applicationId``.
            project_id: Path parameter ``projectId``.
            name: Query parameter ``name``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            sort: Query parameter ``sort``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"name": name, "offset": offset, "limit": limit, "sort": sort}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(
            f"/applications/{application_id}/projects/{project_id}/variants", params=params, **request_kwargs
        )

    def get_variant_in_container(self, application_id, project_id, variant_id, **request_kwargs):
        """Finds a variant in a project.

        Args:
            application_id: Path parameter ``applicationId``.
            project_id: Path parameter ``projectId``.
            variant_id: Path parameter ``variantId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.get(f"/applications/{application_id}/projects/{project_id}/variants/{variant_id}", **request_kwargs)

    def get_requirements_in_variant(
        self,
        application_id,
        project_id,
        variant_id,
        key=None,
        origin_container_id=None,
        include_origin_links=None,
        include_reference_links=None,
        include_from_dependencies=None,
        include_to_dependencies=None,
        include_jira_issue_links=None,
        include_test_case_links=None,
        offset=None,
        limit=None,
        sort=None,
        **request_kwargs,
    ):
        """Finds all the requirements in a variant.

        Args:
            application_id: Path parameter ``applicationId``.
            project_id: Path parameter ``projectId``.
            variant_id: Path parameter ``variantId``.
            key: Query parameter ``key``.
            origin_container_id: Query parameter ``originContainerId``.
            include_origin_links: Query parameter ``includeOriginLinks``.
            include_reference_links: Query parameter ``includeReferenceLinks``.
            include_from_dependencies: Query parameter ``includeFromDependencies``.
            include_to_dependencies: Query parameter ``includeToDependencies``.
            include_jira_issue_links: Query parameter ``includeJiraIssueLinks``.
            include_test_case_links: Query parameter ``includeTestCaseLinks``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            sort: Query parameter ``sort``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {
            "key": key,
            "originContainerId": origin_container_id,
            "includeOriginLinks": include_origin_links,
            "includeReferenceLinks": include_reference_links,
            "includeFromDependencies": include_from_dependencies,
            "includeToDependencies": include_to_dependencies,
            "includeJiraIssueLinks": include_jira_issue_links,
            "includeTestCaseLinks": include_test_case_links,
            "offset": offset,
            "limit": limit,
            "sort": sort,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(
            f"/applications/{application_id}/projects/{project_id}/variants/{variant_id}/requirements",
            params=params,
            **request_kwargs,
        )

    def get_requirement_in_variant(
        self,
        application_id,
        project_id,
        variant_id,
        key,
        include_origin_links=None,
        include_reference_links=None,
        include_from_dependencies=None,
        include_to_dependencies=None,
        include_jira_issue_links=None,
        include_test_case_links=None,
        **request_kwargs,
    ):
        """Finds a requirement in a variant.

        Args:
            application_id: Path parameter ``applicationId``.
            project_id: Path parameter ``projectId``.
            variant_id: Path parameter ``variantId``.
            key: Path parameter ``key``.
            include_origin_links: Query parameter ``includeOriginLinks``.
            include_reference_links: Query parameter ``includeReferenceLinks``.
            include_from_dependencies: Query parameter ``includeFromDependencies``.
            include_to_dependencies: Query parameter ``includeToDependencies``.
            include_jira_issue_links: Query parameter ``includeJiraIssueLinks``.
            include_test_case_links: Query parameter ``includeTestCaseLinks``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {
            "includeOriginLinks": include_origin_links,
            "includeReferenceLinks": include_reference_links,
            "includeFromDependencies": include_from_dependencies,
            "includeToDependencies": include_to_dependencies,
            "includeJiraIssueLinks": include_jira_issue_links,
            "includeTestCaseLinks": include_test_case_links,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(
            f"/applications/{application_id}/projects/{project_id}/variants/{variant_id}/requirements/{key}",
            params=params,
            **request_kwargs,
        )

    def get_requirements_in_current_variant(
        self,
        application_id,
        project_id,
        key=None,
        origin_container_id=None,
        include_origin_links=None,
        include_reference_links=None,
        include_from_dependencies=None,
        include_to_dependencies=None,
        include_jira_issue_links=None,
        include_test_case_links=None,
        offset=None,
        limit=None,
        sort=None,
        **request_kwargs,
    ):
        """Finds all the requirements in the current variant.

        Args:
            application_id: Path parameter ``applicationId``.
            project_id: Path parameter ``projectId``.
            key: Query parameter ``key``.
            origin_container_id: Query parameter ``originContainerId``.
            include_origin_links: Query parameter ``includeOriginLinks``.
            include_reference_links: Query parameter ``includeReferenceLinks``.
            include_from_dependencies: Query parameter ``includeFromDependencies``.
            include_to_dependencies: Query parameter ``includeToDependencies``.
            include_jira_issue_links: Query parameter ``includeJiraIssueLinks``.
            include_test_case_links: Query parameter ``includeTestCaseLinks``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            sort: Query parameter ``sort``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {
            "key": key,
            "originContainerId": origin_container_id,
            "includeOriginLinks": include_origin_links,
            "includeReferenceLinks": include_reference_links,
            "includeFromDependencies": include_from_dependencies,
            "includeToDependencies": include_to_dependencies,
            "includeJiraIssueLinks": include_jira_issue_links,
            "includeTestCaseLinks": include_test_case_links,
            "offset": offset,
            "limit": limit,
            "sort": sort,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(
            f"/applications/{application_id}/projects/{project_id}/variants/current/requirements",
            params=params,
            **request_kwargs,
        )

    def get_requirement_in_current_variant(
        self,
        application_id,
        project_id,
        key,
        include_origin_links=None,
        include_reference_links=None,
        include_from_dependencies=None,
        include_to_dependencies=None,
        include_jira_issue_links=None,
        include_test_case_links=None,
        **request_kwargs,
    ):
        """Finds a requirement in the current variant.

        Args:
            application_id: Path parameter ``applicationId``.
            project_id: Path parameter ``projectId``.
            key: Path parameter ``key``.
            include_origin_links: Query parameter ``includeOriginLinks``.
            include_reference_links: Query parameter ``includeReferenceLinks``.
            include_from_dependencies: Query parameter ``includeFromDependencies``.
            include_to_dependencies: Query parameter ``includeToDependencies``.
            include_jira_issue_links: Query parameter ``includeJiraIssueLinks``.
            include_test_case_links: Query parameter ``includeTestCaseLinks``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {
            "includeOriginLinks": include_origin_links,
            "includeReferenceLinks": include_reference_links,
            "includeFromDependencies": include_from_dependencies,
            "includeToDependencies": include_to_dependencies,
            "includeJiraIssueLinks": include_jira_issue_links,
            "includeTestCaseLinks": include_test_case_links,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(
            f"/applications/{application_id}/projects/{project_id}/variants/current/requirements/{key}",
            params=params,
            **request_kwargs,
        )

    def get_containers_in_application(
        self,
        application_id,
        type=None,
        level=None,
        parent_container_id=None,
        space_id=None,
        space_key=None,
        page_id=None,
        project_id=None,
        issue_id=None,
        workspace_id=None,
        file_name=None,
        offset=None,
        limit=None,
        sort=None,
        **request_kwargs,
    ):
        """Finds all the containers.

        Args:
            application_id: Path parameter ``applicationId``.
            type: Query parameter ``type``.
            level: Query parameter ``level``.
            parent_container_id: Query parameter ``parentContainerId``.
            space_id: Query parameter ``spaceId``.
            space_key: Query parameter ``spaceKey``.
            page_id: Query parameter ``pageId``.
            project_id: Query parameter ``projectId``.
            issue_id: Query parameter ``issueId``.
            workspace_id: Query parameter ``workspaceId``.
            file_name: Query parameter ``fileName``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            sort: Query parameter ``sort``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {
            "type": type,
            "level": level,
            "parentContainerId": parent_container_id,
            "spaceId": space_id,
            "spaceKey": space_key,
            "pageId": page_id,
            "projectId": project_id,
            "issueId": issue_id,
            "workspaceId": workspace_id,
            "fileName": file_name,
            "offset": offset,
            "limit": limit,
            "sort": sort,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/applications/{application_id}/containers", params=params, **request_kwargs)

    def get_container_in_application(self, application_id, container_id, **request_kwargs):
        """Finds a container.

        Args:
            application_id: Path parameter ``applicationId``.
            container_id: Path parameter ``containerId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.get(f"/applications/{application_id}/containers/{container_id}", **request_kwargs)

    def get_user(self, **request_kwargs):
        """Finds the current user.

        Args:
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.get("/users/me", **request_kwargs)

    def update_user(self, data=None, **request_kwargs):
        """Updates the current user.

        Args:
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.put("/users/me", data=data, **request_kwargs)

    def delete_user(self, **request_kwargs):
        """Deletes the current user.

        Args:
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.delete("/users/me", **request_kwargs)

    def execute_aggregation(self, application_id=None, data=None, **request_kwargs):
        """Performs an aggregation over multiple requirements.

        Args:
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post("/aggregations/execute", params=params, data=data, **request_kwargs)

    def parse_aggregation(self, application_id=None, data=None, **request_kwargs):
        """Parses an aggregation formula.

        Args:
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post("/aggregations/parse", params=params, data=data, **request_kwargs)

    def get_current_application(self, **request_kwargs):
        """Finds the current application.

        Args:
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.get("/applications/current", **request_kwargs)

    def get_application(self, application_id, **request_kwargs):
        """Finds an application.

        Args:
            application_id: Path parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.get(f"/applications/{application_id}", **request_kwargs)

    def get_link_requests(self, application_id, offset=None, limit=None, **request_kwargs):
        """Finds all application link requests of an application.

        Args:
            application_id: Path parameter ``applicationId``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"offset": offset, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/applications/{application_id}/link-requests", params=params, **request_kwargs)

    def get_candidates(self, application_id, offset=None, limit=None, **request_kwargs):
        """Finds all applications that could be linked to the current application by joining another organization.

        Args:
            application_id: Path parameter ``applicationId``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"offset": offset, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/applications/{application_id}/link-requests/candidates", params=params, **request_kwargs)

    def get_link_request(self, application_id, organization_id, **request_kwargs):
        """Finds an application link request.

        Args:
            application_id: Path parameter ``applicationId``.
            organization_id: Path parameter ``organizationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.get(f"/applications/{application_id}/link-requests/{organization_id}", **request_kwargs)

    def create_link_request(self, application_id, organization_id, **request_kwargs):
        """Requests to join a different organization.

        Args:
            application_id: Path parameter ``applicationId``.
            organization_id: Path parameter ``organizationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.post(f"/applications/{application_id}/link-requests/{organization_id}", **request_kwargs)

    def cancel_link_request(self, application_id, organization_id, **request_kwargs):
        """Cancels an application link request.

        Args:
            application_id: Path parameter ``applicationId``.
            organization_id: Path parameter ``organizationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.delete(f"/applications/{application_id}/link-requests/{organization_id}", **request_kwargs)

    def execute_calculation(self, application_id=None, data=None, **request_kwargs):
        """Performs a calculation on multiple requirements.

        Args:
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post("/calculations/execute", params=params, data=data, **request_kwargs)

    def parse_calculation(self, application_id=None, data=None, **request_kwargs):
        """Parses a calculation formula.

        Args:
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post("/calculations/parse", params=params, data=data, **request_kwargs)

    def get_containers(
        self,
        application_id,
        type=None,
        level=None,
        parent_container_id=None,
        space_id=None,
        space_key=None,
        page_id=None,
        project_id=None,
        issue_id=None,
        workspace_id=None,
        file_name=None,
        offset=None,
        limit=None,
        sort=None,
        **request_kwargs,
    ):
        """Finds all the containers.

        Args:
            application_id: Query parameter ``applicationId``.
            type: Query parameter ``type``.
            level: Query parameter ``level``.
            parent_container_id: Query parameter ``parentContainerId``.
            space_id: Query parameter ``spaceId``.
            space_key: Query parameter ``spaceKey``.
            page_id: Query parameter ``pageId``.
            project_id: Query parameter ``projectId``.
            issue_id: Query parameter ``issueId``.
            workspace_id: Query parameter ``workspaceId``.
            file_name: Query parameter ``fileName``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            sort: Query parameter ``sort``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {
            "applicationId": application_id,
            "type": type,
            "level": level,
            "parentContainerId": parent_container_id,
            "spaceId": space_id,
            "spaceKey": space_key,
            "pageId": page_id,
            "projectId": project_id,
            "issueId": issue_id,
            "workspaceId": workspace_id,
            "fileName": file_name,
            "offset": offset,
            "limit": limit,
            "sort": sort,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get("/containers", params=params, **request_kwargs)

    def create_container(self, application_id=None, data=None, **request_kwargs):
        """Creates a container.

        Args:
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post("/containers", params=params, data=data, **request_kwargs)

    def get_container(self, container_id, application_id=None, **request_kwargs):
        """Finds a container.

        Args:
            container_id: Path parameter ``containerId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/containers/{container_id}", params=params, **request_kwargs)

    def update_container(self, container_id, application_id=None, data=None, **request_kwargs):
        """Updates a container.

        Args:
            container_id: Path parameter ``containerId``.
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(f"/containers/{container_id}", params=params, data=data, **request_kwargs)

    def delete_container(self, container_id, application_id=None, **request_kwargs):
        """Deletes a container.

        Args:
            container_id: Path parameter ``containerId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(f"/containers/{container_id}", params=params, **request_kwargs)

    def get_dashboards(
        self,
        container_id,
        application_id=None,
        name=None,
        search=None,
        offset=None,
        limit=None,
        sort=None,
        **request_kwargs,
    ):
        """Finds all the dashboards.

        Args:
            container_id: Query parameter ``containerId``.
            application_id: Query parameter ``applicationId``.
            name: Query parameter ``name``.
            search: Query parameter ``search``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            sort: Query parameter ``sort``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {
            "containerId": container_id,
            "applicationId": application_id,
            "name": name,
            "search": search,
            "offset": offset,
            "limit": limit,
            "sort": sort,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get("/dashboards", params=params, **request_kwargs)

    def create_dashboard(self, application_id=None, data=None, **request_kwargs):
        """Creates a dashboard.

        Args:
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post("/dashboards", params=params, data=data, **request_kwargs)

    def get_default_dashboard(self, container_id, application_id=None, **request_kwargs):
        """Finds the default dashboard of a container.

        Args:
            container_id: Query parameter ``containerId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"containerId": container_id, "applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get("/dashboards/default", params=params, **request_kwargs)

    def create_or_update_default_dashboard(self, container_id, application_id=None, data=None, **request_kwargs):
        """Creates or updates the default dashboard of a container.

        Args:
            container_id: Query parameter ``containerId``.
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"containerId": container_id, "applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put("/dashboards/default", params=params, data=data, **request_kwargs)

    def delete_default_dashboard(self, container_id, application_id=None, **request_kwargs):
        """Deletes the default dashboard of a container.

        Args:
            container_id: Query parameter ``containerId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"containerId": container_id, "applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete("/dashboards/default", params=params, **request_kwargs)

    def get_dashboard(self, dashboard_id, application_id=None, **request_kwargs):
        """Finds a dashboard.

        Args:
            dashboard_id: Path parameter ``dashboardId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/dashboards/{dashboard_id}", params=params, **request_kwargs)

    def update_dashboard(self, dashboard_id, application_id=None, data=None, **request_kwargs):
        """Updates a dashboard.

        Args:
            dashboard_id: Path parameter ``dashboardId``.
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(f"/dashboards/{dashboard_id}", params=params, data=data, **request_kwargs)

    def delete_dashboard(self, dashboard_id, application_id=None, **request_kwargs):
        """Deletes a dashboard.

        Args:
            dashboard_id: Path parameter ``dashboardId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(f"/dashboards/{dashboard_id}", params=params, **request_kwargs)

    def make_default(self, dashboard_id, application_id=None, **request_kwargs):
        """Makes a dashboard the default dashboard of the container.

        Args:
            dashboard_id: Path parameter ``dashboardId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(f"/dashboards/{dashboard_id}/make-default", params=params, **request_kwargs)

    def get_metadata_list(
        self,
        application_id=None,
        search=None,
        name=None,
        data_type=None,
        offset=None,
        limit=None,
        sort=None,
        **request_kwargs,
    ):
        """Returns a paginated list of external property metadata.

        Args:
            application_id: Query parameter ``applicationId``.
            search: Query parameter ``search``.
            name: Query parameter ``name``.
            data_type: Query parameter ``dataType``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            sort: Query parameter ``sort``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {
            "applicationId": application_id,
            "search": search,
            "name": name,
            "dataType": data_type,
            "offset": offset,
            "limit": limit,
            "sort": sort,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get("/external-properties", params=params, **request_kwargs)

    def create_metadata(self, application_id=None, data=None, **request_kwargs):
        """Creates a new external property metadata.

        Args:
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post("/external-properties", params=params, data=data, **request_kwargs)

    def import_external_property_values(self, application_id=None, data=None, **request_kwargs):
        """Imports external property values into a container from an uploaded spreadsheet.

        Args:
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post("/external-properties/import", params=params, data=data, **request_kwargs)

    def import_external_property_values_as_json(self, application_id=None, data=None, **request_kwargs):
        """Imports external property values from a JSON file encoded in the request..

        Args:
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post("/external-properties/import/json", params=params, data=data, **request_kwargs)

    def get_metadata_usage(self, ids, application_id=None, **request_kwargs):
        """Returns the usage of the given external properties across requirements, requirement types and baselines.

        Args:
            ids: Query parameter ``ids``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"ids": ids, "applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get("/external-properties/usage", params=params, **request_kwargs)

    def get_metadata(self, id, application_id=None, **request_kwargs):
        """Returns a single external property metadata by id.

        Args:
            id: Path parameter ``id``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/external-properties/{id}", params=params, **request_kwargs)

    def update_metadata(self, id, application_id=None, data=None, **request_kwargs):
        """Updates an existing external property metadata.

        Args:
            id: Path parameter ``id``.
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(f"/external-properties/{id}", params=params, data=data, **request_kwargs)

    def delete_metadata(self, id, application_id=None, **request_kwargs):
        """Deletes an external property metadata and all its associated values.

        Args:
            id: Path parameter ``id``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(f"/external-properties/{id}", params=params, **request_kwargs)

    def get_requirement_type_usage(self, id, application_id=None, offset=None, limit=None, **request_kwargs):
        """Returns a paginated list of the requirement type identifiers that use a given external property.

        Args:
            id: Path parameter ``id``.
            application_id: Query parameter ``applicationId``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id, "offset": offset, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/external-properties/{id}/usage/requirement-types", params=params, **request_kwargs)

    def get_requirement_usage(self, id, application_id=None, offset=None, limit=None, **request_kwargs):
        """Returns a paginated list of the requirement identifiers that use a given external property.

        Args:
            id: Path parameter ``id``.
            application_id: Query parameter ``applicationId``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id, "offset": offset, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/external-properties/{id}/usage/requirements", params=params, **request_kwargs)

    def create_file_metadata(self, application_id=None, data=None, **request_kwargs):
        """Creates a file metadata..

        Args:
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post("/files", params=params, data=data, **request_kwargs)

    def get_file_metadata(self, id, application_id=None, **request_kwargs):
        """Retrieves the metadata of a file..

        Args:
            id: Path parameter ``id``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/files/{id}", params=params, **request_kwargs)

    def download_file(self, id, application_id=None, **request_kwargs):
        """Downloads a file..

        Args:
            id: Path parameter ``id``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/files/{id}/download", params=params, **request_kwargs)

    def download_blob_file(self, id, application_id=None, **request_kwargs):
        """Downloads a file as a base64 encoded string..

        Args:
            id: Path parameter ``id``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/files/{id}/download/blob", params=params, **request_kwargs)

    def get_file_download_url(self, id, application_id=None, **request_kwargs):
        """Retrieves the download URL of a file..

        Args:
            id: Path parameter ``id``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/files/{id}/download/url", params=params, **request_kwargs)

    def upload_file(self, id, application_id=None, data=None, **request_kwargs):
        """Uploads a file..

        Args:
            id: Path parameter ``id``.
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(f"/files/{id}/upload", params=params, data=data, **request_kwargs)

    def upload_blob_file(self, id, application_id=None, data=None, **request_kwargs):
        """Uploads a file as a base64 encoded string..

        Args:
            id: Path parameter ``id``.
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(f"/files/{id}/upload/blob", params=params, data=data, **request_kwargs)

    def get_file_upload_url(self, id, application_id=None, **request_kwargs):
        """Retrieves the upload URL of a file..

        Args:
            id: Path parameter ``id``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/files/{id}/upload/url", params=params, **request_kwargs)

    def get_jobs(
        self,
        application_id=None,
        container_id=None,
        batch_id=None,
        type=None,
        status=None,
        offset=None,
        limit=None,
        sort=None,
        **request_kwargs,
    ):
        """Finds all the jobs.

        Args:
            application_id: Query parameter ``applicationId``.
            container_id: Query parameter ``containerId``.
            batch_id: Query parameter ``batchId``.
            type: Query parameter ``type``.
            status: Query parameter ``status``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            sort: Query parameter ``sort``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {
            "applicationId": application_id,
            "containerId": container_id,
            "batchId": batch_id,
            "type": type,
            "status": status,
            "offset": offset,
            "limit": limit,
            "sort": sort,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get("/jobs", params=params, **request_kwargs)

    def get_job(self, job_id, application_id=None, **request_kwargs):
        """Finds a job.

        Args:
            job_id: Path parameter ``jobId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/jobs/{job_id}", params=params, **request_kwargs)

    def cancel_job(self, job_id, application_id=None, **request_kwargs):
        """Cancels a job.

        Args:
            job_id: Path parameter ``jobId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(f"/jobs/{job_id}/cancel", params=params, **request_kwargs)

    def retry_job(self, job_id, application_id=None, **request_kwargs):
        """Retries a job.

        Args:
            job_id: Path parameter ``jobId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(f"/jobs/{job_id}/retry", params=params, **request_kwargs)

    def get_organization(self, organization_id, **request_kwargs):
        """Finds an organization.

        Args:
            organization_id: Path parameter ``organizationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.get(f"/organizations/{organization_id}", **request_kwargs)

    def update_organization(self, organization_id, data=None, **request_kwargs):
        """Updates an organization.

        Args:
            organization_id: Path parameter ``organizationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.put(f"/organizations/{organization_id}", data=data, **request_kwargs)

    def delete_organization(self, organization_id, **request_kwargs):
        """Deletes an organization.

        Args:
            organization_id: Path parameter ``organizationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.delete(f"/organizations/{organization_id}", **request_kwargs)

    def get_invitations(self, organization_id, offset=None, limit=None, **request_kwargs):
        """Finds all the user invitations of the organization.

        Args:
            organization_id: Path parameter ``organizationId``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"offset": offset, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/organizations/{organization_id}/invitations", params=params, **request_kwargs)

    def create_invitation(self, organization_id, data=None, **request_kwargs):
        """Invites a user to join the organization.

        Args:
            organization_id: Path parameter ``organizationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.post(f"/organizations/{organization_id}/invitations", data=data, **request_kwargs)

    def get_invitation(self, organization_id, invitation_id, **request_kwargs):
        """Finds a user invitation of the organization.

        Args:
            organization_id: Path parameter ``organizationId``.
            invitation_id: Path parameter ``invitationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.get(f"/organizations/{organization_id}/invitations/{invitation_id}", **request_kwargs)

    def update_invitation(self, organization_id, invitation_id, data=None, **request_kwargs):
        """Updates a user invitation of the organization.

        Args:
            organization_id: Path parameter ``organizationId``.
            invitation_id: Path parameter ``invitationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.put(f"/organizations/{organization_id}/invitations/{invitation_id}", data=data, **request_kwargs)

    def delete_invitation(self, organization_id, invitation_id, **request_kwargs):
        """Deletes a user invitation of the organization.

        Args:
            organization_id: Path parameter ``organizationId``.
            invitation_id: Path parameter ``invitationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.delete(f"/organizations/{organization_id}/invitations/{invitation_id}", **request_kwargs)

    def get_organization_link_requests(self, organization_id, offset=None, limit=None, **request_kwargs):
        """Finds all application link requests of the organization.

        Args:
            organization_id: Path parameter ``organizationId``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"offset": offset, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/organizations/{organization_id}/link-requests", params=params, **request_kwargs)

    def get_organization_link_request(self, organization_id, application_id, **request_kwargs):
        """Finds an application link request of the organization.

        Args:
            organization_id: Path parameter ``organizationId``.
            application_id: Path parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.get(f"/organizations/{organization_id}/link-requests/{application_id}", **request_kwargs)

    def approve_link_request(self, organization_id, application_id, **request_kwargs):
        """Approves an application link request of the organization.

        Args:
            organization_id: Path parameter ``organizationId``.
            application_id: Path parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.post(f"/organizations/{organization_id}/link-requests/{application_id}/approve", **request_kwargs)

    def reject_link_request(self, organization_id, application_id, **request_kwargs):
        """Rejects an application link request of the organization.

        Args:
            organization_id: Path parameter ``organizationId``.
            application_id: Path parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.post(f"/organizations/{organization_id}/link-requests/{application_id}/reject", **request_kwargs)

    def get_members(self, organization_id, offset=None, limit=None, **request_kwargs):
        """Finds all the members of the organization.

        Args:
            organization_id: Path parameter ``organizationId``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"offset": offset, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/organizations/{organization_id}/members", params=params, **request_kwargs)

    def get_member(self, organization_id, user_id, **request_kwargs):
        """Finds a member of the organization.

        Args:
            organization_id: Path parameter ``organizationId``.
            user_id: Path parameter ``userId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.get(f"/organizations/{organization_id}/members/{user_id}", **request_kwargs)

    def update_member(self, organization_id, user_id, data=None, **request_kwargs):
        """Updates a member of the organization.

        Args:
            organization_id: Path parameter ``organizationId``.
            user_id: Path parameter ``userId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.put(f"/organizations/{organization_id}/members/{user_id}", data=data, **request_kwargs)

    def remove_member(self, organization_id, user_id, **request_kwargs):
        """Removes a member from the organization.

        Args:
            organization_id: Path parameter ``organizationId``.
            user_id: Path parameter ``userId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.delete(f"/organizations/{organization_id}/members/{user_id}", **request_kwargs)

    def get_atlassian_user(self, account_id, application_id, **request_kwargs):
        """Finds a display-oriented summary of an Atlassian user by their account id, querying the Atlassian
        site that backs the given application (Jira or Confluence depending on its product type).

               Args:
                   account_id: Path parameter ``accountId``.
                   application_id: Query parameter ``applicationId``.
                   **request_kwargs: Additional REST request options.

               Returns:
                   Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/proxy/users/atlassian/{account_id}", params=params, **request_kwargs)

    def get_relationships(self, application_id=None, offset=None, limit=None, **request_kwargs):
        """Finds all the relationships.

        Args:
            application_id: Query parameter ``applicationId``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id, "offset": offset, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get("/relationships", params=params, **request_kwargs)

    def get_requirements(
        self,
        project_container_id,
        application_id=None,
        variant_id=None,
        key=None,
        origin_container_id=None,
        include_origin_links=None,
        include_reference_links=None,
        include_from_dependencies=None,
        include_to_dependencies=None,
        include_jira_issue_links=None,
        include_test_case_links=None,
        offset=None,
        limit=None,
        sort=None,
        **request_kwargs,
    ):
        """Finds all the requirements.

        Args:
            project_container_id: Query parameter ``projectContainerId``.
            application_id: Query parameter ``applicationId``.
            variant_id: Query parameter ``variantId``.
            key: Query parameter ``key``.
            origin_container_id: Query parameter ``originContainerId``.
            include_origin_links: Query parameter ``includeOriginLinks``.
            include_reference_links: Query parameter ``includeReferenceLinks``.
            include_from_dependencies: Query parameter ``includeFromDependencies``.
            include_to_dependencies: Query parameter ``includeToDependencies``.
            include_jira_issue_links: Query parameter ``includeJiraIssueLinks``.
            include_test_case_links: Query parameter ``includeTestCaseLinks``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            sort: Query parameter ``sort``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {
            "projectContainerId": project_container_id,
            "applicationId": application_id,
            "variantId": variant_id,
            "key": key,
            "originContainerId": origin_container_id,
            "includeOriginLinks": include_origin_links,
            "includeReferenceLinks": include_reference_links,
            "includeFromDependencies": include_from_dependencies,
            "includeToDependencies": include_to_dependencies,
            "includeJiraIssueLinks": include_jira_issue_links,
            "includeTestCaseLinks": include_test_case_links,
            "offset": offset,
            "limit": limit,
            "sort": sort,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get("/requirements", params=params, **request_kwargs)

    def create_requirement(self, application_id=None, data=None, **request_kwargs):
        """Creates a requirement.

        Args:
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post("/requirements", params=params, data=data, **request_kwargs)

    def get_requirement(
        self,
        requirement_id,
        application_id=None,
        include_origin_links=None,
        include_reference_links=None,
        include_from_dependencies=None,
        include_to_dependencies=None,
        include_jira_issue_links=None,
        include_test_case_links=None,
        **request_kwargs,
    ):
        """Finds a requirement.

        Args:
            requirement_id: Path parameter ``requirementId``.
            application_id: Query parameter ``applicationId``.
            include_origin_links: Query parameter ``includeOriginLinks``.
            include_reference_links: Query parameter ``includeReferenceLinks``.
            include_from_dependencies: Query parameter ``includeFromDependencies``.
            include_to_dependencies: Query parameter ``includeToDependencies``.
            include_jira_issue_links: Query parameter ``includeJiraIssueLinks``.
            include_test_case_links: Query parameter ``includeTestCaseLinks``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {
            "applicationId": application_id,
            "includeOriginLinks": include_origin_links,
            "includeReferenceLinks": include_reference_links,
            "includeFromDependencies": include_from_dependencies,
            "includeToDependencies": include_to_dependencies,
            "includeJiraIssueLinks": include_jira_issue_links,
            "includeTestCaseLinks": include_test_case_links,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/requirements/{requirement_id}", params=params, **request_kwargs)

    def update_requirement(self, requirement_id, application_id=None, update_origin=None, data=None, **request_kwargs):
        """Updates a requirement.

        Args:
            requirement_id: Path parameter ``requirementId``.
            application_id: Query parameter ``applicationId``.
            update_origin: Query parameter ``updateOrigin``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id, "updateOrigin": update_origin}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(f"/requirements/{requirement_id}", params=params, data=data, **request_kwargs)

    def delete_requirement(self, requirement_id, application_id=None, **request_kwargs):
        """Deletes a requirement.

        Args:
            requirement_id: Path parameter ``requirementId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(f"/requirements/{requirement_id}", params=params, **request_kwargs)

    def get_requirement_external_properties(
        self, requirement_id, application_id=None, offset=None, limit=None, sort=None, **request_kwargs
    ):
        """Returns a paginated list of external property values belonging to the requirement.

        Args:
            requirement_id: Path parameter ``requirementId``.
            application_id: Query parameter ``applicationId``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            sort: Query parameter ``sort``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id, "offset": offset, "limit": limit, "sort": sort}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/requirements/{requirement_id}/external-properties", params=params, **request_kwargs)

    def create_requirement_external_property(self, requirement_id, application_id=None, data=None, **request_kwargs):
        """Creates an external property value on the requirement.

        Args:
            requirement_id: Path parameter ``requirementId``.
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(
            f"/requirements/{requirement_id}/external-properties", params=params, data=data, **request_kwargs
        )

    def update_requirement_external_property(
        self, requirement_id, external_property_id, application_id=None, data=None, **request_kwargs
    ):
        """Updates the value of an existing external property on the requirement.

        Args:
            requirement_id: Path parameter ``requirementId``.
            external_property_id: Path parameter ``externalPropertyId``.
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(
            f"/requirements/{requirement_id}/external-properties/{external_property_id}",
            params=params,
            data=data,
            **request_kwargs,
        )

    def delete_requirement_external_property(
        self, requirement_id, external_property_id, application_id=None, **request_kwargs
    ):
        """Deletes an external property value from the requirement.

        Args:
            requirement_id: Path parameter ``requirementId``.
            external_property_id: Path parameter ``externalPropertyId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(
            f"/requirements/{requirement_id}/external-properties/{external_property_id}",
            params=params,
            **request_kwargs,
        )

    def get_links(
        self,
        requirement_id,
        application_id=None,
        type=None,
        direction=None,
        relationship=None,
        relationship_id=None,
        include_jira_issue_details=None,
        offset=None,
        limit=None,
        sort=None,
        **request_kwargs,
    ):
        """Finds all the links.

        Args:
            requirement_id: Path parameter ``requirementId``.
            application_id: Query parameter ``applicationId``.
            type: Query parameter ``type``.
            direction: Query parameter ``direction``.
            relationship: Query parameter ``relationship``.
            relationship_id: Query parameter ``relationshipId``.
            include_jira_issue_details: Query parameter ``includeJiraIssueDetails``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            sort: Query parameter ``sort``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {
            "applicationId": application_id,
            "type": type,
            "direction": direction,
            "relationship": relationship,
            "relationshipId": relationship_id,
            "includeJiraIssueDetails": include_jira_issue_details,
            "offset": offset,
            "limit": limit,
            "sort": sort,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/requirements/{requirement_id}/links", params=params, **request_kwargs)

    def create_link(self, requirement_id, application_id=None, data=None, **request_kwargs):
        """Creates a link.

        Args:
            requirement_id: Path parameter ``requirementId``.
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(f"/requirements/{requirement_id}/links", params=params, data=data, **request_kwargs)

    def get_link(self, requirement_id, link_id, application_id=None, **request_kwargs):
        """Finds a link.

        Args:
            requirement_id: Path parameter ``requirementId``.
            link_id: Path parameter ``linkId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/requirements/{requirement_id}/links/{link_id}", params=params, **request_kwargs)

    def update_link(self, requirement_id, link_id, application_id=None, data=None, **request_kwargs):
        """Updates a link.

        Args:
            requirement_id: Path parameter ``requirementId``.
            link_id: Path parameter ``linkId``.
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(f"/requirements/{requirement_id}/links/{link_id}", params=params, data=data, **request_kwargs)

    def delete_link(self, requirement_id, link_id, application_id=None, **request_kwargs):
        """Deletes a link.

        Args:
            requirement_id: Path parameter ``requirementId``.
            link_id: Path parameter ``linkId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(f"/requirements/{requirement_id}/links/{link_id}", params=params, **request_kwargs)

    def get_workspaces(self, application_id=None, offset=None, limit=None, **request_kwargs):
        """Finds all the workspaces.

        Args:
            application_id: Query parameter ``applicationId``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id, "offset": offset, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get("/standalone/workspaces", params=params, **request_kwargs)

    def create_workspace(self, application_id=None, data=None, **request_kwargs):
        """Creates a workspace.

        Args:
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post("/standalone/workspaces", params=params, data=data, **request_kwargs)

    def get_workspace(self, workspace_id, application_id=None, **request_kwargs):
        """Finds a workspace.

        Args:
            workspace_id: Path parameter ``workspaceId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/standalone/workspaces/{workspace_id}", params=params, **request_kwargs)

    def update_workspace(self, workspace_id, application_id=None, data=None, **request_kwargs):
        """Updates a workspace.

        Args:
            workspace_id: Path parameter ``workspaceId``.
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(f"/standalone/workspaces/{workspace_id}", params=params, data=data, **request_kwargs)

    def delete_workspace(self, workspace_id, application_id=None, **request_kwargs):
        """Deletes a workspace.

        Args:
            workspace_id: Path parameter ``workspaceId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(f"/standalone/workspaces/{workspace_id}", params=params, **request_kwargs)

    def get_workspace_members(self, workspace_id, application_id=None, offset=None, limit=None, **request_kwargs):
        """Finds all the members of the workspace.

        Args:
            workspace_id: Path parameter ``workspaceId``.
            application_id: Query parameter ``applicationId``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id, "offset": offset, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/standalone/workspaces/{workspace_id}/members", params=params, **request_kwargs)

    def add_workspace_member(self, workspace_id, application_id=None, data=None, **request_kwargs):
        """Adds a member to the workspace.

        Args:
            workspace_id: Path parameter ``workspaceId``.
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post(f"/standalone/workspaces/{workspace_id}/members", params=params, data=data, **request_kwargs)

    def get_workspace_member(self, workspace_id, user_id, application_id=None, **request_kwargs):
        """Finds a member of the workspace.

        Args:
            workspace_id: Path parameter ``workspaceId``.
            user_id: Path parameter ``userId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/standalone/workspaces/{workspace_id}/members/{user_id}", params=params, **request_kwargs)

    def update_workspace_member(self, workspace_id, user_id, application_id=None, data=None, **request_kwargs):
        """Updates a member of the workspace.

        Args:
            workspace_id: Path parameter ``workspaceId``.
            user_id: Path parameter ``userId``.
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(
            f"/standalone/workspaces/{workspace_id}/members/{user_id}", params=params, data=data, **request_kwargs
        )

    def remove_workspace_member(self, workspace_id, user_id, application_id=None, **request_kwargs):
        """Removes a member from the workspace.

        Args:
            workspace_id: Path parameter ``workspaceId``.
            user_id: Path parameter ``userId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(f"/standalone/workspaces/{workspace_id}/members/{user_id}", params=params, **request_kwargs)

    def get_templates(
        self,
        container_id,
        application_id=None,
        type=None,
        name=None,
        search=None,
        shared_level=None,
        offset=None,
        limit=None,
        sort=None,
        **request_kwargs,
    ):
        """Finds templates in a container.

        Args:
            container_id: Query parameter ``containerId``.
            application_id: Query parameter ``applicationId``.
            type: Query parameter ``type``.
            name: Query parameter ``name``.
            search: Query parameter ``search``.
            shared_level: Query parameter ``sharedLevel``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            sort: Query parameter ``sort``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {
            "containerId": container_id,
            "applicationId": application_id,
            "type": type,
            "name": name,
            "search": search,
            "sharedLevel": shared_level,
            "offset": offset,
            "limit": limit,
            "sort": sort,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get("/templates", params=params, **request_kwargs)

    def create_template(self, application_id=None, data=None, **request_kwargs):
        """Creates a template.

        Args:
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post("/templates", params=params, data=data, **request_kwargs)

    def evaluate_template(self, application_id=None, data=None, **request_kwargs):
        """Evaluates the given template.

        Args:
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post("/templates/evaluate", params=params, data=data, **request_kwargs)

    def parse_template(self, application_id=None, data=None, **request_kwargs):
        """Parses the given template and returns the syntax errors of its variables, keyed by variable.

        Args:
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post("/templates/parse", params=params, data=data, **request_kwargs)

    def get_template(self, template_id, application_id=None, **request_kwargs):
        """Finds a template.

        Args:
            template_id: Path parameter ``templateId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/templates/{template_id}", params=params, **request_kwargs)

    def update_template(self, template_id, application_id=None, data=None, **request_kwargs):
        """Updates a template.

        Args:
            template_id: Path parameter ``templateId``.
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(f"/templates/{template_id}", params=params, data=data, **request_kwargs)

    def delete_template(self, template_id, application_id=None, **request_kwargs):
        """Deletes a template.

        Args:
            template_id: Path parameter ``templateId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(f"/templates/{template_id}", params=params, **request_kwargs)

    def get_credentials(self, **request_kwargs):
        """Finds all the credentials of the current user.

        Args:
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.get("/users/me/credentials", **request_kwargs)

    def delete_credential(self, credential_id, **request_kwargs):
        """Deletes a credential of the current user.

        Args:
            credential_id: Path parameter ``credentialId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.delete(f"/users/me/credentials/{credential_id}", **request_kwargs)

    def get_user_invitations(self, offset=None, limit=None, **request_kwargs):
        """Finds all the invitations of the current user.

        Args:
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"offset": offset, "limit": limit}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get("/users/me/invitations", params=params, **request_kwargs)

    def accept_invitation(self, invitation_id, **request_kwargs):
        """Accepts an invitation of the current user.

        Args:
            invitation_id: Path parameter ``invitationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.post(f"/users/me/invitations/{invitation_id}/accept", **request_kwargs)

    def reject_invitation(self, invitation_id, **request_kwargs):
        """Rejects an invitation of the current user
        .

               Args:
                   invitation_id: Path parameter ``invitationId``.
                   **request_kwargs: Additional REST request options.

               Returns:
                   Decoded Requirement Yogi REST response.
        """
        return self.post(f"/users/me/invitations/{invitation_id}/reject", **request_kwargs)

    def get_atlassian_accessible_resources(self, type=None, **request_kwargs):
        """Finds the accessible resources of the linked Atlassian account.

        Args:
            type: Query parameter ``type``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"type": type}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get("/users/me/linked-accounts/atlassian/accessible-resources", params=params, **request_kwargs)

    def get_atlassian_profile(self, **request_kwargs):
        """Finds the user profile of the linked Atlassian account.

        Args:
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.get("/users/me/linked-accounts/atlassian/profile", **request_kwargs)

    def get_linked_account(self, provider_id, **request_kwargs):
        """Finds a linked account of the current user.

        Args:
            provider_id: Path parameter ``providerId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.get(f"/users/me/linked-accounts/{provider_id}", **request_kwargs)

    def delete_linked_account(self, provider_id, **request_kwargs):
        """Deletes a linked account of the current user.

        Args:
            provider_id: Path parameter ``providerId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.delete(f"/users/me/linked-accounts/{provider_id}", **request_kwargs)

    def get_account_linking_url(self, provider_id, redirect_uri, **request_kwargs):
        """Builds the link to initiate the account linking process.

        Args:
            provider_id: Path parameter ``providerId``.
            redirect_uri: Query parameter ``redirectUri``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"redirectUri": redirect_uri}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/users/me/linked-accounts/{provider_id}/link", params=params, **request_kwargs)

    def get_user_organizations(self, **request_kwargs):
        """Finds all the organizations the current user belongs to.

        Args:
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.get("/users/me/organizations", **request_kwargs)

    def get_user_by_id(self, id, **request_kwargs):
        """Finds a display-oriented summary of a user by their id, used to resolve a user's name (e.

        Args:
            id: Path parameter ``id``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        return self.get(f"/users/{id}", **request_kwargs)

    def get_variants(
        self, project_container_id, application_id=None, name=None, offset=None, limit=None, sort=None, **request_kwargs
    ):
        """Finds all the variants.

        Args:
            project_container_id: Query parameter ``projectContainerId``.
            application_id: Query parameter ``applicationId``.
            name: Query parameter ``name``.
            offset: Query parameter ``offset``.
            limit: Query parameter ``limit``.
            sort: Query parameter ``sort``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {
            "projectContainerId": project_container_id,
            "applicationId": application_id,
            "name": name,
            "offset": offset,
            "limit": limit,
            "sort": sort,
        }
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get("/variants", params=params, **request_kwargs)

    def create_variant(self, application_id=None, data=None, **request_kwargs):
        """Creates a variant.

        Args:
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.post("/variants", params=params, data=data, **request_kwargs)

    def get_variant(self, variant_id, application_id=None, **request_kwargs):
        """Finds a variant.

        Args:
            variant_id: Path parameter ``variantId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.get(f"/variants/{variant_id}", params=params, **request_kwargs)

    def update_variant(self, variant_id, application_id=None, data=None, **request_kwargs):
        """Updates a variant.

        Args:
            variant_id: Path parameter ``variantId``.
            application_id: Query parameter ``applicationId``.
            data: JSON request body.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.put(f"/variants/{variant_id}", params=params, data=data, **request_kwargs)

    def delete_variant(self, variant_id, application_id=None, **request_kwargs):
        """Deletes a variant.

        Args:
            variant_id: Path parameter ``variantId``.
            application_id: Query parameter ``applicationId``.
            **request_kwargs: Additional REST request options.

        Returns:
            Decoded Requirement Yogi REST response.
        """
        params = {"applicationId": application_id}
        params = {key: value for key, value in params.items() if value is not None} or None
        return self.delete(f"/variants/{variant_id}", params=params, **request_kwargs)
