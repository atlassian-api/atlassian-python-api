# coding=utf-8
"""Statuspage API wrapper."""
import logging
from enum import Enum

from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Branding(Enum):
    """The main template your statuspage will use"""

    PREMIUM = "premium"
    BASIC = "basic"


class SubscriberType(Enum):
    """The type of subscriber"""

    EMAIL = "email"
    SMS = "sms"
    WEBHOOK = "webhook"
    SLACK = "slack"
    INTEGRATION_PARTNER = "integration_partner"


class SubscriberState(Enum):
    """The state of the subscriber"""

    ACTIVE = "active"
    PENDING = "pending"
    QUARANTINED = "quarantined"
    ALL = "all"


class SortField(Enum):
    """The field to sort by

    Attributes
    ----------
    PRIMARY : str
        to indicate sorting by the identifying field
    CREATED_AT : str
        for sorting by creation timestamp
    QUARANTINED_AT : str
        for sorting by quarantine timestamp
    RELEVANCE : str
        which sorts by the relevancy of the search text
    """

    PRIMARY = "primary"
    CREATED_AT = "created_at"
    QUARANTINED_AT = "quarantined_at"
    RELEVANCE = "relevance"


class SortOrder(Enum):
    """The order to sort by"""

    ASC = "asc"
    DESC = "desc"


class Status(Enum):
    """The status of the incident"""

    INVESTIGATING = "investigating"
    IDENTIFIED = "identified"
    MONITORING = "monitoring"
    RESOLVED = "resolved"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    VERIFYING = "verifying"
    COMPLETED = "completed"


class Impact(Enum):
    """The impact of the incident"""

    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    MAINTENANCE = "maintenance"
    NONE = "none"


class Transform(Enum):
    """The transform to apply to the metric"""

    AVERAGE = "average"
    COUNT = "count"
    MAX = "max"
    MIN = "min"
    SUM = "sum"


class MetricProviderType(Enum):
    """The type of metric provider"""

    PINGDOM = "Pingdom"
    NEW_RELIC = "NewRelic"
    LIBRATO = "Librato"
    DATADOG = "Datadog"
    SELF = "Self"


