# coding=utf-8
import logging

from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Insight(AtlassianRestAPI):
    """Insight for Jira API wrapper."""

    # https://insight-javadoc.riada.io/insight-javadoc-8.6/insight-rest/

    def __init__(self, *args, **kwargs):
        if kwargs.get("cloud"):
            args, kwargs = self.__cloud_init(*args, **kwargs)
        super(Insight, self).__init__(*args, **kwargs)

    def __cloud_init(self, *args, **kwargs):
        del kwargs["cloud"]
        temp = Insight(*args, **kwargs)
        kwargs["api_root"] = "/jsm/insight/workspace/{}/v1/".format(temp.__get_workspace_id())
        kwargs["url"] = "https://api.atlassian.com"
        kwargs["cloud"] = True
        return args, kwargs

    def __get_workspace_id(self):
        return self.get("rest/servicedeskapi/insight/workspace", headers=self.default_headers,)["values"][
            0
        ]["workspaceId"]

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
        url = "rest/insight/1.0/attachments/object/{objectId}".format(objectId=object_id)
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
        params = {"comment": comment, "objectId": object_id, "role": role}
        url = "rest/insight/1.0/comment/create"
        return self.post(url, params=params)

    def get_comment_of_object(self, object_id):
        """
        The object id to fetch comments from
        :param object_id:
        :return:
        """
        url = "rest/insight/1.0/comment/object/{objectId}".format(objectId=object_id)
        return self.get(url)

    # Icon
    # Resources dedicated to load and find icons
    def get_icon_by_id(self, id):
        """
        Load a single icon by id
        :param id:
        :return:
        {
            "id": 1,
            "name": "Delete",
            "url16": "http://jira/rest/insight/1.0/icon/1/icon.png?size=16",
            "url48": "http://jira/rest/insight/1.0/icon/1/icon.png?size=48"
        }
        """
        url = "rest/insight/1.0/icon/{id}".format(id=id)
        return self.get(url)

    def get_all_global_icons(self):
        """
        All existing global icons
        :return:
        """
        url = "rest/insight/1.0/icon/global"
        return self.get(url)

    # Import
    # Start configured imports. To see an ongoing import see the Progress resource
    def start_import_configuration(self, id):
        """
        The id of the import configuration that should be started
        :param id:
        :return:
        """
        url = "rest/insight/1.0/import/start/{id}".format(id=id)
        return self.post(url)

    # Index
    # Handle the indexing of Insight
    def reindex_insight(self):
        """
        Should the reindex clean the index before doing the reindex
        :return:
        """
        url = "rest/insight/1.0/index/reindex/start"
        return self.post(url)

    def reindex_current_node_insight(self):
        """
        Should the reindex clean the index before doing the reindex
        :return:
        """
        url = "rest/insight/1.0/index/reindex/currentnode"
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
        url = "rest/insight/1.0/iql/objects"
        return self.get(url, params=params)
