# coding: utf8
import logging
from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Bitbucket(AtlassianRestAPI):
    def project_list(self):
        """
        Provide the project list
        :return:
        """
        return (self.get('rest/api/1.0/projects') or {}).get('values')

    def project(self, key):
        """
        Provide project info
        :param key:
        :return:
        """
        url = 'rest/api/1.0/projects/{0}'.format(key)
        return (self.get(url) or {}).get('values')

    def project_users(self, key, limit=99999):
        """
        Get users who has permission in project
        :param key:
        :param limit: OPTIONAL: The limit of the number of users to return, this may be restricted by
                            fixed system limits. Default by built-in method: 99999
        :return:
        """
        url = 'rest/api/1.0/projects/{key}/permissions/users'.format(key=key)
        params = {}
        if limit:
            params['limit'] = limit
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

    def project_groups(self, key, limit=99999):
        """
        Get Project Groups
        :param key:
        :param limit: OPTIONAL: The limit of the number of groups to return, this may be restricted by
                            fixed system limits. Default by built-in method: 99999
        :return:
        """
        url = 'rest/api/1.0/projects/{key}/permissions/groups'.format(key=key)
        params = {}
        if limit:
            params['limit'] = limit
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

    def repo_list(self, project_key, limit=25):
        """
        Get repositories list from project
        :param project_key:
        :param limit: OPTIONAL: The limit of the number of repositories to return, this may be restricted by
                        fixed system limits. Default by built-in method: 25
        :return:
        """
        url = 'rest/api/1.0/projects/{projectKey}/repos'.format(projectKey=project_key)
        params = {}
        if limit:
            params['limit'] = limit
        return (self.get(url, params=params) or {}).get('values')

    def get_branches(self, project, repository, base=None, filter=None, start=0, limit=99999, details=True,
                     order_by='MODIFICATION'):
        """
        Retrieve the branches matching the supplied filterText param.
        The authenticated user must have REPO_READ permission for the specified repository to call this resource.
        :param start:
        :param project:
        :param repository:
        :param base: base branch or tag to compare each branch to (for the metadata providers that uses that information)
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
        url = '/api/1.0/projects/{project}/repos/{repository}/pull-requests'.format(project=project,
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
        return (self.get(url, params=params) or {}).get('values')

    def get_pullrequest(self, project, repository, pull_request_Id):
        """
        Retrieve a pull request.
        The authenticated user must have REPO_READ permission
        for the repository that this pull request targets to call this resource.
        :param project:
        :param repository:
        :param pull_request_Id: the ID of the pull request within the repository
        :return:
        """
        url = 'rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pullRequestId}'.format(project=project,
                                                                                                        repository=repository,
                                                                                                        pullRequestId=pull_request_Id)
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
