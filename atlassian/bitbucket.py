# coding=utf-8
import logging

from .rest_client import AtlassianRestAPI
from requests.exceptions import HTTPError

log = logging.getLogger(__name__)


class Bitbucket(AtlassianRestAPI):
    bulk_headers = {"Content-Type": "application/vnd.atl.bitbucket.bulk+json"}

    def project_list(self, limit=None):
        """
        Provide the project list
        :param limit: OPTIONAL 25 is default
        :return:
        """
        params = {}
        if limit:
            params['limit'] = limit
        if not self.cloud:
            return (self.get('rest/api/1.0/projects', params=params) or {}).get('values')
        return (self.get('rest/api/2.0/projects', params=params) or {}).get('values')

    def project(self, key):
        """
        Provide project info
        :param key:
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{0}'.format(key)
        else:
            url = 'rest/api/2.0/projects/{0}'.format(key)
        return self.get(url) or {}

    def create_project(self, key, name, description=""):
        """
        Create project
        :param key:
        :param name:
        :param description:
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects'
        else:
            url = 'rest/api/2.0/projects'
        data = {"key": key,
                "name": name,
                "description": description
                }
        return self.post(url, data=data)

    def update_project(self, key, **params):
        """
        Update project
        :param key:
        :return:
        """
        data = self.project(key)
        if 'errors' not in data:
            data.update(params)
            if not self.cloud:
                url = 'rest/api/1.0/projects/{0}'.format(key)
            else:
                url = 'rest/api/2.0/projects/{0}'.format(key)
            return self.put(url, data=data)
        else:
            log.debug('Failed to update project: {0}: Unable to read project'.format(key))
            return None

    def project_avatar(self, key, content_type='image/png'):
        """
        Get project avatar
        :param content_type:
        :param key:
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{0}/avatar.png'.format(key)
        else:
            url = 'rest/api/2.0/projects/{0}/avatar.png'.format(key)
        headers = dict(self.default_headers)
        headers['Accept'] = content_type
        headers['X-Atlassian-Token'] = 'no-check'

        return self.get(url, not_json_response=True, headers=headers) or {}

    def set_project_avatar(self, key, icon, content_type='image/png'):
        """
        Set project avatar
        :param key: A Project key
        :param icon:
        :param content_type:
        :return:
        """
        headers = {'X-Atlassian-Token': 'no-check'}
        files = {'avatar': ("avatar.png", icon, content_type)}
        if not self.cloud:
            url = 'rest/api/1.0/projects/{0}/avatar.png'.format(key)
        else:
            url = 'rest/api/2.0/projects/{0}/avatar.png'.format(key)
        return self.post(url, files=files, headers=headers) or {}

    def project_users(self, key, limit=99999, filter_str=None):
        """
        Get users who has permission in project
        :param key:
        :param limit: OPTIONAL: The limit of the number of users to return, this may be restricted by
                            fixed system limits. Default by built-in method: 99999
        :param filter_str:  OPTIONAL: users filter string
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{key}/permissions/users'.format(key=key)
        else:
            url = 'rest/api/2.0/projects/{key}/permissions/users'.format(key=key)
        params = {}
        if limit:
            params['limit'] = limit
        if filter_str:
            params['filter'] = filter_str
        return (self.get(url, params=params) or {}).get('values')

    def project_keys(self, key, limit=99999, filter_str=None):
        """
        Get SSH access keys added to the project
        :param key:
        :param limit: OPTIONAL: The limit of the number of users to return, this may be restricted by
                            fixed system limits. Default by built-in method: 99999
        :param filter_str:  OPTIONAL: users filter string
        :return:
        """
        if not self.cloud:
            url = 'rest/keys/1.0/projects/{key}/ssh'.format(key=key)
        else:
            url = 'rest/keys/2.0/projects/{key}/ssh'.format(key=key)
        params = {}
        if limit:
            params['limit'] = limit
        if filter_str:
            params['filter'] = filter_str
        return (self.get(url, params=params) or {}).get('values')

    def repo_users(self, project_key, repo_key, limit=99999, filter_str=None):
        """
        Get users who has permission in repository
        :param project_key:
        :param repo_key:
        :param limit: OPTIONAL: The limit of the number of users to return, this may be restricted by
                            fixed system limits. Default by built-in method: 99999
        :param filter_str:  OPTIONAL: Users filter string
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project_key}/repos/{repo_key}/permissions/users'.format(
                project_key=project_key, repo_key=repo_key)
        else:
            url = 'rest/api/2.0/projects/{project_key}/repos/{repo_key}/permissions/users'.format(
                project_key=project_key, repo_key=repo_key)
        params = {}
        if limit:
            params['limit'] = limit
        if filter_str:
            params['filter'] = filter_str
        return (self.get(url, params=params) or {}).get('values')

    def repo_keys(self, project_key, repo_key, limit=99999, filter_str=None):
        """
        Get SSH access keys added to the repository
        :param project_key:
        :param repo_key:
        :param limit: OPTIONAL: The limit of the number of users to return, this may be restricted by
                            fixed system limits. Default by built-in method: 99999
        :param filter_str:  OPTIONAL: users filter string
        :return:
        """
        if not self.cloud:
            url = 'rest/keys/1.0/projects/{project_key}/repos/{repo_key}/ssh'.format(project_key=project_key,
                                                                                     repo_key=repo_key)
        else:
            url = 'rest/keys/2.0/projects/{project_key}/repos/{repo_key}/ssh'.format(project_key=project_key,
                                                                                     repo_key=repo_key)
        params = {}
        if limit:
            params['limit'] = limit
        if filter_str:
            params['filter'] = filter_str
        return (self.get(url, params=params) or {}).get('values')

    def project_users_with_administrator_permissions(self, key):
        """
        Get project administrators for project
        :param key: project key
        :return: project administrators
        """
        project_administrators = [user['user'] for user in self.project_users(key)
                                  if user['permission'] == 'PROJECT_ADMIN']
        for group in self.project_groups_with_administrator_permissions(key):
            for user in self.group_members(group):
                project_administrators.append(user)
        return project_administrators

    def project_grant_user_permissions(self, project_key, username, permission):
        """
        Grant the specified project permission to an specific user
        :param project_key: project key involved
        :param username: user name to be granted
        :param permission: the project permissions available are 'PROJECT_ADMIN', 'PROJECT_WRITE' and 'PROJECT_READ'
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project_key}/permissions/users?permission={permission}&name={username}' \
                .format(project_key=project_key, permission=permission, username=username)
        else:
            url = 'rest/api/2.0/projects/{project_key}/permissions/users?permission={permission}&name={username}' \
                .format(project_key=project_key, permission=permission, username=username)
        return self.put(url)

    def project_remove_user_permissions(self, project_key, username):
        """
        Revoke all permissions for the specified project for a user.
        The authenticated user must have PROJECT_ADMIN permission for
        the specified project or a higher global permission to call this resource.
        In addition, a user may not revoke their own project permissions if they do not have a higher global permission.
        :param project_key: project key involved
        :param username: user name to be granted
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project_key}/permissions/users?name={username}'.format(
                project_key=project_key, username=username)
        else:
            url = 'rest/api/2.0/projects/{project_key}/permissions/users?name={username}'.format(
                project_key=project_key, username=username)
        return self.delete(url)

    def project_grant_group_permissions(self, project_key, group_name, permission):
        """
        Grant the specified project permission to an specific group
        :param project_key: project key involved
        :param group_name: group to be granted
        :param permission: the project permissions available are 'PROJECT_ADMIN', 'PROJECT_WRITE' and 'PROJECT_READ'
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project_key}/permissions/groups?permission={permission}&name={group_name}' \
                .format(project_key=project_key, permission=permission, group_name=group_name)
        else:
            url = 'rest/api/2.0/projects/{project_key}/permissions/groups?permission={permission}&name={group_name}' \
                .format(project_key=project_key, permission=permission, group_name=group_name)
        return self.put(url)

    def project_remove_group_permissions(self, project_key, groupname):
        """
        Revoke all permissions for the specified project for a group.
        The authenticated user must have PROJECT_ADMIN permission for the specified project
        or a higher global permission to call this resource.
        In addition, a user may not revoke a group's permissions
        if it will reduce their own permission level.
        :param project_key: project key involved
        :param groupname: group to be granted
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project_key}/permissions/groups?name={group_name}'.format(
                project_key=project_key, group_name=groupname)
        else:
            url = 'rest/api/2.0/projects/{project_key}/permissions/groups?name={group_name}'.format(
                project_key=project_key, group_name=groupname)
        return self.delete(url)

    def repo_grant_user_permissions(self, project_key, repo_key, username, permission):
        """
        Grant the specified repository permission to an specific user
        :param project_key: project key involved
        :param repo_key: repository key involved (slug)
        :param username: user name to be granted
        :param permission: the repository permissions available are 'REPO_ADMIN', 'REPO_WRITE' and 'REPO_READ'
        :return:
        """
        params = {'permission': permission,
                  'name': username}
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project_key}/repos/{repo_key}/permissions/users' \
                .format(project_key=project_key, repo_key=repo_key)
        else:
            url = 'rest/api/2.0/projects/{project_key}/repos/{repo_key}/permissions/users' \
                .format(project_key=project_key, repo_key=repo_key)
        return self.put(url, params=params)

    def repo_remove_user_permissions(self, project_key, repo_key, username):
        """
        Revoke all permissions for the specified repository for a user.
        The authenticated user must have REPO_ADMIN permission for the specified repository
        or a higher project or global permission to call this resource.
        In addition, a user may not revoke their own repository permissions
        if they do not have a higher project or global permission.
        :param project_key: project key involved
        :param repo_key: repository key involved (slug)
        :param username: user name to be granted
        :return:
        """
        params = {'name': username}
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project_key}/repos/{repo_key}/permissions/users' \
                .format(project_key=project_key, repo_key=repo_key)
        else:
            url = 'rest/api/2.0/projects/{project_key}/repos/{repo_key}/permissions/users' \
                .format(project_key=project_key, repo_key=repo_key)
        return self.delete(url, params=params)

    def repo_grant_group_permissions(self, project_key, repo_key, groupname, permission):
        """
        Grant the specified repository permission to an specific group
        Promote or demote a group's permission level for the specified repository. Available repository permissions are:
            REPO_READ
            REPO_WRITE
            REPO_ADMIN
        See the Bitbucket Server documentation for a detailed explanation of what each permission entails.
        The authenticated user must have REPO_ADMIN permission for the specified repository or a higher project
        or global permission to call this resource.
        In addition, a user may not demote a group's permission level
        if their own permission level would be reduced as a result.
        :param project_key: project key involved
        :param repo_key: repository key involved (slug)
        :param groupname: group to be granted
        :param permission: the repository permissions available are 'REPO_ADMIN', 'REPO_WRITE' and 'REPO_READ'
        :return:
        """
        params = {'permission': permission,
                  'name': groupname}
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project_key}/repos/{repo_key}/permissions/groups' \
                .format(project_key=project_key, repo_key=repo_key)
        else:
            url = 'rest/api/2.0/projects/{project_key}/repos/{repo_key}/permissions/groups' \
                .format(project_key=project_key, repo_key=repo_key)
        return self.put(url, params=params)

    def repo_remove_group_permissions(self, project_key, repo_key, groupname, permission):
        """
        Revoke all permissions for the specified repository for a group.
        The authenticated user must have REPO_ADMIN permission for the specified repository
        or a higher project or global permission to call this resource.
        In addition, a user may not revoke a group's permissions if it will reduce their own permission level.
        :param project_key: project key involved
        :param repo_key: repository key involved (slug)
        :param groupname: group to be granted
        :param permission: the repository permissions available are 'REPO_ADMIN', 'REPO_WRITE' and 'REPO_READ'
        :return:
        """
        params = {'name': groupname}
        if permission:
            params['permission'] = permission
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project_key}/repos/{repo_key}/permissions/groups' \
                .format(project_key=project_key, repo_key=repo_key)
        else:
            url = 'rest/api/2.0/projects/{project_key}/repos/{repo_key}/permissions/groups' \
                .format(project_key=project_key, repo_key=repo_key)
        return self.delete(url, params=params)

    def project_groups(self, key, limit=99999, filter_str=None):
        """
        Get Project Groups
        :param key:
        :param limit: OPTIONAL: The limit of the number of groups to return, this may be restricted by
                            fixed system limits. Default by built-in method: 99999
        :param filter_str: OPTIONAL: group filter string
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{key}/permissions/groups'.format(key=key)
        else:
            url = 'rest/api/2.0/projects/{key}/permissions/groups'.format(key=key)
        params = {}
        if limit:
            params['limit'] = limit
        if filter_str:
            params['filter'] = filter_str
        return (self.get(url, params=params) or {}).get('values')

    def repo_groups(self, project_key, repo_key, limit=99999, filter_str=None):
        """
        Get repository Groups
        :param project_key:
        :param repo_key:
        :param limit: OPTIONAL: The limit of the number of groups to return, this may be restricted by
                            fixed system limits. Default by built-in method: 99999
        :param filter_str: OPTIONAL: group filter string
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project_key}/repos/{repo_key}/permissions/groups' \
                .format(project_key=project_key, repo_key=repo_key)
        else:
            url = 'rest/api/2.0/projects/{project_key}/repos/{repo_key}/permissions/groups' \
                .format(project_key=project_key, repo_key=repo_key)
        params = {}
        if limit:
            params['limit'] = limit
        if filter_str:
            params['filter'] = filter_str
        return (self.get(url, params=params) or {}).get('values')

    def project_groups_with_administrator_permissions(self, key):
        """
        Get groups with admin permissions
        :param key:
        :return:
        """
        return [group['group']['name'] for group in self.project_groups(key) if group['permission'] == 'PROJECT_ADMIN']

    def project_summary(self, key):
        return {
            'key': key,
            'data': self.project(key),
            'users': self.project_users(key),
            'groups': self.project_groups(key),
            'avatar': self.project_avatar(key)}

    def group_members(self, group, limit=99999):
        """
        Get group of members
        :param group:
        :param limit: OPTIONAL: The limit of the number of users to return, this may be restricted by
                        fixed system limits. Default by built-in method: 99999
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/admin/groups/more-members'
        else:
            url = 'rest/api/2.0/admin/groups/more-members'
        params = {}
        if limit:
            params['limit'] = limit
        if group:
            params['context'] = group
        return (self.get(url, params=params) or {}).get('values')

    def all_project_administrators(self):
        """
        Get the list of project administrators
        :return:
        """
        for project in self.project_list():
            log.info('Processing project: {0} - {1}'.format(project.get('key'), project.get('name')))
            yield {
                'project_key': project.get('key'),
                'project_name': project.get('name'),
                'project_administrators': [{'email': x['emailAddress'], 'name': x['displayName']}
                                           for x in self.project_users_with_administrator_permissions(project['key'])]}

    def repo_list(self, project_key, start=None, limit=25):
        """
        Get repositories list from project
        :param project_key:
        :param start: OPTIONAL: The start of the
        :param limit: OPTIONAL: The limit of the number of repositories to return, this may be restricted by
                        fixed system limits. Default by built-in method: 25
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{projectKey}/repos'.format(projectKey=project_key)
        else:
            url = 'rest/api/2.0/projects/{projectKey}/repos'.format(projectKey=project_key)
        params = {}
        if limit:
            params['limit'] = limit
        if start:
            params['start'] = start
        response = self.get(url, params=params)
        if response.get('isLastPage'):
            log.info('This is a last page of the result')
        else:
            log.info('Next page start at {}'.format(response.get('nextPageStart')))
        return (response or {}).get('values')

    def create_repo(self, project_key, repository, forkable=False, is_private=True):
        """Create a new repository.

        Requires an existing project in which this repository will be created. The only parameters which will be used
        are name and scmId.

        The authenticated user must have PROJECT_ADMIN permission for the context project to call this resource.

        :param project_key: The project matching the projectKey supplied in the resource path as shown in URL.
        :type project_key: str
        :param repository: Name of repository to create (i.e. "My repo").
        :type repository: str
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
        if not self.cloud:
            url = 'rest/api/1.0/projects/{projectKey}/repos'.format(projectKey=project_key)
        else:
            url = 'rest/api/2.0/projects/{projectKey}/repos'.format(projectKey=project_key)
        data = {
            "name": repository,
            "scmId": "git",
            "forkable": forkable,
            "is_private": is_private
        }
        return self.post(url, data=data)

    def get_repo(self, project_key, repository_slug):
        """
        Get a specific repository from a project. This operates based on slug not name which may
        be confusing to some users.
        :param project_key: Key of the project you wish to look in.
        :param repository_slug: url-compatible repository identifier
        :return: Dictionary of request response
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}' \
                .format(project=project_key, repository=repository_slug)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}' \
                .format(project=project_key, repository=repository_slug)
        return self.get(url)

    def get_repo_labels(self, project_key, repository_slug):
        """
        Get labels for a specific repository from a project. This operates based on slug not name which may
        be confusing to some users.
        :param project_key: Key of the project you wish to look in.
        :param repository_slug: url-compatible repository identifier
        :return: Dictionary of request response
        """
        if self.cloud:
            raise Exception("Not supported in Bitbucket Cloud")
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/labels' \
            .format(project=project_key, repository=repository_slug)
        return self.get(url)

    def repo_all_list(self, project_key):
        """
        Get all repositories list from project
        :param project_key:
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{projectKey}/repos'.format(projectKey=project_key)
        else:
            url = 'rest/api/2.0/projects/{projectKey}/repos'.format(projectKey=project_key)
        params = {}
        return self._get_paged(url, params)

    def delete_repo(self, project_key, repository_slug):
        """
        Delete a specific repository from a project. This operates based on slug not name which may
        be confusing to some users.
        :param project_key: Key of the project you wish to look in.
        :param repository_slug: url-compatible repository identifier
        :return: Dictionary of request response
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}'.format(project=project_key,
                                                                              repository=repository_slug)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}'.format(project=project_key,
                                                                              repository=repository_slug)
        return self.delete(url)

    def get_branches(self, project, repository, base=None, filter=None, start=0, limit=99999, details=True,
                     order_by='MODIFICATION'):
        """
        Retrieve the branches matching the supplied filterText param.
        The authenticated user must have REPO_READ permission for the specified repository to call this resource.
        :param start:
        :param project:
        :param repository:
        :param base: base branch/tag to compare each branch to (for the metadata providers that uses that information)
        :param filter:
        :param limit: OPTIONAL: The limit of the number of branches to return, this may be restricted by
                    fixed system limits. Default by built-in method: 99999
        :param details: whether to retrieve plugin-provided metadata about each branch
        :param order_by: OPTIONAL: ordering of refs either ALPHABETICAL (by name) or MODIFICATION (last updated)
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/branches'.format(project=project,
                                                                                       repository=repository)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/branches'.format(project=project,
                                                                                       repository=repository)
        params = {}
        if start:
            params['start'] = start
        if limit:
            params['limit'] = limit
        if filter:
            params['filterText'] = filter
        if base:
            params['base'] = base
        if order_by:
            params['orderBy'] = order_by
        params['details'] = details
        response = self.get(url, params=params)
        if not self.advanced_mode:
            response = (response or {}).get('values')
        return response

    def get_default_branch(self, project, repository):
        """
        Get the default branch of the repository.
        The authenticated user must have REPO_READ permission for the specified repository to call this resource.
        :param project:
        :param repository:
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/branches/default'.format(project=project,
                                                                                               repository=repository)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/branches/default'.format(project=project,
                                                                                               repository=repository)
        return self.get(url)

    def set_default_branch(self, project, repository, ref_branch_name):
        """
        Update the default branch of a repository.
        The authenticated user must have REPO_ADMIN permission for the specified repository to call this resource.
        :param project: project key
        :param repository: repo slug
        :param ref_branch_name: ref name like refs/heads/master
        :return:
        """
        data = {'id': ref_branch_name}
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/branches/default'.format(project=project,
                                                                                               repository=repository)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/branches/default'.format(project=project,
                                                                                               repository=repository)
        return self.put(url, data=data)

    def create_branch(self, project_key, repository, name, start_point, message=""):
        """Creates a branch using the information provided in the request.

        The authenticated user must have REPO_WRITE permission for the context repository to call this resource.

        :param project_key: The project matching the projectKey supplied in the resource path as shown in URL.
        :type project_key: str
        :param repository: Name of repository where branch is created (i.e. "my_repo").
        :type repository: str
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
        if not self.cloud:
            url = 'rest/api/1.0/projects/{projectKey}/repos/{repository}/branches'.format(projectKey=project_key,
                                                                                          repository=repository)
        else:
            url = 'rest/api/2.0/projects/{projectKey}/repos/{repository}/branches'.format(projectKey=project_key,
                                                                                          repository=repository)
        data = {
            "name": name,
            "startPoint": start_point,
            "message": message
        }
        return self.post(url, data=data)

    def delete_branch(self, project, repository, name, end_point):
        """
        Delete branch from related repo
        :param self:
        :param project:
        :param repository:
        :param name:
        :param end_point:
        :return:
        """
        if not self.cloud:
            url = 'rest/branch-utils/1.0/projects/{project}/repos/{repository}/branches'.format(project=project,
                                                                                                repository=repository)
        else:
            url = 'rest/branch-utils/2.0/projects/{project}/repos/{repository}/branches'.format(project=project,
                                                                                                repository=repository)
        data = {"name": str(name), "endPoint": str(end_point)}
        return self.delete(url, data=data)

    def get_pull_request_settings(self, project, repository):
        """
        Get pull request settings.
        :param project:
        :param repository:
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/settings/pull-requests' \
                .format(project=project, repository=repository)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/settings/pull-requests' \
                .format(project=project, repository=repository)
        return self.get(url)

    def set_pull_request_settings(self, project, repository, data):
        """
        Set pull request settings.
        :param project:
        :param repository:
        :param data: json body
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/settings/pull-requests' \
                .format(project=project, repository=repository)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/settings/pull-requests' \
                .format(project=project, repository=repository)
        return self.post(url, data=data)

    def get_pull_requests(self, project, repository, state='OPEN', order='newest', limit=100, start=0, at=None):
        """
        Get pull requests
        :param project:
        :param repository:
        :param state:
        :param order: OPTIONAL: defaults to NEWEST) the order to return pull requests in, either OLDEST
                                (as in: "oldest first") or NEWEST.
        :param limit:
        :param start:
        :param at:
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/pull-requests'.format(project=project,
                                                                                            repository=repository)
        else:
            url = self.resource_url(
                'repositories/{project}/{repository}/pullrequests'.format(
                    project=project, repository=repository))

        params = {}
        if state:
            params['state'] = state
        if limit:
            params['limit'] = limit
        if start:
            params['start'] = start
        if order:
            params['order'] = order
        if at:
            params['at'] = at

        response = self.get(url, params=params)
        if 'values' not in response:
            return []
        pr_list = (response or {}).get('values', [])

        if self.cloud:
            while True:
                next_page = response.get("next")
                if next_page is None:
                    break

                # Strip the base url - it's added when constructing the request
                response = self.get(next_page.replace(self.url, ""))
                pr_list.extend(response.get("values", []))

        else:
            while not response.get('isLastPage'):
                start = response.get('nextPageStart')
                params['start'] = start
                response = self.get(url, params=params)
                pr_list += (response or {}).get('values')

        return pr_list

    def get_pull_requests_activities(self, project, repository, pull_request_id, start=0):
        """
        Get pull requests activities
        :param project:
        :param repository:
        :param pull_request_id: the ID of the pull request within the repository
        :param start:
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}/activities'.format(
                project=project,
                repository=repository,
                pullRequestId=pull_request_id)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}/activities'.format(
                project=project,
                repository=repository,
                pullRequestId=pull_request_id)
        params = {'start': start}
        response = self.get(url, params=params)
        if 'values' not in response:
            return []
        activities_list = (response or {}).get('values')
        while not response.get('isLastPage'):
            params['start'] = response.get('nextPageStart')
            response = self.get(url, params=params)
            activities_list += (response or {}).get('values')
        return activities_list

    def get_pull_requests_changes(self, project, repository, pull_request_id):
        """
        Get pull requests changes
        :param project:
        :param repository:
        :param pull_request_id: the ID of the pull request within the repository
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}/changes'.format(
                project=project,
                repository=repository,
                pullRequestId=pull_request_id)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}/changes'.format(
                project=project,
                repository=repository,
                pullRequestId=pull_request_id)
        params = {'start': 0}
        response = self.get(url, params=params)
        if 'values' not in response:
            return []
        changes_list = (response or {}).get('values')
        while not response.get('isLastPage'):
            params['start'] = response.get('nextPageStart')
            if params['start'] is None:
                log.warning('Too many changes in pull request. Changes list is incomplete.')
                break
            response = self.get(url, params=params)
            changes_list += (response or {}).get('values')
        return changes_list

    def get_pull_requests_commits(self, project, repository, pull_request_id):
        """
        Get pull requests commits
        :param project:
        :param repository:
        :param pull_request_id: the ID of the pull request within the repository
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}/commits'.format(
                project=project, repository=repository, pullRequestId=pull_request_id)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}/commits'.format(
                project=project, repository=repository, pullRequestId=pull_request_id)
        params = {'start': 0}
        response = self.get(url, params=params)
        if 'values' not in response:
            return []
        commits_list = (response or {}).get('values')
        while not response.get('isLastPage'):
            params['start'] = response.get('nextPageStart')
            response = self.get(url, params=params)
            commits_list += (response or {}).get('values')
        return commits_list

    def get_pull_requests_participants(self, project, repository, pull_request_id):
        """
        Get all participants of a pull request
        :param project:
        :param repository:
        :param pull_request_id:
        :return:
        """
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}/participants'.format(
            project=project,
            repository=repository,
            pullRequestId=pull_request_id)
        params = {'start': 0}
        response = self.get(url, params=params)
        if 'values' not in response:
            return []
        participant_list = (response or {}).get('values')
        while not response.get('isLastPage'):
            params['start'] = response.get('nextPageStart')
            response = self.get(url, params=params)
            participant_list += (response or {}).get('values')
        return participant_list

    def open_pull_request(self, source_project, source_repo, dest_project, dest_repo, source_branch, destination_branch,
                          title, description, reviewers=None):
        """
        Create a new pull request between two branches.
        The branches may be in the same repository, or different ones.
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
            'title': title,
            'description': description,
            'fromRef': {
                'id': source_branch,
                'repository': {
                    'slug': source_repo,
                    'name': source_repo,
                    'project': {
                        'key': source_project
                    }
                }
            },
            'toRef': {
                'id': destination_branch,
                'repository': {
                    'slug': dest_repo,
                    'name': dest_repo,
                    'project': {
                        'key': dest_project
                    }
                }
            },
            'reviewers': []
        }

        def add_reviewer(reviewer):
            entry = {
                'user': {
                    'name': reviewer
                }
            }
            body['reviewers'].append(entry)

        if reviewers is not None:
            if isinstance(reviewers, str):
                add_reviewer(reviewers)
            elif isinstance(reviewers, list):
                for reviewer in reviewers:
                    add_reviewer(reviewer)

        return self.create_pull_request(dest_project, dest_repo, body)

    def create_pull_request(self, project_key, repository, data):
        """
        :param project_key:
        :param repository:
        :param data: json body
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{projectKey}/repos/{repository}/pull-requests'.format(projectKey=project_key,
                                                                                               repository=repository)
        else:
            url = self.resource_url(
                'repositories/{projectKey}/{repository}/pullrequests'.format(
                    projectKey=project_key, repository=repository))
        return self.post(url, data=data)

    def delete_pull_request(self, project, repository, pull_request_id, pull_request_version):
        """
        Delete a pull request.

        :param project: the project key
        :param repository: the repository slug
        :param pull_request_id: the ID of the pull request within the repository
        :param pull_request_version: the version of the pull request
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}'.format(
                projectKey=project, repositorySlug=repository, pullRequestId=pull_request_id)
        else:
            url = 'rest/api/2.0/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}'.format(
                projectKey=project, repositorySlug=repository, pullRequestId=pull_request_id)
        data = {'version': pull_request_version}
        return self.delete(url, data=data)

    def decline_pull_request(self, project_key, repository, pr_id, pr_version):
        """
        Decline a pull request.
        The authenticated user must have REPO_READ permission for the repository 
        that this pull request targets to call this resource.

        :param project_key: PROJECT
        :param repository: my_shiny_repo
        :param pr_id: 2341
        :param pr_version: 12
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project_key}/repos/{repository}/pull-requests/{pr_id}/decline'.format(
                project_key=project_key, repository=repository, pr_id=pr_id)
            params = {'version': pr_version}
        else:
            url = self.resource_url(
                'repositories/{project_key}/{repository}/pullrequests/{pr_id}/decline'.format(
                    project_key=project_key, repository=repository, pr_id=pr_id))
            params = {}

        return self.post(url, params=params)

    def is_pull_request_can_be_merged(self, project_key, repository, pr_id):
        """
        Test whether a pull request can be merged.
        A pull request may not be merged if:
        - there are conflicts that need to be manually resolved before merging; and/or
        - one or more merge checks have vetoed the merge.
        The authenticated user must have REPO_READ permission for the repository 
        that this pull request targets to call this resource.

        :param project_key: PROJECT
        :param repository: my_shiny_repo
        :param pr_id: 2341
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project_key}/repos/{repository}/pull-requests/{pr_id}/merge'.format(
                project_key=project_key, repository=repository, pr_id=pr_id)
        else:
            url = 'rest/api/2.0/projects/{project_key}/repos/{repository}/pull-requests/{pr_id}/merge'.format(
                project_key=project_key, repository=repository, pr_id=pr_id)
        return self.get(url)

    def merge_pull_request(self, project_key, repository, pr_id, pr_version):
        """
        Merge pull request
        The authenticated user must have REPO_READ permission for the repository 
        that this pull request targets to call this resource.

        :param pr_version:
        :param project_key: PROJECT
        :param repository: my_shiny_repo
        :param pr_id: 2341
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project_key}/repos/{repository}/pull-requests/{pr_id}/merge'.format(
                project_key=project_key, repository=repository, pr_id=pr_id)
            params = {'version': pr_version}
        else:
            url = self.resource_url(
                'repositories/{project_key}/{repository}/pullrequests/{pr_id}/merge'.format(
                    project_key=project_key, repository=repository, pr_id=pr_id))
            params = {}

        return self.post(url, params=params)

    def reopen_pull_request(self, project_key, repository, pr_id, pr_version):
        """
        Re-open a declined pull request.
        The authenticated user must have REPO_READ permission for the repository 
        that this pull request targets to call this resource.

        :param project_key: PROJECT
        :param repository: my_shiny_repo
        :param pr_id: 2341
        :param pr_version: 12
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project_key}/repos/{repository}/pull-requests/{pr_id}/reopen'.format(
                project_key=project_key, repository=repository, pr_id=pr_id)
        else:
            url = 'rest/api/2.0/projects/{project_key}/repos/{repository}/pull-requests/{pr_id}/reopen'.format(
                project_key=project_key, repository=repository, pr_id=pr_id)
        params = {'version': pr_version}

        return self.post(url, params=params)

    def check_inbox_pull_requests_count(self):
        if not self.cloud:
            return self.get('rest/api/1.0/inbox/pull-requests/count')
        return self.get('rest/api/2.0/inbox/pull-requests/count')

    def check_inbox_pull_requests(self, start=0, limit=None, role=None):
        """
        Get pull request in your inbox
        :param start:
        :param limit:
        :param role:
        :return:
        """
        params = {'start': start}
        if limit:
            params['limit'] = limit
        if role:
            params['role'] = role
        if not self.cloud:
            url = 'rest/api/1.0/inbox/pull-requests'
        else:
            url = 'rest/api/2.0/inbox/pull-requests'
        return self.get(url, params=params)

    def add_pull_request_comment(self, project, repository, pull_request_id, text, parent_id=None):
        """
        Add comment into pull request
        :param project:
        :param repository:
        :param pull_request_id: the ID of the pull request within the repository
        :param text comment text
        :param parent_id parent comment id

        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}/comments'.format(
                project=project, repository=repository, pullRequestId=pull_request_id)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}/comments'.format(
                project=project, repository=repository, pullRequestId=pull_request_id)
        body = {'text': text}
        if parent_id:
            body['parent'] = {'id': parent_id}
        return self.post(url, data=body)

    def get_pull_request_comment(self, project, repository, pull_request_id, comment_id):
        """
        Retrieves a pull request comment.
        The authenticated user must have REPO_READ permission
        for the repository that this pull request targets to call this resource.
        :param project:
        :param repository:
        :param pull_request_id: the ID of the pull request within the repository
        :param comment_id: the ID of the comment to retrieve
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}/comments/' \
                  '{comment_id}'.format(project=project, repository=repository, pullRequestId=pull_request_id,
                                        comment_id=comment_id)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}/comments/' \
                  '{comment_id}'.format(project=project, repository=repository, pullRequestId=pull_request_id,
                                        comment_id=comment_id)
        return self.get(url)

    def update_pull_request_comment(self, project, repository, pull_request_id, comment_id, comment, comment_version):
        """
        Update the text of a comment.
        Only the user who created a comment may update it.

        Note: the supplied supplied JSON object must contain a version
        that must match the server's version of the comment
        or the update will fail.
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repo}/pull-requests/{pull_request}/comments/{comment_id}' \
                .format(project=project, repo=repository, pull_request=pull_request_id, comment_id=comment_id)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repo}/pull-requests/{pull_request}/comments/{comment_id}' \
                .format(project=project, repo=repository, pull_request=pull_request_id, comment_id=comment_id)
        payload = {
            "version": comment_version,
            "text": comment
        }
        return self.put(url, data=payload)

    def get_pull_request(self, project, repository, pull_request_id):
        """
        Retrieve a pull request.
        The authenticated user must have REPO_READ permission
        for the repository that this pull request targets to call this resource.
        :param project:
        :param repository:
        :param pull_request_id: the ID of the pull request within the repository
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}'.format(
                project=project, repository=repository, pullRequestId=pull_request_id)
        else:
            url = self.resource_url(
                'repositories/{project}/{repository}/pullrequests/{pullRequestId}'.format(
                    project=project, repository=repository, pullRequestId=pull_request_id))
        return self.get(url)

    def get_pullrequest(self, *args, **kwargs):
        """
        Deprecated name since 1.15.1. Let's use the get_pull_request()
        """
        return self.get_pull_request(*args, **kwargs)

    def change_reviewed_status(self, project_key, repository_slug, pull_request_id, status, user_slug):
        """
        Change the current user's status for a pull request.
        Implicitly adds the user as a participant if they are not already.
        If the current user is the author, this method will fail.
        :param project_key:
        :param repository_slug:
        :param pull_request_id:
        :param status:
        :param user_slug:
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{projectKey}/repos/{repo}/pull-requests/{pull_request}/participants/' \
                  '{userSlug}'.format(projectKey=project_key, repo=repository_slug, pull_request=pull_request_id,
                                      userSlug=user_slug)
        else:
            url = 'rest/api/2.0/projects/{projectKey}/repos/{repo}/pull-requests/{pull_request}/participants/' \
                  '{userSlug}'.format(projectKey=project_key, repo=repository_slug, pull_request=pull_request_id,
                                      userSlug=user_slug)
        approved = True if status == "APPROVED" else False
        data = {
            "user": {
                "name": user_slug
            },
            "approved": approved,
            "status": status
        }
        return self.put(url, data)

    def get_tags(self, project, repository, filter='', limit=1000, order_by=None, start=0):
        """
        Retrieve the tags matching the supplied filterText param.
        The authenticated user must have REPO_READ permission for the context repository to call this resource.
        :param project:
        :param repository:
        :param filter:
        :param start:
        :param limit: OPTIONAL: The limit of the number of tags to return, this may be restricted by
                fixed system limits. Default by built-in method: 1000
        :param order_by: OPTIONAL: ordering of refs either ALPHABETICAL (by name) or MODIFICATION (last updated)
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/tags'.format(project=project,
                                                                                   repository=repository)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/tags'.format(project=project,
                                                                                   repository=repository)
        params = {}
        if start:
            params['start'] = start
        if limit:
            params['limit'] = limit
        if filter:
            params['filterText'] = filter
        if order_by:
            params['orderBy'] = order_by
        result = self.get(url, params=params)
        if result.get('isLastPage'):
            log.info('This is a last page of the result')
        else:
            log.info('Next page start at {}'.format(result.get('nextPageStart')))
        return (result or {}).get('values')

    def get_project_tags(self, project, repository, tag_name):
        """
        Retrieve a tag in the specified repository.
        The authenticated user must have REPO_READ permission for the context repository to call this resource.
        Search uri is api/1.0/projects/{projectKey}/repos/{repositorySlug}/tags/{name:.*}
        :param project:
        :param repository:
        :param tag_name: OPTIONAL:
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/tags/{tag}'.format(project=project,
                                                                                         repository=repository,
                                                                                         tag=tag_name)
        else:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/tags/{tag}'.format(project=project,
                                                                                         repository=repository,
                                                                                         tag=tag_name)
        return self.get(url)

    def set_tag(self, project, repository, tag_name, commit_revision, description=None):
        """
        Creates a tag using the information provided in the {@link RestCreateTagRequest request}
        The authenticated user must have REPO_WRITE permission for the context repository to call this resource.
        :param project:
        :param repository:
        :param tag_name:
        :param commit_revision: commit hash
        :param description: OPTIONAL:
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/tags'.format(project=project,
                                                                                   repository=repository)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/tags'.format(project=project,
                                                                                   repository=repository)
        body = {}
        if tag_name is not None:
            body['name'] = tag_name
        if tag_name is not None:
            body['startPoint'] = commit_revision
        if tag_name is not None:
            body['message'] = description
        return self.post(url, data=body)

    def delete_tag(self, project, repository, tag_name):
        """
        Creates a tag using the information provided in the {@link RestCreateTagRequest request}
        The authenticated user must have REPO_WRITE permission for the context repository to call this resource.
        :param project:
        :param repository:
        :param tag_name:
        :return:
        """
        if not self.cloud:
            url = 'rest/git/1.0/projects/{project}/repos/{repository}/tags/{tag}'.format(project=project,
                                                                                         repository=repository,
                                                                                         tag=tag_name)
        else:
            url = 'rest/git/2.0/projects/{project}/repos/{repository}/tags/{tag}'.format(project=project,
                                                                                         repository=repository,
                                                                                         tag=tag_name)
        return self.delete(url)

    def get_diff(self, project, repository, path, hash_oldest, hash_newest):
        """
        Gets a diff of the changes available in the {@code from} commit but not in the {@code to} commit.
        If either the {@code from} or {@code to} commit are not specified,
        they will be replaced by the default branch of their containing repository.
        :param project:
        :param repository:
        :param path:
        :param hash_oldest: the source commit (can be a partial/full commit ID or qualified/unqualified ref name)
        :param hash_newest: the target commit (can be a partial/full commit ID or qualified/unqualified ref name)
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/compare/diff/{path}'.format(project=project,
                                                                                                  repository=repository,
                                                                                                  path=path)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/compare/diff/{path}'.format(project=project,
                                                                                                  repository=repository,
                                                                                                  path=path)
        params = {}
        if hash_oldest:
            params['from'] = hash_oldest
        if hash_newest:
            params['to'] = hash_newest
        return (self.get(url, params=params) or {}).get('diffs')

    def get_commits(self, project, repository, hash_oldest=None, hash_newest=None, follow_renames=False,
                    ignore_missing=False, merges="include", with_counts=False,
                    avatar_size=None, avatar_scheme=None, limit=99999):
        """
        Get commit list from repo
        :param project:
        :param repository:
        :param hash_oldest:
        :param hash_newest:
        :param merges: OPTIONAL: include|exclude|only if present, controls how merge commits should be filtered.
        :param follow_renames: OPTIONAL: if true, the commit history of the specified file will be followed past renames
        :param ignore_missing: OPTIONAL: true to ignore missing commits, false otherwise
        :param with_counts: OPTIONAL: optionally include the total number of commits and total number of unique authors
        :param avatar_size: OPTIONAL: if present the service adds avatar URLs for commit authors.
        :param avatar_scheme: OPTIONAL: the desired scheme for the avatar URL
        :param limit: OPTIONAL: The limit of the number of commits to return, this may be restricted by
               fixed system limits. Default by built-in method: 99999
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/commits'.format(project=project,
                                                                                      repository=repository)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/commits'.format(project=project,
                                                                                      repository=repository)
        params = {"merges": merges}
        if hash_oldest:
            params['since'] = hash_oldest
        if hash_newest:
            params['until'] = hash_newest
        if follow_renames:
            params['followRenames'] = follow_renames
        if ignore_missing:
            params['ignoreMissing'] = ignore_missing
        if with_counts:
            params['withCounts'] = with_counts
        if avatar_size:
            params['avatarSize'] = avatar_size
        if avatar_scheme:
            params['avatarScheme'] = avatar_scheme
        if limit:
            params['limit'] = limit
        return (self.get(url, params=params) or {}).get('values')

    def get_commit_info(self, project, repository, commit, path=None):
        """
        Retrieve a single commit identified by its ID>. In general, that ID is a SHA1.
        From 2.11, ref names like "refs/heads/master" are no longer accepted by this resource.
        The authenticated user must have REPO_READ permission for the specified repository to call this resource.
        :param project:
        :param repository:
        :param commit: the commit ID to retrieve
        :param path :OPTIONAL an optional path to filter the commit by.
                        If supplied the details returned may not be for the specified commit.
                        Instead, starting from the specified commit, they will be the details for the first commit
                        affecting the specified path.
        :return:
        """

        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/commits/{commitId}'.format(project=project,
                                                                                                 repository=repository,
                                                                                                 commitId=commit)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/commits/{commitId}'.format(project=project,
                                                                                                 repository=repository,
                                                                                                 commitId=commit)
        params = {}
        if path:
            params['path'] = path
        return self.get(url, params=params)

    def get_pull_requests_contain_commit(self, project, repository, commit):
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/commits/{commitId}/pull-requests'.format(
                project=project, repository=repository, commitId=commit)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/commits/{commitId}/pull-requests'.format(
                project=project, repository=repository, commitId=commit)
        return (self.get(url) or {}).get('values')

    def get_changelog(self, project, repository, ref_from, ref_to, limit=99999):
        """
        Get change log between 2 refs
        :param project:
        :param repository:
        :param ref_from:
        :param ref_to:
        :param limit: OPTIONAL: The limit of the number of changes to return, this may be restricted by
                fixed system limits. Default by built-in method: 99999
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/compare/commits'.format(project=project,
                                                                                              repository=repository)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/compare/commits'.format(project=project,
                                                                                              repository=repository)
        params = {}
        if ref_from:
            params['from'] = ref_from
        if ref_to:
            params['to'] = ref_to
        if limit:
            params['limit'] = limit
        return (self.get(url, params=params) or {}).get('values')

    def get_file_list(self, project, repository, query=None, limit=100000):
        """
        Retrieve a page of files from particular directory of a repository.
        The search is done recursively, so all files from any sub-directory of the specified directory will be returned.
        The authenticated user must have REPO_READ permission for the specified repository to call this resource.
        :param project:
        :param repository:
        :param query: the commit ID or ref (e.g. a branch or tag) to list the files at.
                      If not specified the default branch will be used instead.
        :param limit: OPTIONAL
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/files'.format(project=project,
                                                                                    repository=repository)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/files'.format(project=project,
                                                                                    repository=repository)
        params = {}
        if query:
            params['at'] = query
        if limit:
            params['limit'] = limit
        return (self.get(url, params=params) or {}).get('values')

    def get_content_of_file(self, project, repository, filename, at=None, markup=None):
        """
        Retrieve the raw content for a file path at a specified revision.
        The authenticated user must have REPO_READ permission for the specified repository to call this resource.
        :param project:
        :param repository:
        :param filename:
        :param at: OPTIONAL ref string
        :param markup: 	if present or "true", triggers the raw content to be markup-rendered and returned as HTML;
                        otherwise, if not specified, or any value other than "true",
                        the content is streamed without markup
        :return:
        """
        headers = self.form_token_headers
        url = 'projects/{project}/repos/{repository}/raw/{filename}/'.format(project=project,
                                                                             repository=repository,
                                                                             filename=filename)
        params = {}
        if at is not None:
            params['at'] = at
        if markup is not None:
            params['markup'] = markup
        return self.get(url, params=params, not_json_response=True, headers=headers)

    def get_branches_permissions(self, project, repository=None, start=0, limit=25):
        """
        Get branches permissions from a given repo
        :param project:
        :param repository:
        :param start:
        :param limit:
        :return:
        """
        if repository is not None:
            url = 'rest/branch-permissions/2.0/projects/{project}/repos/{repository}/restrictions'.format(
                project=project,
                repository=repository)
        else:
            url = 'rest/branch-permissions/2.0/projects/{project}/restrictions'.format(project=project)
        params = {}
        if limit:
            params['limit'] = limit
        if start:
            params['start'] = start
        return self.get(url, params=params)

    def set_branches_permissions(self, project_key, multiple_permissions=False, matcher_type=None, matcher_value=None,
                                 permission_type=None, repository=None, except_users=None, except_groups=None,
                                 except_access_keys=None, start=0, limit=25):
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
        :param repository:
        :param except_users:
        :param except_groups:
        :param except_access_keys:
        :param start:
        :param limit:
        :return:
        """
        if except_users is None:
            except_users = []
        if except_groups is None:
            except_groups = []
        if except_access_keys is None:
            except_access_keys = []
        headers = self.default_headers
        if repository:
            url = "rest/branch-permissions/2.0/projects/{project_key}/repos/{repository}/restrictions".format(
                project_key=project_key,
                repository=repository
            )
        else:
            url = "rest/branch-permissions/2.0/projects/{project_key}/restrictions".format(
                project_key=project_key
            )
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
                        "name": matcher_type.capitalize()
                    },
                    "active": True,
                },
                "users": except_users,
                "groups": except_groups,
                "accessKeys": except_access_keys,
            }
        params = {"start": start, "limit": limit}
        return self.post(url, data=restriction, params=params, headers=headers)

    def delete_branch_permission(self, project_key, permission_id, repository=None):
        """
        Deletes a restriction as specified by a restriction id.
        The authenticated user must have REPO_ADMIN permission or higher to call this resource. 

        :param project_key:
        :param repository:
        :param permission_id:
        :return:
        """

        if repository:
            url = "rest/branch-permissions/2.0/projects/{project_key}/repos/{repository}/restrictions/{id}".format(
                project_key=project_key,
                repository=repository,
                id=permission_id
            )
        else:
            url = "rest/branch-permissions/2.0/projects/{project_key}/restrictions/{id}".format(
                project_key=project_key,
                id=permission_id
            )
        return self.delete(url)

    def get_branch_permission(self, project_key, permission_id, repository=None):
        """
        Returns a restriction as specified by a restriction id.
        The authenticated user must have REPO_ADMIN permission or higher to call this resource. 

        :param project_key:
        :param repository:
        :param permission_id:
        :return:
        """

        if repository:
            url = "rest/branch-permissions/2.0/projects/{project_key}/repos/{repository}/restrictions/{id}".format(
                project_key=project_key,
                repository=repository,
                id=permission_id
            )
        else:
            url = "rest/branch-permissions/2.0/projects/{project_key}/restrictions/{id}".format(
                project_key=project_key,
                id=permission_id
            )
        return self.get(url)

    def all_branches_permissions(self, project, repository=None):
        """
        Get branches permissions from a given repo
        :param project:
        :param repository:
        :return:
        """
        start = 0
        branches_permissions = []
        response = self.get_branches_permissions(project=project, repository=repository, start=start)
        branches_permissions += response.get('values')
        while not response.get('isLastPage'):
            start = response.get('nextPageStart')
            response = self.get_branches_permissions(project=project, repository=repository, start=start)
            branches_permissions += response.get('values')
        return branches_permissions

    def reindex(self):
        """
        Rebuild the bundled Elasticsearch indexes for Bitbucket Server
        :return:
        """
        url = 'rest/indexing/latest/sync'
        return self.post(url)

    def reindex_repo(self, project, repository):
        """
        Reindex repo
        :param project:
        :param repository:
        :return:
        """
        url = 'rest/indexing/1.0/projects/{projectKey}/repos/{repositorySlug}/sync'.format(projectKey=project,
                                                                                           repositorySlug=repository)
        return self.post(url)

    def reindex_repo_dev_panel(self, project, repository):
        """
        Reindex all of the Jira issues related to this repository, including branches and pull requests.
        This automatically happens as part of an upgrade, and calling this manually should only be required
        if something unforeseen happens and the index becomes out of sync.
        The authenticated user must have REPO_ADMIN permission for the specified repository to call this resource.
        :param project:
        :param repository:
        :return:
        """
        url = 'rest/jira-dev/1.0/projects/{projectKey}/repos/{repositorySlug}/reindex'.format(projectKey=project,
                                                                                              repositorySlug=repository)
        return self.post(url)

    def check_reindexing_status(self):
        """
        Check reindexing status
        :return:
        """
        url = 'rest/indexing/latest/status'
        return self.get(url)

    def fork_repository(self, project, repository, new_repository):
        """
        Forks a repository within the same project.
        :param project:
        :param repository:
        :param new_repository:
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}'.format(project=project,
                                                                              repository=repository)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}'.format(project=project,
                                                                              repository=repository)
        body = {}
        if new_repository is not None:
            body['name'] = new_repository
        if new_repository is not None:
            body['project'] = {'key': project}
        return self.post(url, data=body)

    def get_current_license(self):
        """
        Retrieves details about the current license, as well as the current status of the system with
        regards to the installed license. The status includes the current number of users applied
        toward the license limit, as well as any status messages about the license (warnings about expiry
        or user counts exceeding license limits).
        The authenticated user must have ADMIN permission. Unauthenticated users, and non-administrators,
        are not permitted to access license details.
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/admin/license'
        else:
            url = 'rest/api/2.0/admin/license'
        return self.get(url)

    def get_mail_configuration(self):
        """
        Retrieves the current mail configuration.
        The authenticated user must have the SYS_ADMIN permission to call this resource.
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/admin/mail-server'
        else:
            url = 'rest/api/2.0/admin/mail-server'
        return self.get(url)

    def get_mail_sender_address(self):
        """
        Retrieves the server email address
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/admin/mail-server/sender-address'
        else:
            url = 'rest/api/2.0/admin/mail-server/sender-address'
        return self.get(url)

    def remove_mail_sender_address(self):
        """
        Clears the server email address.
        The authenticated user must have the ADMIN permission to call this resource.
        :return:
        """
        if not self.cloud:
            url = 'rest/api/1.0/admin/mail-server/sender-address'
        else:
            url = 'rest/api/2.0/admin/mail-server/sender-address'
        return self.delete(url)

    def get_ssh_settings(self):
        """
        Retrieve ssh settings for user
        :return:
        """
        if not self.cloud:
            url = 'rest/ssh/1.0/settings'
        else:
            url = 'rest/ssh/2.0/settings'
        return self.get(url)

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

    def get_branching_model(self, project, repository):
        """
        Get branching model
        :param project:
        :param repository:
        :return:
        """
        url = 'rest/branch-utils/1.0/projects/{project}/repos/{repository}/branchmodel/configuration'.format(
            project=project,
            repository=repository)
        return self.get(url)

    def set_branching_model(self, project, repository, data):
        """
        Set branching model
        :param project:
        :param repository:
        :param data:
        :return:
        """
        url = 'rest/branch-utils/1.0/projects/{project}/repos/{repository}/branchmodel/configuration'.format(
            project=project,
            repository=repository)
        return self.put(url, data=data)

    def enable_branching_model(self, project, repository):
        """
        Enable branching model by setting it with default configuration
        :param project:
        :param repository:
        :return:
        """
        default_model_data = {'development': {'refId': None, 'useDefault': True},
                              'types': [{'displayName': 'Bugfix',
                                         'enabled': True,
                                         'id': 'BUGFIX',
                                         'prefix': 'bugfix/'},
                                        {'displayName': 'Feature',
                                         'enabled': True,
                                         'id': 'FEATURE',
                                         'prefix': 'feature/'},
                                        {'displayName': 'Hotfix',
                                         'enabled': True,
                                         'id': 'HOTFIX',
                                         'prefix': 'hotfix/'},
                                        {'displayName': 'Release',
                                         'enabled': True,
                                         'id': 'RELEASE',
                                         'prefix': 'release/'}]}
        return self.set_branching_model(project,
                                        repository,
                                        default_model_data)

    def disable_branching_model(self, project, repository):
        """
        Disable branching model
        :param project:
        :param repository:
        :return:
        """
        url = 'rest/branch-utils/1.0/projects/{project}/repos/{repository}/branchmodel/configuration'.format(
            project=project,
            repository=repository)
        return self.delete(url)

    def markup_preview(self, data):
        """
        Preview generated HTML for the given markdown content.
        Only authenticated users may call this resource.
        :param data:
        :return:
        """

        if not self.cloud:
            return self.post('rest/api/1.0/markup/preview', data=data)
        return self.post('rest/api/2.0/markup/preview', data=data)

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

    def upload_file(self, project, repository, content, message, branch, filename):
        """
        Upload new file for given branch.
        :param project:
        :param repository:
        :param content:
        :param message:
        :param branch:
        :param filename
        :return:
        """
        data = {
            "content": content,
            "message": message,
            "branch": branch
        }

        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/browse/{filename}'.format(
                project=project, repository=repository, filename=filename)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/browse/{filename}'.format(
                project=project, repository=repository, filename=filename)
        return self.put(url, files=data)

    def update_file(self, project, repository, content, message, branch, filename, source_commit_id):
        """
        Update existing file for given branch.
        :param project:
        :param repository:
        :param content:
        :param message:
        :param branch:
        :param filename:
        :param source_commit_id:
        :return:
        """
        data = {
            "content": content,
            "message": message,
            "branch": branch,
            "sourceCommitId": source_commit_id
        }
        if not self.cloud:
            url = 'rest/api/1.0/projects/{project}/repos/{repository}/browse/{filename}'.format(
                project=project, repository=repository, filename=filename)
        else:
            url = 'rest/api/2.0/projects/{project}/repos/{repository}/browse/{filename}'.format(
                project=project, repository=repository, filename=filename)
        return self.put(url, files=data)

    def get_code_insights_report(self, project_key, repository_slug, commit_id, report_key):
        """
        Retrieve the specified code-insights report.
        :projectKey: str
        :repositorySlug: str
        :commitId: str
        :report_key: str
        """
        url = "rest/insights/1.0/projects/{projectKey}/repos/{repositorySlug}/commits/{commitId}/reports/{key}".format(
            projectKey=project_key, repositorySlug=repository_slug, commitId=commit_id, key=report_key
        )
        return self.get(url)

    def delete_code_insights_report(self, project_key, repository_slug, commit_id, report_key):
        """
        Delete a report for the given commit. Also deletes any annotations associated with this report.
        :projectKey: str
        :repositorySlug: str
        :commitId: str
        :report_key: str
        """
        url = "rest/insights/1.0/projects/{projectKey}/repos/{repositorySlug}/commits/{commitId}/reports/{key}".format(
            projectKey=project_key, repositorySlug=repository_slug, commitId=commit_id, key=report_key
        )
        return self.delete(url)

    def create_code_insights_report(self, project_key, repository_slug, commit_id, report_key, report_title,
                                    **report_params):
        """
        Create a new insight report, or replace the existing one
        if a report already exists for the given repository, commit, and report key.
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
        url = "rest/insights/1.0/projects/{projectKey}/repos/{repositorySlug}/commits/{commitId}/reports/{key}".format(
            projectKey=project_key, repositorySlug=repository_slug, commitId=commit_id, key=report_key
        )
        data = {"title": report_title}
        data.update(report_params)
        return self.put(url, data=data)

    def search_code(self, team, search_query, page=1, limit=10):
        """
        Search repositories for matching code
        :team: str
        :search_query: str
        """
        endpoint = 'rest/api/1.0'
        if self.cloud:
            endpoint = 'rest/api/2.0'
        url = "{endpoint}/teams/{team}/search/code".format(endpoint=endpoint, team=team)
        return self.get(url, params={'search_query': search_query, 'page': page, 'pagelen': limit})

    def get_lfs_repo_status(self, project_key, repo):
        url = 'rest/git-lfs/git-lfs/admin/projects/{projectKey}/repos/{repositorySlug}/enabled'.format(
            projectKey=project_key,
            repositorySlug=repo)
        return self.get(url)

    def get_users(self, user_filter=None):
        """
        Get list of bitbucket users. 
        Use 'user_filter' for get specific users.
        :user_filter: str
        """
        url = "rest/api/1.0/users"
        params = {}
        if user_filter:
            params['filter'] = user_filter
        return self.get(url, params=params)

    def _get_paged(self, url, params):
        """
        Use for get all methods
        :param url:
        :param params:
        :return:
        """
        params['start'] = 0
        response = self.get(url, params=params)
        if 'values' not in response:
            return []
        values = response.get('values')
        while not response.get('isLastPage'):
            params['start'] = response.get('nextPageStart')
            response = self.get(url, params=params)
            values += response.get('values')
        return values

    def get_project_conditions(self, project_key):
        """
        Request type: GET
        Return a page of defaults conditions with reviewers list that have been configured for this project.
        For further information visit:
            https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-default-reviewers-rest.html#idm52264904368
        :projectKey: str
        :return:
        """
        url = 'rest/default-reviewers/1.0/projects/{projectKey}/conditions'.format(
            projectKey=project_key)
        return self.get(url) or {}

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
        url = 'rest/default-reviewers/1.0/projects/{projectKey}/conditions/{idCondition}'.format(
            projectKey=project_key,
            idCondition=id_condition)
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
        url = 'rest/default-reviewers/1.0/projects/{projectKey}/condition'.format(
            projectKey=project_key)
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
        url = 'rest/default-reviewers/1.0/projects/{projectKey}/condition/{idCondition}'.format(
            projectKey=project_key,
            idCondition=id_condition)
        return self.put(url, data=condition) or {}

    def delete_project_condition(self, project_key, id_condition):
        """
        Request type: DELETE
        Delete a specific condition for this repository slug inside project.
        For further information visit:
            https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-default-reviewers-rest.html#idm52264896304
        :projectKey: str- project key involved
        :idCondition: int - condition id involved
        :return:
        """
        url = 'rest/default-reviewers/1.0/projects/{projectKey}/condition/{idCondition}'.format(
            projectKey=project_key,
            idCondition=id_condition)
        return self.delete(url) or {}

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
        url = 'rest/default-reviewers/1.0/projects/{projectKey}/repos/{repoKey}/conditions'.format(
            projectKey=project_key,
            repoKey=repo_key)
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
        type_repo = 'REPOSITORY'
        url = 'rest/default-reviewers/1.0/projects/{projectKey}/repos/{repoKey}/conditions'.format(
            projectKey=project_key,
            repoKey=repo_key)

        response = (self.get(url) or {})
        count = 0
        for condition in response:
            if condition['scope']['type'] == type_repo:
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
        type_proyect = 'PROJECT'
        url = 'rest/default-reviewers/1.0/projects/{projectKey}/repos/{repoKey}/conditions'.format(
            projectKey=project_key,
            repoKey=repo_key)

        response = (self.get(url) or {})
        count = 0
        for condition in response:
            if condition['scope']['type'] == type_proyect:
                del response[count]
            count += 1
        return response

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
        url = 'rest/default-reviewers/1.0/projects/{projectKey}/repos/{repoKey}/conditions/{idCondition}'.format(
            projectKey=project_key,
            repoKey=repo_key,
            idCondition=id_condition)
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
        url = 'rest/default-reviewers/1.0/projects/{projectKey}/repos/{repoKey}/condition'.format(
            projectKey=project_key,
            repoKey=repo_key)
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
        url = 'rest/default-reviewers/1.0/projects/{projectKey}/repos/{repoKey}/condition/{idCondition}'.format(
            projectKey=project_key,
            repoKey=repo_key,
            idCondition=id_condition)
        return self.put(url, data=condition) or {}

    def delete_repo_condition(self, project_key, repo_key, id_condition):
        """
        Request type: DELETE
        Delete a specific condition for this repository slug inside project.
        For further information visit:
            https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-default-reviewers-rest.html#idm8287339888
        :projectKey: str- project key involved
        :repoKey: str - repo key involved
        :idCondition: int - condition id involved
        :return:
        """
        url = 'rest/default-reviewers/1.0/projects/{projectKey}/repos/{repoKey}/condition/{idCondition}'.format(
            projectKey=project_key,
            repoKey=repo_key,
            idCondition=id_condition)
        return self.delete(url) or {}

    def get_associated_build_statuses(self, commit):
        """
        To get the build statuses associated with a commit.
        :commit: str- commit id
        :return:
        """
        if not self.cloud:
            url = '/rest/build-status/1.0/commits/{commitId}'.format(commitId=commit)
        else:
            url = '/rest/build-status/2.0/commits/{commitId}'.format(commitId=commit)

        return self.get(url)

    def get_announcement_banner(self):
        """
        Gets the announcement banner, if one exists and is available to the user
        :return:
        """
        if not self.cloud:
            url = "rest/api/1.0/admin/banner"
        else:
            url = "rest/api/2.0/admin/banner"
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
        if not self.cloud:
            url = "rest/api/1.0/admin/banner"
        else:
            url = "rest/api/2.0/admin/banner"
        return self.put(url, data=body)

    def delete_announcement_banner(self):
        """
        Gets the announcement banner, if one exists and is available to the user
        :return:
        """
        if not self.cloud:
            url = "rest/api/1.0/admin/banner"
        else:
            url = "rest/api/2.0/admin/banner"
        return self.delete(url)

    def get_pipelines(self, workspace, repository, number=10,
                      sort_by="-created_on"):
        """
        Get information about latest pipelines runs.

        :param number: number of pipelines to fetch
        :param :sort_by: optional key to sort available pipelines for
        :return: information in form {"values": [...]}
        """
        resource = "repositories/{workspace}/{repository}/pipelines/".format(
            workspace=workspace, repository=repository)
        return self.get(self.resource_url(resource),
                        params={"pagelen": number, "sort": sort_by},
                        trailing=True)

    def get_pipeline(self, workspace, repository, uuid):
        """
        Get information about the pipeline specified by ``uuid``.
        :param uuid: Pipeline identifier (with surrounding {}; NOT the build number)
        """
        resource = "repositories/{workspace}/{repository}/pipelines/{uuid}".format(
            workspace=workspace, repository=repository, uuid=uuid)
        return self.get(self.resource_url(resource))

    def trigger_pipeline(self, workspace, repository, branch="master", revision=None,
                         name=None):
        """
        Trigger a new pipeline. The following options are possible (1 and 2
        trigger the pipeline that the branch is associated with in the Pipelines
        configuration):
        1. Latest revision of a branch (specify ``branch``)
        2. Specific revision on a branch (additionally specify ``revision``)
        3. Specific pipeline (additionally specify ``name``)
        :return: the initiated pipeline; or error information
        """
        resource = "repositories/{workspace}/{repository}/pipelines/".format(
            workspace=workspace, repository=repository)

        data = {
            "target": {
                "ref_type": "branch",
                "type": "pipeline_ref_target",
                "ref_name": branch,
            },
        }
        if revision:
            data["target"]["commit"] = {
                "type": "commit",
                "hash": revision,
            }
        if name:
            if not revision:
                raise ValueError("Missing revision")
            data["target"]["selector"] = {
                "type": "custom",
                "pattern": name,
            }

        return self.post(self.resource_url(resource), data=data, trailing=True)

    def stop_pipeline(self, workspace, repository, uuid):
        """
        Stop the pipeline specified by ``uuid``.
        :param uuid: Pipeline identifier (with surrounding {}; NOT the build number)

        See the documentation for the meaning of response status codes.
        """
        resource = "repositories/{workspace}/{repository}/pipelines/{uuid}/stopPipeline".format(
            workspace=workspace, repository=repository, uuid=uuid)
        return self.post(self.resource_url(resource))

    def get_pipeline_steps(self, workspace, repository, uuid):
        """
        Get information about the steps of the pipeline specified by ``uuid``.
        :param uuid: Pipeline identifier (with surrounding {}; NOT the build number)
        """
        resource = "repositories/{workspace}/{repository}/pipelines/{uuid}/steps/".format(
            workspace=workspace, repository=repository, uuid=uuid)
        return self.get(self.resource_url(resource), trailing=True)

    def get_pipeline_step(self, workspace, repository, pipeline_uuid, step_uuid):
        """
        Get information about a step of a pipeline, specified by respective UUIDs.
        :param pipeline_uuid: Pipeline identifier (with surrounding {}; NOT the build number)
        :param step_uuid: Step identifier (with surrounding {})
        """
        resource = "repositories/{w}/{r}/pipelines/{p}/steps/{s}".format(
            w=workspace, r=repository, p=pipeline_uuid, s=step_uuid)
        return self.get(self.resource_url(resource))

    def get_pipeline_step_log(self, workspace, repository, pipeline_uuid, step_uuid):
        """
        Get log of a step of a pipeline, specified by respective UUIDs.
        :param pipeline_uuid: Pipeline identifier (with surrounding {}; NOT the build number)
        :param step_uuid: Step identifier (with surrounding {})
        :return: byte string log
        """
        resource = "repositories/{w}/{r}/pipelines/{p}/steps/{s}/log".format(
            w=workspace, r=repository, p=pipeline_uuid, s=step_uuid)
        headers = {"Accept": "application/octet-stream"}
        return self.get(self.resource_url(resource), headers=headers, not_json_response=True)

    def get_tasks(self, project, repository, pull_request_id):
        """
        Get all tasks for the pull request
        :param project:
        :param repository:
        :param pull_request_id: the ID of the pull request within the repository
        :return:
        """
        if self.cloud:
            raise Exception("Not supported in Bitbucket Cloud")
        url = "/rest/api/1.0/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/tasks".format(
            projectKey=project,
            repositorySlug=repository,
            pullRequestId=pull_request_id)
        return self.get(url)

    def add_task(self, anchor, text):
        """
        Add task to the comment
        :param anchor: ID of the comment, 
        :param text: task text
        :return:
        """
        if self.cloud:
            raise Exception("Not supported in Bitbucket Cloud")
        url = "/rest/api/1.0/tasks"
        data = {
            "anchor": {
                "id": anchor,
                "type": "COMMENT"
            },
            "text": text
        }
        return self.post(url, data=data)

    def get_task(self, task_id):
        """
        Get task information by ID
        :param task_id:
        :return:
        """
        if self.cloud:
            raise Exception("Not supported in Bitbucket Cloud")
        url = "/rest/api/1.0/tasks/{taskId}".format(taskId=task_id)
        return self.get(url)

    def delete_task(self, task_id):
        """
        Delete task by ID
        :param task_id:
        :return:
        """
        if self.cloud:
            raise Exception("Not supported in Bitbucket Cloud")
        url = "/rest/api/1.0/tasks/{taskId}".format(taskId=task_id)
        return self.delete(url)

    def update_task(self, task_id, text=None, state=None):
        """
        Update task by ID. It is possible to update state and/or text of the task
        :param task_id:
        :param text: 
        :param state: OPEN, RESOLVED
        :return:
        """
        if self.cloud:
            raise Exception("Not supported in Bitbucket Cloud")
        data = {"id": task_id}
        if text:
            data["text"] = text
        if state:
            data["state"] = state
        url = "/rest/api/1.0/tasks/{taskId}".format(taskId=task_id)
        return self.put(url, data=data)

    def get_issues(self, workspace, repository, sort_by=None, query=None):
        """
        Get information about the issues tracked in the given repository. By
        default, the issues are sorted by ID in descending order.
        :param sort_by: optional key to sort available issues for
        :param query: optional query to filter available issues for. See
          https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering
          for an overview

        :return: List of issues (direct, i.e. without the 'values' key)
        """
        resource = "repositories/{workspace}/{repository}/issues".format(
            workspace=workspace, repository=repository)

        params = {}
        if sort_by is not None:
            params["sort"] = sort_by
        if query is not None:
            params["q"] = query

        response = self.get(self.resource_url(resource), params=params)
        issues = response.get("values", [])

        while True:
            next_page = response.get("next")
            if next_page is None:
                break

            # Strip the base url - it's added when constructing the request
            response = self.get(next_page.replace(self.url, ""))
            issues.extend(response.get("values", []))

        return issues

    def create_issue(self, workspace, repository, title, description="",
                     kind="bug", priority="major"):
        """
        Create a new issue in the issue tracker of the given repository.
        :param kind: one of: bug, enhancement, proposal, task
        :param priority: one of: trivial, minor, major, critical, blocker
        """
        resource = "repositories/{workspace}/{repository}/issues".format(
            workspace=workspace, repository=repository)
        data = {
            "title": title,
            "kind": kind,
            "priority": priority,
            "content": {"raw": description},
        }
        return self.post(self.resource_url(resource), data=data)

    def get_issue(self, workspace, repository, id):
        """
        Get the issue specified by ``id``.
        """
        resource = "repositories/{workspace}/{repository}/issues/{id}".format(
            workspace=workspace, repository=repository, id=id)
        return self.get(self.resource_url(resource))

    def update_issue(self, workspace, repository, id, **fields):
        """
        Update the ``fields`` of the issue specified by ``id``.
        Consult the official API documentation for valid fields.
        """
        resource = "repositories/{workspace}/{repository}/issues/{id}".format(
            workspace=workspace, repository=repository, id=id)
        return self.put(self.resource_url(resource), data=fields)

    def delete_issue(self, workspace, repository, id):
        """
        Delete the issue specified by ``id``.
        """
        resource = "repositories/{workspace}/{repository}/issues/{id}".format(
            workspace=workspace, repository=repository, id=id)
        return self.delete(self.resource_url(resource))

    def get_repositories(self, workspace, role=None, query=None, sort=None, number=10, page=1):
        """
        Get all repositories in a workspace.
        
        :param role: Filters the result based on the authenticated user's role on each repository.
                      One of: member, contributor, admin, owner
        :param query: Query string to narrow down the response.
        :param sort: Field by which the results should be sorted.
        """
        resource = "repositories/{workspace}".format(workspace=workspace)
        
        params = {
            "pagelen": number,
            "page": page
            }
        if not role is None:
            params["role"] = role
        if not query is None:
            params["query"] = query
        if not sort is None:
            params["sort"] = sort
        
        return self.get(self.resource_url(resource), params=params)

    def get_branch_restrictions(self, workspace, repository, kind=None, pattern=None, number=10, page=1):
        """
        Get all branch permissions.
        """
        resource = "repositories/{workspace}/{repository}/branch-restrictions".format(
            workspace=workspace, repository=repository)
        params = {"pagelen": number, "page": page}
        if not kind is None:
            params["kind"] = kind
        if not pattern is None:
            params["pattern"] = pattern

        return self.get(self.resource_url(resource), params=params)

    def add_branch_restriction(self, workspace, repository, kind, branch_match_kind="glob",
                                branch_pattern = "*", branch_type = None,
                                users = None, groups = None, value = None):
        """
        Add a new branch restriction.

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
        :param users: List of user objects that are excluded from the restriction. Minimal: {"username": "<username>"}
        :param groups: List of group objects that are excluded from the restriction. Minimal: {"owner": {"username": "<teamname>"}, "slug": "<groupslug>"}
        """
        resource = "repositories/{workspace}/{repository}/branch-restrictions".format(
            workspace=workspace, repository=repository)

        if branch_match_kind == "branching_model":
            branch_pattern = ""

        data = {
            "kind": kind,
            "branch_match_kind": branch_match_kind,
            "pattern": branch_pattern,
        }

        if branch_match_kind == "branching_model":
            data["branch_type"] = branch_type

        if not users is None:
            data["users"] = users

        if not groups is None:
            data["groups"] = groups

        if not value is None:
            data["value"] = value

        return self.post(self.resource_url(resource), data=data)

    def update_branch_restriction(self, workspace, repository, id, **fields):
        """
        Update an existing branch restriction identified by ``id``.
        Consult the official API documentation for valid fields.
        """
        resource = "repositories/{workspace}/{repository}/branch-restrictions/{id}".format(
            workspace=workspace, repository=repository, id=id)

        return self.put(self.resource_url(resource), data=fields)

    def delete_branch_restriction(self, workspace, repository, id):
        """
        Delete an existing branch restriction identified by ``id``.
        """
        resource = "repositories/{workspace}/{repository}/branch-restrictions/{id}".format(
            workspace=workspace, repository=repository, id=id)

        return self.delete(self.resource_url(resource))

    
    def get_default_reviewers(self, workspace, repository, number=10, page=1):
        """
        Get all default reviewers for the repository.
        """
        resource = "repositories/{workspace}/{repository}/default-reviewers".format(
            workspace=workspace, repository=repository)
        params = {"pagelen": number, "page": page}
        
        return self.get(self.resource_url(resource), params=params)

    def add_default_reviewer(self, workspace, repository, user):
        """
        Add user as default reviewer to the repository.
        Can safely be called multiple times with the same user, only adds once.

        :param user: The username or account UUID to add as default_reviewer.
        """
        resource = "repositories/{workspace}/{repository}/default-reviewers/{user}".format(
            workspace=workspace, repository=repository, user=user)

        # the mention_id parameter is undocumented but if missed, leads to 400 statuses
        return self.put(self.resource_url(resource), data={"mention_id": user})

    def is_default_reviewer(self, workspace, repository, user):
        """
        Check if the user is a default reviewer of the repository.
        
        :param user: The username or account UUID to check.
        :return: True if present, False if not.
        """
        resource = "repositories/{workspace}/{repository}/default-reviewers/{user}".format(
            workspace=workspace, repository=repository, user=user)

        try:
            self.get(self.resource_url(resource))
            return True
        except HTTPError as httpErr:
            if httpErr.response.status_code == 404:
                return False
            raise httpErr

    def delete_default_reviewer(self, workspace, repository, user):
        """
        Remove user as default reviewer from the repository.
        
        :param user: The username or account UUID to delete as default reviewer.
        """
        resource = "repositories/{workspace}/{repository}/default-reviewers/{user}".format(
            workspace=workspace, repository=repository, user=user)

        return self.delete(self.resource_url(resource))
