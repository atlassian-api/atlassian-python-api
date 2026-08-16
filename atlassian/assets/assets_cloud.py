# coding=utf-8
import logging

from ..rest_client import AtlassianRestAPI

# from deprecated import deprecated

log = logging.getLogger(__name__)


class AssetsCloud(AtlassianRestAPI):
    """Assets for Jira API wrapper."""

    # https://developer.atlassian.com/cloud/assets/rest

    def __init__(self, *args, **kwargs):
        """
        Initialize Assets()

        :param args:
        :param kwargs:
        :return: Assets()
        """
        kwargs["api_root"] = "rest/assets/1.0"
        # If cloud is set to true, trigger private __cloud__init method
        if kwargs.get("cloud"):
            args, kwargs = self.__cloud_init(*args, **kwargs)
        super(AssetsCloud, self).__init__(*args, **kwargs)

    def __cloud_init(self, *args, **kwargs):
        """
        Creates a Cloud specific version of Assets()

        Returns:
            Assets(AtlassianRestAPI)
        """
        # trigger a normal init and avoid looping
        del kwargs["cloud"]
        temp = AssetsCloud(*args, **kwargs)
        # retrieve cloud workspace id and generate the api_root
        kwargs["api_root"] = f"/jsm/assets/workspace/{temp.__get_workspace_id()}/v1/"
        # Assets cloud uses the atlassian base url, not custom instance urls
        kwargs["url"] = "https://api.atlassian.com"
        # set cloud back to true and return
        kwargs["cloud"] = True
        # Assets cloud is particular about its headers.
        self.default_headers = {"Accept": "application/json", "Content-Type": "application/json"}
        return args, kwargs

    def __get_workspace_id(self):
        result = self.get(
            "rest/servicedeskapi/assets/workspace",
            headers=self.default_headers,
        )
        return result["values"][0]["workspaceId"]

    def _get_assets_workspace_ids(self):
        """
        Returns all Assets workspace Ids.
        :return: List
        """
        result = self.get(
            "rest/servicedeskapi/assets/workspace",
            headers=self.experimental_headers,
        )
        return [i["workspaceId"] for i in result["values"]]

    def _get_assets_workspace_id(self):
        """
        Returns the first Assets workspace ID.
        :return: str
        """
        return next(iter(self._get_assets_workspace_ids()))

    @staticmethod
    def _params(**kwargs):
        """Drop unset query parameters while preserving false/zero values."""
        return {key: value for key, value in kwargs.items() if value is not None}

    # Attachments
    def get_attachments_of_objects(self, object_id):
        """
        Get Attachment info
        Example output:
        [
            {
                "id": 1,
                "author": "admin",
                "mimeType": "image/png",
                "filename": "astronaut.png",
                "filesize": "490 B",
                "created": "2019-11-27T11:42:22.283Z",
                "comment": "",
                "commentOutput": "",
                "url": "http://jira/rest/assets/1.0/attachments/1"
            }
        ]

        :param object_id Object ID
        :return list of object
            id: required(string)
            author: (string)
            mimeType: (string)
            filename: required(string)
            filesize: (string)
            created: required(datetime)
            comment: (string)
            commentOutput: (string)
            url: required(string)
        """
        if self.cloud:
            raise NotImplementedError
        url = self.url_joiner(
            self.api_root,
            f"attachments/object/{object_id}",
        )
        return self.get(url)

    def upload_attachment_to_object(self, object_id, filename):
        """
        Add attachment to Object
        :param object_id: int
        :param filename: str, name, if file in current directory or full path to file
        """
        if self.cloud:
            raise NotImplementedError
        log.info("Adding attachment...")
        url = f"rest/assets/1.0/attachments/object/{object_id}"
        with open(filename, "rb") as attachment:
            files = {"file": attachment}
            return self.post(url, headers=self.no_check_headers, files=files)

    def delete_attachment(self, attachment_id):
        """
        Add attachment to Object
        :param attachment_id: int
        """
        if self.cloud:
            raise NotImplementedError
        log.info("Deleting attachment...")
        url = f"rest/assets/1.0/attachments/{attachment_id}"
        return self.delete(url)

    # Comments
    # Handle comments on objets
    def add_comment_to_object(self, comment, object_id, role):
        """
        Add comment to Object

        :param comment: str
        :param object_id: int - Object ID
        :param role: int - Role ID
            0	Assets Users
            1	Assets Managers
            2	Assets Administrators
            3	Assets Developers
        :return:
        {
            "created": "2019-11-27T12:37:41.492Z",
            "updated": "2019-11-27T12:37:41.492Z",
            "id": 1,
            "actor": {
                "avatarUrl": "https://www.gravatar.com/avatar/64e1b8d34f425d19e1ee2ea7236d3028?d=mm&s=48",
                "displayName": "admin",
                "name": "admin",
                "key": "admin",
                "renderedLink": "<a href=\"/jira/secure/ViewProfile.jspa?name=admin\">admin</a>",
                "isDeleted": false
            },
            "role": 0,
            "comment": "A comment to be added",
            "commentOutput": "A comment to be added",
            "objectId": 1,
            "canEdit": true,
            "canDelete": true
        }
        """
        if self.cloud:
            raise NotImplementedError
        params = {"comment": comment, "objectId": object_id, "role": role}
        url = "rest/assets/1.0/comment/create"
        return self.post(url, data=params)

    def get_comment_of_object(self, object_id):
        """
        The object id to fetch comments from

        :param object_id:
        :return:
        """
        if self.cloud:
            raise NotImplementedError
        url = f"rest/assets/1.0/comment/object/{object_id}"
        return self.get(url)

    # Icon
    # Resources dedicated to load and find icons
    def get_icon_by_id(self, icon_id):
        """
        Load a single icon by id

        :param icon_id:
        :return:
        {
            "id": 1,
            "name": "Delete",
            "url16": "http://jira/rest/assets/1.0/icon/1/icon.png?size=16",
            "url48": "http://jira/rest/assets/1.0/icon/1/icon.png?size=48"
        }
        """
        url = self.url_joiner(self.api_root, f"icon/{icon_id}")
        return self.get(url)

    def get_all_global_icons(self):
        """
        All existing global icons

        :return:
        """
        url = self.url_joiner(self.api_root, "icon/global")
        return self.get(url)

    def get_icon_image(self, icon_id, not_json_response=True):
        """Return the binary image for an Assets icon."""
        url = self.url_joiner(self.api_root, f"icon/{icon_id}/icon.png")
        return self.get(url, not_json_response=not_json_response)

    # Import
    # Start configured imports. To see an ongoing import see the Progress resource
    def start_import_configuration(self, import_id):
        """
        The id of the import configuration that should be started

        :param import_id:
        :return:
        """
        url = self.url_joiner(
            self.api_root,
            f"import/start/{import_id}",
        )
        return self.post(url)

    def get_import_source(self, import_source_id):
        return self.get(self.url_joiner(self.api_root, f"importsource/{import_source_id}"))

    def update_import_source_mapping(self, import_source_id, data, partial=False):
        url = self.url_joiner(self.api_root, f"importsource/{import_source_id}/mapping")
        if partial:
            return self.patch(url, data=data)
        return self.put(url, data=data)

    def get_import_mapping_progress(self, import_source_id, resource_id):
        url = self.url_joiner(self.api_root, f"importsource/{import_source_id}/mapping/progress/{resource_id}")
        return self.get(url)

    def get_import_config_status(self, import_source_id):
        return self.get(self.url_joiner(self.api_root, f"importsource/{import_source_id}/configstatus"))

    def get_import_schema_and_mapping(self, import_source_id):
        return self.get(self.url_joiner(self.api_root, f"importsource/{import_source_id}/schema-and-mapping"))

    def create_import_execution(self, import_source_id, data=None):
        url = self.url_joiner(self.api_root, f"importsource/{import_source_id}/executions")
        return self.post(url, data=data)

    def delete_import_execution(self, import_source_id, import_execution_id):
        url = self.url_joiner(self.api_root, f"importsource/{import_source_id}/executions/{import_execution_id}")
        return self.delete(url)

    def update_import_execution_progress(self, import_source_id, import_execution_id, data=None):
        url = self.url_joiner(
            self.api_root, f"importsource/{import_source_id}/executions/{import_execution_id}/progress"
        )
        return self.put(url, data=data)

    def add_import_execution_data(self, import_source_id, import_execution_id, data=None):
        url = self.url_joiner(self.api_root, f"importsource/{import_source_id}/executions/{import_execution_id}/data")
        return self.post(url, data=data)

    def get_import_execution_status(self, import_source_id, import_execution_id):
        url = self.url_joiner(self.api_root, f"importsource/{import_source_id}/executions/{import_execution_id}/status")
        return self.get(url)

    def get_import_executions_status(self, import_source_id):
        return self.get(self.url_joiner(self.api_root, f"importsource/{import_source_id}/executions/status"))

    def add_failed_import_execution_history(self, import_source_id, execution_id, data=None):
        url = self.url_joiner(
            self.api_root, f"importsource/{import_source_id}/executions/{execution_id}/history/failed"
        )
        return self.post(url, data=data)

    def create_import_token(self, import_source_id, data=None):
        return self.post(self.url_joiner(self.api_root, f"importsource/{import_source_id}/token"), data=data)

    def get_import_schedule(self, import_source_id):
        return self.get(self.url_joiner(self.api_root, f"importsource/{import_source_id}/schedule"))

    # Index
    # Handle the indexing of Assets
    def reindex_assets(self):
        """
        Should the reindex clean the index before doing the reindex

        :return:
        """
        if self.cloud:
            raise NotImplementedError
        url = self.url_joiner(self.api_root, "index/reindex/start")
        return self.post(url)

    def reindex_current_node_assets(self):
        """
        Should the reindex clean the index before doing the reindex

        :return:
        """
        if self.cloud:
            raise NotImplementedError
        url = self.url_joiner(self.api_root, "index/reindex/currentnode")
        return self.post(url)

    # AQL
    # Fetch Objects by AQL
    # Cloud-only. Server use navlist_aql()
    # https://developer.atlassian.com/cloud/assets/rest/api-group-object/#api-object-aql-post
    def aql(self, query, start=0, max_results=25, include_attributes=True):
        """
        Resource dedicated to finding objects based on the Assets Query Language (AQL)

        :param query:
        :param start:
        :param max_results:
        :param include_attributes:
        :return:
        """
        if not self.cloud:
            raise NotImplementedError
        params = {"startAt": start, "maxResults": max_results, "includeAttributes": include_attributes}
        data = {"qlQuery": query}
        url = self.url_joiner(self.api_root, "object/aql")
        return self.post(url, params=params, data=data)

    def get_aql_objects(
        self,
        query=None,
        page=None,
        result_per_page=None,
        include_attributes=None,
        include_attributes_deep=None,
        include_type_attributes=None,
        include_extended_info=None,
    ):
        """Retrieve objects through the legacy AQL collection endpoint."""
        params = self._params(
            qlQuery=query,
            page=page,
            resultPerPage=result_per_page,
            includeAttributes=include_attributes,
            includeAttributesDeep=include_attributes_deep,
            includeTypeAttributes=include_type_attributes,
            includeExtendedInfo=include_extended_info,
        )
        return self.get(self.url_joiner(self.api_root, "aql/objects"), params=params or None)

    def get_iql_objects(
        self,
        query=None,
        page=None,
        result_per_page=None,
        include_attributes=None,
        include_attributes_deep=None,
        include_type_attributes=None,
        include_extended_info=None,
    ):
        """Retrieve objects through the IQL collection endpoint."""
        params = self._params(
            iql=query,
            page=page,
            resultPerPage=result_per_page,
            includeAttributes=include_attributes,
            includeAttributesDeep=include_attributes_deep,
            includeTypeAttributes=include_type_attributes,
            includeExtendedInfo=include_extended_info,
        )
        return self.get(self.url_joiner(self.api_root, "iql/objects"), params=params or None)

    def iql(self, query, start=0, max_results=25, include_attributes=True):
        """Find Assets objects using the IQL-compatible Cloud endpoint."""
        params = self._params(startAt=start, maxResults=max_results, includeAttributes=include_attributes)
        return self.post(self.url_joiner(self.api_root, "object/aql"), params=params, data={"qlQuery": query})

    # Navlist AQL
    # Retrieve a list of objects based on an AQL query
    # Server-only. Cloud use aql()
    # https://developer.atlassian.com/server/jira-servicedesk/rest/v1006/api-group-assets---object/#api-assets-1-0-object-navlist-aql-post
    def navlist_aql(
        self,
        query,
        object_schema_id,
        page=1,
        order_by_attribute_id=None,
        order_asc=True,
        result_per_page=25,
        include_attributes=True,
        include_attributes_deep=1,
        include_type_attributes=False,
        include_extended_info=False,
        extended=None,
    ):
        """
        Resource dedicated to finding objects based on the Insight Query Language (IQL)

        :param query:
        :param object_schema_id:
        :param page:
        :param order_by_attribute_id:
        :param order_asc:
        :param result_per_page:
        :param include_attributes:
        :param include_attributes_deep:
        :param include_type_attributes:
        :param include_extended_info:
        :param extended:
        :return:
        """
        if self.cloud:
            raise NotImplementedError
        data = {
            "qlQuery": query,
            "objectSchemaId": object_schema_id,
            "page": page,
            "orderAsc": order_asc,
            "resultPerPage": result_per_page,
            "includeAttributes": include_attributes,
            "includeAttributesDeep": include_attributes_deep,
            "includeTypeAttributes": include_type_attributes,
            "includeExtendedInfo": include_extended_info,
        }
        if order_by_attribute_id:
            data["orderByAttributeId"] = order_by_attribute_id
        if extended:
            data["extended"] = extended
        url = self.url_joiner(self.api_root, "object/navlist/aql")
        return self.get(url, data=data)

    # Object
    def get_object(self, object_id):
        """
        Load one object

        :param object_id:
        :return:
        """
        url = self.url_joiner(self.api_root, f"object/{object_id}")
        return self.get(url)

    def update_object(
        self,
        object_id,
        object_type_id,
        attributes,
        has_avatar=False,
        avatar_uuid="",
    ):
        """
        Update an existing object in Assets

        :param object_id:
        :param object_type_id:
        :param attributes:
        :param has_avatar:
        :param avatar_uuid:
        :return:
        """
        body = {
            "attributes": attributes,
            "objectTypeId": object_type_id,
            "avatarUUID": avatar_uuid,
            "hasAvatar": has_avatar,
        }
        url = self.url_joiner(self.api_root, f"object/{object_id}")
        return self.put(url, data=body)

    def delete_object(self, object_id):
        """
        Delete the referenced object

        :param object_id:
        :return:
        """
        url = self.url_joiner(self.api_root, f"object/{object_id}")
        return self.delete(url)

    def get_object_attributes(self, object_id):
        """
        List all attributes for the given object

        :param object_id:
        :return:
        """
        url = self.url_joiner(self.api_root, f"object/{object_id}/attributes")
        return self.get(url)

    def get_object_attribute_value(self, object_id, attribute_id, default=None):
        """Return the first value for an object type attribute.

        Assets exposes object attributes as a collection rather than a
        dedicated value endpoint.  This helper fetches that collection and
        selects the entry whose ``objectTypeAttributeId`` matches
        ``attribute_id``.  ``None`` (or ``default``) is returned when the
        attribute is absent or has no values.

        :param object_id: Assets object ID
        :param attribute_id: object type attribute ID
        :param default: value returned when no matching value exists
        """
        attributes = self.get_object_attributes(object_id)
        if isinstance(attributes, dict):
            attributes = attributes.get("objectAttributeBeans", attributes.get("values", []))
        if not isinstance(attributes, list):
            return default

        for attribute in attributes:
            if not isinstance(attribute, dict):
                continue
            object_type_attribute = attribute.get("objectTypeAttribute") or {}
            current_id = attribute.get("objectTypeAttributeId", object_type_attribute.get("id"))
            if str(current_id) != str(attribute_id):
                continue

            values = attribute.get("objectAttributeValues")
            if values is None:
                values = attribute.get("values")
            if values:
                value = values[0]
                return value.get("value") if isinstance(value, dict) else value
            if "value" in attribute:
                return attribute["value"]
            return default
        return default

    def get_object_history(self, object_id, asc=False, abbreviate=True):
        """
        Retrieve the history entries for this object

        :param object_id:
        :param asc:
        :param abbreviate:
        :return:
        """
        params = {"asc": asc, "abbreviate": abbreviate}
        url = self.url_joiner(self.api_root, f"object/{object_id}/history")
        return self.get(url, params=params)

    def get_object_reference_info(self, object_id):
        """
        Find all references for an object

        :param object_id:
        :return:
        """
        url = self.url_joiner(self.api_root, f"object/{object_id}/referenceinfo")
        return self.get(url)

    def search_objects_aql(self, query, start=0, max_results=25, include_attributes=True):
        return self.aql(query, start=start, max_results=max_results, include_attributes=include_attributes)

    def search_objects_iql(self, query, start=0, max_results=25, include_attributes=True):
        return self.iql(query, start=start, max_results=max_results, include_attributes=include_attributes)

    def search_objects_aql_navigation(self, data=None):
        return self.post(self.url_joiner(self.api_root, "object/navlist/aql"), data=data)

    def search_objects_iql_navigation(self, data=None):
        return self.post(self.url_joiner(self.api_root, "object/navlist/iql"), data=data)

    def get_object_aql_total_count(self, query):
        return self.post(self.url_joiner(self.api_root, "object/aql/totalcount"), data={"qlQuery": query})

    def create_object(self, object_type_id, attributes, has_avatar=False, avatar_uuid=""):
        """
        Create a new object in Assets

        :param object_type_id:
        :param attributes:
        :param has_avatar:
        :param avatar_uuid:
        :return:
        :return:
        """
        data = {
            "attributes": attributes,
            "objectTypeId": object_type_id,
            "avatarUUID": avatar_uuid,
            "hasAvatar": has_avatar,
        }
        url = self.url_joiner(self.api_root, "object/create")
        return self.post(url, data=data)

    # Objectconnectedtickets
    def get_object_connected_tickets(self, object_id):
        """
        Relation between Jira issues and Assets objects

        :param object_id:
        :return:
        """
        url = self.url_joiner(
            self.api_root,
            f"objectconnectedtickets/{object_id}/tickets",
        )
        return self.get(url)

    def list_object_schema(self):
        """
        Resource to find object schemas in Assets
        :return:
        {
            "objectschemas": [
            {
                "id": 1,
                "name": "Test",
                "objectSchemaKey": "TEST",
                "status": "Ok",
                "created": "2019-11-26T08:05:46.894Z",
                "updated": "2019-11-26T08:05:46.894Z",
                "objectCount": 2,
                "objectTypeCount": 3
            }
            ]
        }
        """
        url = self.url_joiner(self.api_root, "objectschema/list")
        return self.get(url)

    def create_object_schema(self, object_schema_key, description):
        data = {"objectSchemaKey": object_schema_key, "description": description}
        return self.post(self.url_joiner(self.api_root, "objectschema/create"), data=data)

    def get_object_schema(self, schema_id):
        """
        Find a schema by id
        :param schema_id:
        """
        url = self.url_joiner(self.api_root, f"objectschema/{schema_id}")
        return self.get(url)

    def update_object_schema(self, schema_id, data=None):
        """
        Update an object schema
        """
        return self.put(self.url_joiner(self.api_root, f"objectschema/{schema_id}"), data=data)

    def delete_object_schema(self, schema_id):
        """
        Delete a schema
        """
        return self.delete(self.url_joiner(self.api_root, f"objectschema/{schema_id}"))

    def get_object_schema_attributes(self, schema_id):
        """
        Find all object type attributes for this object schema
        """
        return self.get(self.url_joiner(self.api_root, f"objectschema/{schema_id}/attributes"))

    def get_object_schema_object_types(self, schema_id):
        return self.get(self.url_joiner(self.api_root, f"objectschema/{schema_id}/objecttypes"))

    def get_object_schema_object_types_flat(self, schema_id, query=None, exclude=None, includeObjectCounts=None):
        """
        Find all object types for this object schema
        https://developer.atlassian.com/cloud/assets/rest/api-group-objectschema/#api-objectschema-id-objecttypes-flat-get
        Args:
            schema_id (str): id of the object schema
            query (bool, optional): Object Type Names to search for, defaults to None (Use API default)
            exclude (str, optional): Exclude objects with this name, defaults to None (Use API default)
            includeObjectCounts (bool, optional): Populate objectCount attribute for each object type, defaults to None (Use API default)
        """
        kwargs = list(locals().items())
        params = dict()
        params.update({k: v for k, v in kwargs if v is not None and k not in ["self", "schema_id"]})
        return self.get(
            f"{self.api_root}/objectschema/{schema_id}/objecttypes/flat",
            params=params,
        )

    def get_object_type_attributes(
        self,
        type_id,
        only_value_editable=None,
        order_by_name=None,
        query=None,
        include_values_exist=None,
        exclude_parent_attributes=None,
        include_children=None,
        order_by_required=None,
    ):
        """
        Find all attributes for this object type
        https://developer.atlassian.com/cloud/assets/rest/api-group-objecttype/#api-objecttype-id-attributes-get
        Args:
            type_id (str): id of the object type
            only_value_editable (bool, optional): only return editable values, defaults to None (Use API default)
            order_by_name (bool, optional): values, defaults to None (Use API default)
            query (str, optional): Not documented in API, defaults to None (Use API default)
            include_values_exist (bool, optional): Include only where values exist, defaults to None (Use API default)
            exclude_parent_attributes (bool, optional): Exclude parent attributes, defaults to None (Use API default)
            include_children (bool, optional): include attributes from children, defaults to None (Use API default)
            order_by_required (bool, optional): Order by required fields, defaults to None (Use API default)
        """

        params = {
            "onlyValueEditable": only_value_editable,
            "orderByName": order_by_name,
            "query": query,
            "includeValuesExist": include_values_exist,
            "excludeParentAttributes": exclude_parent_attributes,
            "includeChildren": include_children,
            "orderByRequired": order_by_required,
        }
        params = {k: v for k, v in params.items() if v is not None}

        return self.get(
            f"{self.api_root}/objecttype/{type_id}/attributes",
            headers=self.experimental_headers,
            params=params,
        )

    # Objecttype
    # TODO: Post objecttype {id} position:
    #       https://developer.atlassian.com/cloud/assets/rest/api-group-objecttype/#api-objecttype-id-position-post
    # TODO: Post objecttype create:
    #       https://developer.atlassian.com/cloud/assets/rest/api-group-objecttype/#api-objecttype-create-post

    # Assets ObjectTypeAttribute API
    # TODO: Post objecttypeattribute {objectTypeId}:
    #       https://developer.atlassian.com/cloud/assets/rest/api-group-objecttypeattribute/#api-objecttypeattribute-objecttypeid-post
    # TODO: Put objecttypeattribute {objectTypeId} {id}:
    #       https://developer.atlassian.com/cloud/assets/rest/api-group-objecttypeattribute/#api-objecttypeattribute-objecttypeid-id-put
    # TODO: Delete objecttypeattribute {id}:
    #       https://developer.atlassian.com/cloud/assets/rest/api-group-objecttypeattribute/#api-objecttypeattribute-id-delete

    # Assets Progress API
    # TODO: Get progress category imports {id}:
    #       https://developer.atlassian.com/cloud/assets/rest/api-group-progress/#api-progress-category-imports-id-get
    def get_progress_of_reindex(self):
        """
        Show ongoing assets processes
        :return:
        """
        if self.cloud:
            raise NotImplementedError
        # Yes, the Assets Server API still uses "insight-reindex" as a category (as of April 2025)
        # https://developer.atlassian.com/server/jira-servicedesk/rest/v1006/api-group-assets---progress/#api-assets-1-0-progress-category-category-resourceid-get
        url = self.url_joiner(self.api_root, "progress/category/insight-reindex/reindex")
        return self.get(url)

    def get_progress_of_import(self, import_id):
        """
        Show ongoing assets processes
        :type import_id: int: The id of the import source configuration
                              that the progress should be fetched for
        :return:
        """
        if self.cloud:
            raise NotImplementedError
        url = self.url_joiner(self.api_root, f"progress/category/imports/{import_id}")
        return self.get(url)

    def get_import_progress(self, import_id):
        """Return progress for a Cloud import."""
        return self.get(self.url_joiner(self.api_root, f"progress/category/imports/{import_id}"))

    # Assets Config API
    # TODO: Get config statustype:
    #       https://developer.atlassian.com/cloud/assets/rest/api-group-config/#api-config-statustype-get
    # TODO: Post config statustype:
    #       https://developer.atlassian.com/cloud/assets/rest/api-group-config/#api-config-statustype-post
    # TODO: Get config statustype {id}:
    #       https://developer.atlassian.com/cloud/assets/rest/api-group-config/#api-config-statustype-id-get
    # TODO: Put config statustype {id}:
    #       https://developer.atlassian.com/cloud/assets/rest/api-group-config/#api-config-statustype-id-put
    # TODO: Delete config statustype {id}:
    #       https://developer.atlassian.com/cloud/assets/rest/api-group-config/#api-config-statustype-id-delete

    # Update Issue with Assets Field
    def update_issue_assets_field(self, key, field_id, assets_keys, add=False):
        """
        Set the value of an Assets field.
        Args:
            key (str): Jira issue key, eg. SFT-446
            field_id (str): The internal Jira name of the Assets field, e.g. customfield_10200
            assets_keys (list): List of Assets objects to associate with the field. Limited
                to 20 objects. If the field only takes a single object pass a single value list.
            add (bool, optional): Add to the existing field rather than setting the field value.
                Defaults to False.
        Returns:
            [type]: The assets object updated.
        """
        base_url = self.resource_url("issue")
        action = "add" if add else "set"
        data = {
            "update": {
                field_id: [{action: [{"key": i} for i in assets_keys]}],
            }
        }
        data = {"fields": {field_id: [{"key": i} for i in assets_keys]}}
        return self.put(f"{base_url}/{key}", data=data)

    # Object type and configuration resources
    def get_object_type(self, object_type_id):
        return self.get(self.url_joiner(self.api_root, f"objecttype/{object_type_id}"))

    def update_object_type(self, object_type_id, data=None):
        return self.put(self.url_joiner(self.api_root, f"objecttype/{object_type_id}"), data=data)

    def delete_object_type(self, object_type_id):
        return self.delete(self.url_joiner(self.api_root, f"objecttype/{object_type_id}"))

    def create_object_type(self, data=None):
        return self.post(self.url_joiner(self.api_root, "objecttype/create"), data=data)

    def move_object_type(self, object_type_id, data=None):
        return self.post(self.url_joiner(self.api_root, f"objecttype/{object_type_id}/position"), data=data)

    def create_object_type_attribute(self, object_type_id, data=None):
        return self.post(self.url_joiner(self.api_root, f"objecttypeattribute/{object_type_id}"), data=data)

    def update_object_type_attribute(self, object_type_id, attribute_id, data=None):
        url = self.url_joiner(self.api_root, f"objecttypeattribute/{object_type_id}/{attribute_id}")
        return self.put(url, data=data)

    def delete_object_type_attribute(self, attribute_id):
        return self.delete(self.url_joiner(self.api_root, f"objecttypeattribute/{attribute_id}"))

    def get_status_types(self):
        return self.get(self.url_joiner(self.api_root, "config/statustype"))

    def create_status_type(self, data=None):
        return self.post(self.url_joiner(self.api_root, "config/statustype"), data=data)

    def get_status_type(self, status_type_id):
        return self.get(self.url_joiner(self.api_root, f"config/statustype/{status_type_id}"))

    def update_status_type(self, status_type_id, data=None):
        return self.put(self.url_joiner(self.api_root, f"config/statustype/{status_type_id}"), data=data)

    def delete_status_type(self, status_type_id):
        return self.delete(self.url_joiner(self.api_root, f"config/statustype/{status_type_id}"))

    def get_reference_types(self):
        return self.get(self.url_joiner(self.api_root, "config/referencetype"))

    def create_reference_type(self, data=None):
        return self.post(self.url_joiner(self.api_root, "config/referencetype"), data=data)

    def set_object_schema_property(self, schema_id, data=None):
        url = self.url_joiner(self.api_root, f"global/config/objectschema/{schema_id}/property")
        return self.post(url, data=data)

    def create_import_schedule(self, import_source_id, data=None):
        url = self.url_joiner(self.api_root, f"importsource/{import_source_id}/importschedule")
        return self.post(url, data=data)

    def get_import_schedule_by_id(self, import_source_id, import_schedule_id):
        url = self.url_joiner(self.api_root, f"importsource/{import_source_id}/importschedule/{import_schedule_id}")
        return self.get(url)

    def update_import_schedule(self, import_source_id, import_schedule_id, data=None):
        url = self.url_joiner(self.api_root, f"importsource/{import_source_id}/importschedule/{import_schedule_id}")
        return self.put(url, data=data)

    def delete_import_schedule(self, import_source_id, import_schedule_id):
        url = self.url_joiner(self.api_root, f"importsource/{import_source_id}/importschedule/{import_schedule_id}")
        return self.delete(url)

    def get_usage(self):
        return self.get(self.url_joiner(self.api_root, "usage"))

    def export_dataset(self, **filters):
        """Export dataset information as CSV."""
        allowed = {"testIssueId", "testIssueKey", "testVersion", "contextIssueId", "contextIssueKey", "resolved"}
        params = self._params(**{key: value for key, value in filters.items() if key in allowed})
        return self.get(self.url_joiner(self.api_root, "dataset/export"), params=params or None, not_json_response=True)

    def import_dataset(self, files=None, **filters):
        """Import a dataset CSV using optional entity context filters."""
        allowed = {"testIssueId", "testIssueKey", "testVersion", "contextIssueId", "contextIssueKey"}
        params = self._params(**{key: value for key, value in filters.items() if key in allowed})
        return self.post(self.url_joiner(self.api_root, "dataset/import"), params=params or None, files=files)
