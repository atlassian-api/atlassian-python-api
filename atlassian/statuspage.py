# coding=utf-8
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

    "to indicate sorting by the identifying field"
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

    def page_get(self, page_id):
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
        url = "v1/pages/{}".format(page_id)
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

        Returns
        -------
        any
        """
        url = "v1/pages/{}".format(page_id)
        return self.put(url, data={"page": page})

    def organization_get_users(self, organization_id, page_offset=0, per_page=100):
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
        page_offset : int
            Page offset to fetch. Beginning February 28, 2023,
            this endpoint will return paginated data even if this query parameter is not provided.
        per_page : int
            Number of results to return per page. Beginning February 28, 2023,
            a default and maximum limit of 100 will be imposed and this endpoint will return paginated data
            even if this query parameter is not provided.
        Returns
        -------
        any
        """
        url = "v1/organizations/{}/users".format(organization_id)
        return self.get(url, params={"page": page_offset, "per_page": per_page})

    def organization_user_permissions(self, organization_id, user_id):
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
        url = "v1/organizations/{}/permissions/{}".format(organization_id, user_id)
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
        url = "v1/organizations/{}/permissions/{}".format(organization_id, user_id)
        return self.put(url, data={"pages": pages})

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
        url = "v1/pages/{}/status_embed_config".format(page_id)
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
        url = "v1/pages/{}/status_embed_config".format(page_id)
        return self.put(url, status_embed_config)

    def page_access_users_list(self, page_id, email, page_offset=0, per_page=100):
        """
        Get a list of page access users

        Parameters
        ----------
        page_id : str
            Your page unique ID
        email : str
            Email address to search for
        page_offset : int
            Page offset to fetch. Beginning February 28, 2023,
            this endpoint will return paginated data even if this query parameter is not provided.
        per_page : int
            Number of results to return per page. Beginning February 28, 2023,
            a default and maximum limit of 100 will be imposed and this endpoint will return paginated data
            even if this query parameter is not provided.

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
        url = "v1/pages/{}/page_access_users".format(page_id)
        return self.get(url, params={"email": email, "page": page_offset, "per_page": per_page})

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
        url = "v1/pages/{}/page_access_users/{}".format(page_id, page_access_user_id)
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
        url = "v1/pages/{}/page_access_users/{}".format(page_id, page_access_user_id)
        return self.put(
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
        url = "v1/pages/{}/page_access_users/{}".format(page_id, page_access_user_id)
        return self.delete(url)

    def page_get_components_access_user(self, page_id, page_access_user_id, page_offset=0, per_page=100):
        """
        Get components for page access user

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_user_id : str
            Page Access User Identifier
        page_offset : int
            Page offset to fetch. Beginning February 28, 2023,
            this endpoint will return paginated data even if this query parameter is not provided.
        per_page : int
            Number of results to return per page. Beginning February 28, 2023,
            a default and maximum limit of 100 will be imposed and this endpoint will return paginated data
            even if this query parameter is not provided.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdPageAccessUsersPageAccessUserIdComponents

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = "v1/pages/{}/page_access_users/{}/components".format(page_id, page_access_user_id)
        return self.get(url, params={"page": page_offset, "per_page": per_page})

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

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = "v1/pages/{}/page_access_users/{}/components".format(page_id, page_access_user_id)
        return self.put(url, data={"component_ids": component_ids})

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

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = "v1/pages/{}/page_access_users/{}/components".format(page_id, page_access_user_id)
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

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = "v1/pages/{}/page_access_users/{}/components".format(page_id, page_access_user_id)
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

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = "v1/pages/{}/page_access_users/{}/components/{}".format(page_id, page_access_user_id, component_id)
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
        
        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info
            
        Returns
        -------
        any
        """
        url = "v1/pages/{}/page_access_users/{}/metrics".format(page_id, page_access_user_id)
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
        
        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info
            
        Returns
        -------
        any
        """
        url = "v1/pages/{}/page_access_users/{}/metrics".format(page_id, page_access_user_id)
        return self.put(url, data={"metric_ids": metric_ids})

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
        
        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info
            
        Returns
        -------
        any
        """
        url = "v1/pages/{}/page_access_users/{}/metrics".format(page_id, page_access_user_id)
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

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = "v1/pages/{}/page_access_users/{}/metrics".format(page_id, page_access_user_id)
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
        
        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info
            
        Returns
        -------
        any
        """
        url = "v1/pages/{}/page_access_users/{}/metrics/{}".format(page_id, page_access_user_id, metric_id)
        return self.delete(url)

    def page_get_access_groups(self, page_id, page_offset=0, per_page=100):
        """
        Get a list of page access groups
        
        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_offset : int
            Page offset to fetch. Beginning February 28, 2023,
            this endpoint will return paginated data even if this query parameter is not provided.
        per_page : int
            Number of results to return per page. Beginning February 28, 2023,
            a default and maximum limit of 100 will be imposed and this endpoint will return paginated data
            even if this query parameter is not provided.
        
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
        url = "v1/pages/page_access_groups".format(page_id)
        return self.get(url, params={"page": page_offset, "per_page": per_page})

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
        url = "v1/pages/{}/page_access_groups/{}".format(page_id, page_access_group_id)
        return self.get(url)

    def page_create_access_group(self, page_id, name, external_identifier, component_ids, metric_ids,
                                 page_access_user_ids):
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
        url = "v1/pages/{}/page_access_groups".format(page_id)
        return self.post(url, data={"page_access_group": {
            "name": name,
            "external_identifier": external_identifier,
            "component_ids": component_ids,
            "metric_ids": metric_ids,
            "page_access_user_ids": page_access_user_ids
        }})

    def page_replace_access_group(self, page_id, page_access_group_id, name, external_identifier, component_ids,
                                  metric_ids, page_access_user_ids):
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
        url = "v1/pages/{}/page_access_groups/{}".format(page_id, page_access_group_id)
        return self.put(url, data={"page_access_group": {
            "name": name,
            "external_identifier": external_identifier,
            "component_ids": component_ids,
            "metric_ids": metric_ids,
            "page_access_user_ids": page_access_user_ids
        }})

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
        
        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info
            
        Returns
        -------
        any
        """
        url = "v1/pages/{}/page_access_groups/{}".format(page_id, page_access_group_id)
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
        url = "v1/pages/{}/page_access_groups/{}/components".format(page_id, page_access_group_id)
        return self.put(url, data={"component_ids": component_ids})

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
        
        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info
            
        Returns
        -------
        any
        """
        url = "v1/pages/{}/page_access_groups/{}/components".format(page_id, page_access_group_id)
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

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = "v1/pages/{}/page_access_groups/{}/components".format(page_id, page_access_group_id)
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

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = "v1/pages/{}/page_access_groups/{}/components/{}".format(page_id, page_access_group_id, component_id)
        return self.delete(url)

    def page_get_components_for_access_group(self, page_id, page_access_group_id, page_offset=0, per_page=100):
        """
        Add components to page access group

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_access_group_id : str
            Page Access Group Identifier
        page_offset : int
            Page offset to fetch. Beginning February 28, 2023,
            this endpoint will return paginated data even if this query parameter is not provided.
        per_page : int
            Number of results to return per page. Beginning February 28, 2023,
            a default and maximum limit of 100 will be imposed and this endpoint will return paginated data
            even if this query parameter is not provided.

        Notes
        -----
        See available fields: https://developer.statuspage.io/#operation/getPagesPageIdPageAccessGroupsPageAccessGroupIdComponents

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = "v1/pages/{}/page_access_groups/{}/components".format(page_id, page_access_group_id)
        return self.get(url)

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
        url = "v1/pages/{}/subscribers/{}".format(page_id, subscriber_id)
        return self.get(url)

    def page_get_subscribers(self, page_id, q, subscriber_type, subscriber_state, sort_field, sort_direction,
                             page_offset=0, per_page=100):
        """
        Get all subscribers

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_offset : int
            Page offset to fetch. Beginning February 28, 2023,
            this endpoint will return paginated data even if this query parameter is not provided.
        per_page : int
            Number of results to return per page. Beginning February 28, 2023,
            a default and maximum limit of 100 will be imposed and this endpoint will return paginated data
            even if this query parameter is not provided.
        q : str
            If this is specified, search the contact information (email, endpoint, or phone number) for the provided value.
            This parameter doesn't support searching for Slack subscribers.
        subscriber_type : SubscriberType
            If this is specified, only return subscribers of the specified type.
        subscriber_state : SubscriberState
            If this is specified, only return subscribers of the specified state.
            Specify state "all" to find subscribers in any states.
        sort_field : SortField
            The field on which to sort
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
        url = "v1/pages/{}/subscribers".format(page_id)
        return self.get(url, params={
            "page": page_offset,
            "per_page": per_page,
            "q": q,
            "type": subscriber_type,
            "state": subscriber_state,
            "sort_field": sort_field,
            "sort_direction": sort_direction
        })

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
        url = "v1/pages/{}/subscribers/{}".format(page_id, subscriber_id)
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
        url = "v1/pages/{}/subscribers/{}".format(page_id, subscriber_id)
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

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = "v1/pages/{}/subscribers/{}/resend_confirmation".format(page_id, subscriber_id)
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
        url = "v1/pages/{}/subscribers".format(page_id)
        return self.post(url, data={"subscriber": subscriber})

    def page_get_list_unsubscribed(self, page_id, page_offset=0, per_page=100):
        """
        Get a list of unsubscribed subscribers

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_offset : int
            Page offset to fetch. Beginning February 28, 2023,
            this endpoint will return paginated data even if this query parameter is not provided.
        per_page : int
            Number of results to return per page. Beginning February 28, 2023,
            a default and maximum limit of 100 will be imposed and this endpoint will return paginated data
            even if this query parameter is not provided.

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
        url = "v1/pages/{}/unsubscribed".format(page_id)
        return self.get(url, params={
            "page": page_offset,
            "per_page": per_page
        })

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
        url = "v1/pages/{}/subscribers/count".format(page_id)
        return self.get(url, params={
            "type": subscriber_type,
            "state": subscriber_state
        })

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
        url = "v1/pages/{}/subscribers/histogram".format(page_id)
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
        url = "v1/pages/{}/subscribers/reactivate".format(page_id)
        return self.post(url, data={"subscribers": subscriber_ids, "type": subscriber_type})

    def page_unsubscribe_subscribers(self, page_id, subscriber_ids, subscriber_type,
                                     skip_unsubscription_notification=False):
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
        url = "v1/pages/{}/subscribers/unsubscribe".format(page_id)
        return self.post(url, data={"subscribers": subscriber_ids, "type": subscriber_type,
                                    "skip_unsubscription_notification": skip_unsubscription_notification})

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
        url = "v1/pages/{}/subscribers/resend_confirmation".format(page_id)
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
        url = "v1/pages/{}/templates".format(page_id)
        return self.post(url, data={"template": template})

    def page_get_templates(self, page_id, page_offset=1, per_page=100):
        """
        Get a list of templates

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_offset : int
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
        url = "v1/pages/{}/templates".format(page_id)
        return self.get(url, params={
            "page": page_offset,
            "per_page": per_page
        })

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
        url = "v1/pages/{}/incidents".format(page_id)
        return self.post(url, data={"incident": incident})

    def page_list_incidents(self, page_id, q, page_offset=1, per_page=100):
        """
        Get a list of incidents

        Parameters
        ----------
        page_id : str
            Your page unique ID
        q : str
            The search query to filter incidents by. If this is specified, search for the text query string in
            the incident's name, status, postmortem_body, and incident_updates fields.
        page_offset : int
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
        url = "v1/pages/{}/incidents".format(page_id)
        return self.get(url, params={
            "q": q,
            "page": page_offset,
            "per_page": per_page
        })

    def page_list_active_maintances(self, page_id, page_offset=1, per_page=100):
        """
        Get a list of active maintenances

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_offset : int
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
        url = "v1/pages/{}/incidents/active_maintenance".format(page_id)
        return self.get(url, params={
            "page": page_offset,
            "per_page": per_page
        })

    def page_list_upcoming_incidents(self, page_id, page_offset=1, per_page=100):
        """
        Get a list of upcoming incidents

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_offset : int
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
        url = "v1/pages/{}/incidents/upcoming".format(page_id)
        return self.get(url, params={
            "page": page_offset,
            "per_page": per_page
        })

    def page_list_scheduled_incidents(self, page_id, page_offset=1, per_page=100):
        """
        Get a list of scheduled incidents

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_offset : int
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
        url = "v1/pages/{}/incidents/scheduled".format(page_id)
        return self.get(url, params={
            "page": page_offset,
            "per_page": per_page
        })

    def page_list_unresolved_incidents(self, page_id, page_offset=1, per_page=100):
        """
        Get a list of unresolved incidents

        Parameters
        ----------
        page_id : str
            Your page unique ID
        page_offset : int
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
        url = "v1/pages/{}/incidents/unresolved".format(page_id)
        return self.get(url, params={
            "page": page_offset,
            "per_page": per_page
        })

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
        url = "v1/pages/{}/incidents/{}".format(page_id, incident_id)
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
        url = "v1/pages/{}/incidents/{}".format(page_id, incident_id)
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
        url = "v1/pages/{}/incidents/{}".format(page_id, incident_id)
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

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = "v1/pages/{}/incidents/{}/incidents_update/{}".format(page_id, incident_id, incident_update_id)
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
        url = "v1/pages/{}/incidents/{}/subscribers".format(page_id, incident_id)
        return self.post(url, data={"subscriber": subscriber})

    def page_list_incident_subscribers(self, page_id, incident_id, page_offset=1, per_page=100):
        """
        Get a list of subscribers for an incident

        Parameters
        ----------
        page_id : str
            Your page unique ID
        incident_id : str
            The incident unique ID
        page_offset : int
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
        url = "v1/pages/{}/incidents/{}/subscribers".format(page_id, incident_id)
        return self.get(url)

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
        url = "v1/pages/{}/incidents/{}/subscribers/{}".format(page_id, incident_id, subscriber_id)
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

        Raises
        ------
        requests.exceptions.HTTPError
            Use `json.loads(exceptions.response.content)` to get API error info

        Returns
        -------
        any
        """
        url = "v1/pages/{}/incidents/{}/subscribers/{}".format(page_id, incident_id, subscriber_id)
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
        url = "v1/pages/{}/incidents/{}/subscribers/{}/resend_confirmation".format(page_id, incident_id, subscriber_id)
        return self.post(url)