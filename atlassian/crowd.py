# coding=utf-8
import logging

from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Crowd(AtlassianRestAPI):
    """Crowd API wrapper.
    Important to note that you will have to use an application credentials,
    not user credentials, in order to access Crowd APIs"""

    def __init__(
        self,
        url,
        username,
        password,
        timeout=60,
        api_root="rest",
        api_version="latest",
    ):
        super(Crowd, self).__init__(url, username, password, timeout, api_root, api_version)

    def _crowd_api_url(self, api, resource):
        return "/{api_root}/{api}/{version}/{resource}".format(
            api_root=self.api_root,
            api=api,
            version=self.api_version,
            resource=resource,
        )

    def _user_change_status(self, username, active):
        """
        Change user status.
        :param username: str - username
        :param active: bool - True/False
        :return:
        """

        user = self.user(username)

        user_object = {
            "name": username,
            "active": active,
            "display-name": user.get("display-name"),
            "first-name": user.get("first-name"),
            "last-name": user.get("last-name"),
            "email": user.get("email"),
        }

        params = {"username": username}

        return self.put(
            self._crowd_api_url("usermanagement", "user"),
            params=params,
            data=user_object,
        )

    def user(self, username):
        """
        Get user information
        :param username:
        :return:
        """
        params = {"username": username}
        return self.get(self._crowd_api_url("usermanagement", "user"), params=params)

    def user_activate(self, username):
        """
        Activate user
        :param username: str - username
        """

        return self._user_change_status(username, True)

    def user_create(
        self,
        username,
        active,
        first_name,
        last_name,
        display_name,
        email,
        password,
    ):
        """
        Create new user method
        :param  active: bool:
        :param  username: string: username
        :param  active: bool:
        :param  first_name: string:
        :param  last_name: string:
        :param  display_name:  string:
        :param  email: string:
        :param  password: string:
        :return:
        """

        user_object = {
            "name": username,
            "password": {"value": password},
            "active": active,
            "first-name": first_name,
            "last-name": last_name,
            "display-name": display_name,
            "email": email,
        }

        return self.post(self._crowd_api_url("usermanagement", "user"), data=user_object)

    def user_deactivate(self, username):
        """
        Deactivate user

        :return:
        """

        return self._user_change_status(username, False)

    def user_delete(self, username):
        """
        Delete user
        :param username: str - username
        :return:
        """

        params = {"username": username}

        return self.delete(self._crowd_api_url("usermanagement", "user"), params=params)

    def group_add_user(self, username, groupname):
        """
        Add user to group
        :return:
        """

        data = {"name": groupname}

        params = {"username": username}

        return self.post(
            self._crowd_api_url("usermanagement", "user/group/direct"),
            params=params,
            json=data,
        )

    def group_nested_members(self, group):
        """
        Get nested members of group
        :param group:
        :return:
        """
        params = {"groupname": group}
        return self.get(self._crowd_api_url("group", "nested"), params=params)

    def health_check(self):
        """
        Get health status
        https://confluence.atlassian.com/jirakb/how-to-retrieve-health-check-results-using-rest-api-867195158.html
        :return:
        """
        # check as Troubleshooting & Support Tools Plugin
        response = self.get("rest/troubleshooting/1.0/check/")
        if not response:
            # check as support tools
            response = self.get("rest/supportHealthCheck/1.0/check/")
        return response

    def get_plugins_info(self):
        """
        Provide plugins info
        :return a json of installed plugins
        """
        url = "rest/plugins/1.0/"
        return self.get(url, headers=self.no_check_headers, trailing=True)

    def get_plugin_info(self, plugin_key):
        """
        Provide plugin info
        :return a json of installed plugins
        """
        url = "rest/plugins/1.0/{plugin_key}-key".format(plugin_key=plugin_key)
        return self.get(url, headers=self.no_check_headers, trailing=True)

    def get_plugin_license_info(self, plugin_key):
        """
        Provide plugin license info
        :return a json specific License query
        """
        url = "rest/plugins/1.0/{plugin_key}-key/license".format(plugin_key=plugin_key)
        return self.get(url, headers=self.no_check_headers, trailing=True)

    def upload_plugin(self, plugin_path):
        """
        Provide plugin path for upload into Jira e.g. useful for auto deploy
        :param plugin_path:
        :return:
        """
        files = {"plugin": open(plugin_path, "rb")}
        upm_token = self.request(
            method="GET",
            path="rest/plugins/1.0/",
            headers=self.no_check_headers,
            trailing=True,
        ).headers["upm-token"]
        url = "rest/plugins/1.0/?token={upm_token}".format(upm_token=upm_token)
        return self.post(url, files=files, headers=self.no_check_headers)

    def delete_plugin(self, plugin_key):
        """
        Delete plugin
        :param plugin_key:
        :return:
        """
        url = "rest/plugins/1.0/{}-key".format(plugin_key)
        return self.delete(url)

    def check_plugin_manager_status(self):
        url = "rest/plugins/latest/safe-mode"
        return self.request(method="GET", path=url, headers=self.safe_mode_headers)

    def update_plugin_license(self, plugin_key, raw_license):
        """
        Update license for plugin
        :param plugin_key:
        :param raw_license:
        :return:
        """
        app_headers = {
            "X-Atlassian-Token": "nocheck",
            "Content-Type": "application/vnd.atl.plugins+json",
        }
        url = "/plugins/1.0/{plugin_key}/license".format(plugin_key=plugin_key)
        data = {"rawLicense": raw_license}
        return self.put(url, data=data, headers=app_headers)
