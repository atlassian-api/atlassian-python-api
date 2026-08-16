# coding=utf-8
"""Versioned Jira Cloud clients.

These clients are deliberately additive. ``Jira`` and ``ServiceDesk`` remain
the compatibility clients for Server, Data Center, and existing Cloud users.
"""

from typing import Any, Dict, List, Optional, Union

from ..rest_client import AtlassianRestAPI
from .core_methods import JiraCloudCoreMethods
from .service_management_methods import JiraServiceManagementMethods
from .software_methods import JiraSoftwareMethods


class JiraCloud(JiraCloudCoreMethods, AtlassianRestAPI):
    """Jira Cloud platform (Core) REST API client for version 2 or 3.

    Use ``api_version=3`` for new integrations; version 2 is retained for
    payload compatibility. The legacy ``Jira`` methods remain in
    :class:`JiraServer` and are intentionally not mixed into this client.
    """

    SUPPORTED_API_VERSIONS = (2, 3)

    def __init__(self, url: str, *args: Any, api_version: Union[str, int] = 3, **kwargs: Any):
        api_version = int(api_version)
        if api_version not in self.SUPPORTED_API_VERSIONS:
            raise ValueError("Jira Cloud Core api_version must be 2 or 3")
        kwargs["api_version"] = api_version
        kwargs["cloud"] = True
        super(JiraCloud, self).__init__(url, *args, **kwargs)

    def endpoint(self, resource: str, api_version: Optional[Union[str, int]] = None) -> str:
        """Return a Core REST endpoint path without issuing a request."""
        version = self.api_version if api_version is None else int(api_version)
        if version not in self.SUPPORTED_API_VERSIONS:
            raise ValueError("Jira Cloud Core api_version must be 2 or 3")
        return self.resource_url(resource, api_root="rest/api", api_version=version)

    def enhanced_jql(
        self,
        jql: str,
        fields: Union[str, List[str]] = "*all",
        nextPageToken: Optional[str] = None,
        limit: Optional[int] = None,
        expand: Optional[str] = None,
    ):
        """Search Jira Cloud issues through the v3 enhanced JQL endpoint.

        Use ``nextPageToken`` from a previous response to retrieve the next
        page. Unlike the older search API, enhanced JQL is cursor-paginated.
        """
        params: Dict[str, Union[str, int]] = {"jql": jql}
        if nextPageToken is not None:
            params["nextPageToken"] = str(nextPageToken)
        if limit is not None:
            params["maxResults"] = int(limit)
        if fields is not None:
            params["fields"] = ",".join(fields) if isinstance(fields, (list, tuple, set)) else fields
        if expand is not None:
            params["expand"] = expand
        return self.get(self.endpoint("search/jql", api_version=3), params=params)

    def enhanced_jql_get_list_of_tickets(
        self,
        jql: str,
        fields: Union[str, List[str]] = "*all",
        limit: Optional[int] = None,
        expand: Optional[str] = None,
    ) -> list:
        """Return all cursor-paginated enhanced JQL issues up to ``limit``.

        When ``limit`` is omitted, iteration continues until Jira marks the
        result set as final.
        """
        results = []
        next_page_token = None
        while True:
            response = self.enhanced_jql(
                jql,
                fields=fields,
                nextPageToken=next_page_token,
                limit=limit,
                expand=expand,
            )
            if not response:
                break
            results.extend(response.get("issues", []))
            if limit is not None and len(results) >= limit:
                return results[:limit]
            next_page_token = response.get("nextPageToken")
            if response.get("isLast", False) or not next_page_token:
                break
        return results

    def get_project_workflow_scheme_associations(self, project_ids):
        """Return workflow-scheme associations for one or more project IDs.

        Team-managed and non-existent projects are omitted by Jira Cloud. The
        caller requires the Administer Jira global permission.

        :param project_ids: Project ID or iterable of project IDs.
        :return: Jira's workflow-scheme association container.
        """
        if isinstance(project_ids, (str, int)):
            project_ids = [project_ids]
        else:
            project_ids = list(project_ids)
        if not project_ids:
            raise ValueError("project_ids must contain at least one project ID")
        return self.get(self.endpoint("workflowscheme/project", api_version=3), params={"projectId": project_ids})

    def assign_project_workflow_scheme(self, project_id, workflow_scheme_id):
        """Assign a workflow scheme to a classic Jira Cloud project.

        Jira only permits this operation when the project has no issues. The
        caller requires the Administer Jira global permission.

        :param project_id: Numeric Jira project ID.
        :param workflow_scheme_id: Workflow scheme ID.
        :return: Jira response (normally ``None`` for HTTP 204).
        """
        data = {"projectId": str(project_id), "workflowSchemeId": str(workflow_scheme_id)}
        return self.put(self.endpoint("workflowscheme/project", api_version=3), data=data)

    def add_version(
        self,
        project_id,
        version,
        project_key: Optional[str] = None,
        is_archived: bool = False,
        is_released: bool = False,
    ):
        """Create a Jira Cloud project version through REST v3.

        ``version`` can be a name or a complete payload dictionary. Cloud's
        create-version API identifies the project with its numeric ID.
        """
        if isinstance(version, dict):
            data = dict(version)
        else:
            data = {"name": version, "archived": is_archived, "released": is_released}
        try:
            data["projectId"] = int(data.get("projectId", project_id))
        except (TypeError, ValueError) as error:
            raise ValueError("project_id must be a numeric Jira Cloud project ID") from error
        if project_key is not None:
            data.setdefault("project", project_key)
        return self.post(self.endpoint("version", api_version=3), data=data)


