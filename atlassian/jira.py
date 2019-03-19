# coding: utf8
import logging as log 
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
        return self.get(url, not_json_response=True, header={'Accept': 'application/csv'})

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
        url = 'rest/api/2/user/search'
        url += "?username={username}&includeInactive={include_inactive}&startAt={start}&maxResults={limit}".format(
            username=username, include_inactive=include_inactive_users, start=start, limit=limit)
        return self.get(url)

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

    def get_all_custom_fields(self):
        """
        Returns a list of all fields, both System and Custom
        :return: application/jsonContains a full representation of all visible fields in JSON.
        """
        url = 'rest/api/2/field'
        return self.get(url)

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
        :param visibility: Optional
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

    def get_issue_remotelinks(self, issue_key, global_id=None):
        """
        Finding all Remote Links on an issue, also with filtering by Global ID
        :param issue_key:
        :param global_id: str
        :return:
        """
        url = 'rest/api/2/issue/{issue_key}/remotelink'.format(issue_key=issue_key)
        params = {}
        if global_id:
            params['globalId'] = global_id
        return self.get(url, params=params)

    def get_issue_transitions(self, issue_key):
        url = 'rest/api/2/issue/{issue_key}?expand=transitions.fields&fields=status'.format(issue_key=issue_key)
        return [{'name': transition['name'], 'id': int(transition['id']), 'to': transition['to']['name']}
                for transition in (self.get(url) or {}).get('transitions')]

    def get_status_id_from_name(self, status_name):
        url = 'rest/api/2/status/{name}'.format(name=status_name)
        return int((self.get(url) or {}).get('id'))

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
        upm_token = self.request(method='GET', path='rest/plugins/1.0/', headers=headers).headers['upm-token']
        url = 'rest/plugins/1.0/?token={upm_token}'.format(upm_token=upm_token)
        return self.post(url, files=files, headers=headers)

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
