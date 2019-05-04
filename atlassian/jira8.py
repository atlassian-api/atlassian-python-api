# coding: utf-8
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
