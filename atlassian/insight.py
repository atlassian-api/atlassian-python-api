# coding=utf-8
import logging

from .rest_client import AtlassianRestAPI
from deprecated import deprecated

log = logging.getLogger(__name__)


class Insight(AtlassianRestAPI):
    """Insight for Jira API wrapper."""

    # https://insight-javadoc.riada.io/insight-javadoc-8.6/insight-rest/

    def __init__(self, *args, **kwargs):
        """
        Initialize Insight()

        :param args:
        :param kwargs:
        :return: Insight()
        """
        kwargs["api_root"] = "rest/insight/1.0"
        # If cloud is set to true, trigger private __cloud__init method
        if kwargs.get("cloud"):
            args, kwargs = self.__cloud_init(*args, **kwargs)
        super(Insight, self).__init__(*args, **kwargs)

    def __cloud_init(self, *args, **kwargs):
        """
        Creates a InsightCloud specific version of Insight()

        Returns:
            Insight(AtlassianRestAPI)
        """
        # trigger a normal init and avoid looping
        del kwargs["cloud"]
        temp = Insight(*args, **kwargs)
        # retrieve cloud workspace id and generate the api_root
        kwargs["api_root"] = "/jsm/insight/workspace/{}/v1/".format(temp.__get_workspace_id())
        # insight cloud uses the atlassian base url, not custom instnace urls
        kwargs["url"] = "https://api.atlassian.com"
        # set cloud back to true and return
        kwargs["cloud"] = True
        # Insight cloud is particular about its headers.
        self.default_headers = {"Accept": "application/json"}
        return args, kwargs

    def __get_workspace_id(self):
        result = self.get(
            "rest/servicedeskapi/insight/workspace",
            headers=self.default_headers,
        )
        return result["values"][0]["workspaceId"]

    def _get_insight_workspace_ids(self):
        """
        Returns all Insight workspace Ids.
        :return: List
        """
        result = self.get(
            "rest/servicedeskapi/insight/workspace",
            headers=self.experimental_headers,
        )
        return [i["workspaceId"] for i in result["values"]]

    def _get_insight_workspace_id(self):
        """
        Returns the first Insight workspace ID.
        :return: str
        """
        return next(iter(self._get_insight_workspace_ids()))

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
                "url": "http://jira/rest/insight/1.0/attachments/1"
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
            "attachments/object/{objectId}".format(objectId=object_id),
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
        log.warning("Adding attachment...")
        url = "rest/insight/1.0/attachments/object/{objectId}".format(objectId=object_id)
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
        log.warning("Adding attachment...")
        url = "rest/insight/1.0/attachments/{attachmentId}".format(attachmentId=attachment_id)
        return self.delete(url)

    # Comments
    # Handle comments on objets
    def add_comment_to_object(self, comment, object_id, role):
        """
        Add comment to Object

        :param comment: str
        :param object_id: int
        :param role: int
            0	Insight Users
            1	Insight Managers
            2	Insight Administrators
            3	Insight Developers
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
        url = "rest/insight/1.0/comment/create"
        return self.post(url, params=params)

    def get_comment_of_object(self, object_id):
        """
        The object id to fetch comments from

        :param object_id:
        :return:
        """
        if self.cloud:
            raise NotImplementedError
        url = "rest/insight/1.0/comment/object/{objectId}".format(objectId=object_id)
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
            "url16": "http://jira/rest/insight/1.0/icon/1/icon.png?size=16",
            "url48": "http://jira/rest/insight/1.0/icon/1/icon.png?size=48"
        }
        """
        url = self.url_joiner(self.api_root, "icon/{id}".format(id=icon_id))
        return self.get(url)

    def get_all_global_icons(self):
        """
        All existing global icons

        :return:
        """
        url = self.url_joiner(self.api_root, "icon/global")
        return self.get(url)

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
            "import/start/{import_id}".format(import_id=import_id),
        )
        return self.post(url)

    # Index
    # Handle the indexing of Insight
    def reindex_insight(self):
        """
        Should the reindex clean the index before doing the reindex

        :return:
        """
        if self.cloud:
            raise NotImplementedError
        url = self.url_joiner(self.api_root, "index/reindex/start")
        return self.post(url)

    def reindex_current_node_insight(self):
        """
        Should the reindex clean the index before doing the reindex

        :return:
        """
        if self.cloud:
            raise NotImplementedError
        url = self.url_joiner(self.api_root, "index/reindex/currentnode")
        return self.post(url)

    # IQL
    # Resource dedicated to finding objects based on the Insight Query Language (IQL)
    def iql(
        self,
        iql,
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

        :param iql:
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
        params = {"iql": iql, "objectSchemaId": object_schema_id, "page": page}
        if order_by_attribute_id:
            params["orderByAttributeId"] = order_by_attribute_id
        params["orderAsc"] = order_asc
        params["resultPerPage"] = result_per_page
        params["includeAttributes"] = include_attributes
        params["includeAttributesDeep"] = include_attributes_deep
        params["includeTypeAttributes"] = include_type_attributes
        params["includeExtendedInfo"] = include_extended_info
        if extended:
            params["extended"] = extended
        url = self.url_joiner(self.api_root, "iql/objects")
        return self.get(url, params=params)

    # Object
    def get_object(self, object_id):
        """
        Load one object

        :param object_id:
        :return:
        """
        url = self.url_joiner(self.api_root, "object/{id}".format(id=object_id))
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
        Update an existing object in Insight

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
        url = self.url_joiner(self.api_root, "object/{id}".format(id=object_id))
        return self.put(url, data=body)

    def delete_object(self, object_id):
        """
        Delete the referenced object

        :param object_id:
        :return:
        """
        url = self.url_joiner(self.api_root, "object/{id}".format(id=object_id))
        return self.delete(url)

    def get_object_attributes(self, object_id):
        """
        List all attributes for the given object

        :param object_id:
        :return:
        """
        url = self.url_joiner(self.api_root, "object/{id}/attributes".format(id=object_id))
        return self.get(url)

    def get_object_history(self, object_id, asc=False, abbreviate=True):
        """
        Retrieve the history entries for this object

        :param object_id:
        :param asc:
        :param abbreviate:
        :return:
        """
        params = {"asc": asc, "abbreviate": abbreviate}
        url = self.url_joiner(self.api_root, "object/{id}/history".format(id=object_id))
        return self.get(url, params=params)

    @deprecated(version="3.29.0", reason="Use get_object_reference_info()")
    def get_object_referenceinfo(self, object_id):
        """Let's use the get_object_reference_info()"""
        log.warning("Please, be informed that is deprecated as typo naming")
        self.get_object_reference_info(object_id)

    def get_object_reference_info(self, object_id):
        """
        Find all references for an object

        :param object_id:
        :return:
        """
        url = self.url_joiner(self.api_root, "object/{id}/referenceinfo".format(id=object_id))
        return self.get(url)

    def create_object(self, object_type_id, attributes, has_avatar=False, avatar_uuid=""):
        """
        Create a new object in Insight

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

    def create_object_navlist_iql(
        self,
        iql,
        object_type_id,
        results_per_page,
        order_by_type_attr_id,
        object_id,
        object_schema_id,
        include_attributes,
        attributes_to_display,
        page=1,
        asc=0,
    ):
        """
        A filter object that is used to find a paginated result set based on an object type and an IQL query

        :param iql:
        :param object_type_id:
        :param page:
        :param results_per_page:
        :param order_by_type_attr_id:
        :param asc:
        :param object_id:
        :param object_schema_id:
        :param include_attributes:
        :param attributes_to_display:
        :return:
        """
        data = {
            "objectTypeId": object_type_id,
            "iql": iql,
            "resultsPerPage": results_per_page,
            "page": page,
            "asc": asc,
        }
        if attributes_to_display is not None:
            data["attributesToDisplay"] = attributes_to_display
        if include_attributes is not None:
            data["includeAttributes"] = include_attributes
        if object_schema_id is not None:
            data["objectSchemaId"] = object_schema_id
        if order_by_type_attr_id is not None:
            data["orderByTypeAttrId"] = order_by_type_attr_id
        if object_id is not None:
            data["objectId"] = object_id
        url = self.url_joiner(self.api_root, "iql/objects")
        return self.post(url, data=data)

    # Objectconnectedtickets
    def get_object_connected_tickets(self, object_id):
        """
        Relation between Jira issues and Insight objects

        :param object_id:
        :return:
        """
        url = self.url_joiner(
            self.api_root,
            "objectconnectedtickets/{id}/tickets".format(id=object_id),
        )
        return self.get(url)

    # Object schema
    @deprecated(version="3.29.1", reason="Use list_object_schema()")
    def list_objectschema(self):
        return self.list_object_schema()

    def list_object_schema(self):
        """
        Resource to find object schemas in Insight
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
        raise NotImplementedError

    @deprecated(version="3.29.1", reason="Use get_objectschema()")
    def get_objectschema(self, schema_id):
        return self.get_objectschema(schema_id=schema_id)

    def get_object_schema(self, schema_id):
        """
        Find a schema by id
        :param schema_id:
        """
        url = self.url_joiner(self.api_root, "objectschema/{id}".format(id=schema_id))
        return self.get(url)

    def update_object_schema(self, schema_id):
        """
        Update an object schema
        """
        raise NotImplementedError

    def delete_object_schema(self, schema_id):
        """
        Delete a schema

        """
        raise NotImplementedError

    def get_object_schema_attributes(self, schema_id):
        """
        Find all object type attributes for this object schema
        """
        raise NotImplementedError

    def get_object_schema_object_types_flat(self, schema_id):
        """
        Find all object types for this object schema
        """
        raise NotImplementedError

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
        https://developer.atlassian.com/cloud/insight/rest/api-group-objecttype/#api-objecttype-id-attributes-get
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

        kwargs = locals().items()
        params = dict()
        params.update({k: v for k, v in kwargs if v is not None and k not in ["self", "type_id"]})

        return self.get(
            "{0}/objecttype/{1}/attributes".format(self.api_root, type_id),
            headers=self.experimental_headers,
            params=params,
        )

    # Objecttype
    # TODO: Post objecttype {id} position:
    #       https://developer.atlassian.com/cloud/insight/rest/api-group-objecttype/#api-objecttype-id-position-post
    # TODO: Post objecttype create:
    #       https://developer.atlassian.com/cloud/insight/rest/api-group-objecttype/#api-objecttype-create-post

    # Insight ObjectTypeAttribute API
    # TODO: Post objecttypeattribute {objectTypeId}:
    #       https://developer.atlassian.com/cloud/insight/rest/api-group-objecttypeattribute/#api-objecttypeattribute-objecttypeid-post
    # TODO: Put objecttypeattribute {objectTypeId} {id}:
    #       https://developer.atlassian.com/cloud/insight/rest/api-group-objecttypeattribute/#api-objecttypeattribute-objecttypeid-id-put
    # TODO: Delete objecttypeattribute {id}:
    #       https://developer.atlassian.com/cloud/insight/rest/api-group-objecttypeattribute/#api-objecttypeattribute-id-delete

    # Insight Progress API
    # TODO: Get progress category imports {id}:
    #       https://developer.atlassian.com/cloud/insight/rest/api-group-progress/#api-progress-category-imports-id-get
    def get_progress_of_reindex(self):
        """
        Show ongoing insight processes
        :return:
        """
        if self.cloud:
            raise NotImplementedError
        url = self.url_joiner(self.api_root, "progress/category/insight-reindex/reindex")
        return self.get(url)

    def get_progress_of_import(self, import_id):
        """
        Show ongoing insight processes
        :type import_id: int: The id of the import source configuration
                              that the progress should be fetched for
        :return:
        """
        if self.cloud:
            raise NotImplementedError
        url = self.url_joiner(self.api_root, "progress/category/imports/{id}".format(id=import_id))
        return self.get(url)

    # Insight Config API
    # TODO: Get config statustype:
    #       https://developer.atlassian.com/cloud/insight/rest/api-group-config/#api-config-statustype-get
    # TODO: Post config statustype:
    #       https://developer.atlassian.com/cloud/insight/rest/api-group-config/#api-config-statustype-post
    # TODO: Get config statustype {id}:
    #       https://developer.atlassian.com/cloud/insight/rest/api-group-config/#api-config-statustype-id-get
    # TODO: Put config statustype {id}:
    #       https://developer.atlassian.com/cloud/insight/rest/api-group-config/#api-config-statustype-id-put
    # TODO: Delete config statustype {id}:
    #       https://developer.atlassian.com/cloud/insight/rest/api-group-config/#api-config-statustype-id-delete

    # Update Issue with Insight Field
    def update_issue_insight_field(self, key, field_id, insight_keys, add=False):
        """
        Set the value of an Insight field.
        Args:
            key (str): Jira issue key, eg. SFT-446
            field_id (str): The internal Jira name of the Insight field, e.g. customfield_10200
            insight_keys (list): List of Insight objects to associate with the field. Limited
                to 20 objects. If the field only takes a single object pass a single value list.
            add (bool, optional): Add to the existing field rather than setting the field value.
                Defaults to False.
        Returns:
            [type]: The insight object updated.
        """
        base_url = self.resource_url("issue")
        action = "add" if add else "set"
        data = {
            "update": {
                field_id: [{action: [{"key": i} for i in insight_keys]}],
            }
        }
        data = {"fields": {field_id: [{"key": i} for i in insight_keys]}}
        return self.put("{base_url}/{key}".format(base_url=base_url, key=key), data=data)
