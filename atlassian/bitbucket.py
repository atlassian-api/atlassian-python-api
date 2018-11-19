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
        url = 'rest/api/1.0/projects/{key}/permissions/users?limit={limit}'.format(key=key, limit=limit)
        return (self.get(url) or {}).get('values')

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
        url = 'rest/api/1.0/projects/{key}/permissions/groups?limit={limit}'.format(key=key, limit=limit)
        return (self.get(url) or {}).get('values')

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
        url = 'rest/api/1.0/admin/groups/more-members?context={group}&limit={limit}'.format(group=group, limit=limit)
        return (self.get(url) or {}).get('values')

    def all_project_administrators(self):
        for project in self.project_list():
            log.info('Processing project: {0} - {1}'.format(project['key'], project['name']))
            yield {
                'project_key': project['key'],
                'project_name': project['name'],
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
        url = 'rest/api/1.0/projects/{projectKey}/repos?limit={limit}'.format(projectKey=project_key, limit=limit)
        return (self.get(url) or {}).get('values')

    def get_branches(self, project, repository, filter='', limit=99999, details=True):
        """
        Get branches from repo
        :param project:
        :param repository:
        :param filter:
        :param limit: OPTIONAL: The limit of the number of branches to return, this may be restricted by
                    fixed system limits. Default by built-in method: 99999
        :param details:
        :return:
        """
        url = "rest/api/1.0/projects/{project}/repos/{repository}/branches".format(project=project,
                                                                                   repository=repository)
        url += "?limit={limit}&filterText={filter}&details={details}".format(limit=limit,
                                                                             filter=filter,
                                                                             details=details)

        return (self.get(url) or {}).get('values')

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
        :param order:
        :param limit:
        :param start:
        :return:
        """
        url = "rest/api/1.0/projects/{project}/repos/{repository}/pull-requests".format(project=project,
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
        url += '?from={hash_oldest}&to={hash_newest}'.format(hash_oldest=hash_oldest,
                                                             hash_newest=hash_newest)
        return (self.get(url) or {}).get('diffs')

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
        url += '?since={hash_from}&until={hash_to}&limit={limit}'.format(hash_from=hash_oldest,
                                                                         hash_to=hash_newest,
                                                                         limit=limit)
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
        url += '?from={ref_from}&to={ref_to}&limit={limit}'.format(ref_from=ref_from,
                                                                   ref_to=ref_to,
                                                                   limit=limit)
        return (self.get(url) or {}).get('values')

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
        url = "rest/api/1.0/projects/{project}/repos/{repository}/files?at={query}&limit={limit}".format(
            project=project,
            repository=repository,
            query=query,
            limit=limit)

        return (self.get(url) or {}).get('values')

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
        params = {}
        if at is not None:
            params['at'] = at
        if markup is not None:
            params['markup'] = markup
        url = 'projects/{project}/repos/{repository}/raw/{filename}/'.format(project=project,
                                                                             repository=repository,
                                                                             filename=filename)
        return self.get(url, params=params, not_json_response=True, headers=headers)

    def get_branches_permissions(self, project, repository, limit=25):
        """
        Get branches permissions from a given repo
        :param project:
        :param repository:
        :param limit:
        :return:
        """
        url = 'rest/branch-permissions/2.0/projects/{project}/repos/{repository}/restrictions' \
              '?limit={limit}'.format(project=project,
                                      repository=repository,
                                      limit=limit)

        return self.get(url)

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