class StatusPage(AtlassianRestAPI):
    """StatusPage API wrapper."""

    def __init__(self, *args, **kwargs):
        super(StatusPage, self).__init__(*args, **kwargs)

    def page_list_pages(self):
        """
        Get a list of pages

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exception.response.content)` to get API error info


        Notes
        -----
        Available fields: https://developer.statuspage.io/#operation/getPages

        Returns
        -------
        any
        """
        url = "v1/pages"
        return self.get(url)

    def get_page(self, page_id):
        """
        Get page information

        Parameters
        ----------
        page_id : str
            Your page unique ID

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exception.response.content)` to get API error info

        Notes
        -----
        Available fields: https://developer.statuspage.io/#operation/getPagesPageId

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}"
        return self.get(url)

    def page_update(self, page_id, page):
        """
        Update a page

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page : dict[str,any]
            Your page values that you want to change

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exception.response.content)` to get API error info

        Notes
        -----
        Available fields: https://developer.statuspage.io/#operation/patchPagesPageId

        Description of fields:

        name : str
            The name of your page

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}"
        return self.patch(url, data={"page": page})

    def organization_get_users(self, organization_id, page=1, per_page=100):
        """
        Get a list of users

        Notes
        -----
        Available fields: https://developer.statuspage.io/#operation/getOrganizationsOrganizationIdUsers

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exception.response.content)` to get API error info

        Parameters
        ----------
        organization_id : str
            Unique organization ID
        page : int
            Page offset to fetch. Defaults to 1.
        per_page : int
            Number of results to return per page. Defaults to 100.
        Returns
        -------
        any
        """
        url = f"v1/organizations/{organization_id}/users"
        return self.get(url, params={"page": page, "per_page": per_page})

    def organization_get_user_permissions(self, organization_id, user_id):
        """
        Get a user's permissions in organization

        Parameters
        ----------
        organization_id : str
            Unique organization ID
        user_id : str
            Unique user ID

        Notes
        -----
        Available fields: https://developer.statuspage.io/#operation/getOrganizationsOrganizationIdPermissionsUserId

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exception.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/organizations/{organization_id}/permissions/{user_id}"
        return self.get(url)

    def organization_set_user_permissions(self, organization_id, user_id, pages):
        """
        Update a user's role permissions. Payload should contain a mapping of pages to a set of the desired roles,
        if the page has Role Based Access Control. Otherwise, the pages should map to an empty hash.
        User will lose access to any pages omitted from the payload.

        Parameters
        ----------
        organization_id : str
            Unique organization ID
        user_id : str
            Unique user ID
        pages : dict[str, any]
            You can specify "page_configuration", "incident_manager" and "maintenance_manager" booleans here

        Notes
        -----
        Available fields: https://developer.statuspage.io/#operation/putOrganizationsOrganizationIdPermissionsUserId

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exception.response.content)` to get API error info

        Examples
        --------
        >>> client = StatusPage(url="https://api.statuspage.io", token="YOUR-TOKEN")
        >>> client.organization_set_user_permissions(
        ...    "ORGANIZATION-ID",
        ...    "USER-ID",
        ...     {
        ...         "PAGE-ID": {
        ...             "page_configuration": True,
        ...             "incident_manager": True,
        ...             "maintenance_manager": True
        ...         }
        ...     }
        ... )

        Returns
        -------
        any
        """
        url = f"v1/organizations/{organization_id}/permissions/{user_id}"
        return self.patch(url, data={"pages": pages})

    def page_get_embed_config_settings(self, page_id):
        """
        Get status embed config settings

        Parameters
        ----------
        page_id : str
            Your page unique ID

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exception.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdStatusEmbedConfig

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/status_embed_config"
        return self.get(url)

    def page_update_embed_config_settings(self, page_id, status_embed_config):
        """
        Update status embed config settings

        Parameters
        ----------
        page_id : str
            Your page unique ID
        status_embed_config : dict[str, any]

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Examples
        --------
        >>> client = StatusPage(url="https://api.statuspage.io", token="YOUR-TOKEN")
        >>> client.page_update_embed_config_settings(
        ...    "PAGE-ID",
        ...     {
        ...         "position": "string",
        ...         "incident_background_color": "string",
        ...         "incident_text_color": "string",
        ...         "maintenance_background_color": "string",
        ...         "maintenance_text_color": "string"
        ...     }
        ... )

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/putPagesPageIdStatusEmbedConfig

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/status_embed_config"
        return self.patch(url, status_embed_config)

    def page_access_users_list(self, page_id, email, page=1, per_page=100):
        """
        Get a list of page access users

        Parameters
        ----------
        page_id : str
            Your page unique ID
        email : str
            Email address to search for
        page : int
            Page offset to fetch. Defaults to 1.
        per_page : int
            Number of results to return per page. Defaults to 100.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdPageAccessUsers

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_users"
        return self.get(url, params={"email": email, "page": page, "per_page": per_page})

    def page_get_access_user(self, page_id, page_access_user_id):
        """
        Get page access user

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_user_id : str
            Page Access User Identifier

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdPageAccessUsersPageAccessUserId

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_users/{page_access_user_id}"
        return self.get(url)

    def page_set_access_user(self, page_id, page_access_user_id, external_login, email, page_access_group_ids):
        """
        Update page access user

        Warnings
        --------
        TODO: Fields that can be updated are undocumented as well as their descriptions.

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_user_id : str
            Page Access User Identifier
        external_login : str
            IDP login user id. Key is typically "uid".
        email : str
            Email address
        page_access_group_ids : list[str]
            Group IDs

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/patchPagesPageIdPageAccessUsersPageAccessUserId

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_users/{page_access_user_id}"
        return self.patch(
            url, data={"external_login": external_login, "email": email, "page_access_group_ids": page_access_group_ids}
        )

    def page_delete_access_user(self, page_id, page_access_user_id):
        """
        Delete page access user

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_user_id : str
            Page Access User Identifier

        Notes
        -----
        See available fields:
        https://developer.statuspage.io/#operation/deletePagesPageIdPageAccessUsersPageAccessUserId

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_users/{page_access_user_id}"
        return self.delete(url)

    def page_get_components_access_user(self, page_id, page_access_user_id, page=1, per_page=100):
        """
        Get components for page access user

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_user_id : str
            Page Access User Identifier
        page : int
            Page offset to fetch. Defaults to 1.
        per_page : int
            Number of results to return per page. Defaults to 100.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdPageAccessUsersPageAccessUserIdComponents
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_users/{page_access_user_id}/components"
        return self.get(url, params={"page": page, "per_page": per_page})

    def page_add_components_access_user(self, page_id, page_access_user_id, component_ids):
        """
        Add components for page access user

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_user_id : str
            Page Access User Identifier
        component_ids : list[str]
            List of component codes to allow access to

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/putPagesPageIdPageAccessUsersPageAccessUserIdComponents
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_users/{page_access_user_id}/components"
        return self.patch(url, data={"component_ids": component_ids})

    def page_replace_components_access_user(self, page_id, page_access_user_id, component_ids):
        """
        Replace components for page access user

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_user_id : str
            Page Access User Identifier
        component_ids : list[str]
            List of component codes to allow access to

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdPageAccessUsersPageAccessUserIdComponents
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_users/{page_access_user_id}/components"
        return self.post(url, data={"component_ids": component_ids})

    def page_delete_components_access_user(self, page_id, page_access_user_id, component_ids):
        """
        Delete components for page access user.

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_user_id : str
            Page Access User Identifier
        component_ids : list[str]
            List of components codes to remove. **If omitted, all components will be removed.**

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/deletePagesPageIdPageAccessUsersPageAccessUserIdComponents
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_users/{page_access_user_id}/components"
        return self.delete(url, data={"component_ids": component_ids})

    def page_delete_component_access_user(self, page_id, page_access_user_id, component_id):
        """
        Delete components for page access user.

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_user_id : str
            Page Access User Identifier
        component_id : str
            Component identifier

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/deletePagesPageIdPageAccessUsersPageAccessUserIdComponentsComponentId
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_users/{page_access_user_id}/components/{component_id}"
        return self.delete(url)

    def page_get_metrics_access_user(self, page_id, page_access_user_id):
        """
        Get metrics for page access user

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_user_id : str
            Page Access User Identifier

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdPageAccessUsersPageAccessUserIdMetrics
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_users/{page_access_user_id}/metrics"
        return self.get(url)

    def page_add_metrics_access_user(self, page_id, page_access_user_id, metric_ids):
        """
        Add metrics for page access user

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_user_id : str
            Page Access User Identifier
        metric_ids : list[str]
            List of metrics to add

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/putPagesPageIdPageAccessUsersPageAccessUserIdMetrics
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_users/{page_access_user_id}/metrics"
        return self.patch(url, data={"metric_ids": metric_ids})

    def page_replace_metrics_access_user(self, page_id, page_access_user_id, metric_ids):
        """
        Replace metrics for page access user

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_user_id : str
            Page Access User Identifier
        metric_ids : list[str]
            List of metrics to replace

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdPageAccessUsersPageAccessUserIdMetrics
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_users/{page_access_user_id}/metrics"
        return self.post(url, data={"metric_ids": metric_ids})

    def page_delete_metrics_access_user(self, page_id, page_access_user_id, metric_ids):
        """
        Delete metrics for page access user

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_user_id : str
            Page Access User Identifier
        metric_ids : list[str]
            List of metrics to remove

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/deletePagesPageIdPageAccessUsersPageAccessUserIdMetrics
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_users/{page_access_user_id}/metrics"
        return self.delete(url, data={"metric_ids": metric_ids})

    def page_delete_metric_access_user(self, page_id, page_access_user_id, metric_id):
        """
        Delete metric for page access user

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_user_id : str
            Page Access User Identifier
        metric_id : str
            Identifier of metric requested

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/deletePagesPageIdPageAccessUsersPageAccessUserIdMetricsMetricId
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_users/{page_access_user_id}/metrics/{metric_id}"
        return self.delete(url)

    def page_get_access_groups(self, page_id, page=1, per_page=100):
        """
        Get a list of page access groups

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page : int
            Page offset to fetch. Defaults to 1.
        per_page : int
            Number of results to return per page. Defaults to 100.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdPageAccessGroups

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_groups"
        return self.get(url, params={"page": page, "per_page": per_page})

    def page_get_access_group(self, page_id, page_access_group_id):
        """
        Get a page access group

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_group_id : str
            Page Access Group Identifier

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdPageAccessGroupsPageAccessGroupId

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_groups/{page_access_group_id}"
        return self.get(url)

    def page_create_access_group(
        self, page_id, name, external_identifier, component_ids, metric_ids, page_access_user_ids
    ):
        """
        Create a page access group

        Parameters
        ----------
        page_id : str
            Your page unique ID
        name : str
            Name for this Group
        external_identifier : str
            Associates group with external group
        component_ids : list[str]
        metric_ids : list[str]
        page_access_user_ids : list[str]

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdPageAccessGroups

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_groups"
        return self.post(
            url,
            data={
                "page_access_group": {
                    "name": name,
                    "external_identifier": external_identifier,
                    "component_ids": component_ids,
                    "metric_ids": metric_ids,
                    "page_access_user_ids": page_access_user_ids,
                }
            },
        )

    def page_replace_access_group(
        self, page_id, page_access_group_id, name, external_identifier, component_ids, metric_ids, page_access_user_ids
    ):
        """
        Update a page access group

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_group_id : str
            Page Access Group Identifier
        name : str
            Name for this Group
        external_identifier : str
            Associates group with external group
        component_ids : list[str]
        metric_ids : list[str]
        page_access_user_ids : list[str]

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/putPagesPageIdPageAccessGroupsPageAccessGroupId

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_groups/{page_access_group_id}"
        return self.patch(
            url,
            data={
                "page_access_group": {
                    "name": name,
                    "external_identifier": external_identifier,
                    "component_ids": component_ids,
                    "metric_ids": metric_ids,
                    "page_access_user_ids": page_access_user_ids,
                }
            },
        )

    def page_delete_access_group(self, page_id, page_access_group_id):
        """
        Remove a page access group

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_group_id : str
            Page Access Group Identifier

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/deletePagesPageIdPageAccessGroupsPageAccessGroupId
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_groups/{page_access_group_id}"
        return self.delete(url)

    def page_add_components_to_access_group(self, page_id, page_access_group_id, component_ids):
        """
        Add components to page access group

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_group_id : str
            Page Access Group Identifier
        component_ids : list[str]
            List of Component identifiers

        Notes
        -----
        See available fields: https://developer.statuspage.io/#tag/page-access-group-components

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_groups/{page_access_group_id}/components"
        return self.patch(url, data={"component_ids": component_ids})

    def page_replace_components_for_access_page(self, page_id, page_access_group_id, component_ids):
        """
        Replace components for a page access group

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_group_id : str
            Page Access Group Identifier
        component_ids : list[str]
            List of components codes to set on the page access group

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdPageAccessGroupsPageAccessGroupIdComponents
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_groups/{page_access_group_id}/components"
        return self.post(url, data={"component_ids": component_ids})

    def page_delete_components_for_access_page(self, page_id, page_access_group_id, component_ids):
        """
        Delete components for a page access group

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_group_id : str
            Page Access Group Identifier
        component_ids : list[str]
            List of Component identifiers

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/deletePagesPageIdPageAccessGroupsPageAccessGroupIdComponents
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_groups/{page_access_group_id}/components"
        return self.delete(url, data={"component_ids": component_ids})

    def page_delete_component_for_access_page(self, page_id, page_access_group_id, component_id):
        """
        Remove a component from a page access group

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_group_id : str
            Page Access Group Identifier
        component_id : str
            Component identifier

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/deletePagesPageIdPageAccessGroupsPageAccessGroupIdComponentsComponentId
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_groups/{page_access_group_id}/components/{component_id}"
        return self.delete(url)

    def page_get_components_for_access_group(self, page_id, page_access_group_id, page=1, per_page=100):
        """
        Add components to page access group

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_group_id : str
            Page Access Group Identifier
        page : int
            Page offset to fetch. Defaults to 1.
        per_page : int
            Number of results to return per page. Defaults to 100.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdPageAccessGroupsPageAccessGroupIdComponents
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/page_access_groups/{page_access_group_id}/components"
        return self.get(url, params={"page": page, "per_page": per_page})

    def page_get_subscriber(self, page_id, subscriber_id):
        """
        Get a subscriber

        Parameters
        ----------
        page_id : str
            Your page unique ID
        subscriber_id : str
            Subscriber identifier

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdSubscribersSubscriberId

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/subscribers/{subscriber_id}"
        return self.get(url)

    def page_get_subscribers(self, page_id, search_by=None, sort_direction="asc", page=1, per_page=100):
        """
        Get all subscribers

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page : int
            Page offset to fetch. Defaults to 1.
        per_page : int
            Number of results to return per page. Defaults to 100.
        search_by : dict[str, any]
            What to search by.

            "q" : str
            If this is specified, search the contact information (email, endpoint, or phone number)
            for the provided value. This parameter doesn't support searching for Slack subscribers.

            "subscriber_type" : SubscriberType
            If this is specified, only return subscribers of the specified type.

            "subscriber_state" : SubscriberState
            If this is specified, only return subscribers of the specified state.
            Specify state "all" to find subscribers in any states.

            "sort_field" : SortField
            The field on which to sort the results.

        sort_direction : SortOrder
            The direction in which to sort the results.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdSubscribers

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/subscribers"

        params = {}

        if search_by:
            if "q" in search_by:
                params["q"] = search_by["q"]
            if "subscriber_type" in search_by:
                params["type"] = search_by["subscriber_type"]
            if "subscriber_state" in search_by:
                params["state"] = search_by["subscriber_state"]
            if "sort_field" in search_by:
                params["sort_field"] = search_by["sort_field"]

        params["sort_direction"] = sort_direction
        params["page"] = page
        params["per_page"] = per_page

        return self.get(url, params=params)

    def page_update_subscriber(self, page_id, subscriber_id, component_ids):
        """
        Update a subscriber

        Parameters
        ----------
        page_id : str
            Your page unique ID
        subscriber_id : str
            Subscriber identifier
        component_ids : list[str]
            A list of component ids for which the subscriber should receive updates for.
            Components must be an array with at least one element if it is passed at all.
            Each component must belong to the page indicated in the path.
            To set the subscriber to be subscribed to all components on the page, exclude this parameter.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/patchPagesPageIdSubscribersSubscriberId

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/subscribers/{subscriber_id}"
        return self.patch(url, data={"component_ids": component_ids})

    def page_unsubscribe_subscriber(self, page_id, subscriber_id, skip_unsubscription_notifications=False):
        """
        Unsubscribe a subscriber

        Parameters
        ----------
        page_id : str
            Your page unique ID
        subscriber_id : str
            Subscriber identifier
        skip_unsubscription_notifications : bool
            If true, the subscriber will not receive an email notification when they are unsubscribed.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/deletePagesPageIdSubscribersSubscriberId

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/subscribers/{subscriber_id}"
        return self.delete(url, params={"skip_unsubscription_notifications": skip_unsubscription_notifications})

    def page_resend_confirmation_subscribers(self, page_id, subscriber_id):
        """
        Resend confirmation email to a subscriber

        Parameters
        ----------
        page_id : str
            Your page unique ID
        subscriber_id : str
            Subscriber identifier

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdSubscribersSubscriberIdResendConfirmation
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/subscribers/{subscriber_id}/resend_confirmation"
        return self.post(url)

    def page_create_subscriber(self, page_id, subscriber):
        """
        Create a subscriber

        Parameters
        ----------
        page_id : str
            Your page unique ID
        subscriber : dict[str, any]
            Subscriber object. You can specify email, endpoint, phone_country, phone_number,
            skip_confirmation_notification, page_access_user and component_ids. Check notes for all available fields.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdSubscribers

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/subscribers"
        return self.post(url, data={"subscriber": subscriber})

    def page_get_list_unsubscribed(self, page_id, page=1, per_page=100):
        """
        Get a list of unsubscribed subscribers

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page : int
            Page offset to fetch. Defaults to 1.
        per_page : int
            Number of results to return per page. Defaults to 100.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdSubscribersUnsubscribed

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/unsubscribed"
        return self.get(url, params={"page": page, "per_page": per_page})

    def page_count_subscribers_by_type(self, page_id, subscriber_type, subscriber_state):
        """
        Count subscribers by type

        Parameters
        ----------
        page_id : str
            Your page unique ID
        subscriber_type : SubscriberType
            If this is specified, only return subscribers of the specified type.
        subscriber_state : SubscriberState
            If this is specified, only return subscribers of the specified state.
            Specify state "all" to find subscribers in any states.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdSubscribersCount

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/subscribers/count"
        return self.get(url, params={"type": subscriber_type, "state": subscriber_state})

    def page_get_histogram_of_subscribers_with_state(self, page_id):
        """
        Get a histogram of subscribers with state

        Parameters
        ----------
        page_id : str
            Your page unique ID

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdSubscribersHistogramByState

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/subscribers/histogram"
        return self.get(url)

    def page_reactivate_subscribers(self, page_id, subscriber_ids, subscriber_type):
        """
        Reactivate a list of quarantined subscribers

        Parameters
        ----------
        page_id : str
            Your page unique ID
        subscriber_ids : list[str]
            A list of subscriber ids to reactivate.
        subscriber_type : SubscriberType
            If this is present, only reactivate subscribers of this type.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdSubscribersReactivate

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/subscribers/reactivate"
        return self.post(url, data={"subscribers": subscriber_ids, "type": subscriber_type})

    def page_unsubscribe_subscribers(
        self, page_id, subscriber_ids, subscriber_type, skip_unsubscription_notification=False
    ):
        """
        Unsubscribe a list of subscribers

        Parameters
        ----------
        page_id : str
            Your page unique ID
        subscriber_ids : str | list[str]
            The array of subscriber codes to unsubscribe (limited to 100),
            or "all" to unsubscribe all subscribers if the number of subscribers is less than 100.
        subscriber_type : SubscriberType
            If this is present, only unsubscribe subscribers of this type.
        skip_unsubscription_notification : bool
            If this is true, do not send an unsubscription notification to the subscriber.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdSubscribersUnsubscribe

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/subscribers/unsubscribe"
        return self.post(
            url,
            data={
                "subscribers": subscriber_ids,
                "type": subscriber_type,
                "skip_unsubscription_notification": skip_unsubscription_notification,
            },
        )

    def page_resend_confirmations_to_subscribers(self, page_id, subscriber_ids):
        """
        Resend confirmation emails to a list of subscribers

        Parameters
        ----------
        page_id : str
            Your page unique ID
        subscriber_ids : str | list[str]
            The array of subscriber codes to resend confirmations for,
            or "all" to resend confirmations to all subscribers.
            Only unconfirmed email subscribers will receive this notification.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdSubscribersResendConfirmation

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/subscribers/resend_confirmation"
        return self.post(url, data={"subscribers": subscriber_ids})

    def page_create_template(self, page_id, template):
        """
        Create a template. "name", "title" and "body" is required in the template.

        Parameters
        ----------
        page_id : str
            Your page unique ID
        template : dict[str, any]
            The template to create

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdIncidentTemplates


        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incident_templates"
        return self.post(url, data={"template": template})

    def page_get_templates(self, page_id, page=1, per_page=100):
        """
        Get a list of templates

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page : int
            The page offset to return. Defaults to 1.
        per_page : int
            The number of templates to return per page. Defaults to 100.
            If this is set to 0, a default and maximum limit of 100
            will be imposed and this endpoint will return paginated data
            even if this query parameter is not provided.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdIncidentTemplates

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incident_templates"
        return self.get(url, params={"page": page, "per_page": per_page})

    def page_create_incident(self, page_id, incident):
        """
        Create an incident. "name" is required in the incident.

        Parameters
        ----------
        page_id : str
            Your page unique ID
        incident : dict[str, any]
            The incident to create

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdIncidents

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents"
        return self.post(url, data={"incident": incident})

    def page_list_incidents(self, page_id, q, page=1, per_page=100):
        """
        Get a list of incidents

        Parameters
        ----------
        page_id : str
            Your page unique ID
        q : str
            The search query to filter incidents by. If this is specified, search for the text query string in
            the incident's name, status, postmortem_body, and incident_updates fields.
        page : int
            The page offset to return. Defaults to 1.
        per_page : int
            The number of incidents to return per page. Defaults to 100.
            If this is set to 0, a default and maximum limit of 100
            will be imposed and this endpoint will return paginated data
            even if this query parameter is not provided.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdIncidents

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents"
        return self.get(url, params={"q": q, "page": page, "per_page": per_page})

    def page_list_active_maintenances(self, page_id, page=1, per_page=100):
        """
        Get a list of active maintenances

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page : int
            The page offset to return. Defaults to 1.
        per_page : int
            The number of maintenances to return per page. Defaults to 100.
            If this is set to 0, a default and maximum limit of 100
            will be imposed and this endpoint will return paginated data
            even if this query parameter is not provided.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdIncidentsActiveMaintenance

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/active_maintenance"
        return self.get(url, params={"page": page, "per_page": per_page})

    def page_list_upcoming_incidents(self, page_id, page=1, per_page=100):
        """
        Get a list of upcoming incidents

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page : int
            The page offset to return. Defaults to 1.
        per_page : int
            The number of incidents to return per page. Defaults to 100.
            If this is set to 0, a default and maximum limit of 100
            will be imposed and this endpoint will return paginated data
            even if this query parameter is not provided.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdIncidentsUpcoming

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/upcoming"
        return self.get(url, params={"page": page, "per_page": per_page})

    def page_list_scheduled_incidents(self, page_id, page=1, per_page=100):
        """
        Get a list of scheduled incidents

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page : int
            The page offset to return. Defaults to 1.
        per_page : int
            The number of incidents to return per page. Defaults to 100.
            If this is set to 0, a default and maximum limit of 100
            will be imposed and this endpoint will return paginated data
            even if this query parameter is not provided.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdIncidentsScheduled

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/scheduled"
        return self.get(url, params={"page": page, "per_page": per_page})

    def page_list_unresolved_incidents(self, page_id, page=1, per_page=100):
        """
        Get a list of unresolved incidents

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page : int
            The page offset to return. Defaults to 1.
        per_page : int
            The number of incidents to return per page. Defaults to 100.
            If this is set to 0, a default and maximum limit of 100
            will be imposed and this endpoint will return paginated data
            even if this query parameter is not provided.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdIncidentsUnresolved

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/unresolved"
        return self.get(url, params={"page": page, "per_page": per_page})

    def page_delete_incident(self, page_id, incident_id):
        """
        Delete an incident

        Parameters
        ----------
        page_id : str
            Your page unique ID
        incident_id : str
            The incident unique ID

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/{incident_id}"
        return self.delete(url)

    def page_update_incident(self, page_id, incident_id, incident):
        """
        Update an incident

        Parameters
        ----------
        page_id : str
            Your page unique ID
        incident_id : str
            The incident unique ID
        incident : dict[str, any]
            The incident data to update

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/patchPagesPageIdIncidentsIncidentId

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/{incident_id}"
        return self.patch(url, data={"incident": incident})

    def page_get_incident(self, page_id, incident_id):
        """
        Get an incident

        Parameters
        ----------
        page_id : str
            Your page unique ID
        incident_id : str
            The incident unique ID

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdIncidentsIncidentId

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/{incident_id}"
        return self.get(url)

    def page_update_incident_updates(self, page_id, incident_id, incident_update_id, incident_update):
        """
        Update a previous incident update

        Parameters
        ----------
        page_id : str
            Your page unique ID
        incident_id : str
            The incident unique ID
        incident_update_id : str
            The incident update unique ID
        incident_update : dict[str, any]
            The incident update data to update

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/patchPagesPageIdIncidentsIncidentIdIncidentUpdatesIncidentUpdateId
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/{incident_id}/incidents_update/{incident_update_id}"
        return self.patch(url, data={"incident_update": incident_update})

    def page_create_incident_subscriber(self, page_id, incident_id, subscriber):
        """
        Create a subscriber for an incident

        Parameters
        ----------
        page_id : str
            Your page unique ID
        incident_id : str
            The incident unique ID
        subscriber : dict[str, any]
            The subscriber data to create

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdIncidentsIncidentIdSubscribers

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/{incident_id}/subscribers"
        return self.post(url, data={"subscriber": subscriber})

    def page_list_incident_subscribers(self, page_id, incident_id, page=1, per_page=100):
        """
        Get a list of subscribers for an incident

        Parameters
        ----------
        page_id : str
            Your page unique ID
        incident_id : str
            The incident unique ID
        page : int
            The page offset to return. Defaults to 1.
        per_page : int
            The number of subscribers to return per page. Defaults to 100.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdIncidentsIncidentIdSubscribers

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/{incident_id}/subscribers"
        return self.get(url, params={"page": page, "per_page": per_page})

    def page_unsubscribe_incident_subscriber(self, page_id, incident_id, subscriber_id):
        """
        Unsubscribe a subscriber from an incident

        Parameters
        ----------
        page_id : str
            Your page unique ID
        incident_id : str
            The incident unique ID
        subscriber_id : str
            The subscriber unique ID

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/{incident_id}/subscribers/{subscriber_id}"
        return self.delete(url)

    def page_get_incident_subscriber(self, page_id, incident_id, subscriber_id):
        """
        Get a subscriber for an incident

        Parameters
        ----------
        page_id : str
            Your page unique ID
        incident_id : str
            The incident unique ID
        subscriber_id : str
            The subscriber unique ID

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdIncidentsIncidentIdSubscribersSubscriberId
        # noqa: E501

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/{incident_id}/subscribers/{subscriber_id}"
        return self.get(url)

    def page_resend_confirmation_incident_subscriber(self, page_id, incident_id, subscriber_id):
        """
        Resend the confirmation email for a subscriber

        Parameters
        ----------
        page_id : str
            Your page unique ID
        incident_id : str
            The incident unique ID
        subscriber_id : str
            The subscriber unique ID

        Warnings
        --------
        Only returns 201 code

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/{incident_id}/subscribers/{subscriber_id}/resend_confirmation"
        return self.post(url)

    def page_get_postmortem(self, page_id, incident_id):
        """
        Get a postmortem

        Parameters
        ----------
        page_id : str
            Your page unique ID
        incident_id : str
            The incident unique ID

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdIncidentsIncidentIdPostmortem

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/{incident_id}/postmortem"
        return self.get(url)

    def page_create_postmortem(self, page_id, incident_id, postmortem):
        """
        Create a postmortem

        Parameters
        ----------
        page_id : str
            Your page unique ID
        incident_id : str
            The incident unique ID
        postmortem : str
            Body of Postmortem to create.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/putPagesPageIdIncidentsIncidentIdPostmortem

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/{incident_id}/postmortem"
        return self.post(url, data={"postmortem": {"body_draft": postmortem}})

    def page_delete_postmortem(self, page_id, incident_id):
        """
        Delete a postmortem

        Parameters
        ----------
        page_id : str
            Your page unique ID
        incident_id : str
            The incident unique ID

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/deletePagesPageIdIncidentsIncidentIdPostmortem

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/{incident_id}/postmortem"
        return self.delete(url)

    def page_publish_postmortem(self, page_id, incident_id, postmortem):
        """
        Publish a postmortem

        Parameters
        ----------
        page_id : str
            Your page unique ID
        incident_id : str
            The incident unique ID
        postmortem : dict[str, any]
            Body of Postmortem to publish
            Available fields: "notify_twitter", "notify_subscribers", and "custom_tweet"

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/putPagesPageIdIncidentsIncidentIdPostmortemPublish
        # noqa: E501

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/{incident_id}/postmortem/publish"
        return self.post(url, data={"postmortem": postmortem})

    def page_revert_postmortem(self, page_id, incident_id):
        """
        Revert a postmortem

        Parameters
        ----------
        page_id : str
            Your page unique ID
        incident_id : str
            The incident unique ID

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/putPagesPageIdIncidentsIncidentIdPostmortemRevert
        # noqa: E501

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/incidents/{incident_id}/postmortem/revert"
        return self.post(url)

    def page_create_component(self, page_id, component):
        """
        Create a component

        Parameters
        ----------
        page_id : str
            Your page unique ID
        component : dict[str, any]
            The component to create
            Available fields: "name", "description", "status", "group_id", "showcase", "only_show_if_degraded",
            and "start_date"

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdComponents

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/components"
        return self.post(url, data={"component": component})

    def page_get_components(self, page_id, per_page=100, page=1):
        """
        Get all components

        Parameters
        ----------
        page_id : str
            Your page unique ID
        per_page : int
            Number of components to return per page (default is 100)
        page : int
            Page number to return (default is 1)

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdComponents

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/components"
        return self.get(url, params={"per_page": per_page, "page": page})

    def page_update_component(self, page_id, component_id, component):
        """
        Update a component

        Warnings
        --------
        If "group_id" is Null then the component will be removed from a group

        Parameters
        ----------
        page_id : str
            Your page unique ID
        component_id : str
            The component unique ID
        component : dict[str, any]
            The component to update
            Available fields: "name", "description", "status", "group_id", "showcase", "only_show_if_degraded",
            and "start_date"

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/patchPagesPageIdComponentsComponentId

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/components/{component_id}"
        return self.patch(url, data={"component": component})

    def page_delete_component(self, page_id, component_id):
        """
        Delete a component

        Parameters
        ----------
        page_id : str
            Your page unique ID
        component_id : str
            The component unique ID

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/deletePagesPageIdComponentsComponentId

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/components/{component_id}"
        return self.delete(url)

    def page_get_component(self, page_id, component_id):
        """
        Get a component

        Parameters
        ----------
        page_id : str
            Your page unique ID
        component_id : str
            The component unique ID

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdComponentsComponentId

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/components/{component_id}"
        return self.get(url)

    def page_get_uptime_component(self, page_id, component_id, start=None, end=None):
        """
        Get a component's uptime

        Parameters
        ----------
        page_id : str
            Your page unique ID
        component_id : str
            The component unique ID
        start : str
            The start date for uptime calculation
            (defaults to the component's start_date field or 90 days ago, whichever is more recent).
            The maximum supported date range is six calendar months.
            If the year is given, the date defaults to the first day of the year.
            If the year and month are given, the start date defaults to the first day of that month.
            The earliest supported date is January 1, 1970.
        end : str
            The end date for uptime calculation (defaults to today in the page's time zone).
            The maximum supported date range is six calendar months.
            If the year is given, the date defaults to the last day of the year.
            If the year and month are given, the date defaults to the last day of that month.
            The earliest supported date is January 1, 1970.

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdComponentsComponentIdUptime

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/components/{component_id}/uptime"

        params = {}
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end

        return self.get(url, params=params)

    def page_remove_access_users_from_component(self, page_id, component_id):
        """
        Remove access users from a component

        Parameters
        ----------
        page_id : str
            Your page unique ID
        component_id : str
            The component unique ID

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/deletePagesPageIdComponentsComponentIdPageAccessUsers
        # noqa: E501

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/components/{component_id}/page_access_users"
        return self.delete(url)

    def page_add_access_users_to_component(self, page_id, component_id, page_access_user_ids):
        """
        Add access users to a component

        Parameters
        ----------
        page_id : str
            Your page unique ID
        component_id : str
            The component unique ID
        page_access_user_ids : list[str]
            The users to add

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdComponentsComponentIdPageAccessUsers
        # noqa: E501

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/components/{component_id}/page_access_users"
        return self.post(url, data={"page_access_user_ids": page_access_user_ids})

    def page_remove_access_users_from_group(self, page_id, component_id):
        """
        Remove access users from a group

        Parameters
        ----------
        page_id : str
            Your page unique ID
        component_id : str
            The component unique ID

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/deletePagesPageIdComponentsComponentIdPageAccessGroups
        # noqa: E501

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/components/{component_id}/page_access_groups"
        return self.delete(url)

    def page_add_access_users_to_group(self, page_id, component_id, page_access_group_ids):
        """
        Add page access groups to a component

        Parameters
        ----------
        page_id : str
            Your page unique ID
        component_id : str
            The component unique ID
        page_access_group_ids : list[str]
            The groups to add

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdComponentsComponentIdPageAccessGroups
        # noqa: E501

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/components/{component_id}/page_access_groups"
        return self.post(url, data={"page_access_group_ids": page_access_group_ids})

    def page_create_component_group(self, page_id, description, components_group):
        """
        Create a component group

        Parameters
        ----------
        page_id : str
            Your page unique ID
        description : str
            The description of the component group
        components_group : dick[str, any]
            The components to add to the group
            Available fields: "components" (array of strings), "name"

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdComponentGroups

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/component_groups"
        return self.post(url, data={"description": description, "components_group": components_group})

    def page_get_list_of_component_groups(self, page_id, per_page=100, page=1):
        """
        Get a list of component groups

        Parameters
        ----------
        page_id : str
            Your page unique ID
        per_page : int
            The number of results to return per page (defaults to 100)
        page : int
            The page to return (defaults to 1)

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdComponentGroups

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/component_groups"
        return self.get(url, params={"per_page": per_page, "page": page})

    def page_update_component_group(self, page_id, component_group_id, description, component_group):
        """
        Update a component group

        Parameters
        ----------
        page_id : str
            Your page unique ID
        component_group_id : str
            Component group identifier
        description : str
            The description of the component group
        component_group : dict[str, any]
            The components to update
            Available fields: "name", "components" (array of strings)

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/patchPagesPageIdComponentGroupsId

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/component_groups/{component_group_id}"
        return self.patch(url, data={"description": description, "component_group": component_group})

    def page_delete_component_group(self, page_id, component_group_id):
        """
        Delete a component group

        Parameters
        ----------
        page_id : str
            Your page unique ID
        component_group_id : str
            Component group identifier

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/deletePagesPageIdComponentGroupsId

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/component_groups/{component_group_id}"
        return self.delete(url)

    def page_get_component_group(self, page_id, component_group_id):
        """
        Get a component group

        Parameters
        ----------
        page_id : str
            Your page unique ID
        component_group_id : str
            Component group identifier

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdComponentGroupsId

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/component_groups/{component_group_id}"
        return self.get(url)

    def page_get_uptime_for_component_group(self, page_id, component_group_id, start=None, end=None):
        """
        Get uptime for a component group

        Parameters
        ----------
        page_id : str
            Your page unique ID
        component_group_id : str
            Component group identifier
        start : str
            The start date for uptime calculation
            (defaults to the date of the component in the group with the earliest start_date,
            or 90 days ago, whichever is more recent).
            The maximum supported date range is six calendar months.
            If the year is given, the date defaults to the first day of the year.
            If the year and month are given, the start date defaults to the first day of that month.
            The earliest supported date is January 1, 1970.
        end : str
            The end date for uptime calculation (defaults to today in the page's time zone).
            The maximum supported date range is six calendar months.
            If the year is given, the date defaults to the last day of the year.
            If the year and month are given, the date defaults to the last day of that month.
            The earliest supported date is January 1, 1970.

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdComponentGroupsIdUptime

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/component_groups/{component_group_id}/uptime"

        params = {}
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end

        return self.get(url, params=params)

    def page_add_data_points_to_metric(self, page_id, data):
        """
        Add data points to a metric

        Parameters
        ----------
        page_id : str
            Your page unique ID
        data : dict[str, any]
            The data points to add
            Requires "metric_id", which specifies identifier to add data to
            In "metric_id" you should have array of "timestamp" and "value"

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdMetricsData

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/metrics/data"
        return self.post(url, data={"data": data})

    def page_get_list_of_metrics(self, page_id, per_page=100, page=1):
        """
        Get a list of metrics

        Parameters
        ----------
        page_id : str
            Your page unique ID
        per_page : int
            The number of results to return per page (defaults to 100)
        page : int
            The page to return (defaults to 1)

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdMetrics

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/metrics"
        return self.get(url, params={"per_page": per_page, "page": page})

    def page_update_metric(self, page_id, metric_id, metric):
        """
        Update a metric

        Parameters
        ----------
        page_id : str
            Your page unique ID
        metric_id : str
            Metric identifier
        metric : dict[str, any]
            The metric to update

            Available fields in metric: "name", "metric_identifier"
            "name" - Name of metric,
            "metric_identifier" - Metric Display identifier used to look up the metric data from the provider

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/patchPagesPageIdMetricsMetricId

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/metrics/{metric_id}"
        return self.patch(url, data={"metric": metric})

    def page_update_metric_data(self, page_id, metric_id, metric):
        """
        Update metric data

        Parameters
        ----------
        page_id : str
            Your page unique ID
        metric_id : str
            Metric identifier
        metric : dict[str, any]
            The metric to update

            Available fields in metric: "name", "metric_identifier"
            "name" - Name of metric,
            "metric_identifier" - Metric Display identifier used to look up the metric data from the provider

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/patchPagesPageIdMetricsMetricId

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/metrics/{metric_id}"
        return self.patch(url, data={"metric": metric})

    def page_delete_metric(self, page_id, metric_id):
        """
        Delete a metric

        Parameters
        ----------
        page_id : str
            Your page unique ID
        metric_id : str
            Metric identifier

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/deletePagesPageIdMetricsMetricId

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/metrics/{metric_id}"
        return self.delete(url)

    def page_get_metric(self, page_id, metric_id):
        """
        Get a metric

        Parameters
        ----------
        page_id : str
            Your page unique ID
        metric_id : str
            Metric identifier

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdMetricsMetricId

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/metrics/{metric_id}"
        return self.get(url)

    def page_reset_data_for_metric(self, page_id, metric_id):
        """
        Reset data for a metric

        Parameters
        ----------
        page_id : str
            Your page unique ID
        metric_id : str
            Metric identifier

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/deletePagesPageIdMetricsMetricIdData

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/metrics/{metric_id}/data"
        return self.delete(url)

    def page_add_data_to_metric(self, page_id, metric_id, data):
        """
        Add data to a metric

        Parameters
        ----------
        page_id : str
            Your page unique ID
        metric_id : str
            Metric identifier
        data : dict[str, any]
            The data to add

            Requires "timestamp" and "value"

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdMetricsMetricIdData

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/metrics/{metric_id}/data"
        return self.post(url, data={"data": data})

    def page_list_metric_for_metric_provider(self, page_id, metric_provider_id, per_page=100, page=1):
        """
        List metrics for a metric provider

        Parameters
        ----------
        page_id : str
            Your page unique ID
        metric_provider_id : str
            Metric provider identifier
        per_page : int
            The number of results to return per page (defaults to 100)
        page : int
            The page to return (defaults to 1)

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdMetricsProvidersMetricsProviderIdMetrics
        # noqa: E501

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/metrics_providers/{metric_provider_id}/metrics"
        return self.get(url, params={"per_page": per_page, "page": page})

    def page_create_metric_for_metric_provider(self, page_id, metric_provider_id, metric):
        """
        Create a metric for a metric provider

        Parameters
        ----------
        page_id : str
            Your page unique ID
        metric_provider_id : str
            Metric provider identifier
        metric : dict[str, any]
            The metric to create

            Available fields in metric: "name", "metric_identifier", "transform", "suffix",
            "y_axis_min", "y_axis_max", "y_axis_hidden", "display",
            "decimal_places", "tooltip_description"

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdMetricsProvidersMetricsProviderIdMetrics
        # noqa: E501

        Descriptions of the fields that can be added to the metric:
            "name" - Name of metric,

            "metric_identifier" - The identifier used to look up the metric data from the provider

            "transform" - The transform to apply to metric before pulling into Statuspage.
            See transform enum for available values

            "suffix" - Suffix to describe the units on the graph

            "y_axis_min" - Minimum value for the y-axis

            "y_axis_max" - Maximum value for the y-axis

            "y_axis_hidden" - Should the values on the y-axis be hidden on render

            "display" - Should the metric be displayed on the status page

            "decimal_places" - How many decimal places to render on the graph

            "tooltip_description" - Description to show on the tooltip

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/metrics_providers/{metric_provider_id}/metrics"
        return self.post(url, data={"metric": metric})

    def page_list_metric_providers(self, page_id):
        """
        Get a list of metric providers

        Parameters
        ----------
        page_id : str
            Your page unique ID
        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdMetricsProviders

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/metrics_providers"
        return self.get(url)

    def page_create_metric_provider(self, page_id, metric_provider):
        """
        Create a metric provider

        Parameters
        ----------
        page_id : str
            Your page unique ID
        metric_provider : dict[str, any]
            The metric provider to create

            Available fields in metric_provider: "email", "password", "api_key", "api_token",
            "application_key", "type", "metric_base_uri"

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/postPagesPageIdMetricsProviders

        Descriptions of the fields that can be added to the metric_provider:
            "email" - Required by the Librato metrics provider

            "password" - Just a password!

            "api_key" - Required by the Datadog and NewRelic type metrics providers

            "api_token" - Required by the Librato, Datadog and Pingdom type metrics providers

            "application_key" - Required by the Pingdom-type metrics provider

            "type" - The type of metrics provider. See MetricProviderType enum for available values

            "metric_base_uri" - The base URI for the metrics provider.
            Required by the Datadog and NewRelic type metrics providers.


        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/metrics_providers"
        return self.post(url, data={"metric_provider": metric_provider})

    def page_get_metric_provider(self, page_id, metric_provider_id):
        """
        Get a metric provider

        Parameters
        ----------
        page_id : str
            Your page unique ID
        metric_provider_id : str
            Metric provider identifier

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdMetricsProvidersMetricsProviderId

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/metrics_providers/{metric_provider_id}"
        return self.get(url)

    def page_update_metric_provider(self, page_id, metric_provider_id, metric_provider):
        """
        Update a metric provider

        Parameters
        ----------
        page_id : str
            Your page unique ID
        metric_provider_id : str
            Metric provider identifier
        metric_provider : dict[str, any]
            Metric provider to update


        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdMetricsProvidersMetricsProviderId

        Available fields in metric_provider: "type", "metric_base_uri"

        Descriptions of the fields that can be added to the metric_provider:
            "type" - The type of metrics provider. See MetricProviderType enum for available values

            "metric_base_uri" - The base URI for the metrics provider.
            Required by the Datadog and NewRelic type metrics providers.

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/metrics_providers/{metric_provider_id}"
        return self.patch(url, data={"metric_provider": metric_provider})

    def page_delete_metric_provider(self, page_id, metric_provider_id):
        """
        Delete a metric provider

        Parameters
        ----------
        page_id : str
            Your page unique ID
        metric_provider_id : str
            Metric provider identifier

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = f"v1/pages/{page_id}/metrics_providers/{metric_provider_id}"
        return self.delete(url)
