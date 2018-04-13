import logging
from requests.exceptions import HTTPError
from .rest_client import AtlassianRestAPI


log = logging.getLogger('atlassian.jira')


class Jira(AtlassianRestAPI):

    def reindex_status(self):
        return self.get('/rest/api/2/reindex')

    def reindex(self):
        return self.post('/rest/api/2/reindex')

    def jql(self, jql, fields='*all', limit=999999):
        return self.get('/rest/api/2/search?maxResults={limit}&fields={fields}&jql={jql}'.format(
            limit=limit,
            fields=fields,
            jql=jql))

    def user(self, username):
        return self.get('/rest/api/2/user?username={0}'.format(username))

    def projects(self):
        return self.get('/rest/api/2/project')

    def project(self, key):
        return self.get('/rest/api/2/project/{0}'.format(key))

    def get_project_components(self, key):
        return self.get('/rest/api/2/project/{0}/components'.format(key))

    def issue(self, key, fields='*all'):
        return self.get('/rest/api/2/issue/{0}?fields={1}'.format(key, fields))

    def issue_field_value(self, key, field):
        issue = self.get('/rest/api/2/issue/{0}?fields={1}'.format(key, field))
        return issue['fields'][field]

    def update_issue_field(self, key, fields='*all'):
        return self.put('/rest/api/2/issue/{0}'.format(key), data={'fields': fields})

    def project_leaders(self):
        for project in self.projects():
            key = project['key']
            project_data = self.project(key)
            lead = self.user(project_data['lead']['name'])
            yield {
                'project_key': key,
                'project_name': project['name'],
                'lead_name': lead['displayName'],
                'lead_key': lead['name'],
                'lead_email': lead['emailAddress']}

    def rename_sprint(self, sprint_id, name, start_date, end_date):
        return self.put('/rest/greenhopper/1.0/sprint/{0}'.format(sprint_id), data={
            'name': name,
            'startDate': start_date,
            'endDate': end_date})

    def get_project_issuekey_last(self, project):
        jql = 'project = {project} ORDER BY issuekey DESC'.format(project=project)
        return self.jql(jql)['issues'][0]['key']

    def get_project_issuekey_all(self, project):
        jql = 'project = {project} ORDER BY issuekey ASC'.format(project=project)
        return [issue['key'] for issue in self.jql(jql)['issues']]

    def get_project_issues_count(self, project):
        jql = 'project = {project}'.format(project=project)
        return self.jql(jql, fields='*none')['total']

    def get_all_project_issues(self, project, fields='*all'):
        jql = 'project = {project} ORDER BY key'.format(project=project)
        return self.jql(jql, fields=fields)['issues']

    def issue_exists(self, issuekey):
        try:
            self.issue(issuekey, fields='*none')
            log.info('Issue "{issuekey}" exists'.format(issuekey=issuekey))
            return True
        except HTTPError as e:
            if e.response.status_code == 404:
                log.info('Issue "{issuekey}" does not exists'.format(issuekey=issuekey))
                return False
            else:
                log.info('Issue "{issuekey}" existsted, but now it\'s deleted'.format(issuekey=issuekey))
                return True

    def issue_deleted(self, issuekey):
        try:
            self.issue(issuekey, fields='*none')
            log.info('Issue "{issuekey}" is not deleted'.format(issuekey=issuekey))
            return False
        except HTTPError:
            log.info('Issue "{issuekey}" is deleted'.format(issuekey=issuekey))
            return True

    def issue_update(self, issuekey, fields):
        log.warning('Updating issue "{issuekey}" with "{summary}"'.format(issuekey=issuekey, summary=fields['summary']))
        url = '/rest/api/2/issue/{0}'.format(issuekey)
        return self.put(url, data={'fields': fields})

    def issue_create(self, fields):
        log.warning('Creating issue "{summary}"'.format(summary=fields['summary']))
        url = '/rest/api/2/issue/'
        return self.post(url, data={'fields': fields})

    def issue_create_or_update(self, fields):
        issuekey = fields.get('issuekey', None)

        if not issuekey or not self.issue_exists(issuekey):
            log.info('Issuekey is not provided or does not exists in destination. Will attempt to create an issue')
            del fields['issuekey']
            return self.issue_create(fields)

        if self.issue_deleted(issuekey):
            log.warning('Issue "{issuekey}" deleted, skipping'.format(issuekey=issuekey))
            return None

        log.info('Issue "{issuekey}" exists, will update'.format(issuekey=issuekey))
        del fields['issuekey']
        return self.issue_update(issuekey, fields)

    def get_issue_transitions(self, issuekey):
        url = '/rest/api/2/issue/{issuekey}?expand=transitions.fields&fields=status'.format(issuekey=issuekey)
        return [{'name': transition['name'], 'id': int(transition['id']), 'to': transition['to']['name']}
                for transition in self.get(url)['transitions']]

    def get_status_id_from_name(self, status_name):
        url = '/rest/api/2/status/{name}'.format(name=status_name)
        return int(self.get(url)['id'])

    def get_transition_id_to_status_name(self, issuekey, status_name):
        for transition in self.get_issue_transitions(issuekey):
            if status_name.lower() == transition['to'].lower():
                return int(transition['id'])

    def issue_transition(self, issuekey, status):
        return self.set_issue_status(issuekey, status)

    def set_issue_status(self, issuekey, status_name):
        url = '/rest/api/2/issue/{issuekey}/transitions'.format(issuekey=issuekey)
        transition_id = self.get_transition_id_to_status_name(issuekey, status_name)
        return self.post(url, data={'transition': {'id': transition_id}})

    def get_issue_status(self, issuekey):
        url = '/rest/api/2/issue/{issuekey}?fields=status'.format(issuekey=issuekey)
        return self.get(url)['fields']['status']['name']

    def component(self, componentid):
        return self.get('/rest/api/2/component/{componentid}'.format(componentid=componentid))

    def create_component(self, component):
        log.warning('Creating component "{name}"'.format(name=component['name']))
        url = '/rest/api/2/component/'
        return self.post(url, data=component)

    def delete_component(self, componentid):
        log.warning('Deleting component "{componentid}"'.format(componentid=componentid))
        return self.delete('/rest/api/2/component/{componentid}'.format(componentid=componentid))
