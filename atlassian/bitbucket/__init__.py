# coding=utf-8
import logging

from deprecated import deprecated
from requests import HTTPError

from .base import BitbucketBase
from atlassian.bitbucket.cloud import Cloud

log = logging.getLogger(__name__)


class Bitbucket(BitbucketBase):
    def __init__(self, url, *args, **kwargs):
        if "cloud" not in kwargs and ("bitbucket.org" in url):
            kwargs["cloud"] = True
        if "api_version" not in kwargs:
            kwargs["api_version"] = "2.0" if "cloud" in kwargs and kwargs["cloud"] else "1.0"
        if "cloud" in kwargs:
            kwargs["api_root"] = "" if "api.bitbucket.org" in url else "rest/api"

        super(Bitbucket, self).__init__(url, *args, **kwargs)

    def markup_preview(self, data):
        """
        Preview generated HTML for the given markdown content.
        Only authenticated users may call this resource.
        :param data:
        :return:
        """

        url = self.resource_url("markup/preview")
        return self.post(url, data=data)

    ################################################################################################
    # Administrative functions
    ################################################################################################

    def _url_admin(self, api_version=None):
        return self.resource_url("admin", api_version=api_version)

    def group_members(self, group, start=0, limit=None):
        """
        Get group of members
        :param group: The group name to query
        :param start:
        :param limit:
        :return: A list of group members
        """

        url = "{}/groups/more-members".format(self._url_admin())
        params = {}
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        if group:
            params["context"] = group
        return self._get_paged(url, params=params)

    def all_project_administrators(self):
        """
        Get the list of project administrators

        :return: A generator object containing a map with the project_key, project_name and project_administrators
        """
        for project in self.project_list():
            log.info("Processing project: %s - %s", project.get("key"), project.get("name"))
            yield {
                "project_key": project.get("key"),
                "project_name": project.get("name"),
                "project_administrators": [
                    {"email": x["emailAddress"], "name": x["displayName"]}
                    for x in self.project_users_with_administrator_permissions(project["key"])
                ],
            }

    def reindex(self):
        """
        Rebuild the bundled Elasticsearch indexes for Bitbucket Server
        :return:
        """
        url = self.resource_url("sync", api_root="rest/indexing", api_version="latest")
        return self.post(url)

    def check_reindexing_status(self):
        """
        Check reindexing status
        :return:
        """
        url = self.resource_url("status", api_root="rest/indexing", api_version="latest")
        return self.get(url)

    def get_users(self, user_filter=None, limit=25, start=0):
        """
        Get list of bitbucket users.
        Use 'user_filter' for get specific users or get all users if necessary.
        :param user_filter: str - username, displayname or email
        :param limit: int - paginated limit to retrieve
        :param start: int - paginated point to start retreiving
        :return: The collection as JSON with all relevant information about the licensed user
        """
        url = self.resource_url("users", api_version="1.0")
        params = {}
        if user_filter:
            params["filter"] = user_filter
        if limit:
            params["limit"] = limit
        if start:
            params["start"] = start
        return self.get(url, params=params)

    def get_users_info(self, user_filter=None, start=0, limit=25):
        """
        The authenticated user must have the LICENSED_USER permission to call this resource.
        :param user_filter: if specified only users with usernames, display name or email addresses
            containing the supplied string will be returned
        :param limit:
        :param start:
        :return:
        """
        url = "{}/users".format(self._url_admin(api_version="1.0"))
        params = {}
        if limit:
            params["limit"] = limit
        if start:
            params["start"] = start
        if user_filter:
            params["filter"] = user_filter
        return self._get_paged(url, params=params)

    def get_current_license(self):
        """
        Retrieves details about the current license, as well as the current status of the system with
        regard to the installed license. The status includes the current number of users applied
        toward the license limit, as well as any status messages about the license (warnings about expiry
        or user counts exceeding license limits).
        The authenticated user must have ADMIN permission. Unauthenticated users, and non-administrators,
        are not permitted to access license details.
        :return:
        """
        url = "{}/license".format(self._url_admin())
        return self.get(url)

    def _url_mail_server(self):
        return "{}/mail-server".format(self._url_admin())

    def get_mail_configuration(self):
        """
        Retrieves the current mail configuration.
        The authenticated user must have the SYS_ADMIN permission to call this resource.
        :return:
        """
        url = self._url_mail_server()
        return self.get(url)

    def _url_mail_server_sender_address(self):
        return "{}/sender-address".format(self._url_mail_server())

    def get_mail_sender_address(self):
        """
        Retrieves the server email address
        :return:
        """
        url = self._url_mail_server_sender_address()
        return self.get(url)

    def remove_mail_sender_address(self):
        """
        Clears the server email address.
        The authenticated user must have the ADMIN permission to call this resource.
        :return:
        """
        url = self._url_mail_server_sender_address()
        return self.delete(url)

    def get_ssh_settings(self):
        """
        Retrieve ssh settings for user
        :return:
        """
        url = self.resource_url("settings", api_root="rest/ssh")
        return self.get(url)

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

    def get_associated_build_statuses(self, commit):
        """
        To get the build statuses associated with a commit.
        :commit: str- commit id
        :return:
        """
        url = self.resource_url(
            "commits/{commitId}".format(commitId=commit),
            api_root="rest/build-status",
        )
        return self.get(url)

    def _url_announcement_banner(self):
        return "{}/banner".format(self._url_admin())

    def get_announcement_banner(self):
        """
        Gets the announcement banner, if one exists and is available to the user
        :return:
        """
        url = self._url_announcement_banner()
        return self.get(url)

    def set_announcement_banner(self, body):
        """
        Sets the announcement banner with the provided JSON.
        Only users authenticated as Admins may call this resource
        :param body
            {
                "id": "https://docs.atlassian.com/jira/REST/schema/rest-announcement-banner#",
                "title": "Rest Announcement Banner",
                "type": "object"
            }
        :return:
        """
        url = self._url_announcement_banner()
        return self.put(url, data=body)

    def delete_announcement_banner(self):
        """
        Gets the announcement banner, if one exists and is available to the user
        :return:
        """
        url = self._url_announcement_banner()
        return self.delete(url)

    def upload_plugin(self, plugin_path):
        """
        Provide plugin path for upload into BitBucket e.g. useful for auto deploy
        :param plugin_path:
        :return:
        """
        upm_token = self.request(
            method="GET",
            path="rest/plugins/1.0/",
            headers=self.no_check_headers,
            trailing=True,
        ).headers["upm-token"]
        url = "rest/plugins/1.0/?token={}".format(upm_token)
        files = {"plugin": open(plugin_path, "rb")}
        return self.post(url, files=files, headers=self.no_check_headers)

    def get_categories(self, project_key, repository_slug=None):
        """
        Get a list of categories assigned to a project or repository.
        :param project_key: The project key as shown in URL.
        :param repository_slug: The repository as shown in URL (optional).
        :return: If 'repository_slug', returns the list with categories of the repository,
        otherwise, returns the list with the categories of the project 'project_key'
        """
        url = "project/{}".format(project_key)
        if repository_slug:
            url = "{}/repository/{}".format(url, repository_slug)
        url = self.resource_url(url, api_root="rest/categories", api_version="latest")
        data = self.get(url)
        return data.get("result").get("categories")

    ################################################################################################
    # Functions related to projects
    ################################################################################################

    def _url_projects(self, api_root=None, api_version=None):
        return self.resource_url("projects", api_root, api_version)

    def project_list(self, start=0, limit=None):
        """
        Provide the project list

        :return: A list of projects
        """
        url = self._url_projects()
        params = {}
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        return self._get_paged(url, params=params)

    def create_project(self, key, name, description=""):
        """
        Create project
        :param key: The project key
        :param name: The project name
        :param description: The project description

        :return: The value of the post request.
        """
        url = self._url_projects()
        data = {"key": key, "name": name, "description": description}
        return self.post(url, data=data)

    ################################################################################################
    # Functions related to a specific project
    ################################################################################################

    def _url_project(self, project_key, api_root=None, api_version=None):
        return "{}/{}".format(self._url_projects(api_root, api_version), project_key)

    def project(self, key):
        """
        Provide project info
        :param key: The project key
        :return:
        """
        url = self._url_project(key)
        return self.get(url) or {}

    def project_exists(self, project_key):
        """
        Check if project with the provided project key exists and available.
        :param project_key: Key of the project where to check for repository.
        :return: False is requested repository doesn't exist in the project or not accessible to the requestor
        """
        exists = False
        try:
            self.project(project_key)
            exists = True
        except HTTPError as e:
            if e.response.status_code in (401, 404):
                pass
        return exists

    def update_project(self, key, **params):
        """
        Update project
        :param key: The project key
        :return: The value of the put request.
        """
        url = self._url_project(key)
        return self.put(url, data=params)

    def _url_project_avatar(self, project_key):
        return "{}/avatar.png".format(self._url_project(project_key))

    def project_summary(self, key):
        """
        Get a project summary
        :param key: The project key

        :return: Map with the project information
        """
        return {
            "key": key,
            "data": self.project(key),
            "users": self.project_users(key),
            "groups": self.project_groups(key),
            "avatar": self.project_avatar(key),
        }

    def project_avatar(self, key, content_type="image/png"):
        """
        Get project avatar
        :param key: The project key
        :param content_type: The content type to get

        :return: Value of get request
        """
        url = self._url_project_avatar(key)
        headers = dict(self.default_headers)
        headers["Accept"] = content_type
        headers["X-Atlassian-Token"] = "no-check"

        return self.get(url, not_json_response=True, headers=headers)

    def set_project_avatar(self, key, icon, content_type="image/png"):
        """
        Set project avatar
        :param key: The Project key
        :param icon: The icon file
        :param content_type: The content type of icon

        :return: Value of post request
        """
        url = self._url_project_avatar(key)
        headers = {"X-Atlassian-Token": "no-check"}
        files = {"avatar": ("avatar.png", icon, content_type)}
        return self.post(url, files=files, headers=headers)

    def project_keys(self, key, start=0, limit=None, filter_str=None):
        """
        Get SSH access keys added to the project
        :param start:
        :param limit:
        :param key: The project key
        :param filter_str:  OPTIONAL: users filter string
        :return: The list of SSH access keys
        """
        url = "{}/ssh".format(self._url_project(key, api_root="rest/keys"))
        params = {}
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        if filter_str:
            params["filter"] = filter_str
        return self._get_paged(url, params=params)

    def _url_project_users(self, project_key):
        return "{}/permissions/users".format(self._url_project(project_key))

    def project_users(self, key, start=0, limit=None, filter_str=None):
        """
        Get users with permission in project
        :param key: The project key
        :param filter_str:  OPTIONAL: users filter string
        :param start:
        :param limit:
        :return: The list of project users
        """
        url = self._url_project_users(key)
        params = {}
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        if filter_str:
            params["filter"] = filter_str
        return self._get_paged(url, params=params)

    def project_users_with_administrator_permissions(self, key):
        """
        Get project administrators for project
        :param key: The project key
        :return: List of project administrators
        """
        project_administrators = [
            user["user"] for user in self.project_users(key) if user["permission"] == "PROJECT_ADMIN"
        ]
        for group in self.project_groups_with_administrator_permissions(key):
            for user in self.group_members(group):
                project_administrators.append(user)
        return project_administrators

    def project_grant_user_permissions(self, project_key, username, permission):
        """
        Grant the specified project permission to a specific user
        :param project_key: The project key
        :param username: username to be granted
        :param permission: the project permissions available are 'PROJECT_ADMIN', 'PROJECT_WRITE' and 'PROJECT_READ'
        :return:
        """
        url = self._url_project_users(project_key)
        params = {"permission": permission, "name": username}
        return self.put(url, params=params)

    def project_remove_user_permissions(self, project_key, username):
        """
        Revoke all permissions for the specified project for a user.
        The authenticated user must have PROJECT_ADMIN permission for
        the specified project or a higher global permission to call this resource.
        In addition, a user may not revoke their own project permissions if they do not have a higher global permission.
        :param project_key: The project key
        :param username: username to be granted
        :return:
        """
        url = self._url_project_users(project_key)
        params = {"name": username}
        return self.delete(url, params=params)

    def _url_project_groups(self, project_key):
        return "{}/permissions/groups".format(self._url_project(project_key))

    def project_groups(self, key, start=0, limit=None, filter_str=None):
        """
        Get Project Groups
        :param limit:
        :param limit:
        :param start:
        :param key: The project key
        :param filter_str: OPTIONAL: group filter string
        :return:
        """
        url = self._url_project_groups(key)
        params = {}
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        if filter_str:
            params["filter"] = filter_str
        return self._get_paged(url, params=params)

    def project_grant_group_permissions(self, project_key, group_name, permission):
        """
        Grant the specified project permission to a specific group
        :param project_key: The project key
        :param group_name: group to be granted
        :param permission: the project permissions available are 'PROJECT_ADMIN', 'PROJECT_WRITE' and 'PROJECT_READ'
        :return:
        """
        url = self._url_project_groups(project_key)
        params = {"permission": permission, "name": group_name}
        return self.put(url, params=params)

    def project_remove_group_permissions(self, project_key, groupname):
        """
        Revoke all permissions for the specified project for a group.
        The authenticated user must have PROJECT_ADMIN permission for the specified project
        or a higher global permission to call this resource.
        In addition, a user may not revoke a group's permissions
        if it will reduce their own permission level.
        :param project_key: The project key
        :param groupname: group to be granted
        :return:
        """
        url = self._url_project_groups(project_key)
        params = {"name": groupname}
        return self.delete(url, params=params)

    def project_default_permissions(self, project_key, permission):
        """
        Check if the specified permission is the default permission for a given project
        :param project_key: The project key
        :param permission: the project permissions available are 'PROJECT_ADMIN', 'PROJECT_WRITE' and 'PROJECT_READ'
        :return:
        """
        url = "{}/permissions/{}/all".format(self._url_project(project_key), permission)
        return self.get(url)

    def project_grant_default_permissions(self, project_key, permission):
        """
        Grant the specified project permission to all users for a given project
        :param project_key: The project key
        :param permission: the project permissions available are 'PROJECT_ADMIN', 'PROJECT_WRITE' and 'PROJECT_READ'
        :return:
        """
        url = "{}/permissions/{}/all".format(self._url_project(project_key), permission)
        return self.post(url, params={"allow": True})

    def project_remove_default_permissions(self, project_key, permission):
        """
        Revoke the specified project permission for all users for a given project
        :param project_key: The project key
        :param permission: the project permissions available are 'PROJECT_ADMIN', 'PROJECT_WRITE' and 'PROJECT_READ'
        :return:
        """
        url = "{}/permissions/{}/all".format(self._url_project(project_key), permission)
        return self.post(url, params={"allow": False})

    def _url_project_repo_hook_settings(self, project_key):
        return "{}/settings/hooks".format(self._url_project(project_key))

    def all_project_repo_hook_settings(self, project_key, start=0, limit=None, filter_type=None):
        """
        Get all repository hooks for a given project
        :param project_key: The project key
        :param start:
        :param limit: OPTIONAL: The limit of the number of changes to return, this may be restricted by
                fixed system limits. Default by built-in method: None
        :param filter_type: OPTIONAL: PRE_RECEIVE|POST_RECEIVE if present,
                                    controls how repository hooks should be filtered.
        :return:
        """
        url = self._url_project_repo_hook_settings(project_key)
        params = {}
        if filter_type:
            params["type"] = filter_type
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        return self._get_paged(url, params)

    def get_project_repo_hook_settings(self, project_key, hook_key):
        """
        Get a repository hook from a given project
        :param project_key: The project key
        :param hook_key: The repository hook key
        :return:
        """
        url = "{}/{}".format(self._url_project_repo_hook_settings(project_key), hook_key)
        return self.get(url)

    def enable_project_repo_hook_settings(self, project_key, hook_key):
        """
        Enable a repository hook for a given project
        :param project_key: The project key
        :param hook_key: The repository hook key
        :return:
        """
        url = "{}/{}/enabled".format(self._url_project_repo_hook_settings(project_key), hook_key)
        return self.put(url)

    def disable_project_repo_hook_settings(self, project_key, hook_key):
        """
        Disable a repository hook for a given project
        :param project_key: The project key
        :param hook_key: The repository hook key
        :return:
        """
        url = "{}/{}/enabled".format(self._url_project_repo_hook_settings(project_key), hook_key)
        return self.delete(url)

    def _url_project_conditions(self, project_key):
        return "{}/conditions".format(
            self._url_project(
                project_key,
                api_root="rest/default-reviewers",
                api_version="1.0",
            )
        )

    def get_project_conditions(self, project_key):
        """
        Request type: GET
        Return a page of defaults conditions with reviewers list that have been configured for this project.
        For further information visit:
            https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-default-reviewers-rest.html#idm52264904368
        :projectKey: str
        :return:
        """
        url = self._url_project_conditions(project_key)
        return self.get(url) or {}

    def _url_project_condition(self, project_key, id_condition=None):
        url = "{}/condition".format(
            self._url_project(
                project_key,
                api_root="rest/default-reviewers",
                api_version="1.0",
            )
        )
        if id_condition is not None:
            url += "/{}".format(id_condition)
        return url

    def get_project_condition(self, project_key, id_condition):
        """
        Request type: GET
        Return a specific condition with reviewers list that has been configured for this project.
        For further information visit:
            https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-default-reviewers-rest.html#idm52264901504
        :projectKey: str - project key involved
        :idCondition: int - condition id involved
        :return:
        """
        url = self._url_project_condition(project_key, id_condition)
        return self.get(url) or {}

    def create_project_condition(self, project_key, condition):
        """
        Request type: POST
        Create a new condition for this project.
        For further information visit:
            https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-default-reviewers-rest.html#idm52264893584
        :projectKey: str- project key involved
        :data: condition: dictionary object
        :example condition: '{"sourceMatcher":
                                {"id":"any",
                                "type":{"id":"ANY_REF"}},
                                "targetMatcher":{"id":"refs/heads/master","type":{"id":"BRANCH"}},
                                "reviewers":[{"id": 12}],"requiredApprovals":"0"
                            }'
        :return:
        """
        url = self._url_project_condition(project_key)
        return self.post(url, data=condition) or {}

    def update_project_condition(self, project_key, condition, id_condition):
        """
        Request type: PUT
        Update a new condition for this project.
        For further information visit:
            https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-default-reviewers-rest.html#idm52264927632
        :projectKey: str- project key involved
        :idCondition: int - condition id involved
        :data: condition: dictionary object
        :example condition: '{"sourceMatcher":
                                {"id":"any",
                                "type":{"id":"ANY_REF"}},
                                "targetMatcher":{"id":"refs/heads/master","type":{"id":"BRANCH"}},
                                "reviewers":[{"id": 12}],"requiredApprovals":"0"
                            }'
        :return:
        """
        url = self._url_project_condition(project_key, id_condition)
        return self.put(url, data=condition) or {}

    def delete_project_condition(self, project_key, id_condition):
        """
        Delete a specific condition for this repository slug inside project.
        For further information visit:
            https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-default-reviewers-rest.html#idm52264896304
        Request type: DELETE
        :projectKey: str- project key involved
        :idCondition: int - condition id involved
        :return:
        """
        url = self._url_project_condition(project_key, id_condition)
        return self.delete(url) or {}

    def _url_project_audit_log(self, project_key):
        if self.cloud:
            raise Exception("Not supported in Bitbucket Cloud")

        return "{}/events".format(self._url_project(project_key, api_root="rest/audit"))

    def get_project_audit_log(self, project_key, start=0, limit=None):
        """
        Get the audit log of the project
        :param start:
        :param limit:
        :param project_key: The project key
        :return: List of events of the audit log
        """
        url = self._url_project_audit_log(project_key)
        params = {}
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        return self._get_paged(url, params=params)

    def _url_repos(self, project_key, api_root=None, api_version=None):
        return "{}/repos".format(self._url_project(project_key, api_root, api_version))

    def repo_list(self, project_key, start=0, limit=25):
        """
        Get repositories list from project

        :param project_key: The project key
        :param start:
        :param limit:
        :return:
        """
        url = self._url_repos(project_key)
        params = {}
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        return self._get_paged(url, params=params)

    def repo_all_list(self, project_key):
        """
        Get all repositories list from project
        :param project_key:
        :return:
        """
        return self.repo_list(project_key, limit=None)

    def create_repo(self, project_key, repository_slug, forkable=False, is_private=True):
        """Create a new repository.

        Requires an existing project in which this repository will be created. The only parameters which will be used
        are name and scmId.

        The authenticated user must have PROJECT_ADMIN permission for the context project to call this resource.

        :param project_key: The project matching the projectKey supplied in the resource path as shown in URL.
        :type project_key: str
        :param repository_slug: Name of repository to create (i.e. "My repo").
        :param forkable: Set the repository to be forkable or not.
        :type forkable: bool
        :param is_private: Set the repository to be private or not.
        :type is_private: bool
        :return:
            201 - application/json (repository)
            400 - application/json (errors)
            401 - application/json (errors)
            409 - application/json (errors)
        :rtype: requests.Response
        """
        url = self._url_repos(project_key)
        data = {
            "name": repository_slug,
            "scmId": "git",
            "forkable": forkable,
            "is_private": is_private,
        }
        return self.post(url, data=data)

    ################################################################################################
    # Functions related to a specific repository
    ################################################################################################

    def _url_repo(self, project_key, repo, api_root=None, api_version=None):
        return "{}/{}".format(self._url_repos(project_key, api_root, api_version), repo)

    def reindex_repo(self, project_key, repository_slug):
        """
        Reindex repo
        :param project_key:
        :param repository_slug:
        :return:
        """
        url = "{urlRepo}/sync".format(
            urlRepo=self._url_repo(
                project_key,
                repository_slug,
                api_root="rest/indexing",
                api_version="1.0",
            )
        )
        return self.post(url)

    def reindex_repo_dev_panel(self, project_key, repository_slug):
        """
        Reindex all the Jira issues related to this repository_slug, including branches and pull requests.
        This automatically happens as part of an upgrade, and calling this manually should only be required
        if something unforeseen happens and the index becomes out of sync.
        The authenticated user must have REPO_ADMIN permission for the specified repository to call this resource.
        :param project_key:
        :param repository_slug:
        :return:
        """
        url = "{}/reindex".format(self._url_repo(project_key, repository_slug, api_root="rest/jira-dev"))
        return self.post(url)

    def get_repo(self, project_key, repository_slug):
        """
        Get a specific repository from a project. This operates based on slug not name which may
        be confusing to some users.
        :param project_key: Key of the project you wish to look in.
        :param repository_slug: url-compatible repository identifier
        :return: Dictionary of request response
        """
        url = self._url_repo(project_key, repository_slug)
        return self.get(url)

    def repo_exists(self, project_key, repository_slug):
        """
        Check if given combination of project and repository exists and available.
        :param project_key: Key of the project where to check for repository.
        :param repository_slug: url-compatible repository identifier to look for.
        :return: False is requested repository doesn't exist in the project or not accessible to the requestor
        """
        exists = False
        try:
            self.get_repo(project_key, repository_slug)
            exists = True
        except HTTPError as e:
            if e.response.status_code in (401, 404):
                pass
        return exists

    def update_repo(self, project_key, repository_slug, **params):
        """
        Update a repository in a project. This operates based on slug not name which may
        be confusing to some users.
        :param project_key: Key of the project you wish to look in.
        :param repository_slug: url-compatible repository identifier
        :return: The value of the put request.
        """
        url = self._url_repo(project_key, repository_slug)
        return self.put(url, data=params)

    def delete_repo(self, project_key, repository_slug):
        """
        Delete a specific repository from a project. This operates based on slug not name which may
        be confusing to some users.
        :param project_key: Key of the project you wish to look in.
        :param repository_slug: url-compatible repository identifier
        :return: Dictionary of request response
        """
        url = self._url_repo(project_key, repository_slug)
        return self.delete(url)

    def fork_repository(self, project_key, repository_slug, new_repository_slug):
        """
        Forks a repository within the same project.
        :param project_key:
        :param repository_slug:
        :param new_repository_slug:
        :return:
        """
        url = self._url_repo(project_key, repository_slug)
        body = {}
        if new_repository_slug is not None:
            body["name"] = new_repository_slug
            body["project"] = {"key": project_key}
        return self.post(url, data=body)

    def fork_repository_new_project(
        self,
        project_key,
        repository_slug,
        new_project_key,
        new_repository_slug,
    ):
        """
        Forks a repository to a separate project.
        :param project_key: Origin Project Key
        :param repository_slug: Origin repository slug
        :param new_project_key: Project Key of target project
        :param new_repository_slug: Target Repository slug
        :return:
        """
        url = self._url_repo(project_key, repository_slug)
        body = {}
        if new_repository_slug is not None and new_project_key is not None:
            body["name"] = new_repository_slug
            body["project"] = {"key": new_project_key}
        return self.post(url, data=body)

    def repo_keys(self, project_key, repo_key, start=0, limit=None, filter_str=None):
        """
        Get SSH access keys added to the repository
        :param start:
        :param limit:
        :param project_key: The project key
        :param repo_key: The repository key
        :param filter_str:  OPTIONAL: users filter string
        :return:
        """
        url = "{}/ssh".format(self._url_repo(project_key, repo_key, api_root="rest/keys"))
        params = {}
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        if filter_str:
            params["filter"] = filter_str
        return self._get_paged(url, params=params)

    def _url_repo_users(self, project_key, repo):
        return "{}/permissions/users".format(self._url_repo(project_key, repo))

    def repo_users(self, project_key, repo_key, start=0, limit=None, filter_str=None):
        """
        Get users with permission in repository
        :param start:
        :param limit:
        :param project_key: The project key
        :param repo_key: The repository key
        :param filter_str:  OPTIONAL: Users filter string
        :return:
        """
        url = self._url_repo_users(project_key, repo_key)
        params = {}
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        if filter_str:
            params["filter"] = filter_str
        return self._get_paged(url, params=params)

    def repo_grant_user_permissions(self, project_key, repo_key, username, permission):
        """
        Grant the specified repository permission to a specific user
        :param project_key: The project key
        :param repo_key: The repository key (slug)
        :param username: username to be granted
        :param permission: the repository permissions available are 'REPO_ADMIN', 'REPO_WRITE' and 'REPO_READ'
        :return:
        """
        url = self._url_repo_users(project_key, repo_key)
        params = {"permission": permission, "name": username}
        return self.put(url, params=params)

    def repo_remove_user_permissions(self, project_key, repo_key, username):
        """
        Revoke all permissions for the specified repository for a user.
        The authenticated user must have REPO_ADMIN permission for the specified repository
        or a higher project or global permission to call this resource.
        In addition, a user may not revoke their own repository permissions
        if they do not have a higher project or global permission.
        :param project_key: The project key
        :param repo_key: The repository key (slug)
        :param username: username to be granted
        :return:
        """
        url = self._url_repo_users(project_key, repo_key)
        params = {"name": username}
        return self.delete(url, params=params)

    def _url_repo_groups(self, project_key, repo):
        return "{}/permissions/groups".format(self._url_repo(project_key, repo))

    def repo_groups(self, project_key, repo_key, start=0, limit=None, filter_str=None):
        """
        Get repository Groups
        :param start:
        :param limit:
        :param project_key: The project key
        :param repo_key: The repository key
        :param filter_str: OPTIONAL: group filter string
        :return:
        """
        url = self._url_repo_groups(project_key, repo_key)
        params = {}
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        if filter_str:
            params["filter"] = filter_str
        return self._get_paged(url, params=params)

    def project_groups_with_administrator_permissions(self, key):
        """
        Get groups with admin permissions
        :param key:
        :return:
        """
        return [group["group"]["name"] for group in self.project_groups(key) if group["permission"] == "PROJECT_ADMIN"]

    def repo_users_with_administrator_permissions(self, project_key, repo_key):
        """
        Get repository administrators for repository
        :param project_key: The project key
        :param repo_key: The repository key
        :return: List of repo administrators
        """
        repo_administrators = []
        for user in self.repo_users(project_key, repo_key):
            if user["permission"] == "REPO_ADMIN":
                repo_administrators.append(user)
        for group in self.repo_groups_with_administrator_permissions(project_key, repo_key):
            for user in self.group_members(group):
                repo_administrators.append(user)
        for user in self.project_users_with_administrator_permissions(project_key):
            repo_administrators.append(user)
        # We convert to a set to ensure uniqueness then back to a list for later useability
        return list({user["id"]: user for user in repo_administrators}.values())

    def repo_groups_with_administrator_permissions(self, project_key, repo_key):
        """
        Get groups with admin permissions
        :param project_key:
        :param repo_key:
        :return:
        """
        repo_group_administrators = []
        for group in self.repo_groups(project_key, repo_key):
            if group["permission"] == "REPO_ADMIN":
                repo_group_administrators.append(group["group"]["name"])
        for group in self.project_groups_with_administrator_permissions(project_key):
            repo_group_administrators.append(group)
        # We convert to a set to ensure uniqueness, then back to a list for later useability
        return list(set(repo_group_administrators))

    def repo_grant_group_permissions(self, project_key, repo_key, groupname, permission):
        """
        Grant the specified repository permission to a specific group
        Promote or demote a group's permission level for the specified repository. Available repository permissions are:
            REPO_READ
            REPO_WRITE
            REPO_ADMIN
        See the Bitbucket Server documentation for a detailed explanation of what each permission entails.
        The authenticated user must have REPO_ADMIN permission for the specified repository or a higher project
        or global permission to call this resource.
        In addition, a user may not demote a group's permission level
        if their own permission level would be reduced as a result.
        :param project_key: The project key
        :param repo_key: The repository key (slug)
        :param groupname: group to be granted
        :param permission: the repository permissions available are 'REPO_ADMIN', 'REPO_WRITE' and 'REPO_READ'
        :return:
        """
        url = self._url_repo_groups(project_key, repo_key)
        params = {"permission": permission, "name": groupname}
        return self.put(url, params=params)

    def repo_remove_group_permissions(self, project_key, repo_key, groupname, permission):
        """
        Revoke all permissions for the specified repository for a group.
        The authenticated user must have REPO_ADMIN permission for the specified repository
        or a higher project or global permission to call this resource.
        In addition, a user may not revoke a group's permissions if it will reduce their own permission level.
        :param project_key: The project key
        :param repo_key: The repository key (slug)
        :param groupname: group to be granted
        :param permission: the repository permissions available are 'REPO_ADMIN', 'REPO_WRITE' and 'REPO_READ'
        :return:
        """
        url = self._url_repo_groups(project_key, repo_key)
        params = {"name": groupname}
        if permission:
            params["permission"] = permission
        return self.delete(url, params=params)

    def _url_repo_labels(self, project_key, repository_slug):
        if self.cloud:
            raise Exception("Not supported in Bitbucket Cloud")

        return "{}/labels".format(self._url_repo(project_key, repository_slug))

    def get_repo_labels(self, project_key, repository_slug):
        """
        Get labels for a specific repository from a project. This operates based on slug not name which may
        be confusing to some users. (BitBucket Server only)
        :param project_key: Key of the project you wish to look in.
        :param repository_slug: url-compatible repository identifier
        :return: Dictionary of request response
        """
        url = self._url_repo_labels(project_key, repository_slug)
        return self.get(url)

    def set_repo_label(self, project_key, repository_slug, label_name):
        """
        Sets a label on a repository. (BitBucket Server only)
        The authenticated user must have REPO_ADMIN permission for the specified repository to call this resource.
        :param project_key: Key of the project you wish to look in.
        :param repository_slug: url-compatible repository identifier
        :param label_name: label name to apply
        :return:
        """
        url = self._url_repo_labels(project_key, repository_slug)
        data = {"name": label_name}
        return self.post(url, data=data)

    def _url_repo_audit_log(self, project_key, repository_slug):
        if self.cloud:
            raise Exception("Not supported in Bitbucket Cloud")

        return "{}/events".format(self._url_repo(project_key, repository_slug, api_root="rest/audit"))

    def get_repo_audit_log(self, project_key, repository_slug, start=0, limit=None):
        """
        Get the audit log of the repository
        :param start:
        :param limit:
        :param project_key: Key of the project you wish to look in.
        :param repository_slug: url-compatible repository identifier
        :return: List of events of the audit log
        """
        url = self._url_repo_audit_log(project_key, repository_slug)
        params = {}
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        return self._get_paged(url, params=params)

    def _url_repo_branches(self, project_key, repository_slug, api_root=None):
        return "{}/branches".format(self._url_repo(project_key, repository_slug, api_root=api_root))

    def get_branches(
        self,
        project_key,
        repository_slug,
        base=None,
        filter=None,
        start=0,
        limit=None,
        details=True,
        order_by="MODIFICATION",
    ):
        """
        Retrieve the branches matching the supplied filterText param.
        The authenticated user must have REPO_READ permission for the specified repository to call this resource.
        :param start:
        :param project_key:
        :param repository_slug:
        :param base: base branch/tag to compare each branch to (for the metadata providers that uses that information)
        :param filter:
        :param limit: OPTIONAL: The limit of the number of branches to return, this may be restricted by
                    fixed system limits. Default by built-in method: None
        :param details: whether to retrieve plugin-provided metadata about each branch
        :param order_by: OPTIONAL: ordering of refs either ALPHABETICAL (by name) or MODIFICATION (last updated)
        :return:
        """
        url = self._url_repo_branches(project_key, repository_slug)
        params = {}
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        if filter:
            params["filterText"] = filter
        if base:
            params["base"] = base
        if order_by:
            params["orderBy"] = order_by
        params["details"] = details
        return self._get_paged(url, params=params)

    def _url_repo_default_branche(self, project_key, repository_slug):
        return "{}/default".format(self._url_repo_branches(project_key, repository_slug))

    def get_default_branch(self, project_key, repository_slug):
        """
        Get the default branch of the repository.
        The authenticated user must have REPO_READ permission for the specified repository to call this resource.
        :param project_key: The project key
        :param repository_slug: The repository key
        :return:
        """
        url = self._url_repo_default_branche(project_key, repository_slug)
        return self.get(url)

    def set_default_branch(self, project_key, repository_slug, ref_branch_name):
        """
        Update the default branch of a repository.
        The authenticated user must have REPO_ADMIN permission for the specified repository to call this resource.
        :param project_key: The project key
        :param repository_slug: The repository key (slug)
        :param ref_branch_name: ref name like refs/heads/master
        :return:
        """
        url = self._url_repo_default_branche(project_key, repository_slug)
        data = {"id": ref_branch_name}
        return self.put(url, data=data)

    def create_branch(self, project_key, repository_slug, name, start_point, message=""):
        """Creates a branch using the information provided in the request.

        The authenticated user must have REPO_WRITE permission for the context repository to call this resource.

        :param project_key: The project matching the projectKey supplied in the resource path as shown in URL.
        :type project_key: str
        :param repository_slug: Name of repository where branch is created (i.e. "my_repo").
        :param name: Name of branch to create (i.e. "my_branch").
        :type name: str
        :param start_point: Name of branch to branch from.
        :type start_point: str
        :param message: Branch message.
        :type message: str
        :return:
            200 - application/json (repository)
            401 - application/json (errors)
            404 - application/json (errors)
        :rtype: requests.Response
        """
        url = self._url_repo_branches(project_key, repository_slug)
        data = {"name": name, "startPoint": start_point, "message": message}
        return self.post(url, data=data)

    def delete_branch(self, project_key, repository_slug, name, end_point=None):
        """
        Delete branch from related repo
        :param self:
        :param project_key:
        :param repository_slug:
        :param name:
        :param end_point:
        :return:
        """
        url = self._url_repo_branches(project_key, repository_slug, api_root="rest/branch-utils")
        data = {"name": str(name)}
        if end_point:
            data["endPoint"] = end_point
        return self.delete(url, data=data)

    def _url_repo_tags(self, project_key, repository_slug, api_root=None):
        if self.cloud:
            return "{}/refs/tags".format(self._url_repo(project_key, repository_slug, api_root=api_root))
        else:
            return "{}/tags".format(self._url_repo(project_key, repository_slug, api_root=api_root))

    def get_tags(
        self,
        project_key,
        repository_slug,
        filter="",
        limit=1000,
        order_by=None,
        start=0,
    ):
        """
        Retrieve the tags matching the supplied filterText param.
        The authenticated user must have REPO_READ permission for the context repository to call this resource.
        :param project_key:
        :param repository_slug:
        :param filter:
        :param start:
        :param limit: OPTIONAL: The limit of the number of tags to return, this may be restricted by
                fixed system limits. Default by built-in method: 1000
        :param order_by: OPTIONAL: ordering of refs either ALPHABETICAL (by name) or MODIFICATION (last updated)
        :return:
        """
        url = self._url_repo_tags(project_key, repository_slug)
        params = {}
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        if filter:
            params["filterText"] = filter
        if order_by:
            params["orderBy"] = order_by
        return self._get_paged(url, params=params)

    def get_project_tags(self, project_key, repository_slug, tag_name=None):
        """
        Retrieve a tag in the specified repository.
        The authenticated user must have REPO_READ permission for the context repository to call this resource.
        Search uri is api/1.0/projects/{projectKey}/repos/{repositorySlug}/tags/{name:.*}
        :param project_key:
        :param repository_slug:
        :param tag_name: OPTIONAL:
        :return:
        """
        url = self._url_repo_tags(project_key, repository_slug)
        if tag_name is not None:
            return self.get("{}/{}".format(url, tag_name))

        return self._get_paged(url)

    def set_tag(
        self,
        project_key,
        repository_slug,
        tag_name,
        commit_revision,
        description=None,
    ):
        """
        Creates a tag using the information provided in the {@link RestCreateTagRequest request}
        The authenticated user must have REPO_WRITE permission for the context repository to call this resource.
        :param project_key:
        :param repository_slug:
        :param tag_name:
        :param commit_revision: commit hash
        :param description: OPTIONAL:
        :return:
        """
        url = self._url_repo_tags(project_key, repository_slug)
        body = {
            "name": tag_name,
            "startPoint": commit_revision,
        }
        if description is not None:
            body["message"] = description

        return self.post(url, data=body)

    def delete_tag(self, project_key, repository_slug, tag_name):
        """
        Creates a tag using the information provided in the {@link RestCreateTagRequest request}
        The authenticated user must have REPO_WRITE permission for the context repository to call this resource.
        :param project_key:
        :param repository_slug:
        :param tag_name:
        :return:
        """
        url = "{}/{}".format(
            self._url_repo_tags(project_key, repository_slug, api_root="rest/git"),
            tag_name,
        )
        return self.delete(url)

    def _url_repo_hook_settings(self, project_key, repository_slug):
        return "{}/settings/hooks".format(self._url_repo(project_key, repository_slug))

    def all_repo_hook_settings(
        self,
        project_key,
        repository_slug,
        start=0,
        limit=None,
        filter_type=None,
    ):
        """
        Get all repository hooks for a given repo
        :param project_key: The project key
        :param repository_slug: The repository key
        :param start:
        :param limit: OPTIONAL: The limit of the number of changes to return, this may be restricted by
                fixed system limits. Default by built-in method: None
        :param filter_type: OPTIONAL: PRE_RECEIVE|POST_RECEIVE if present,
                                    controls how repository hooks should be filtered.
        :return:
        """
        url = self._url_repo_hook_settings(project_key, repository_slug)
        params = {}
        if filter_type:
            params["type"] = filter_type
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        return self._get_paged(url, params)

    def get_repo_hook_settings(self, project_key, repository_slug, hook_key):
        """
        Get a repository hook from a given repo
        :param project_key: The project key
        :param repository_slug: The repository key
        :param hook_key: The repository hook key
        :return:
        """
        url = "{}/{}".format(
            self._url_repo_hook_settings(project_key, repository_slug),
            hook_key,
        )
        return self.get(url)

    def enable_repo_hook_settings(self, project_key, repository_slug, hook_key):
        """
        Enable a repository hook for a given repo
        :param project_key: The project key
        :param repository_slug: The repository key
        :param hook_key: The repository hook key
        :return:
        """
        url = "{}/{}/enabled".format(
            self._url_repo_hook_settings(project_key, repository_slug),
            hook_key,
        )
        return self.put(url)

    def disable_repo_hook_settings(self, project_key, repository_slug, hook_key):
        """
        Disable a repository hook for a given repo
        :param project_key: The project key
        :param repository_slug: The repository key
        :param hook_key: The repository hook key
        :return:
        """
        url = "{}/{}/enabled".format(
            self._url_repo_hook_settings(project_key, repository_slug),
            hook_key,
        )
        return self.delete(url)

    def _url_webhooks(self, project_key, repository_slug):
        return "{}/webhooks".format(self._url_repo(project_key, repository_slug))

    def get_webhooks(
        self,
        project_key,
        repository_slug,
        event=None,
        statistics=False,
    ):
        """
        Get webhooks
        :param project_key:
        :param repository_slug:
        :param event: OPTIONAL: defaults to None
        :param statistics: OPTIONAL: defaults to False
        :return:
        """
        url = self._url_webhooks(project_key, repository_slug)
        params = {}
        if event:
            params["event"] = event
        if statistics:
            params["statistics"] = statistics
        return self._get_paged(url, params=params)

    def create_webhook(
        self,
        project_key,
        repository_slug,
        name,
        events,
        webhook_url,
        active,
        secret=None,
    ):
        """Creates a webhook using the information provided in the request.

        The authenticated user must have REPO_ADMIN permission for the context repository to call this resource.

        :param project_key: The project matching the projectKey supplied in the resource path as shown in URL.
        :param repository_slug:
        :param name: Name of webhook to create.
        :param events: List of event. (i.e. ["repo:refs_changed", "pr:merged", "pr:opened"])
        :param webhook_url:
        :param active:
        :param secret: The string is used to verify data integrity between Bitbucket and your endpoint.
        :return:
        """
        url = self._url_webhooks(project_key, repository_slug)
        body = {
            "name": name,
            "events": events,
            "url": webhook_url,
            "active": active,
        }
        if secret:
            body["configuration"] = {"secret": secret}
        return self.post(url, data=body)

    def _url_webhook(self, project_key, repository_slug, webhook_id):
        return "{}/{}".format(self._url_webhooks(project_key, repository_slug), webhook_id)

    def get_webhook(self, project_key, repository_slug, webhook_id):
        """
        Retrieve a webhook.
        The authenticated user must have REPO_ADMIN permission for the context repository to call this resource.
        :param project_key:
        :param repository_slug:
        :param webhook_id: the ID of the webhook within the repository
        :return:
        """
        url = self._url_webhook(project_key, repository_slug, webhook_id)
        return self.get(url)

    def update_webhook(self, project_key, repository_slug, webhook_id, **params):
        """
        Update a webhook.
        The authenticated user must have REPO_ADMIN permission for the context repository to call this resource.
        :param project_key:
        :param repository_slug:
        :param webhook_id: the ID of the webhook within the repository
        :return:
        """
        url = self._url_webhook(project_key, repository_slug, webhook_id)
        return self.put(url, data=params)

    def delete_webhook(self, project_key, repository_slug, webhook_id):
        """
        Delete a webhook.
        The authenticated user must have REPO_ADMIN permission for the context repository to call this resource.
        :param project_key:
        :param repository_slug:
        :param webhook_id: the ID of the webhook within the repository
        :return:
        """
        url = self._url_webhook(project_key, repository_slug, webhook_id)
        return self.delete(url)

    def _url_pull_request_settings(self, project_key, repository_slug):
        return "{}/settings/pull-requests".format(self._url_repo(project_key, repository_slug))

    def get_pull_request_settings(self, project_key, repository_slug):
        """
        Get pull request settings.
        :param project_key:
        :param repository_slug:
        :return:
        """
        url = self._url_pull_request_settings(project_key, repository_slug)
        return self.get(url)

    def set_pull_request_settings(self, project_key, repository_slug, data):
        """
        Set pull request settings.
        :param project_key:
        :param repository_slug:
        :param data: json body
        :return:
        """
        url = self._url_pull_request_settings(project_key, repository_slug)
        return self.post(url, data=data)

    def _url_pull_requests(self, project_key, repository_slug):
        if self.cloud:
            return self.resource_url("repositories/{}/{}/pullrequests".format(project_key, repository_slug))
        else:
            return "{}/pull-requests".format(self._url_repo(project_key, repository_slug))

    def get_pull_requests(
        self,
        project_key,
        repository_slug,
        state="OPEN",
        order="newest",
        limit=100,
        start=0,
        at=None,
    ):
        """
        Get pull requests
        :param project_key:
        :param repository_slug:
        :param state:
        :param order: OPTIONAL: defaults to NEWEST the order to return pull requests in, either OLDEST
                                (as in: "oldest first") or NEWEST.
        :param limit:
        :param start:
        :param at:
        :return:
        """
        url = self._url_pull_requests(project_key, repository_slug)
        params = {}
        if state:
            params["state"] = state
        if limit:
            params["limit"] = limit
        if start:
            params["start"] = start
        if order:
            params["order"] = order
        if at:
            params["at"] = at
        return self._get_paged(url, params=params)

    def open_pull_request(
        self,
        source_project,
        source_repo,
        dest_project,
        dest_repo,
        source_branch,
        destination_branch,
        title,
        description,
        reviewers=None,
    ):
        """
        Create a new pull request between two branches.
        The branches may be in the same repository_slug, or different ones.
        When using different repositories, they must still be in the same {@link Repository#getHierarchyId() hierarchy}.
        The authenticated user must have REPO_READ permission for the "from" and "to"repositories to call this resource.
        :param source_project: the project that the PR source is from
        :param source_repo: the repository that the PR source is from
        :param source_branch: the branch name of the PR
        :param dest_project: the project that the PR destination is from
        :param dest_repo: the repository that the PR destination is from
        :param destination_branch: where the PR is being merged into
        :param title: the title of the PR
        :param description: the description of what the PR does
        :param reviewers: the list of reviewers or a single reviewer of the PR
        :return:
        """
        body = {
            "title": title,
            "description": description,
            "fromRef": {
                "id": source_branch,
                "repository": {
                    "slug": source_repo,
                    "name": source_repo,
                    "project": {"key": source_project},
                },
            },
            "toRef": {
                "id": destination_branch,
                "repository": {
                    "slug": dest_repo,
                    "name": dest_repo,
                    "project": {"key": dest_project},
                },
            },
            "reviewers": [],
        }

        def add_reviewer(reviewer_name):
            entry = {"user": {"name": reviewer_name}}
            body["reviewers"].append(entry)

        if reviewers is not None:
            if isinstance(reviewers, str):
                add_reviewer(reviewers)
            elif isinstance(reviewers, list):
                for reviewer in reviewers:
                    add_reviewer(reviewer)

        return self.create_pull_request(dest_project, dest_repo, body)

    def create_pull_request(self, project_key, repository_slug, data):
        """
        :param project_key:
        :param repository_slug:
        :param data: json body
        :return:
        """
        url = self._url_pull_requests(project_key, repository_slug)
        return self.post(url, data=data)

    def _url_pull_request(self, project_key, repository_slug, pull_request_id):
        return "{}/{}".format(
            self._url_pull_requests(project_key, repository_slug),
            pull_request_id,
        )

    def get_pull_request(self, project_key, repository_slug, pull_request_id):
        """
        Retrieve a pull request.
        The authenticated user must have REPO_READ permission
        for the repository that this pull request targets to call this resource.
        :param project_key:
        :param repository_slug:
        :param pull_request_id: the ID of the pull request within the repository
        :return:
        """
        url = self._url_pull_request(project_key, repository_slug, pull_request_id)
        return self.get(url)

    @deprecated(version="1.15.1", reason="Use get_pull_request()")
    def get_pullrequest(self, *args, **kwargs):
        """
        Deprecated name since 1.15.1. Let's use the get_pull_request()
        """

    def update_pull_request(self, project_key, repository_slug, pull_request_id, data):
        """
        Update a pull request.
        The authenticated user must have REPO_WRITE permission
        for the repository that this pull request targets to call this resource.
        :param project_key:
        :param repository_slug:
        :param pull_request_id: the ID of the pull request within the repository
        :param data: json body
        :return:
        """

        url = self._url_pull_request(project_key, repository_slug, pull_request_id)
        return self.put(url, data=data)

    def delete_pull_request(
        self,
        project_key,
        repository_slug,
        pull_request_id,
        pull_request_version,
    ):
        """
        Delete a pull request.

        :param project_key: the project key
        :param repository_slug: the repository slug
        :param pull_request_id: the ID of the pull request within the repository
        :param pull_request_version: the version of the pull request
        :return:
        """
        url = self._url_pull_request(project_key, repository_slug, pull_request_id)
        data = {"version": pull_request_version}
        return self.delete(url, data=data)

    def get_pull_requests_activities(
        self,
        project_key,
        repository_slug,
        pull_request_id,
        start=0,
        limit=None,
    ):
        """
        Get pull requests activities
        :param limit:
        :param project_key:
        :param repository_slug:
        :param pull_request_id: the ID of the pull request within the repository
        :param start:
        :return:
        """
        url = "{}/activities".format(self._url_pull_request(project_key, repository_slug, pull_request_id))
        params = {}
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        return self._get_paged(url, params)

    def get_pull_requests_changes(
        self,
        project_key,
        repository_slug,
        pull_request_id,
        start=0,
        limit=None,
    ):
        """
        Get pull requests changes
        :param start:
        :param limit:
        :param project_key:
        :param repository_slug:
        :param pull_request_id: the ID of the pull request within the repository
        :return:
        """
        url = "{}/changes".format(self._url_pull_request(project_key, repository_slug, pull_request_id))
        params = {}
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        return self._get_paged(url, params)

    def get_pull_requests_commits(
        self,
        project_key,
        repository_slug,
        pull_request_id,
        start=0,
        limit=None,
    ):
        """
        Get pull requests commits
        :param start:
        :param limit:
        :param project_key:
        :param repository_slug:
        :param pull_request_id: the ID of the pull request within the repository
        :start
        :limit
        :return:
        """
        url = "{}/commits".format(self._url_pull_request(project_key, repository_slug, pull_request_id))
        params = {}
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        return self._get_paged(url, params)

    def _url_pull_request_participants(self, project_key, repository_slug, pull_request_id):
        return "{}/{}/participants".format(
            self._url_pull_requests(project_key, repository_slug),
            pull_request_id,
        )

    def get_pull_requests_participants(
        self,
        project_key,
        repository_slug,
        pull_request_id,
        start=0,
        limit=None,
    ):
        """
        Get all participants of a pull request
        :param start:
        :param limit:
        :param project_key:
        :param repository_slug:
        :param pull_request_id:
        :return:
        """
        url = self._url_pull_request_participants(project_key, repository_slug, pull_request_id)
        params = {}
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        return self._get_paged(url, params)

    def change_reviewed_status(self, project_key, repository_slug, pull_request_id, status, user_slug):
        """
        Change the current user's status for a pull request.
        Implicitly adds the user as a participant if they are not already.
        If the current user is the author, this method will fail.
        :param project_key
        :param repository_slug:
        :param pull_request_id:
        :param status:
        :param user_slug:
        :return:
        """
        url = "{}/{}".format(
            self._url_pull_request_participants(project_key, repository_slug, pull_request_id),
            user_slug,
        )
        approved = True if status == "APPROVED" else False
        data = {
            "user": {"name": user_slug},
            "approved": approved,
            "status": status,
        }
        return self.put(url, data)

    def _url_pull_request_comments(self, project_key, repository_slug, pull_request_id):
        url = "{}/comments".format(self._url_pull_request(project_key, repository_slug, pull_request_id))
        return url

    def add_pull_request_comment(
        self,
        project_key,
        repository_slug,
        pull_request_id,
        text,
        parent_id=None,
    ):
        """
        Add comment into pull request
        :param project_key:
        :param repository_slug:
        :param pull_request_id: the ID of the pull request within the repository
        :param text comment text
        :param parent_id parent comment id

        :return:
        """
        url = self._url_pull_request_comments(project_key, repository_slug, pull_request_id)
        body = {"text": text}
        if parent_id:
            body["parent"] = {"id": parent_id}
        return self.post(url, data=body)

    def _url_pull_request_comment(self, project_key, repository_slug, pull_request_id, comment_id):
        url = "{}/{}".format(
            self._url_pull_request_comments(project_key, repository_slug, pull_request_id),
            comment_id,
        )
        return url

    def get_pull_request_comment(self, project_key, repository_slug, pull_request_id, comment_id):
        """
        Retrieves a pull request comment.
        The authenticated user must have REPO_READ permission
        for the repository that this pull request targets to call this resource.
        :param project_key:
        :param repository_slug:
        :param pull_request_id: the ID of the pull request within the repository
        :param comment_id: the ID of the comment to retrieve
        :return:
        """
        url = self._url_pull_request_comment(project_key, repository_slug, pull_request_id, comment_id)
        return self.get(url)

    def update_pull_request_comment(
        self,
        project_key,
        repository_slug,
        pull_request_id,
        comment_id,
        comment,
        comment_version,
    ):
        """
        Update the text of a comment.
        Only the user who created a comment may update it.

        Note: the supplied JSON object must contain a version
        that must match the server's version of the comment
        or the update will fail.
        """
        url = self._url_pull_request_comment(project_key, repository_slug, pull_request_id, comment_id)
        data = {"version": comment_version, "text": comment}
        return self.put(url, data=data)

    @deprecated(version="2.4.2", reason="Use delete_pull_request_comment()")
    def delete_pull_reques_comment(
        self,
        project_key,
        repository_slug,
        pull_request_id,
        comment_id,
        comment_version,
    ):
        """
        Deprecated name since 2.4.2. Let's use the get_pull_request()
        """
        return self.delete_pull_request_comment(
            project_key,
            repository_slug,
            pull_request_id,
            comment_id,
            comment_version,
        )

    def delete_pull_request_comment(
        self,
        project_key,
        repository_slug,
        pull_request_id,
        comment_id,
        comment_version,
    ):
        """
        Delete a comment.
        Only the repository admin or user who created a comment may update it.

        Note: the supplied JSON object must contain a version
        that must match the server's version of the comment
        or delete will fail.
        """
        url = self._url_pull_request_comment(project_key, repository_slug, pull_request_id, comment_id)
        data = {"version": comment_version}
        return self.delete(url, params=data)

    def decline_pull_request(self, project_key, repository_slug, pr_id, pr_version):
        """
        Decline a pull request.
        The authenticated user must have REPO_READ permission for the repository
        that this pull request targets to call this resource.

        :param project_key: PROJECT
        :param repository_slug: my_shiny_repo
        :param pr_id: 2341
        :param pr_version: 12
        :return:
        """
        url = "{}/decline".format(self._url_pull_request(project_key, repository_slug, pr_id))
        params = {}
        if not self.cloud:
            params["version"] = pr_version
        return self.post(url, params=params)

    def get_tasks(self, project_key, repository_slug, pull_request_id):
        """
        Get all tasks for the pull request
        :param project_key:
        :param repository_slug:
        :param pull_request_id: the ID of the pull request within the repository
        :return:
        """
        if self.cloud:
            raise Exception("Not supported in Bitbucket Cloud")
        url = "{}/tasks".format(self._url_pull_request(project_key, repository_slug, pull_request_id))
        return self.get(url)

    def _url_tasks(self):
        if self.cloud:
            raise Exception("Not supported in Bitbucket Cloud")
        return self.resource_url("tasks")

    def add_task(self, anchor, text):
        """
        Add task to the comment
        :param anchor: ID of the comment,
        :param text: task text
        :return:
        """
        url = self._url_tasks()
        data = {"anchor": {"id": anchor, "type": "COMMENT"}, "text": text}
        return self.post(url, data=data)

    def _url_task(self, task_id):
        return "{}/{}".format(self._url_tasks(), task_id)

    def get_task(self, task_id):
        """
        Get task information by ID
        :param task_id:
        :return:
        """
        url = self._url_task(task_id)
        return self.get(url)

    def delete_task(self, task_id):
        """
        Delete task by ID
        :param task_id:
        :return:
        """
        url = self._url_task(task_id)
        return self.delete(url)

    def update_task(self, task_id, text=None, state=None):
        """
        Update task by ID. It is possible to update state and/or text of the task
        :param task_id:
        :param text:
        :param state: OPEN, RESOLVED
        :return:
        """
        url = self._url_task(task_id)
        data = {"id": task_id}
        if text:
            data["text"] = text
        if state:
            data["state"] = state
        return self.put(url, data=data)

    def is_pull_request_can_be_merged(self, project_key, repository_slug, pr_id):
        """
        Test whether a pull request can be merged.
        A pull request may not be merged if:
        - there are conflicts that need to be manually resolved before merging; and/or
        - one or more merge checks have vetoed the merge.
        The authenticated user must have REPO_READ permission for the repository
        that this pull request targets to call this resource.

        :param project_key: PROJECT
        :param repository_slug: my_shiny_repo
        :param pr_id: 2341
        :return:
        """
        url = "{}/merge".format(self._url_pull_request(project_key, repository_slug, pr_id))
        return self.get(url)

    def merge_pull_request(self, project_key, repository_slug, pr_id, pr_version):
        """
        Merge pull request
        The authenticated user must have REPO_READ permission for the repository
        that this pull request targets to call this resource.

        :param project_key: PROJECT
        :param repository_slug: my_shiny_repo
        :param pr_id: 2341
        :param pr_version:
        :return:
        """
        url = "{}/merge".format(self._url_pull_request(project_key, repository_slug, pr_id))
        params = {}
        if not self.cloud:
            params["version"] = pr_version
        return self.post(url, params=params)

    def reopen_pull_request(self, project_key, repository_slug, pr_id, pr_version):
        """
        Re-open a declined pull request.
        The authenticated user must have REPO_READ permission for the repository
        that this pull request targets to call this resource.

        :param project_key: PROJECT
        :param repository_slug: my_shiny_repo
        :param pr_id: 2341
        :param pr_version: 12
        :return:
        """
        url = "{}/reopen".format(self._url_pull_request(project_key, repository_slug, pr_id))
        params = {"version": pr_version}
        return self.post(url, params=params)

    def _url_inbox_pull_requests(self):
        return "inbox/pull-requests"

    def check_inbox_pull_requests_count(self):
        url = "{}/count".format(self._url_inbox_pull_requests())
        return self.get(url)

    def check_inbox_pull_requests(self, start=0, limit=None, role=None):
        """
        Get pull request in your inbox
        :param start:
        :param limit:
        :param role:
        :return:
        """
        url = self._url_inbox_pull_requests()
        params = {"start": start}
        if limit:
            params["limit"] = limit
        if role:
            params["role"] = role
        return self._get_paged(url, params=params)

    def _url_repo_compare(self, project_key, repository_slug):
        url = "{}/compare".format(self._url_repo(project_key, repository_slug))
        return url

    def get_diff(self, project_key, repository_slug, path, hash_oldest, hash_newest):
        """
        Gets a diff of the changes available in the {@code from} commit but not in the {@code to} commit.
        If either the {@code from} or {@code to} commit are not specified,
        they will be replaced by the default branch of their containing repository.
        :param project_key:
        :param repository_slug:
        :param path:
        :param hash_oldest: the source commit (can be a partial/full commit ID or qualified/unqualified ref name)
        :param hash_newest: the target commit (can be a partial/full commit ID or qualified/unqualified ref name)
        :return:
        """
        url = "{}/diff/{}".format(self._url_repo_compare(project_key, repository_slug), path)
        params = {}
        if hash_oldest:
            params["from"] = hash_oldest
        if hash_newest:
            params["to"] = hash_newest
        return (self.get(url, params=params) or {}).get("diffs")

    def _url_commits(self, project_key, repository_slug, api_root=None, api_version=None):
        return "{}/commits".format(
            self._url_repo(
                project_key,
                repository_slug,
                api_root=api_root,
                api_version=api_version,
            )
        )

    def get_commits(
        self,
        project_key,
        repository_slug,
        hash_oldest=None,
        hash_newest=None,
        follow_renames=False,
        ignore_missing=False,
        merges="include",
        with_counts=False,
        avatar_size=None,
        avatar_scheme=None,
        limit=None,
        until=None,
        since=None,
    ):
        """
        Get commit list from repo
        :param project_key:
        :param repository_slug:
        :param hash_oldest:
        :param hash_newest:
        :param merges: OPTIONAL: include|exclude|only if present, controls how merge commits should be filtered.
        :param follow_renames: OPTIONAL: if true, the commit history of the specified file will be followed past renames
        :param ignore_missing: OPTIONAL: true to ignore missing commits, false otherwise
        :param with_counts: OPTIONAL: optionally include the total number of commits and total number of unique authors
        :param avatar_size: OPTIONAL: if present the service adds avatar URLs for commit authors.
        :param avatar_scheme: OPTIONAL: the desired scheme for the avatar URL
        :param limit: OPTIONAL: The limit of the number of commits to return, this may be restricted by
               fixed system limits. Default by built-in method: None
        :param until: OPTIONAL: The commit ID or ref (inclusively) to retrieve commits before
        :param since: OPTIONAL: The commit ID or ref (exclusively) to retrieve commits after
        :return:
        """
        url = self._url_commits(project_key, repository_slug)
        params = {"merges": merges}
        if hash_oldest:
            params["since"] = hash_oldest
        if hash_newest:
            params["until"] = hash_newest
        if follow_renames:
            params["followRenames"] = follow_renames
        if ignore_missing:
            params["ignoreMissing"] = ignore_missing
        if with_counts:
            params["withCounts"] = with_counts
        if avatar_size:
            params["avatarSize"] = avatar_size
        if avatar_scheme:
            params["avatarScheme"] = avatar_scheme
        if limit:
            params["limit"] = limit
        if self.cloud and (since or until):
            raise Exception("Not supported in Bitbucket Cloud")
        if since:
            params["since"] = since
        if until:
            params["until"] = until
        return self._get_paged(url, params=params)

    def get_commit_changes(self, project_key, repository_slug, hash_newest=None, merges="include", commit_id=None):
        """
        Get commit list from repo
        :param project_key:
        :param repository_slug:
        :param hash_newest:
        :param merges: OPTIONAL: include|exclude|only if present, controls how merge commits should be filtered.
        :param commit_id
        :return:
        """
        url = self._url_commit_c(project_key, repository_slug, commit_id=commit_id)
        params = {"merges": merges}
        if hash_newest:
            params["until"] = hash_newest
        return self.get(url, params=params)

    def _url_commit_c(self, project_key, repository_slug, api_root=None, api_version=None, commit_id=None):
        return "{}/commits/{}/changes".format(
            self._url_repo(
                project_key,
                repository_slug,
                api_root=api_root,
                api_version=api_version,
            ),
            commit_id,
        )

    def _url_commit(
        self,
        project_key,
        repository_slug,
        commit_id,
        api_root=None,
        api_version=None,
    ):
        return "{}/{}".format(
            self._url_commits(
                project_key,
                repository_slug,
                api_root=api_root,
                api_version=api_version,
            ),
            commit_id,
        )

    def get_commit_info(self, project_key, repository_slug, commit, path=None):
        """
        Retrieve a single commit identified by its ID>. In general, that ID is a SHA1.
        From 2.11, ref names like "refs/heads/master" are no longer accepted by this resource.
        The authenticated user must have REPO_READ permission for the specified repository to call this resource.
        :param project_key:
        :param repository_slug:
        :param commit: the commit ID to retrieve
        :param path :OPTIONAL an optional path to filter the commit by.
                        If supplied the details returned may not be for the specified commit.
                        Instead, starting from the specified commit, they will be the details for the first commit
                        affecting the specified path.
        :return:
        """

        url = self._url_commit(project_key, repository_slug, commit)
        params = {}
        if path:
            params["path"] = path
        return self.get(url, params=params)

    def _url_commit_pull_requests(self, project_key, repository_slug, commit_id):
        return "{}/pull-requests".format(self._url_commit(project_key, repository_slug, commit_id))

    def get_pull_requests_contain_commit(self, project_key, repository_slug, commit):
        url = self._url_commit_pull_requests(project_key, repository_slug, commit)
        return (self.get(url) or {}).get("values")

    def get_changelog(
        self,
        project_key,
        repository_slug,
        ref_from,
        ref_to,
        start=0,
        limit=None,
    ):
        """
        Get change log between 2 refs
        :param start:
        :param project_key:
        :param repository_slug:
        :param ref_from:
        :param ref_to:
        :param limit: OPTIONAL: The limit of the number of changes to return, this may be restricted by
                fixed system limits. Default by built-in method: None
        :return:
        """
        url = "{}/compare/commits".format(self._url_repo(project_key, repository_slug))
        params = {}
        if ref_from:
            params["from"] = ref_from
        if ref_to:
            params["to"] = ref_to
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        return self._get_paged(url, params=params)

    def _url_code_insights_annotations(self, project_key, repository_slug, commit_id, report_key):
        return "{}/reports/{}/annotations".format(
            self._url_commit(
                project_key,
                repository_slug,
                commit_id,
                api_root="rest/insights",
                api_version="1.0",
            ),
            report_key,
        )

    def add_code_insights_annotations_to_report(self, project_key, repository_slug, commit_id, report_key, annotations):
        """
        Adds annotations to an existing insight report.
        For further information visit:
        https://docs.atlassian.com/bitbucket-server/rest/6.6.1/bitbucket-code-insights-rest.html
        :project_key: str
        :repository_slug: str
        :commit_id: str
        :report_key: str
        :annotations: list
        """
        url = self._url_code_insights_annotations(project_key, repository_slug, commit_id, report_key)
        data = {"annotations": annotations}
        return self.post(url, data=data)

    def _url_code_insights_report(self, project_key, repository_slug, commit_id, report_key):
        return "{}/reports/{}".format(
            self._url_commit(
                project_key,
                repository_slug,
                commit_id,
                api_root="rest/insights",
                api_version="1.0",
            ),
            report_key,
        )

    def get_code_insights_report(self, project_key, repository_slug, commit_id, report_key):
        """
        Retrieve the specified code-insights report.
        :projectKey: str
        :repositorySlug: str
        :commit_id: str
        :report_key: str
        """
        url = self._url_code_insights_report(project_key, repository_slug, commit_id, report_key)
        return self.get(url)

    def delete_code_insights_report(self, project_key, repository_slug, commit_id, report_key):
        """
        Delete a report for the given commit. Also deletes any annotations associated with this report.
        :projectKey: str
        :repositorySlug: str
        :commit_id: str
        :report_key: str
        """
        url = self._url_code_insights_report(project_key, repository_slug, commit_id, report_key)
        return self.delete(url)

    def create_code_insights_report(
        self,
        project_key,
        repository_slug,
        commit_id,
        report_key,
        report_title,
        **report_params
    ):  # fmt: skip
        """
        Create a new insight report, or replace the existing one
        if a report already exists for the given repository_slug, commit, and report key.
        A request to replace an existing report will be rejected
        if the authenticated user was not the creator of the specified report.
        For further information visit:
        https://docs.atlassian.com/bitbucket-server/rest/6.6.1/bitbucket-code-insights-rest.html
        :projectKey: str
        :repositorySlug: str
        :commitId: str
        :report_key: str
        :report_title: str
        :report_params:
        """
        url = self._url_code_insights_report(project_key, repository_slug, commit_id, report_key)
        data = {"title": report_title}
        data.update(report_params)
        return self.put(url, data=data)

    def get_file_list(
        self,
        project_key,
        repository_slug,
        sub_folder=None,
        query=None,
        start=0,
        limit=None,
    ):
        """
        Retrieve a page of files from particular directory of a repository.
        The search is done recursively, so all files from any subdirectory of the specified directory will be returned.
        The authenticated user must have REPO_READ permission for the specified repository to call this resource.
        :param start:
        :param project_key:
        :param repository_slug:
        :param sub_folder: a sub folder in the target repository to list the files from.
        :param query: the commit ID or ref (e.g. a branch or tag) to list the files at.
                      If not specified the default branch will be used instead.
        :param limit: OPTIONAL
        :return:
        """
        url = "{}/files".format(self._url_repo(project_key, repository_slug))
        if sub_folder:
            url = "{}/{}".format(url, sub_folder.lstrip("/"))
        params = {}
        if query:
            params["at"] = query
        if start:
            params["start"] = start
        if limit:
            params["limit"] = limit
        return self._get_paged(url, params=params)

    def get_content_of_file(self, project_key, repository_slug, filename, at=None, markup=None):
        """
        Retrieve the raw content for a file path at a specified revision.
        The authenticated user must have REPO_READ permission for the specified repository to call this resource.
        :param project_key:
        :param repository_slug:
        :param filename:
        :param at: OPTIONAL ref string
        :param markup: if present or "true", triggers the raw content to be markup-rendered and returned as HTML;
            otherwise, if not specified, or any value other than "true" the content is streamed without markup.
        :return:
        """
        url = "{}/raw/{}".format(self._url_repo(project_key, repository_slug), filename)
        params = {}
        if at is not None:
            params["at"] = at
        if markup is not None:
            params["markup"] = markup
        headers = self.form_token_headers
        return self.get(url, params=params, not_json_response=True, headers=headers)

    def _url_branches_permissions(self, project_key, permission_id=None, repository_slug=None):
        if repository_slug is None:
            base = self._url_project(
                project_key,
                api_root="rest/branch-permissions",
                api_version="2.0",
            )
        else:
            base = self._url_repo(
                project_key,
                repository_slug,
                api_root="rest/branch-permissions",
                api_version="2.0",
            )

        return "{}/restrictions/{}".format(base, "" if permission_id is None else str(permission_id))

    def get_branches_permissions(
        self,
        project_key,
        permission_id,
        repository_slug=None,
        start=0,
        limit=25,
    ):
        """
        Get branches permissions from a given repo
        :param project_key:
        :param permission_id:
        :param repository_slug:
        :param start:
        :param limit:
        :return:
        """
        url = self._url_branches_permissions(project_key, permission_id, repository_slug)
        params = {}
        if limit:
            params["limit"] = limit
        if start:
            params["start"] = start
        return self.get(url, params=params)

    def set_branches_permissions(
        self,
        project_key,
        multiple_permissions=False,
        matcher_type=None,
        matcher_value=None,
        permission_type=None,
        repository_slug=None,
        except_users=None,
        except_groups=None,
        except_access_keys=None,
        start=0,
        limit=25,
    ):
        """
        Create a restriction for the supplied branch or set of branches to be applied to the given repository.
        Allows creating multiple restrictions at once.
        To use multiple restrictions you should format payload manually -
        see the bitbucket-branch-restrictions.py example.
        Reference: https://docs.atlassian.com/bitbucket-server/rest/6.8.0/bitbucket-ref-restriction-rest.html
        :param project_key:
        :param multiple_permissions:
        :param matcher_type:
        :param matcher_value:
        :param permission_type:
        :param repository_slug:
        :param except_users:
        :param except_groups:
        :param except_access_keys:
        :param start:
        :param limit:
        :return:
        """
        url = self._url_branches_permissions(project_key=project_key, repository_slug=repository_slug)
        if except_users is None:
            except_users = []
        if except_groups is None:
            except_groups = []
        if except_access_keys is None:
            except_access_keys = []
        headers = self.default_headers
        if multiple_permissions:
            headers = self.bulk_headers
            restriction = multiple_permissions
        else:
            restriction = {
                "type": permission_type,
                "matcher": {
                    "id": matcher_value,
                    "displayId": matcher_value,
                    "type": {
                        "id": matcher_type.upper(),
                        "name": matcher_type.capitalize(),
                    },
                    "active": True,
                },
                "users": except_users,
                "groups": except_groups,
                "accessKeys": except_access_keys,
            }
        params = {"start": start, "limit": limit}
        return self.post(url, data=restriction, params=params, headers=headers)

    def delete_branch_permission(self, project_key, permission_id, repository_slug=None):
        """
        Deletes a restriction as specified by a restriction id.
        The authenticated user must have REPO_ADMIN permission or higher to call this resource.

        :param project_key:
        :param repository_slug:
        :param permission_id:
        :return:
        """
        url = self._url_branches_permissions(project_key, permission_id, repository_slug)
        return self.delete(url)

    def get_branch_permission(self, project_key, permission_id, repository_slug=None):
        """
        Returns a restriction as specified by a restriction id.
        The authenticated user must have REPO_ADMIN permission or higher to call this resource.

        :param project_key:
        :param repository_slug:
        :param permission_id:
        :return:
        """
        url = self._url_branches_permissions(project_key, permission_id, repository_slug)
        return self._get_paged(url)

    def all_branches_permissions(self, project_key, permission_id, repository_slug=None):
        """
        Get branches permissions from a given repo
        :param project_key:
        :param permission_id
        :param repository_slug:
        :return:
        """
        url = self._url_branches_permissions(project_key, permission_id, repository_slug)
        return self._get_paged(url)

    def _url_branching_model(self, project_key, repository_slug):
        return "{}/branchmodel/configuration".format(
            self._url_repo(
                project_key,
                repository_slug,
                api_root="rest/branch-utils",
                api_version="1.0",
            )
        )

    def get_branching_model(self, project_key, repository_slug):
        """
        Get branching model
        :param project_key:
        :param repository_slug:
        :return:
        """
        url = self._url_branching_model(project_key, repository_slug)
        return self.get(url)

    def set_branching_model(self, project_key, repository_slug, data):
        """
        Set branching model
        :param project_key:
        :param repository_slug:
        :param data:
        :return:
        """
        url = self._url_branching_model(project_key, repository_slug)
        return self.put(url, data=data)

    def enable_branching_model(self, project_key, repository_slug):
        """
        Enable branching model by setting it with default configuration
        :param project_key:
        :param repository_slug:
        :return:
        """
        default_model_data = {
            "development": {"refId": None, "useDefault": True},
            "types": [
                {
                    "displayName": "Bugfix",
                    "enabled": True,
                    "id": "BUGFIX",
                    "prefix": "bugfix/",
                },
                {
                    "displayName": "Feature",
                    "enabled": True,
                    "id": "FEATURE",
                    "prefix": "feature/",
                },
                {
                    "displayName": "Hotfix",
                    "enabled": True,
                    "id": "HOTFIX",
                    "prefix": "hotfix/",
                },
                {
                    "displayName": "Release",
                    "enabled": True,
                    "id": "RELEASE",
                    "prefix": "release/",
                },
            ],
        }
        return self.set_branching_model(project_key, repository_slug, default_model_data)

    def disable_branching_model(self, project_key, repository_slug):
        """
        Disable branching model
        :param project_key:
        :param repository_slug:
        :return:
        """
        return self.delete(self._url_branching_model(project_key, repository_slug))

    def _url_file(self, project_key, repository_slug, filename):
        return "{}/browse/{}".format(self._url_repo(project_key, repository_slug), filename)

    def upload_file(self, project_key, repository_slug, content, message, branch, filename):
        """
        Upload new file for given branch.
        :param project_key:
        :param repository_slug:
        :param content:
        :param message:
        :param branch:
        :param filename
        :return:
        """
        url = self._url_file(project_key, repository_slug, filename)
        data = {"content": content, "message": message, "branch": branch}
        return self.put(url, files=data, headers={"Accept": "application/json"})

    def update_file(
        self,
        project_key,
        repository_slug,
        content,
        message,
        branch,
        filename,
        source_commit_id,
    ):
        """
        Update existing file for given branch.
        :param project_key:
        :param repository_slug:
        :param content:
        :param message:
        :param branch:
        :param filename:
        :param source_commit_id:
        :return:
        """
        url = self._url_file(project_key, repository_slug, filename)
        data = {
            "content": content,
            "message": message,
            "branch": branch,
            "sourceCommitId": source_commit_id,
        }
        return self.put(url, files=data, headers={"Accept": "application/json"})

    def search_code(self, team, search_query, page=1, limit=10):
        """
        Search repositories for matching code
        :team: str
        :search_query: str
        """
        url = self.resource_url("teams/{team}/search/code".format(team=team))
        return self.get(
            url,
            params={"search_query": search_query, "page": page, "pagelen": limit},
        )

    def get_lfs_repo_status(self, project_key, repo):
        url = "rest/git-lfs/admin/projects/{projectKey}/repos/{repositorySlug}/enabled".format(
            projectKey=project_key, repositorySlug=repo
        )
        return self.get(url)

    def set_lfs_repo_status(self, project_key, repo, enable=True):
        url = "rest/git-lfs/admin/projects/{projectKey}/repos/{repositorySlug}/enabled".format(
            projectKey=project_key, repositorySlug=repo
        )
        if enable:
            return self.put(url)
        else:
            return self.delete(url)

    def _url_repo_conditions(self, project_key, repo_key):
        return "{}/conditions".format(
            self._url_repo(
                project_key,
                repo_key,
                api_root="rest/default-reviewers",
                api_version="1.0",
            )
        )

    def get_repo_conditions(self, project_key, repo_key):
        """
        Request type: GET
        Return a page of defaults conditions with reviewers list (type REPOSITORY or PROJECT)
        that have been configured for this repository slug inside project specified.
        For further information visit:
            https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-default-reviewers-rest.html#idm52264928992
        :projectKey: str- project key involved
        :repoKey: str - repo key involved
        :return:
        """
        url = self._url_repo_conditions(project_key, repo_key)
        return self.get(url) or {}

    def get_repo_project_conditions(self, project_key, repo_key):
        """
        Request type: GET
        Return a page of repository conditions (only type PROJECT) with reviewers list associated
        that have been configured for this repository slug inside project specified.
        For further information visit:
            https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-default-reviewers-rest.html#idm52264928992
        :projectKey: str- project key involved
        :repoKey: str - repo key involved
        :return:
        """
        response = self.get_repo_conditions(project_key, repo_key)
        count = 0
        for condition in response:
            if condition["scope"]["type"] == "REPOSITORY":
                del response[count]
            count += 1
        return response

    def get_repo_repo_conditions(self, project_key, repo_key):
        """
        Request type: GET
        Return a page of repository conditions (only type REPOSITORY) with reviewers list associated
        that have been configured for this repository slug inside project specified.
        For further information visit:
            https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-default-reviewers-rest.html#idm52264928992
        :projectKey: str- project key involved
        :repoKey: str - repo key involved
        :return:
        """
        response = self.get_repo_conditions(project_key, repo_key)
        count = 0
        for condition in response:
            if condition["scope"]["type"] == "PROJECT":
                del response[count]
            count += 1
        return response

    def _url_repo_condition(self, project_key, repo_key, id_condition=None):
        return "{}/condition/{}".format(
            self._url_repo(
                project_key,
                repo_key,
                api_root="rest/default-reviewers",
                api_version="1.0",
            ),
            "" if id_condition is None else str(id_condition),
        )

    def get_repo_condition(self, project_key, repo_key, id_condition):
        """
        Request type: GET
        Return a specific condition with reviewers list
            that have been configured for this repository slug inside project specified.
        For further information visit:
            https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-default-reviewers-rest.html#idm52264927632
        :projectKey: str- project key involved
        :repoKey: str - repo key involved
        :idCondition: int - condition id involved
        :return:
        """
        url = self._url_repo_condition(project_key, repo_key, id_condition)
        return self.get(url) or {}

    def create_repo_condition(self, project_key, repo_key, condition):
        """
        Request type: POST
        Create a new condition for this repository slug inside project specified.
        For further information visit:
            https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-default-reviewers-rest.html#idm52264908128
        :projectKey: str- project key involved
        :repoKey: str - repo key involved
        :data: condition: dictionary object
        :example condition: '{"sourceMatcher":
                                {"id":"any",
                                "type":{"id":"ANY_REF"}},
                                "targetMatcher":{"id":"refs/heads/master","type":{"id":"BRANCH"}},
                                "reviewers":[{"id": 12}],"requiredApprovals":"0"
                            }'
        :return:
        """
        url = self._url_repo_condition(project_key, repo_key)
        return self.post(url, data=condition) or {}

    def update_repo_condition(self, project_key, repo_key, condition, id_condition):
        """
        Request type: PUT
        Update a specific condition for this repository slug inside project.
        For further information visit:
            https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-default-reviewers-rest.html#idm52264927632
        :projectKey: str- project key involved
        :repoKey: str - repo key involved
        :idCondition: int - condition id involved
        :data: condition: dictionary object
        :example condition: '{"sourceMatcher":
                                {"id":"any",
                                "type":{"id":"ANY_REF"}},
                                "targetMatcher":{"id":"refs/heads/master","type":{"id":"BRANCH"}},
                                "reviewers":[{"id": 12}],"requiredApprovals":"0"
                            }'
        :return:
        """
        url = self._url_repo_condition(project_key, repo_key, id_condition)
        return self.put(url, data=condition) or {}

    def delete_repo_condition(self, project_key, repo_key, id_condition):
        """
        Delete a specific condition for this repository slug inside project.
        For further information visit:
            https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-default-reviewers-rest.html#idm8287339888
        Request type: DELETE
        :projectKey: str- project key involved
        :repoKey: str - repo key involved
        :idCondition: int - condition id involved
        :return:
        """
        url = self._url_repo_condition(project_key, repo_key, id_condition)
        return self.delete(url) or {}

    def download_repo_archive(
        self,
        project_key,
        repository_slug,
        dest_fd,
        at=None,
        filename=None,
        format=None,
        path=None,
        prefix=None,
        chunk_size=128,
    ):
        """
        Downloads a repository archive.
        Note that the data is written to the specified file-like object,
        rather than simply being returned.
        For further information visit:
           https://docs.atlassian.com/bitbucket-server/rest/7.13.0/bitbucket-rest.html#idp199
        :param project_key:
        :param repository_slug:
        :param dest_fd: a file-like object to which the archive will be written
        :param at: string: Optional, the commit to download an archive of; if not supplied,
                         an archive of the default branch is downloaded
        :param filename: string: Optional, a filename to include the "Content-Disposition" header
        :param format: string: Optional, the format to stream the archive in; must be one of: zip, tar, tar.gz or tgz.
                    If not specified, then the archive will be in zip format.
        :param path: string: Optional, path to include in the streamed archive
        :param prefix: string: Optional, a prefix to apply to all entries in the streamed archive;
                    if the supplied prefix does not end with a trailing /, one will be added automatically
        :param chunk_size: int: Optional, download chunk size. Defeault is 128
        """
        url = "{}/archive".format(self._url_repo(project_key, repository_slug))
        params = {}
        if at is not None:
            params["at"] = at
        if filename is not None:
            params["filename"] = filename
        if format is not None:
            params["format"] = format
        if path is not None:
            params["path"] = path
        if prefix is not None:
            params["prefix"] = prefix
        headers = {"Accept": "*/*"}
        response = self.get(url, params=params, headers=headers, advanced_mode=True)
        for chunk in response.iter_content(chunk_size=chunk_size):
            dest_fd.write(chunk)

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def get_repositories(self, workspace, role=None, query=None, sort=None):
        """
        Get all repositories in a workspace.

        :param workspace:
        :param role: Filters the result based on the authenticated user's role on each repository.
                      One of: member, contributor, admin, owner
        :param query: Query string to narrow down the response.
        :param sort: Field by which the results should be sorted.
        """
        return [
            r.data
            for r in Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.each(role=role, q=query, sort=sort)
        ]

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def get_pipelines(self, workspace, repository_slug, number=10, sort_by="-created_on"):
        """
        Get information about latest pipelines runs.

        :param workspace:
        :param repository_slug:
        :param sort_by:
        :param number: number of pipelines to fetch
        :param :sort_by: optional key to sort available pipelines for
        :return: List of pipeline data
        """
        values = []
        for p in (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .pipelines.each(sort=sort_by)
        ):
            values.append(p.data)
            if len(values) == number:
                break

        return values

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def trigger_pipeline(
        self,
        workspace,
        repository_slug,
        branch="master",
        revision=None,
        name=None,
    ):
        """
        Trigger a new pipeline. The following options are possible (1 and 2
        trigger the pipeline that the branch is associated with in the Pipelines
        configuration):
        1. Latest revision of a branch (specify ``branch``)
        2. Specific revision on a branch (additionally specify ``revision``)
        3. Specific pipeline (additionally specify ``name``)
        :return: the initiated pipeline; or error information
        """
        return (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .pipelines.trigger(branch=branch, commit=revision, pattern=name)
            .data
        )

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def get_pipeline(self, workspace, repository_slug, uuid):
        """
        Get information about the pipeline specified by ``uuid``.
        :param workspace:
        :param repository_slug:
        :param uuid: Pipeline identifier (with surrounding {}; NOT the build number)
        """
        return (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .pipelines.get(uuid)
            .data
        )

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def stop_pipeline(self, workspace, repository_slug, uuid):
        """
        Stop the pipeline specified by ``uuid``.
        :param workspace:
        :param repository_slug:
        :param uuid: Pipeline identifier (with surrounding {}; NOT the build number)

        See the documentation for the meaning of response status codes.
        """
        return (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .pipelines.get(uuid)
            .stop()
        )

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def get_pipeline_steps(self, workspace, repository_slug, uuid):
        """
        Get information about the steps of the pipeline specified by ``uuid``.
        :param workspace:
        :param repository_slug:
        :param uuid: Pipeline identifier (with surrounding {}; NOT the build number)
        """
        values = []
        for s in (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .pipelines.get(uuid)
            .steps()
        ):
            values.append(s.data)

        return values

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def get_pipeline_step(self, workspace, repository_slug, pipeline_uuid, step_uuid):
        """
        Get information about a step of a pipeline, specified by respective UUIDs.
        :param workspace:
        :param repository_slug:
        :param pipeline_uuid: Pipeline identifier (with surrounding {}; NOT the build number)
        :param step_uuid: Step identifier (with surrounding {})
        """
        return (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .pipelines.get(pipeline_uuid)
            .step(step_uuid)
            .data
        )

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def get_pipeline_step_log(self, workspace, repository_slug, pipeline_uuid, step_uuid):
        """
        Get log of a step of a pipeline, specified by respective UUIDs.
        :param workspace:
        :param repository_slug:
        :param pipeline_uuid: Pipeline identifier (with surrounding {}; NOT the build number)
        :param step_uuid: Step identifier (with surrounding {})
        :return: byte string log
        """
        return (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .pipelines.get(pipeline_uuid)
            .step(step_uuid)
            .log()
        )

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def create_issue(
        self,
        workspace,
        repository_slug,
        title,
        description="",
        kind="bug",
        priority="major",
    ):
        """
        Create a new issue in the issue tracker of the given repository.
        :param workspace:
        :param repository_slug:
        :param title:
        :param description:
        :param kind: one of: bug, enhancement, proposal, task
        :param priority: one of: trivial, minor, major, critical, blocker
        """
        return (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .issues.create(
                title=title,
                description=description,
                kind=kind,
                priority=priority,
            )
            .data
        )

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def get_issues(self, workspace, repository_slug, sort_by=None, query=None):
        """
        Get information about the issues tracked in the given repository. By
        default, the issues are sorted by ID in descending order.
        :param workspace:
        :param repository_slug:
        :param sort_by: optional key to sort available issues for
        :param query: optional query to filter available issues for. See
          https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering
          for an overview

        :return: List of issues (direct, i.e. without the 'values' key)
        """
        values = []
        for p in (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .issues.each(q=query, sort=sort_by)
        ):
            values.append(p.data)

        return values

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def get_issue(self, workspace, repository_slug, id):
        """
        Get the issue specified by ``id``.
        """
        return (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .issues.get(id)
            .data
        )

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def update_issue(self, workspace, repository_slug, id, **fields):
        """
        Update the ``fields`` of the issue specified by ``id``.
        Consult the official API documentation for valid fields.
        """
        return (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .issues.get(id)
            .update(**fields)
            .data
        )

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def delete_issue(self, workspace, repository_slug, id):
        """
        Delete the issue specified by ``id``.
        """
        return (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .issues.get(id)
            .delete()
        )

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def add_branch_restriction(
        self,
        workspace,
        repository_slug,
        kind,
        branch_match_kind="glob",
        branch_pattern="*",
        branch_type=None,
        users=None,
        groups=None,
        value=None,
    ):
        """
        Add a new branch restriction.

        :param workspace:
        :param repository_slug:
        :param value:
        :param kind: One of require_tasks_to_be_completed, force, restrict_merges,
                      enforce_merge_checks, require_approvals_to_merge, delete,
                      require_all_dependencies_merged, push, require_passing_builds_to_merge,
                      reset_pullrequest_approvals_on_change, require_default_reviewer_approvals_to_merge
        :param branch_match_kind: branching_model or glob, if branching_model use
                      param branch_type otherwise branch_pattern.
        :param branch_pattern: A glob specifying the branch this restriction should
                      apply to (supports * as wildcard).
        :param branch_type: The branch type specifies the branches this restriction
                      should apply to. One of: feature, bugfix, release, hotfix, development, production.
        :param users: List of user objects that are excluded from the restriction.
                        Minimal: {"username": "<username>"}
        :param groups: List of group objects that are excluded from the restriction.
                        Minimal: {"owner": {"username": "<teamname>"}, "slug": "<groupslug>"}
        """
        return (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .branch_restrictions.create(
                kind,
                branch_match_kind=branch_match_kind,
                branch_pattern=branch_pattern,
                branch_type=branch_type,
                users=users,
                groups=groups,
                value=value,
            )
            .data
        )

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def get_branch_restrictions(self, workspace, repository_slug, kind=None, pattern=None, number=10):
        """
        Get all branch permissions.
        """
        values = []
        for p in (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .branch_restrictions.each(kind=kind, pattern=pattern)
        ):
            values.append(p.data)
            if len(values) == number:
                break

        return values

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def update_branch_restriction(self, workspace, repository_slug, id, **fields):
        """
        Update an existing branch restriction identified by ``id``.
        Consult the official API documentation for valid fields.
        """
        return (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .branch_restrictions.get(id)
            .update(**fields)
            .data
        )

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def delete_branch_restriction(self, workspace, repository_slug, id):
        """
        Delete an existing branch restriction identified by ``id``.
        """
        return (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .branch_restrictions.get(id)
            .delete()
        )

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def add_default_reviewer(self, workspace, repository_slug, user):
        """
        Add user as default reviewer to the repository.
        Can safely be called multiple times with the same user, only adds once.

        :param workspace:
        :param repository_slug:
        :param user: The username or account UUID to add as default_reviewer.
        """
        return (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .default_reviewers.add(user)
            .data
        )

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def get_default_reviewers(self, workspace, repository_slug, number=10):
        """
        Get all default reviewers for the repository.
        """
        values = []
        for p in (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .default_reviewers.each()
        ):
            values.append(p.data)
            if len(values) == number:
                break

        return values

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def is_default_reviewer(self, workspace, repository_slug, user):
        """
        Check if the user is a default reviewer of the repository.

        :param workspace:
        :param repository_slug:
        :param user: The username or account UUID to check.
        :return: True if present, False if not.
        """
        if (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .default_reviewers.get(user)
            is None
        ):
            return False

        return True

    @deprecated(
        version="2.0.2",
        reason="Use atlassian.bitbucket.cloud instead of atlassian.bitbucket",
    )
    def delete_default_reviewer(self, workspace, repository_slug, user):
        """
        Remove user as default reviewer from the repository.

        :param repository_slug:
        :param workspace:
        :param user: The username or account UUID to delete as default reviewer.
        """
        return (
            Cloud(self.url, **self._new_session_args)
            .workspaces.get(workspace)
            .repositories.get(repository_slug)
            .default_reviewers.get(user)
            .delete()
        )
