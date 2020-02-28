# coding=utf-8
import logging

from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Crowd(AtlassianRestAPI):
    """Crowd API wrapper.
    Important to note that you will have to use an application credentials,
    not user credentials, in order to access Crowd APIs"""

    def __init__(self, url, username, password, timeout=60, api_root='rest', api_version='latest'):
        super(Crowd, self).__init__(url, username, password, timeout, api_root, api_version)

    def _crowd_api_url(self, api, resource):
        return '{server}/{api_root}/{api}/{version}/{resource}'.format(
            server=self.url,
            api_root=self.api_root,
            api=api,
            version=self.api_version,
            resource=resource
        )

    def user(self, username):
        params = {'username': username}
        return self.get(self._crowd_api_url('usermanagement', 'user'), params=params)

    def group_nested_members(self, group):
        params = {'groupname': group}
        return self.get(self._crowd_api_url('group', 'nested'), params=params)

    def health_check(self):
        """
        Get health status
        https://confluence.atlassian.com/jirakb/how-to-retrieve-health-check-results-using-rest-api-867195158.html
        :return:
        """
        # check as Troubleshooting & Support Tools Plugin
        response = self.get('rest/troubleshooting/1.0/check/')
        if not response:
            # check as support tools
            response = self.get('rest/supportHealthCheck/1.0/check/')
        return response

    def upload_plugin(self, plugin_path):
        """
        Provide plugin path for upload into Jira e.g. useful for auto deploy
        :param plugin_path:
        :return:
        """
        files = {
            'plugin': open(plugin_path, 'rb')
        }
        upm_token = \
            self.request(method='GET', path='rest/plugins/1.0/', headers=self.no_check_headers, trailing=True).headers[
                'upm-token']
        url = 'rest/plugins/1.0/?token={upm_token}'.format(upm_token=upm_token)
        return self.post(url, files=files, headers=self.no_check_headers)
