# coding=utf-8
import logging
from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Jira8(AtlassianRestAPI):

    # API/2 Get permissions
    def get_permissions(self, project_id=None, project_key=None, issue_id=None, issue_key=None):
        """
        Returns all permissions in the system and whether the currently logged in user has them.
        You can optionally provide a specific context
        to get permissions for (projectKey OR projectId OR issueKey OR issueId)

        :param project_id: str
        :param project_key: str
        :param issue_id: str
        :param issue_key: str
        :return:
        """
        url = 'rest/api/2/mypermissions'
        params = {}

        if project_id:
            params['projectId'] = project_id
        if project_key:
            params['projectKey'] = project_key
        if issue_id:
            params['issueId'] = issue_id
        if issue_key:
            params['issueKey'] = issue_key

        return self.get(url, params=params)

    def get_all_permissions(self):
        """
        Returns all permissions that are present in the JIRA instance - Global, Project
        and the global ones added by plugins

        :return: All permissions
        """
        url = 'rest/api/2/permissions'

        return self.get(url)

    # Application properties
    def get_property(self, key=None, permission_level=None, key_filter=None):
        """
        Returns an application property

        :param key: str
        :param permission_level: str
        :param key_filter: str
        :return: list or item
        """
        url = 'rest/api/2/application-properties'
        params = {}

        if key:
            params['key'] = key
        if permission_level:
            params['permissionLevel'] = permission_level
        if key_filter:
            params['keyFilter'] = key_filter

        return self.get(url, params=params)

    def set_property(self, property_id, value):
        url = 'rest/api/2/application-properties/{}'.format(property_id)
        data = {'id': property_id, 'value': value}

        return self.put(url, data=data)

    def get_advanced_settings(self):
        """
        Returns the properties that are displayed on the "General Configuration > Advanced Settings" page

        :return:
        """
        url = 'rest/api/2/application-properties/advanced-settings'

        return self.get(url)

    # Application roles
    def get_all_application_roles(self):
        """
        Returns all ApplicationRoles in the system

        :return:
        """
        url = 'rest/api/2/applicationrole'

        return self.get(url)

    def get_application_role(self, role_key):
        """
        Returns the ApplicationRole with passed key if it exists

        :param role_key: str
        :return:
        """
        url = 'rest/api/2/applicationrole/{}'.format(role_key)

        return self.get(url)

    # Attachments
    def get_attachment(self, attachment_id):
        """
        Returns the meta-data for an attachment, including the URI of the actual attached file

        :param attachment_id: int
        :return:
        """
        url = 'rest/api/2/attachment/{}'.format(attachment_id)

        return self.get(url)

    def remove_attachment(self, attachment_id):
        """
        Remove an attachment from an issue

        :param attachment_id: int
        :return: if success, return None
        """
        url = 'rest/api/2/attachment/{}'.format(attachment_id)

        return self.delete(url)

    def get_attachment_meta(self):
        """
        Returns the meta information for an attachments,
        specifically if they are enabled and the maximum upload size allowed

        :return:
        """
        url = 'rest/api/2/attachment/meta'

        return self.get(url)

    # Issues
    def create_issue(self, fields, update_history=False):
        """
        Creates an issue or a sub-task from a JSON representation

        :param fields: JSON data
        :param update_history: bool (if true then the user's project history is updated)
        :return:
        """
        url = 'rest/api/2/issue'
        data = {'fields': fields}
        params = {}

        if update_history is True:
            params['updateHistory'] = 'true'
        else:
            params['updateHistory'] = 'false'

        return self.post(url, params=params, data=data)

    def create_issues(self, list_of_issues_data):
        """
        Creates issues or sub-tasks from a JSON representation
        Creates many issues in one bulk operation

        :param list_of_issues_data: list of JSON data
        :return:
        """
        url = 'rest/api/2/issue/bulk'
        data = {'issueUpdates': list_of_issues_data}

        return self.post(url, data=data)

    def delete_issue(self, issue_id_or_key, delete_subtasks=True):
        """
        Delete an issue
        If the issue has subtasks you must set the parameter delete_subtasks = True to delete the issue
        You cannot delete an issue without its subtasks also being deleted

        :param issue_id_or_key:
        :param delete_subtasks:
        :return:
        """
        url = 'rest/api/2/issue/{}'.format(issue_id_or_key)
        params = {}

        if delete_subtasks is True:
            params['deleteSubtasks'] = 'true'
        else:
            params['deleteSubtasks'] = 'false'

        log.warning('Removing issue {}...'.format(issue_id_or_key))

        return self.delete(url, params=params)

    def edit_issue(self, issue_id_or_key, fields, notify_users=True):
        """
        Edits an issue from a JSON representation
        The issue can either be updated by setting explicit the field
        value(s) or by using an operation to change the field value

        :param issue_id_or_key: str
        :param fields: JSON
        :param notify_users: bool
        :return:
        """
        url = 'rest/api/2/issue/{}'.format(issue_id_or_key)
        params = {}
        data = {'update': fields}

        if notify_users is True:
            params['notifyUsers'] = 'true'
        else:
            params['notifyUsers'] = 'false'

        return self.put(url, data=data, params=params)

    def get_issue(self, issue_id_or_key, fields=None, properties=None, update_history=True):
        """
        Returns a full representation of the issue for the given issue key
        By default, all fields are returned in this get-issue resource

        :param issue_id_or_key: str
        :param fields: str
        :param properties: str
        :param update_history: bool
        :return: issue
        """
        url = 'rest/api/2/issue/{}'.format(issue_id_or_key)
        params = {}

        if fields is not None:
            params['fields'] = fields
        if properties is not None:
            params['properties'] = properties
        if update_history is True:
            params['updateHistory'] = 'true'
        if update_history is False:
            params['updateHistory'] = 'false'

        return self.get(url, params=params)