class JiraSoftware(JiraSoftwareMethods, AtlassianRestAPI):
    """Jira Software Cloud REST APIs.

    ``endpoint`` covers documented Agile, Software, DevInfo, deployments,
    builds, feature-flags, remote-links, security, operations, and DevOps
    component roots. Call ``get``, ``post``, ``put``, or ``delete`` with its
    returned path.
    """

    API_VERSIONS = {
        "agile": "1.0",
        "software": "1.0",
        "devinfo": "0.10",
        "featureflags": "0.1",
        "deployments": "0.1",
        "builds": "0.1",
        "remotelinks": "1.0",
        "security": "1.0",
        "operations": "1.0",
        "devopscomponents": "1.0",
    }

    def __init__(self, url: str, *args: Any, **kwargs: Any):
        # These APIs do not share one root/version, so endpoint() supplies it.
        kwargs["cloud"] = True
        kwargs.setdefault("api_root", "rest")
        kwargs.setdefault("api_version", None)
        super(JiraSoftware, self).__init__(url, *args, **kwargs)

    def endpoint(self, api: str, resource: str = "", api_version: Optional[str] = None) -> str:
        """Build a Jira Software Cloud endpoint path.

        ``api`` is one of :attr:`API_VERSIONS`; ``resource`` is the documented
        portion following its version (for example ``"board/42/sprint"``).
        """
        if api not in self.API_VERSIONS:
            supported = ", ".join(sorted(self.API_VERSIONS))
            raise ValueError(f"Unsupported Jira Software API '{api}'. Use one of: {supported}")
        version = api_version or self.API_VERSIONS[api]
        return self.resource_url(resource, api_root=f"rest/{api}", api_version=version)


class JiraServiceManagement(JiraServiceManagementMethods, AtlassianRestAPI):
    """Jira Service Management Cloud public REST API client.

    This client is independent from the legacy ``ServiceDesk`` surface, which
    remains available unchanged for existing integrations.
    """

    API_VERSION = "1"

    def __init__(self, url: str, *args: Any, **kwargs: Any):
        kwargs["cloud"] = True
        super(JiraServiceManagement, self).__init__(url, *args, **kwargs)

    def endpoint(self, resource: str = "") -> str:
        """Return a JSM public REST endpoint path without issuing a request."""
        return self.url_joiner("rest/servicedeskapi", resource)

    def get_sla_metrics(self, service_desk_id, start=None, limit=None):
        """Return SLA metric configuration from Jira's agent endpoint.

        This is an internal endpoint used by the JSM settings UI and may not
        be available on every Cloud or Data Center release.
        """
        params = {key: value for key, value in {"start": start, "limit": limit}.items() if value is not None}
        return self.get(
            f"rest/servicedesk/1/servicedesk/agent/{service_desk_id}/sla/metrics",
            params=params or None,
        )

    def update_sla_metric(self, service_desk_id, sla_id, data):
        """Update an SLA metric configuration for a service desk.

        Jira exposes this through an internal agent endpoint used by the JSM
        settings UI. The payload is passed through unchanged to support the
        metric schema used by the target Jira release.
        """
        return self.put(
            f"rest/servicedesk/1/servicedesk/agent/{service_desk_id}/sla/metrics/{sla_id}",
            data=data,
        )

    def set_sla_metric(self, service_desk_id, sla_id, data):
        """Backward-compatible alias for :meth:`update_sla_metric`."""
        return self.update_sla_metric(service_desk_id, sla_id, data)


def create_jira_cloud(url: str, *args: Any, api_version: Union[str, int] = 3, **kwargs: Any) -> JiraCloud:
    """Create a versioned Jira Cloud Core client (v3 by default)."""
    return JiraCloud(url, *args, api_version=api_version, **kwargs)
