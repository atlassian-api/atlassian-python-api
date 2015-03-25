import logging
from atlassian import AtlassianRestAPI


log = logging.getLogger('atlassian.stash')


class Stash(AtlassianRestAPI):

    def project_list(self):
        return self.get('/rest/api/1.0/projects')['values']

    def project(self, key):
        url = '/rest/api/1.0/projects/{0}'.format(key)
        return self.get(url)['values']

    def project_users(self, key, limit=99999):
        url = '/rest/api/1.0/projects/{key}/permissions/users?limit={limit}'.format(key=key, limit=limit)
        return self.get(url)['values']

    def project_users_with_administrator_permissions(self, key):
        project_administrators = [user['user'] for user in self.project_users(key)
                                  if user['permission'] == 'PROJECT_ADMIN']
        for group in self.project_groups_with_administrator_permissions(key):
            for user in self.group_members(group):
                project_administrators.append(user)
        return project_administrators

    def project_groups(self, key, limit=99999):
        url = '/rest/api/1.0/projects/{key}/permissions/groups?limit={limit}'.format(key=key, limit=limit)
        return self.get(url)['values']

    def project_groups_with_administrator_permissions(self, key):
        return [group['group']['name'] for group in self.project_groups(key) if group['permission'] == 'PROJECT_ADMIN']

    def project_summary(self, key):
        return {
            'key': key,
            'data': self.project(key),
            'users': self.project_users(key),
            'groups': self.project_groups(key)}

    def group_members(self, group, limit=99999):
        url = '/rest/api/1.0/admin/groups/more-members?context={group}&limit={limit}'.format(group=group, limit=limit)
        return self.get(url)['values']

    def all_project_administrators(self):
        for project in self.project_list():
            log.info('Processing project: {0} - {1}'.format(project['key'], project['name']))
            yield {
                'project_key': project['key'],
                'project_name': project['name'],
                'project_administrators': [{'email': x['emailAddress'], 'name': x['displayName']}
                                           for x in self.project_users_with_administrator_permissions(project['key'])]}

    def get_branches(self, project, repository, filter='', limit=99999):
        url = '/rest/api/1.0/projects/{project}/repos/{repository}/branches?limit={limit}&filterText={filter}'.format(
            project=project,
            repository=repository,
            limit=limit,
            filter=filter)
        return self.get(url)['values']

    def get_tags(self, project, repository, filter='', limit=99999):
        url = '/rest/api/1.0/projects/{project}/repos/{repository}/tags?limit={limit}&filterText={filter}'.format(
            project=project,
            repository=repository,
            limit=limit,
            filter=filter)
        return self.get(url)['values']

    def get_diff(self, project, repository, path, hash_oldest, hash_newest):
        url = '/rest/api/1.0/projects/{project}/repos/{repository}/compare/diff/{path}?from={hash_oldest}&to={hash_newest}'.format(
            project=project,
            repository=repository,
            path=path,
            hash_oldest=hash_oldest,
            hash_newest=hash_newest)
        return self.get(url)['diffs']

    def get_commits(self, project, repository, hash_oldest, hash_newest, limit=99999):
        url = '/rest/api/1.0/projects/{project}/repos/{repository}/commits?since={hash_oldest}&until={hash_newest}&limit={limit}'.format(
            project=project,
            repository=repository,
            hash_from=hash_oldest,
            hash_to=hash_newest,
            limit=limit)
        return self.get(url)['values']

    def get_changelog(self, project, repository, ref_from, ref_to, limit=99999):
        url = '/rest/api/1.0/projects/{project}/repos/{repository}/compare/commits?from={ref_from}&to={ref_to}&limit={limit}'.format(
            project=project,
            repository=repository,
            ref_from=ref_from,
            ref_to=ref_to,
            limit=limit)
        return self.get(url)['values']
