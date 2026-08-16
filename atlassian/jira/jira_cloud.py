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


def create_jira_cloud(url: str, *args: Any, api_version: Union[str, int] = 3, **kwargs: Any) -> JiraCloud:
    """Create a versioned Jira Cloud Core client (v3 by default)."""
    return JiraCloud(url, *args, api_version=api_version, **kwargs)
