# coding=utf-8
import logging
from enum import Enum

from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Branding(Enum):
    """The main template your statuspage will use"""

    PREMIUM = "premium"
    BASIC = "basic"


class StatusPage(AtlassianRestAPI):
    """StatusPage API wrapper."""

    def __init__(self, *args, **kwargs):
        super(StatusPage, self).__init__(*args, **kwargs)

    def list_pages(self):
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
        url = "v1/pages/{}".format(page_id)
        return self.get(url)

    def update_page(self, page_id, page):
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

    def get_embed_config_settings(self, page_id):
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

    def update_embed_config_settings(self, page_id, status_embed_config):
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
        >>> client.update_embed_config_settings(
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
