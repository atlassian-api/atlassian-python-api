# coding: utf8
import logging
from requests.exceptions import HTTPError
from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Jira(AtlassianRestAPI):
    def reindex_status(self):
        return self.get('rest/api/2/reindex')

    def reindex(self, comments=True, change_history=True, worklogs=True):
        """
        Reindex the Jira instance
        Kicks off a reindex. Need Admin permissions to perform this reindex.
        :param comments: Indicates that comments should also be reindexed. Not relevant for foreground reindex,
        where comments are always reindexed.
        :param change_history: Indicates that changeHistory should also be reindexed.
        Not relevant for foreground reindex, where changeHistory is always reindexed.
        :param worklogs: Indicates that changeHistory should also be reindexed.
        Not relevant for foreground reindex, where changeHistory is always reindexed.
        :return:
        """
        params = {}
        if not comments:
            params['indexComments'] = comments
        if not change_history:
            params['indexChangeHistory'] = change_history
        if not worklogs:
            params['indexWorklogs'] = worklogs
        return self.post('rest/api/2/reindex', params=params)

    def reindex_with_type(self, indexing_type="BACKGROUND_PREFERRED"):
        """
        Reindex the Jira instance
        Type of re-indexing available:
        FOREGROUND - runs a lock/full reindexing
        BACKGROUND - runs a background reindexing.
                   If Jira fails to finish the background reindexing, respond with 409 Conflict (error message).
        BACKGROUND_PREFERRED  - If possible do a background reindexing.
                   If it's not possible (due to an inconsistent index), do a foreground reindexing.
        :param indexing_type: OPTIONAL: The default value for the type is BACKGROUND_PREFFERED
        :return:
        """
        return self.post('rest/api/2/reindex?type={}'.format(indexing_type))

    def reindex_project(self, project_key):
        return self.post('secure/admin/IndexProject.jspa', data='confirmed=true&key={}'.format(project_key),
                         headers=self.form_token_headers)

    def reindex_issue(self, list_of_):
        pass

    def jql(self, jql, fields='*all', start=0, limit=None):
        """
        Get issues from jql search result with all related fields
        :param jql:
        :param fields: list of fields, for example: ['priority', 'summary', 'customfield_10007']
        :param start: OPTIONAL: The start point of the collection to return. Default: 0.
        :param limit: OPTIONAL: The limit of the number of issues to return, this may be restricted by
                fixed system limits. Default by built-in method: 50
        :return:
        """
        params = {}
        if start is not None:
            params['startAt'] = int(start)
        if limit is not None:
            params['maxResults'] = int(limit)
        if fields is not None:
            if isinstance(fields, (list, tuple, set)):
                fields = ','.join(fields)
            params['fields'] = fields
        if jql is not None:
            params['jql'] = jql
        return self.get('rest/api/2/search', params=params)

    def csv(self, jql, limit=1000):
        """
        Get issues from jql search result with all related fields
        :param jql: JQL query
        :param limit: max results in the output file
        :return: CSV file
        """
        url = 'sr/jira.issueviews:searchrequest-csv-all-fields/temp/SearchRequest.csv?tempMax={limit}&jqlQuery={jql}'.format(
            limit=limit, jql=jql)
        return self.get(url, not_json_response=True, headers={'Accept': 'application/csv'})

    def user(self, username):
        return self.get('rest/api/2/user?username={0}'.format(username))

    def user_remove(self, username):
        """
        Remove user from Jira if this user does not have any activity
        :param username:
        :return:
        """
        return self.delete('rest/api/2/user?username={0}'.format(username))

    def user_update(self, username, data):
        """
        Update user attributes based on json
        :param username:
        :param data:
        :return:
        """
        url = 'rest/api/2/user?username={0}'.format(username)
        return self.put(url, data=data)

    def user_update_email(self, username, email):
        """
        Update user email for new domain changes
        :param username:
        :param email:
        :return:
        """
        data = {'name': username, 'emailAddress': email}
        return self.user_update(username, data=data)

    def user_deactivate(self, username):
        """
        Disable user
        :param username:
        :return:
        """
        url = 'secure/admin/user/EditUser.jspa'
        headers = self.form_token_headers
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
        return self.user_deactivate(username)

    def user_disable_throw_rest_endpoint(self, username, url='rest/scriptrunner/latest/custom/disableUser',
                                         param='userName'):
        """The disable method throw own rest enpoint"""
        url = "{}?{}={}".format(url, param, username)
        return self.get(path=url)

    def user_get_websudo(self):
        """ Get web sudo cookies using normal http request"""
        url = 'secure/admin/WebSudoAuthenticate.jspa'
        headers = self.form_token_headers
        data = {
            'webSudoPassword': self.password,
        }
        return self.post(path=url, data=data, headers=headers)

    def user_find_by_user_string(self, username, start=0, limit=50, include_inactive_users=False,
                                 include_active_users=True):
        """
        Fuzzy search using username and display name
        :param username: Use '.' to find all users
        :param start: OPTIONAL: The start point of the collection to return. Default: 0.
        :param limit: OPTIONAL: The limit of the number of users to return, this may be restricted by
                fixed system limits. Default by built-in method: 50
        :param include_inactive_users: OPTIONAL: Return users with "active: False"
        :param include_active_users: OPTIONAL: Return users with "active: True".
        :return:
        """
        url = 'rest/api/2/user/search'
        params = {'username': username,
                  'includeActive': include_active_users,
                  'includeInactive': include_inactive_users,
                  'startAt': start,
                  'maxResults': limit
                  }
        return self.get(url, params=params)

    def projects(self, included_archived=None):
        """Returns all projects which are visible for the currently logged in user.
        If no user is logged in, it returns the list of projects that are visible when using anonymous access.
        :param included_archived: boolean whether to include archived projects in response, default: false
        :return:
        """
        params = {}
        if included_archived:
            params['includeArchived'] = included_archived
        return self.get('rest/api/2/project')

    def get_all_projects(self, included_archived=None):
        return self.projects(included_archived)

    def project(self, key):
        return self.get('rest/api/2/project/{0}'.format(key))

    def delete_project(self, key):
        """
        DELETE /rest/api/2/project/<project_key>
        :param key: str
        :return:
        """
        return self.delete('rest/api/2/project/{0}'.format(key))

    def get_project_components(self, key):
        """
        Get project components using project key
        :param key: str
        :return:
        """
        return self.get('rest/api/2/project/{0}/components'.format(key))

    def get_project_versions(self, key, expand=None):
        """
        Contains a full representation of a the specified project's versions.
        :param key:
        :param expand: the parameters to expand
        :return:
        """
        params = {}
        if expand is not None:
            params['expand'] = expand
        return self.get('rest/api/2/project/{}/versions'.format(key), params=params)

    def get_project_versions_paginated(self, key, start=None, limit=None, order_by=None, expand=None):
        """
        Returns all versions for the specified project. Results are paginated.
        Results can be ordered by the following fields:
            sequence
            name
            startDate
            releaseDate
        :param key: the project key or id
        :param start: the page offset, if not specified then defaults to 0
        :param limit: how many results on the page should be included. Defaults to 50.
        :param order_by: ordering of the results.
        :param expand: the parameters to expand
        :return:
        """
        params = {}
        if start is not None:
            params['startAt'] = int(start)
        if limit is not None:
            params['maxResults'] = int(limit)
        if order_by is not None:
            params['orderBy'] = order_by
        if expand is not None:
            params['expand'] = expand
        return self.get('rest/api/2/project/{}/version'.format(key), params)

    def get_project_roles(self, project_key):
        """
        Provide associated project roles
        :param project_key:
        :return:
        """
        return self.get('rest/api/2/project/{0}/role'.format(project_key))

    def get_project_actors_for_role_project(self, project_key, role_id):
        """
        Returns the details for a given project role in a project.
        :param project_key:
        :param role_id:
        :return:
        """
        url = 'rest/api/2/project/{projectIdOrKey}/role/{id}'.format(projectIdOrKey=project_key,
                                                                     id=role_id)
        return (self.get(url) or {}).get('actors')

    def delete_project_actors(self, project_key, role_id, actor, actor_type=None):
        """
        Deletes actors (users or groups) from a project role.
        Delete a user from the role: /rest/api/2/project/{projectIdOrKey}/role/{roleId}?user={username}
        Delete a group from the role: /rest/api/2/project/{projectIdOrKey}/role/{roleId}?group={groupname}
        :param project_key:
        :param role_id:
        :param actor:
        :param actor_type: str : group or user string
        :return:
        """
        url = 'rest/api/2/project/{projectIdOrKey}/role/{roleId}'.format(projectIdOrKey=project_key,
                                                                         roleId=role_id)
        params = {}
        if actor_type is not None and actor_type in ['group', 'user']:
            params[actor_type] = actor
        return self.delete(url, params=params)

    def add_project_actor_in_role(self, project_key, role_id, actor, actor_type):
        """

        :param project_key:
        :param role_id:
        :param actor:
        :param actor_type:
        :return:
        """
        url = 'rest/api/2/project/{projectIdOrKey}/role/{roleId}'.format(projectIdOrKey=project_key,
                                                                         roleId=role_id)
        data = {}
        if actor_type in ['group', 'atlassian-group-role-actor']:
            data['group'] = [actor]
        elif actor_type in ['user', 'atlassian-user-role-actor']:
            data['user'] = [actor]

        return self.post(url, data=data)

    def update_project(self, project_key, data, expand=None):
        """
        Updates a project.
        Update project: /rest/api/2/project/{projectIdOrKey}

        :param project_key: project key of project that needs to be updated
        :param data: dictionary containing the data to be updated
        :param expand: the parameters to expand
        """
        if expand:
            url = 'rest/api/2/project/{projectIdOrKey}?expand={expand}'.format(projectIdOrKey=project_key,
                                                                               expand=expand)
        else:
            url = 'rest/api/2/project/{projectIdOrKey}'.format(projectIdOrKey=project_key)
        return self.put(url, data)

    def create_issue_type(self, name, description='', type='standard'):
        """
        Create a new issue type
        :param name:
        :param description:
        :param type: standard or sub-task
        :return:
        """
        data = {
            'name': name,
            'description': description,
            'type': type
        }
        return self.post('rest/api/2/issuetype', data=data)

    def issue(self, key, fields='*all'):
        return self.get('rest/api/2/issue/{0}?fields={1}'.format(key, fields))

    def issue_add_json_worklog(self, key, worklog):
        """

        :param key:
        :param worklog:
        :return:
        """
        url = 'rest/api/2/issue/{}/worklog'.format(key)
        return self.post(url, data=worklog)

    def issue_worklog(self, key, started, time_sec):
        """

        :param key:
        :param time_sec: int: second
        :param started:
        :return:
        """
        data = {
            # "comment": "Work on {}".format(key),
            "started": started,
            "timeSpentSeconds": time_sec
        }
        return self.issue_add_json_worklog(key=key, worklog=data)

    def issue_field_value(self, key, field):
        issue = self.get('rest/api/2/issue/{0}?fields={1}'.format(key, field))
        return issue['fields'][field]

    def update_issue_field(self, key, fields='*all'):
        return self.put('rest/api/2/issue/{0}'.format(key), data={'fields': fields})

    def get_custom_fields(self, search=None, start=1, limit=50):
        """
        Get custom fields. Evaluated on 7.12
        :param search: str
        :param start: long Default: 1
        :param limit: int Default: 50
        :return:
        """
        url = 'rest/api/2/customFields'
        params = {}
        if search:
            params['search'] = search
        if start:
            params['startAt'] = start
        if limit:
            params['maxResults'] = limit
        return self.get(url, params=params)

    def get_all_available_screen_fields(self, screen_id):
        """
        Get all available fields by screen id
        :param screen_id:
        :return:
        """
        url = 'rest/api/2/screens/{}/availableFields'.format(screen_id)
        return self.get(url)

    def get_screen_tabs(self, screen_id):
        """
        Get tabs for the screen id
        :param screen_id:
        :return:
        """
        url = 'rest/api/2/screens/{}/tabs'.format(screen_id)
        return self.get(url)

    def get_screen_tab_fields(self, screen_id, tab_id):
        """
        Get fields by the tab id and the screen id
        :param tab_id:
        :param screen_id:
        :return:
        """
        url = 'rest/api/2/screens/{}/tabs/{}/fields'.format(screen_id, tab_id)
        return self.get(url)

    def get_all_screen_fields(self, screen_id):
        """
        Get all fields by screen id
        :param screen_id:
        :return:
        """
        screen_tabs = self.get_screen_tabs(screen_id)
        fields = []
        for screen_tab in screen_tabs:
            tab_id = screen_tab['id']
            if tab_id:
                tab_fields = self.get_screen_tab_fields(screen_id=screen_id, tab_id=tab_id)
                fields = fields + tab_fields
        return fields

    def get_issue_labels(self, issue_key):
        """
        Get issue labels.
        :param issue_key:
        :return:
        """
        url = 'rest/api/2/issue/{issue_key}?fields=labels'.format(issue_key=issue_key)
        return (self.get(url) or {}).get('fields').get('labels')

    def get_all_fields(self):
        """
        Returns a list of all fields, both System and Custom
        :return: application/jsonContains a full representation of all visible fields in JSON.
        """
        url = 'rest/api/2/field'
        return self.get(url)

    def get_all_custom_fields(self):
        """
        Returns a list of all custom fields
        That method just filtering all fields method
        :return: application/jsonContains a full representation of all visible fields in JSON.
        """
        fields = self.get_all_fields()
        custom_fields = []
        for field in fields:
            if field['custom']:
                custom_fields.append(field)
        return custom_fields

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
        return (self.jql(jql).get('issues') or {})[0]['key']

    def get_project_issuekey_all(self, project):
        jql = 'project = {project} ORDER BY issuekey ASC'.format(project=project)
        return [issue['key'] for issue in self.jql(jql)['issues']]

    def get_project_issues_count(self, project):
        jql = 'project = "{project}" '.format(project=project)
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
        url = 'rest/api/2/user/assignable/search?project={project_key}&startAt={start}&maxResults={limit}'.format(
            project_key=project_key,
            start=start,
            limit=limit)
        return self.get(url)

    def get_groups(self, query=None, exclude=None, limit=20):
        """
        REST endpoint for searching groups in a group picker
        Returns groups with substrings matching a given query. This is mainly for use with the group picker,
        so the returned groups contain html to be used as picker suggestions. The groups are also wrapped
        in a single response object that also contains a header for use in the picker,
        specifically Showing X of Y matching groups.
        The number of groups returned is limited by the system property "jira.ajax.autocomplete.limit"
        The groups will be unique and sorted.
        :param query: str
        :param exclude: str
        :param limit: int
        :return: Returned even if no groups match the given substring
        """
        url = 'rest/api/2/groups/picker'
        params = {}
        if query:
            params['query'] = query
        else:
            params['query'] = ''
        if exclude:
            params['exclude'] = exclude
        if limit:
            params['maxResults'] = limit
        return self.get(url, params=params)

    def create_group(self, name):
        """
        Create a group by given group parameter

        :param name: str
        :return: New group params
        """
        url = 'rest/api/2/group'
        data = {'name': name}

        return self.post(url, data=data)

    def remove_group(self, name, swap_group=None):
        """
        Delete a group by given group parameter
        If you delete a group and content is restricted to that group, the content will be hidden from all users
        To prevent this, use this parameter to specify a different group to transfer the restrictions
        (comments and worklogs only) to

        :param name: str
        :param swap_group: str
        :return:
        """
        log.warning('Removing group...')
        url = 'rest/api/2/group'
        if swap_group is not None:
            params = {'groupname': name, 'swapGroup': swap_group}
        else:
            params = {'groupname': name}

        return self.delete(url, params=params)

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
        url = 'rest/api/2/group/member'
        params = {}
        if group:
            params['groupname'] = group
        params['includeInactiveUsers'] = include_inactive_users
        params['startAt'] = start
        params['maxResults'] = limit
        return self.get(url, params=params)

    def add_user_to_group(self, username, group_name):
        """
        Add given user to a group

        :param username: str
        :param group_name: str
        :return: Current state of the group
        """
        url = 'rest/api/2/group/user'
        params = {'groupname': group_name}
        data = {'name': username}

        return self.post(url, params=params, data=data)

    def remove_user_from_group(self, username, group_name):
        """
        Remove given user from a group

        :param username: str
        :param group_name: str
        :return:
        """
        log.warning('Removing user from a group...')
        url = 'rest/api/2/group/user'
        params = {'groupname': group_name, 'username': username}

        return self.delete(url, params=params)

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

    def issue_add_comment(self, issue_key, comment, visibility=None):
        """
        Add comment into Jira issue
        :param issue_key:
        :param comment:
        :param visibility: OPTIONAL
        :return:
        """
        url = 'rest/api/2/issue/{issueIdOrKey}/comment'.format(issueIdOrKey=issue_key)
        data = {'body': comment}
        if visibility:
            data['visibility'] = visibility
        return self.post(url, data=data)

    def add_attachment(self, issue_key, filename):
        """
        Add attachment to Issue

        :param issue_key: str
        :param filename: str, name, if file in current directory or full path to file
        """
        log.warning('Adding attachment...')
        headers = {'X-Atlassian-Token': 'no-check'}
        with open(filename, 'rb') as file:
            files = {'file': file}
            url = 'rest/api/2/issue/{}/attachments'.format(issue_key)

            return self.post(url, headers=headers, files=files)

    def get_issue_remotelinks(self, issue_key, global_id=None, internal_id=None):
        """
        Compatibility naming method with get_issue_remote_links()
        """
        return self.get_issue_remote_links(issue_key, global_id, internal_id)

    def get_issue_remote_links(self, issue_key, global_id=None, internal_id=None):
        """
        Finding all Remote Links on an issue, also with filtering by Global ID and internal ID
        :param issue_key:
        :param global_id: str
        :param internal_id: str
        :return:
        """
        url = 'rest/api/2/issue/{issue_key}/remotelink'.format(issue_key=issue_key)
        params = {}
        if global_id:
            params['globalId'] = global_id
        if internal_id:
            url += '/' + internal_id
        return self.get(url, params=params)

    def create_or_update_issue_remote_links(self, issue_key, link_url, title, global_id=None, relationship=None):
        """
        Add Remote Link to Issue, update url if global_id is passed
        :param issue_key: str
        :param link_url: str
        :param title: str
        :param global_id: str, OPTIONAL:
        :param relationship: str, OPTIONAL: Default by built-in method: 'Web Link'
        """
        url = 'rest/api/2/issue/{issue_key}/remotelink'.format(issue_key=issue_key)
        data = {'object': {'url': link_url, 'title': title}}
        if global_id:
            data['globalId'] = global_id
        if relationship:
            data['relationship'] = relationship
        return self.post(url, data=data)

    def get_issue_remote_link_by_id(self, issue_key, link_id):
        url = 'rest/api/2/issue/{issue_key}/remotelink/{link_id}'.format(issue_key=issue_key, link_id=link_id)
        return self.get(url)

    def update_issue_remote_link_by_id(self, issue_key, link_id, url, title, global_id=None, relationship=None):
        """
        Update existing Remote Link on Issue
        :param issue_key: str
        :param link_id: str
        :param url: str
        :param title: str
        :param global_id: str, OPTIONAL:
        :param relationship: str, Optional. Default by built-in method: 'Web Link'

        """
        data = {'object': {'url': url, 'title': title}}
        if global_id:
            data['globalId'] = global_id
        if relationship:
            data['relationship'] = relationship
        url = 'rest/api/2/issue/{issue_key}/remotelink/{link_id}'.format(issue_key=issue_key, link_id=link_id)
        return self.put(url, data=data)

    def delete_issue_remote_link_by_id(self, issue_key, link_id):
        """
        Deletes Remote Link on Issue
        :param issue_key: str
        :param link_id: str
        """
        url = 'rest/api/2/issue/{issue_key}/remotelink/{link_id}'.format(issue_key=issue_key, link_id=link_id)
        return self.delete(url)

    def get_issue_transitions(self, issue_key):
        url = 'rest/api/2/issue/{issue_key}?expand=transitions.fields&fields=status'.format(issue_key=issue_key)
        return [{'name': transition['name'], 'id': int(transition['id']), 'to': transition['to']['name']}
                for transition in (self.get(url) or {}).get('transitions')]

    def get_status_id_from_name(self, status_name):
        url = 'rest/api/2/status/{name}'.format(name=status_name)
        return int((self.get(url) or {}).get('id'))

    def get_status_for_project(self, project_key):
        url = 'rest/api/2/project/{name}/statuses'.format(name=project_key)
        return self.get(url)

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
        return (self.get(url) or {}).get('fields').get('status').get('name')

    def get_issue_link_types(self):
        """Returns a list of available issue link types,
        if issue linking is enabled.
        Each issue link type has an id,
        a name and a label for the outward and inward link relationship.
        """
        url = 'rest/api/2/issueLinkType'
        return (self.get(url) or {}).get('issueLinkTypes')

    def get_issue_link_types_names(self):
        """
        Provide issue link type names
        :return:
        """
        return [link_type['name'] for link_type in self.get_issue_link_types()]

    def create_issue_link_type_by_json(self, data):
        """Create a new issue link type.
        :param data:
                {
                    "name": "Duplicate",
                    "inward": "Duplicated by",
                    "outward": "Duplicates"
                }
        :return:
        """
        url = 'rest/api/2/issueLinkType'
        return self.post(url, data=data)

    def create_issue_link_type(self, link_type_name, inward, outward):
        """Create a new issue link type.
        :param outward:
        :param inward:
        :param link_type_name:
        :return:
        """
        if link_type_name.lower() in [x.lower() for x in self.get_issue_link_types_names()]:
            log.error("Link type name already exists")
            return "Link type name already exists"
        data = {
            'name': link_type_name,
            'inward': inward,
            'outward': outward
        }
        return self.create_issue_link_type_by_json(data=data)

    def get_issue_link_type(self, issue_link_type_id):
        """Returns for a given issue link type id all information about this issue link type.
        """
        url = 'rest/api/2/issueLinkType/{issueLinkTypeId}'.format(issueLinkTypeId=issue_link_type_id)
        return self.get(url)

    def delete_issue_link_type(self, issue_link_type_id):
        """Delete the specified issue link type."""
        url = 'rest/api/2/issueLinkType/{issueLinkTypeId}'.format(issueLinkTypeId=issue_link_type_id)
        return self.delete(url)

    def update_issue_link_type(self, issue_link_type_id, data):
        """
        Update the specified issue link type.
        :param issue_link_type_id:
        :param data: {
                         "name": "Duplicate",
                          "inward": "Duplicated by",
                         "outward": "Duplicates"
                    }
        :return:
        """
        url = 'rest/api/2/issueLinkType/{issueLinkTypeId}'.format(issueLinkTypeId=issue_link_type_id)
        return self.put(url, data=data)

    def create_filter(self, name, jql, description=None, favourite=False):
        """
        :param name: str
        :param jql: str
        :param description: str, Optional. Empty string by default
        :param favourite: bool, Optional. False by default
        """
        data = {'jql': jql,
                'name': name}
        data['description'] = description if description else ''
        data['favourite'] = 'true' if favourite else 'false'
        url = 'rest/api/2/filter'
        return self.post(url, data=data)
    
    def component(self, component_id):
        return self.get('rest/api/2/component/{component_id}'.format(component_id=component_id))

    def get_component_related_issues(self, component_id):
        """
        Returns counts of issues related to this component.
        :param component_id:
        :return:
        """
        url = 'rest/api/2/component/{component_id}/relatedIssueCounts'.format(component_id=component_id)
        return self.get(url)

    def create_component(self, component):
        log.warning('Creating component "{name}"'.format(name=component['name']))
        url = 'rest/api/2/component/'
        return self.post(url, data=component)

    def delete_component(self, component_id):
        log.warning('Deleting component "{component_id}"'.format(component_id=component_id))
        return self.delete('rest/api/2/component/{component_id}'.format(component_id=component_id))

    def get_resolution_by_id(self, resolution_id):
        """
        Get Resolution info by id
        :param resolution_id:
        :return:
        """
        url = 'rest/api/2/resolution/{}'.format(resolution_id)
        return self.get(url)

    def get_priority_by_id(self, priority_id):
        """
        Get Priority info by id
        :param priority_id:
        :return:
        """
        url = 'rest/api/2/resolution/{}'.format(priority_id)
        return self.get(url)

    def get_all_workflows(self):
        """
        Provide all workflows for application admin
        :return:
        """
        url = 'rest/api/2/workflow'
        return self.get(url)

    def get_all_statuses(self):
        """
        Returns a list of all statuses
        :return:
        """
        url = 'rest/api/2/status'
        return self.get(url)

    def get_all_resolutions(self):
        """
        Returns a list of all resolutions.
        :return:
        """
        url = 'rest/api/2/resolution'
        return self.get(url)

    def get_all_priorities(self):
        """
        Returns a list of all priorities.
        :return:
        """
        url = 'rest/api/2/priority'
        return self.get(url)

    def get_all_global_project_roles(self):
        """
        Get all the ProjectRoles available in Jira. Currently this list is global.
        :return:
        """
        url = 'rest/api/2/role'
        return self.get(url)

    def upload_plugin(self, plugin_path):
        """
        Provide plugin path for upload into Jira e.g. useful for auto deploy
        :param plugin_path:
        :return:
        """
        files = {
            'plugin': open(plugin_path, 'rb')
        }
        headers = {
            'X-Atlassian-Token': 'nocheck'
        }
        upm_token = self.request(method='GET', path='rest/plugins/1.0/', headers=headers, trailing=True).headers[
            'upm-token']
        url = 'rest/plugins/1.0/?token={upm_token}'.format(upm_token=upm_token)
        return self.post(url, files=files, headers=headers)

    def check_plugin_manager_status(self):
        headers = {
            'X-Atlassian-Token': 'nocheck',
            'Content-Type': 'application/vnd.atl.plugins.safe.mode.flag+json'
        }
        url = 'rest/plugins/latest/safe-mode'
        return self.request(method='GET', path=url, headers=headers)

    def get_all_permissions(self):
        """
        Returns all permissions that are present in the Jira instance -
        Global, Project and the global ones added by plugins
        :return:
        """
        url = 'rest/api/2/permissions'
        return self.get(url)

    def get_all_permissionschemes(self, expand=None):
        """
        Returns a list of all permission schemes.
        By default only shortened beans are returned.
        If you want to include permissions of all the schemes,
        then specify the permissions expand parameter.
        Permissions will be included also if you specify any other expand parameter.
        :param expand : permissions,user,group,projectRole,field,all
        :return:
        """
        url = 'rest/api/2/permissionscheme'
        params = {}
        if expand:
            params['expand'] = expand
        return (self.get(url, params=params) or {}).get('permissionSchemes')

    def get_permissionscheme(self, permission_id, expand=None):
        """
        Returns a list of all permission schemes.
        By default only shortened beans are returned.
        If you want to include permissions of all the schemes,
        then specify the permissions expand parameter.
        Permissions will be included also if you specify any other expand parameter.
        :param permission_id
        :param expand : permissions,user,group,projectRole,field,all
        :return:
        """
        url = 'rest/api/2/permissionscheme/{schemeID}'.format(schemeID=permission_id)
        params = {}
        if expand:
            params['expand'] = expand
        return self.get(url, params=params)

    def set_permissionscheme_grant(self, permission_id, new_permission):
        """
        Creates a permission grant in a permission scheme.
        Example:

        {
            "holder": {
                "type": "group",
                "parameter": "jira-developers"
            },
            "permission": "ADMINISTER_PROJECTS"
        }

        :param permission_id
        :param new_permission
        :return:
        """
        url = 'rest/api/2/permissionscheme/{schemeID}/permission'.format(schemeID=permission_id)

        return self.post(url, data=new_permission)

    """
    #######################################################################
    #                   Tempo Account REST API implements                 #
    #######################################################################
    """

    def tempo_account_get_accounts(self, skip_archived=None, expand=None):
        """
        Get all Accounts that the logged in user has permission to browse.
        :param skip_archived: bool OPTIONAL: skip archived Accounts, either true or false, default value true.
        :param expand: bool OPTIONAL: With expanded data or not
        :return:
        """
        params = {}
        if skip_archived is not None:
            params['skipArchived'] = skip_archived
        if expand is not None:
            params['expand'] = expand
        url = 'rest/tempo-accounts/1/account'
        return self.get(url, params=params)

    def tempo_account_get_accounts_by_jira_project(self, project_id):
        """
        Get Accounts by JIRA Project. The Caller must have the Browse Account permission for Account.
        This will return Accounts for which the Caller has Browse Account Permission for.
        :param project_id: str the project id.
        :return:
        """
        url = 'rest/tempo-accounts/1/account/project/{}'.format(project_id)
        return self.get(url)

    def tempo_account_associate_with_jira_project(self, account_id, project_id,
                                                  default_account=False,
                                                  link_type='MANUAL'):
        """
        The AccountLinkBean for associate Account with project
        Adds a link to an Account.
        {
            scopeType:PROJECT
            defaultAccount:boolean
            linkType:IMPORTED | MANUAL
            name:string
            key:string
            accountId:number
            scope:number
            id:number
        }
        :param project_id:
        :param account_id
        :param default_account
        :param link_type
        :return:
        """
        data = {}
        if account_id:
            data['accountId'] = account_id
        if default_account:
            data['defaultAccount'] = default_account
        if link_type:
            data['linkType'] = link_type
        if project_id:
            data['scope'] = project_id
        data['scopeType'] = 'PROJECT'

        url = 'rest/tempo-accounts/1/link/'
        return self.post(url, data=data)

    def tempo_account_add_account(self, data=None):
        """
        Creates Account, adding new Account requires the Manage Accounts Permission.
        :param data: String then it will convert to json
        :return:
        """
        url = 'rest/tempo-accounts/1/account/'
        if data is None:
            return """Please, provide data e.g.
                       {name: "12312312321",
                       key: "1231231232",
                       lead: {name: "myusername"},
                       }
                       detail info: http://developer.tempo.io/doc/accounts/api/rest/latest/#-700314780
                   """
        return self.post(url, data=data)

    def tempo_account_delete_account_by_id(self, account_id):
        """
        Delete an Account by id. Caller must have the Manage Account Permission for the Account.
        The Account can not be deleted if it has an AccountLinkBean.
        :param account_id: the id of the Account to be deleted.
        :return:
        """
        url = 'rest/tempo-accounts/1/account/{id}/'.format(id=account_id)
        return self.delete(url)

    def tempo_account_get_all_account_by_customer_id(self, customer_id):
        """
        Get un-archived Accounts by customer. The Caller must have the Browse Account permission for the Account.
        :param customer_id: the Customer id.
        :return:
        """
        url = 'rest/tempo-accounts/1/account/customer/{customerId}/'.format(customerId=customer_id)
        return self.get(url)

    def tempo_account_get_customers(self, query=None, count_accounts=None):
        """
        Gets all or some Attribute whose key or name contain a specific substring.
        Attributes can be a Category or Customer.
        :param query: OPTIONAL: query for search
        :param count_accounts: bool OPTIONAL: provide how many associated Accounts with Customer
        :return: list of customers
        """
        params = {}
        if query is not None:
            params['query'] = query
        if count_accounts is not None:
            params['countAccounts'] = count_accounts
        url = 'rest/tempo-accounts/1/customer'
        return self.get(url, params=params)

    def tempo_account_add_customer(self, data=None):
        """
        Gets all or some Attribute whose key or name contain a specific substring.
        Attributes can be a Category or Customer.
        :param data:
        :return: if error will show in error log, like validation unsuccessful. If success will good.
        """
        if data is None:
            return """Please, set the data as { isNew:boolean
                                                name:string
                                                key:string
                                                id:number } or you can put only name and key parameters"""
        url = 'rest/tempo-accounts/1/customer'
        return self.post(url, data=data)

    def tempo_account_get_customer_by_id(self, customer_id=1):
        """
        Get Account Attribute whose key or name contain a specific substring. Attribute can be a Category or Customer.
        :param customer_id: id of Customer record
        :return: Customer info
        """
        url = 'rest/tempo-accounts/1/customer/{id}'.format(id=customer_id)
        return self.get(url)

    def tempo_account_update_customer_by_id(self, customer_id=1, data=None):
        """
        Updates an Attribute. Caller must have Manage Account Permission. Attribute can be a Category or Customer.
        :param customer_id: id of Customer record
        :param data: format is
                    {
                        isNew:boolean
                        name:string
                        key:string
                        id:number
                    }
        :return: json with parameters name, key and id.
        """
        if data is None:
            return """Please, set the data as { isNew:boolean
                                                name:string
                                                key:string
                                                id:number }"""
        url = 'rest/tempo-accounts/1/customer/{id}'.format(id=customer_id)
        return self.put(url, data=data)

    def tempo_account_delete_customer_by_id(self, customer_id=1):
        """
        Delete an Attribute. Caller must have Manage Account Permission. Attribute can be a Category or Customer.
        :param customer_id: id of Customer record
        :return: Customer info
        """
        url = 'rest/tempo-accounts/1/customer/{id}'.format(id=customer_id)
        return self.delete(url)

    def tempo_account_export_accounts(self):
        """
        Get csv export file of Accounts from Tempo
        :return: csv file
        """
        headers = self.form_token_headers
        url = 'rest/tempo-accounts/1/export'
        return self.get(url, headers=headers, not_json_response=True)

    """
    #######################################################################
    #   Agile(Formerly Greenhopper) REST API implements                  #
    #######################################################################
    """

    def get_all_agile_boards(self, board_name=None, project_key=None, board_type=None, start=0, limit=50):
        """
        Returns all boards. This only includes boards that the user has permission to view.
        :param board_name:
        :param project_key:
        :param board_type:
        :param start:
        :param limit:
        :return:
        """
        url = 'rest/agile/1.0/board'
        params = {}
        if board_name:
            params['name'] = board_name
        if project_key:
            params['projectKeyOrId'] = project_key
        if board_type:
            params['type'] = board_type
        if start:
            params['startAt'] = int(start)
        if limit:
            params['maxResults'] = int(limit)

        return self.get(url, params=params)

    def get_agile_board(self, board_id):
        """
        Get agile board info by id
        :param board_id:
        :return:
        """
        url = 'rest/agile/1.0/board/{}'.format(str(board_id))
        return self.get(url)
    
    def create_agile_board(self, name, type, filter_id, location=None):
        """
        Create an agile board
        :param name: str
        :param type: str, scrum or kanban
        :param filter_id: int
        :param location: dict, Optional. Default is user
        """
        data = {'name': name,
                'type': type,
                'filterId': filter_id}
        if location:
            data['location'] = location
        else:
            data['location'] = {'type': 'user'}
        url = 'rest/agile/1.0/board'
        return self.post(url, data=data)

    def get_agile_board_by_filter_id(self, filter_id):
        """
        Gets an agile board by the filter id
        :param filter_id: int, str
        """
        url = 'rest/agile/1.0/board/filter/{filter_id}'.format(filter_id=filter_id)
        return self.get(url)

    def get_agile_board_configuration(self, board_id):
        """
        Get the board configuration. The response contains the following fields:
        id - Id of the board.
        name - Name of the board.
        filter - Reference to the filter used by the given board.
        subQuery (Kanban only) - JQL subquery used by the given board.
        columnConfig - The column configuration lists the columns for the board,
             in the order defined in the column configuration. For each column,
             it shows the issue status mapping as well as the constraint type
             (Valid values: none, issueCount, issueCountExclSubs) for
             the min/max number of issues. Note, the last column with statuses
             mapped to it is treated as the "Done" column, which means that issues
             in that column will be marked as already completed.
        estimation (Scrum only) - Contains information about type of estimation used for the board.
            Valid values: none, issueCount, field. If the estimation type is "field",
            the Id and display name of the field used for estimation is also returned.
            Note, estimates for an issue can be updated by a PUT /rest/api/2/issue/{issueIdOrKey}
            request, however the fields must be on the screen. "timeoriginalestimate" field will never be
            on the screen, so in order to update it "originalEstimate" in "timetracking" field should be updated.
        ranking - Contains information about custom field used for ranking in the given board.
        :param board_id:
        :return:
        """
        url = 'rest/agile/1.0/board/{}/configuration'.format(str(board_id))
        return self.get(url)

    def get_issues_for_backlog(self, board_id):
        """
        :param board_id: int, str
        """
        url = 'rest/agile/1.0/{board_id}/backlog'.format(board_id=board_id)
        return self.get(url)
    
    def delete_agile_board(self, board_id):
        """
        Delete agile board by id
        :param board_id:
        :return:
        """
        url = 'rest/agile/1.0/board/{}'.format(str(board_id))
        return self.delete(url)

    def get_agile_board_properties(self, board_id):
        """
        Gets a list of all the board properties
        :param board_id: int, str
        """
        url = 'rest/agile/1.0/board/{board_id}/properties'.format(board_id=board_id)
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
