import logging
from atlassian import AtlassianRestAPI


logging.basicConfig(level=logging.INFO, format="[%(asctime).19s] [%(levelname)s] %(message)s")
logging.getLogger("requests").setLevel(logging.WARNING)
log = logging.getLogger("atlassian.stash")


class Stash(AtlassianRestAPI):

    def project_list(self):
        return self.get('/rest/api/1.0/projects')['values']

    def project(self, key):
        return self.get('/rest/api/1.0/projects/{}'.format(key))['values']

    def project_users(self, key):
        return self.get('/rest/api/1.0/projects/{}/permissions/users?limit=99999'.format(key))['values']

    def project_users_with_administrator_permissions(self, key):
        project_administrators = [user['user'] for user in self.project_users(key) if user['permission'] == 'PROJECT_ADMIN']

        for group in self.project_groups_with_administrator_permissions(key):
            for user in self.group_members(group):
                project_administrators.append(user)

        return project_administrators

    def project_groups(self, key):
        return self.get('/rest/api/1.0/projects/{}/permissions/groups?limit=99999'.format(key))['values']

    def project_groups_with_administrator_permissions(self, key):
        return [group['group']['name'] for group in self.project_groups(key) if group['permission'] == 'PROJECT_ADMIN']

    def project_summary(self, key):
        return {
            'key': key,
            'data': self.project(key),
            'users': self.project_users(key),
            'groups': self.project_groups(key)}

    def group_members(self, group):
        return self.get('/rest/api/1.0/admin/groups/more-members?context={}&limit=99999'.format(group))['values']

    def all_project_administrators(self):
        for project in self.project_list():
            log.info("Processing project: {0} - {1}".format(project['key'], project['name']))
            yield {
                'project_key': project['key'],
                'project_name': project['name'],
                'project_administrators': [{'email': x['emailAddress'], 'name': x['displayName']} for x in self.project_users_with_administrator_permissions(project['key'])]}
