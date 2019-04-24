# coding: utf8
import logging
from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Bitbucket(AtlassianRestAPI):
    def project_list(self, limit=None):
        """
        Provide the project list
        :param limit: OPTIONAL 25 is default
        :return:
        """
        params = {}
        if limit:
            params['limit'] = limit
        return (self.get('rest/api/1.0/projects', params=params) or {}).get('values')

    def project(self, key):
        """
        Provide project info
        :param key:
        :return:
        """
        url = 'rest/api/1.0/projects/{0}'.format(key)
        return (self.get(url) or {}).get('values')

    def create_project(self, key, name, description=""):
        """
        Create project
        :param key:
        :param name:
        :param description:
        :return:
        """
        url = 'rest/api/1.0/projects'
        data = {"key": key,
                "name": name,
                "description": description
                }
        return self.post(url, data=data)

    def project_users(self, key, limit=99999, filter_str=None):
        """
        Get users who has permission in project
        :param key:
        :param limit: OPTIONAL: The limit of the number of users to return, this may be restricted by
                            fixed system limits. Default by built-in method: 99999
        :param filter_str:  OPTIONAL: users filter string
        :return:
        """
        url = 'rest/api/1.0/projects/{key}/permissions/users'.format(key=key)
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
        url = 'rest/api/1.0/projects/{project_key}/repos/{repo_key}/permissions/users'.format(
            project_key=project_key,
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

    def project_groups(self, key, limit=99999, filter_str=None):
        """
        Get Project Groups
        :param key:
        :param limit: OPTIONAL: The limit of the number of groups to return, this may be restricted by
                            fixed system limits. Default by built-in method: 99999
        :param filter_str: OPTIONAL: group filter string
        :return:
        """
        url = 'rest/api/1.0/projects/{key}/permissions/groups'.format(key=key)
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
        url = 'rest/api/1.0/projects/{project_key}/repos/{repo_key}/permissions/groups'.format(
            project_key=project_key,
            repo_key=repo_key)
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
            'groups': self.project_groups(key)}

    def group_members(self, group, limit=99999):
        """
        Get group of members
        :param group:
        :param limit: OPTIONAL: The limit of the number of users to return, this may be restricted by
                        fixed system limits. Default by built-in method: 99999
        :return:
        """
        url = 'rest/api/1.0/admin/groups/more-members'
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
        url = 'rest/api/1.0/projects/{projectKey}/repos'.format(projectKey=project_key)
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

        url = 'rest/api/1.0/projects/{projectKey}/repos'.format(projectKey=project_key)
        data = {
            "name": repository,
            "scmId": "git",
            "forkable": forkable,
            "is_private": is_private
        }
        return self.post(url, data=data)

    def repo_all_list(self, project_key):
        """
        Get all repositories list from project
        :param project_key:
        :return:
        """
        url = 'rest/api/1.0/projects/{projectKey}/repos'.format(projectKey=project_key)
        params = {}
        start = 0
        params['start'] = start
        response = self.get(url, params=params)
        if 'values' not in response:
            return []
        repo_list = (response or {}).get('values')
        while not response.get('isLastPage'):
            start = response.get('nextPageStart')
            params['start'] = start
            response = self.get(url, params=params)
            repo_list += (response or {}).get('values')
        return repo_list

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
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/branches'.format(project=project,
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

        return (self.get(url, params=params) or {}).get('values')

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

        url = 'rest/api/1.0/projects/{projectKey}/repos/{repository}/branches'.format(projectKey=project_key,
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

        url = 'rest/branch-utils/1.0/projects/{project}/repos/{repository}/branches'.format(project=project,
                                                                                            repository=repository)

        data = {"name": str(name), "endPoint": str(end_point)}
        return self.delete(url, data=data)

    def get_pull_requests(self, project, repository, state='OPEN', order='newest', limit=100, start=0):
        """
        Get pull requests
        :param project:
        :param repository:
        :param state:
        :param order: OPTIONAL: defaults to NEWEST) the order to return pull requests in, either OLDEST
                                (as in: "oldest first") or NEWEST.
        :param limit:
        :param start:
        :return:
        """
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/pull-requests'.format(project=project,
                                                                                        repository=repository)
        params = {}
        if state:
            params['state'] = state
        if limit:
            params['limit'] = limit
        if start:
            params['start'] = start
        if order:
            params['order'] = order
        response = self.get(url, params=params)
        if 'values' not in response:
            return []
        pr_list = (response or {}).get('values')
        while not response.get('isLastPage'):
            start = response.get('nextPageStart')
            params['start'] = start
            response = self.get(url, params=params)
            pr_list += (response or {}).get('values')
        return pr_list

    def get_pull_requests_activities(self, project, repository, pull_request_id):
        """
        Get pull requests activities
        :param project:
        :param repository:
        :param pull_request_id: the ID of the pull request within the repository
        :return:
        """
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}/activities'.format(
            project=project,
            repository=repository,
            pullRequestId=pull_request_id)
        params = {'start': 0}
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
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}/changes'.format(
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
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}/commits'.format(
            project=project,
            repository=repository,
            pullRequestId=pull_request_id)
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

    def add_pull_request_comment(self, project, repository, pull_request_id, text):
        """
        Add comment into pull request
        :param project:
        :param repository:
        :param pull_request_id: the ID of the pull request within the repository
        :param text comment text
        :return:
        """
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}/comments'.format(
            project=project,
            repository=repository,
            pullRequestId=pull_request_id)
        body = {'text': text}
        return self.post(url, data=body)

    def get_pullrequest(self, project, repository, pull_request_id):
        """
        Retrieve a pull request.
        The authenticated user must have REPO_READ permission
        for the repository that this pull request targets to call this resource.
        :param project:
        :param repository:
        :param pull_request_id: the ID of the pull request within the repository
        :return:
        """
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}'.format(project=project,
                                                                                                        repository=repository,
                                                                                                        pullRequestId=pull_request_id)
        return self.get(url)

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
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/tags'.format(project=project,
                                                                               repository=repository)
        params = {}
        if start:
            params['start'] = start
        if limit:
            params['limit'] = limit
        if filter:
            params['filter'] = filter
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
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/tags'.format(project=project,
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
        url = 'rest/git/1.0/projects/{project}/repos/{repository}/tags/{tag}'.format(project=project,
                                                                                     repository=repository,
                                                                                     tag=tag_name)
        return self.delete(url)

    def get_diff(self, project, repository, path, hash_oldest, hash_newest):
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/compare/diff/{path}'.format(project=project,
                                                                                              repository=repository,
                                                                                              path=path)
        params = {}
        if hash_oldest:
            params['from'] = hash_oldest
        if hash_newest:
            params['to'] = hash_newest
        return (self.get(url, params=params) or {}).get('diffs')

    def get_commits(self, project, repository, hash_oldest, hash_newest, limit=99999):
        """
        Get commit list from repo
        :param project:
        :param repository:
        :param hash_oldest:
        :param hash_newest:
        :param limit: OPTIONAL: The limit of the number of commits to return, this may be restricted by
               fixed system limits. Default by built-in method: 99999
        :return:
        """
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/commits'.format(project=project,
                                                                                  repository=repository)
        params = {}
        if hash_oldest:
            params['since'] = hash_oldest
        if hash_newest:
            params['until'] = hash_newest
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
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/commits/{commitId}'.format(project=project,
                                                                                             repository=repository,
                                                                                             commitId=commit)
        params = {}
        if path:
            params['path'] = path
        return self.get(url, params=params)

    def get_pull_requests_contain_commit(self, project, repository, commit):
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/commits/{commitId}/pull-requests'.format(
            project=project,
            repository=repository,
            commitId=commit)
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
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/compare/commits'.format(project=project,
                                                                                          repository=repository)
        params = {}
        if ref_from:
            params['from'] = ref_from
        if ref_to:
            params['to'] = ref_to
        if limit:
            params['limit'] = limit
        return (self.get(url, params=params) or {}).get('values')

    def get_file_list(self, project, repository, query, limit=100000):
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
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/files'.format(project=project,
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

    def get_branches_permissions(self, project, repository, limit=25):
        """
        Get branches permissions from a given repo
        :param project:
        :param repository:
        :param limit:
        :return:
        """
        url = 'rest/branch-permissions/2.0/projects/{project}/repos/{repository}/restrictions'.format(project=project,
                                                                                                      repository=repository)
        params = {}
        if limit:
            params['limit'] = limit
        return self.get(url, params=params)

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
        url = 'rest/api/1.0/projects/{project}/repos/{repository}'.format(project=project,
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
        url = 'rest/api/1.0/admin/license'
        return self.get(url)

    def get_mail_configuration(self):
        """
        Retrieves the current mail configuration.
        The authenticated user must have the SYS_ADMIN permission to call this resource.
        :return:
        """
        url = 'rest/api/1.0/admin/mail-server'
        return self.get(url)

    def get_mail_sender_address(self):
        """
        Retrieves the server email address
        :return:
        """
        url = 'rest/api/1.0/admin/mail-server/sender-address'
        return self.get(url)

    def remove_mail_sender_address(self):
        """
        Clears the server email address.
        The authenticated user must have the ADMIN permission to call this resource.
        :return:
        """
        url = 'rest/api/1.0/admin/mail-server/sender-address'
        return self.delete(url)

    def get_ssh_settings(self):
        """
        Retrieve ssh settings for user
        :return:
        """
        url = 'rest/ssh/1.0/settings'
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
