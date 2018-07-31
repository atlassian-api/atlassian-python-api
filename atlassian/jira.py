# coding: utf8
import logging
from requests.exceptions import HTTPError
from .rest_client import AtlassianRestAPI

log = logging.getLogger('atlassian.jira')


class Jira(AtlassianRestAPI):
    def reindex_status(self):
        return self.get('rest/api/2/reindex')

    def reindex(self):
        return self.post('rest/api/2/reindex')

    def jql(self, jql, fields='*all', start=0, limit=None):
        """
        Get issues from jql search result with all related fields
        :param jql:
        :param fields:
        :param start: OPTIONAL: The start point of the collection to return. Default: 0.
        :param limit: OPTIONAL: The limit of the number of issues to return, this may be restricted by
                fixed system limits. Default by built-in method: 50
        :return:
        """
        params = {}
        if start is not None:
            params["startAt"] = int(start)
        if limit is not None:
            params["maxResults"] = int(limit)
        if fields is not None:
            params["fields"] = fields
        if jql is not None:
            params['jql'] = jql
        return self.get('rest/api/2/search', params=params)

    def user(self, username):
        return self.get('rest/api/2/user?username={0}'.format(username))

    def user_remove(self, username):
        """
        Remove user from Jira if this user does not have any activity
        :param username:
        :return:
        """
        return self.delete('rest/api/2/user?username={0}'.format(username))

    def user_deactivate(self, username):
        """
        Disable user
        :param username:
        :return:
        """
        url = 'secure/admin/user/EditUser.jspa'
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Atlassian-Token': 'no-check'}
        user = self.user(username)
        user_update_info = {
            'inline': 'true',
            'decorator': 'dialog',
            'username': user['name'],
            'fullName': user['displayName'],
            'email': user['emailAddress'],
            'editName': user['name']
        }
        return self.post(data=user_update_info, path=url, headers=headers)

    def user_disable(self, username):
        """Override the disable method"""
        return self.user_deactivate(self, username)

    def user_disable_throw_rest_endpoint(self, username, url='/rest/scriptrunner/latest/custom/disableUser',
                                         param='userName'):
        """The disable method throw own rest enpoint"""
        url = "{}?{}={}".format(url, param, username)
        return self.get(path=url)

    def user_get_websudo(self):
        url = 'secure/admin/WebSudoAuthenticate.jspa'
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'X-Atlassian-Token': 'no-check'
                   }
        data = {
            'webSudoPassword': self.password,
        }
        return self.post(path=url, data=data, headers=headers)

    def user_find_by_user_string(self, username, start=0, limit=50, include_inactive_users=False):
        """
        Fuzzy search using username and display name
        :param username:
        :param start: OPTIONAL: The start point of the collection to return. Default: 0.
        :param limit: OPTIONAL: The limit of the number of users to return, this may be restricted by
                fixed system limits. Default by built-in method: 50
        :param include_inactive_users:
        :return:
        """
        url = "rest/api/2/user/search"
        url += "?username={username}&includeInactive={include_inactive}&startAt={start}&maxResults={limit}".format(
            username=username, include_inactive=include_inactive_users, start=start, limit=limit)
        return self.get(url)

    def projects(self):
        return self.get('rest/api/2/project')

    def project(self, key):
        return self.get('rest/api/2/project/{0}'.format(key))

    def get_project_components(self, key):
        """
        Get project components using project key
        :param key: str
        :return:
        """
        return self.get('rest/api/2/project/{0}/components'.format(key))

    def issue(self, key, fields='*all'):
        return self.get('rest/api/2/issue/{0}?fields={1}'.format(key, fields))

    def issue_field_value(self, key, field):
        issue = self.get('rest/api/2/issue/{0}?fields={1}'.format(key, field))
        return issue['fields'][field]

    def update_issue_field(self, key, fields='*all'):
        return self.put('rest/api/2/issue/{0}'.format(key), data={'fields': fields})

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
        return self.put('rest/greenhopper/1.0/sprint/{0}'.format(sprint_id), data={
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

    def get_all_assignable_users_for_project(self, project_key, start=0, limit=50):
        """
        Provide assignable users for project
        :param project_key:
        :param start: OPTIONAL: The start point of the collection to return. Default: 0.
        :param limit: OPTIONAL: The limit of the number of users to return, this may be restricted by
                fixed system limits. Default by built-in method: 50
        :return:
        """
        url = "rest/api/2/user/assignable/search?project={project_key}&startAt={start}&maxResults={limit}".format(
            project_key=project_key,
            start=start,
            limit=limit)
        return self.get(url)

    def get_all_users_from_group(self, group, include_inactive_users=False, start=0, limit=50):
        """
        Just wrapping method user group members
        :param group:
        :param include_inactive_users:
        :param start: OPTIONAL: The start point of the collection to return. Default: 0.
        :param limit: OPTIONAL: The limit of the number of users to return, this may be restricted by
                fixed system limits. Default by built-in method: 50
        :return:
        """
        url = "rest/api/2/group/member"
        url += "?groupname={group}&includeInactiveUsers={include_inactive}&startAt={start}&maxResults={limit}".format(
            group=group, include_inactive=include_inactive_users, start=start, limit=limit)
        return self.get(url)

    def issue_exists(self, issue_key):
        try:
            self.issue(issue_key, fields='*none')
            log.info('Issue "{issue_key}" exists'.format(issue_key=issue_key))
            return True
        except HTTPError as e:
            if e.response.status_code == 404:
                log.info('Issue "{issue_key}" does not exists'.format(issue_key=issue_key))
                return False
            else:
                log.info('Issue "{issue_key}" existed, but now it\'s deleted'.format(issue_key=issue_key))
                return True

    def issue_deleted(self, issue_key):
        try:
            self.issue(issue_key, fields='*none')
            log.info('Issue "{issue_key}" is not deleted'.format(issue_key=issue_key))
            return False
        except HTTPError:
            log.info('Issue "{issue_key}" is deleted'.format(issue_key=issue_key))
            return True

    def issue_update(self, issue_key, fields):
        log.warning('Updating issue "{issue_key}" with "{fields}"'.format(issue_key=issue_key, fields=fields))
        url = 'rest/api/2/issue/{0}'.format(issue_key)
        return self.put(url, data={'fields': fields})

    def issue_create(self, fields):
        log.warning('Creating issue "{summary}"'.format(summary=fields['summary']))
        url = 'rest/api/2/issue/'
        return self.post(url, data={'fields': fields})

    def issue_create_or_update(self, fields):
        issue_key = fields.get('issuekey', None)

        if not issue_key or not self.issue_exists(issue_key):
            log.info('IssueKey is not provided or does not exists in destination. Will attempt to create an issue')
            del fields['issuekey']
            return self.issue_create(fields)

        if self.issue_deleted(issue_key):
            log.warning('Issue "{issue_key}" deleted, skipping'.format(issue_key=issue_key))
            return None

        log.info('Issue "{issue_key}" exists, will update'.format(issue_key=issue_key))
        del fields['issuekey']
        return self.issue_update(issue_key, fields)

    def get_issue_transitions(self, issue_key):
        url = 'rest/api/2/issue/{issue_key}?expand=transitions.fields&fields=status'.format(issue_key=issue_key)
        return [{'name': transition['name'], 'id': int(transition['id']), 'to': transition['to']['name']}
                for transition in self.get(url)['transitions']]

    def get_status_id_from_name(self, status_name):
        url = 'rest/api/2/status/{name}'.format(name=status_name)
        return int(self.get(url)['id'])

    def get_transition_id_to_status_name(self, issue_key, status_name):
        for transition in self.get_issue_transitions(issue_key):
            if status_name.lower() == transition['to'].lower():
                return int(transition['id'])

    def issue_transition(self, issue_key, status):
        return self.set_issue_status(issue_key, status)

    def set_issue_status(self, issue_key, status_name):
        url = 'rest/api/2/issue/{issue_key}/transitions'.format(issue_key=issue_key)
        transition_id = self.get_transition_id_to_status_name(issue_key, status_name)
        return self.post(url, data={'transition': {'id': transition_id}})

    def get_issue_status(self, issue_key):
        url = 'rest/api/2/issue/{issue_key}?fields=status'.format(issue_key=issue_key)
        return self.get(url)['fields']['status']['name']

    def component(self, component_id):
        return self.get('rest/api/2/component/{component_id}'.format(component_id=component_id))

    def create_component(self, component):
        log.warning('Creating component "{name}"'.format(name=component['name']))
        url = 'rest/api/2/component/'
        return self.post(url, data=component)

    def delete_component(self, component_id):
        log.warning('Deleting component "{component_id}"'.format(component_id=component_id))
        return self.delete('rest/api/2/component/{component_id}'.format(component_id=component_id))
