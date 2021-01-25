# coding=utf-8
import logging
import re

from requests import HTTPError

from .errors import ApiNotFoundError, ApiPermissionError
from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Jira(AtlassianRestAPI):
    """
    Provide permission information for the current user.
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2
    """

    def get_permissions(self, project_id=None, project_key=None, issue_id=None, issue_key=None):
        """
        Returns all permissions in the system and whether the currently logged in user has them.
        You can optionally provide a specific context
        to get permissions for (projectKey OR projectId OR issueKey OR issueId)
        When no context supplied the project related permissions will return true
        if the user has that permission in ANY project
        If a project context is provided, project related permissions will return true
        if the user has the permissions in the specified project.
        For permissions that are determined using issue data (e.g Current Assignee), true will be returned
        if the user meets the permission criteria in ANY issue in that project If an issue context is provided,
        it will return whether or not the user has each permission in that specific issue
        NB: The above means that for issue-level permissions (EDIT_ISSUE for example),
        hasPermission may be true when no context is provided, or when a project context is provided,
        but may be false for any given (or all) issues. This would occur (for example)
        if Reporters were given the EDIT_ISSUE permission.
        This is because any user could be a reporter,
        except in the context of a concrete issue, where the reporter is known.

        Global permissions will still be returned for all scopes.

        Prior to version 6.4 this service returned project permissions with keys corresponding to
        com.atlassian.jira.security.Permissions.Permission constants.
        Since 6.4 those keys are considered deprecated and this service returns system project permission keys
        corresponding to constants defined in com.atlassian.jira.permission.ProjectPermissions.
        Permissions with legacy keys are still also returned for backwards compatibility,
        they are marked with an attribute deprecatedKey=true.
        The attribute is missing for project permissions with the current keys.

        :param project_id: (str)  id of project to scope returned permissions for.
        :param project_key: (str) key of project to scope returned permissions for.
        :param issue_id: (str)  key of the issue to scope returned permissions for.
        :param issue_key: (str) id of the issue to scope returned permissions for.
        :return:
        """
        url = "rest/api/2/mypermissions"
        params = {}

        if project_id:
            params["projectId"] = project_id
        if project_key:
            params["projectKey"] = project_key
        if issue_id:
            params["issueId"] = issue_id
        if issue_key:
            params["issueKey"] = issue_key

        return self.get(url, params=params)

    def get_all_permissions(self):
        """
        Returns all permissions that are present in the Jira instance -
        Global, Project and the global ones added by plugins
        :return: All permissions
        """
        url = "rest/api/2/permissions"
        return self.get(url)

    """
    Application properties
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/application-properties
    """

    def get_property(self, key=None, permission_level=None, key_filter=None):
        """
        Returns an application property
        :param key: str
        :param permission_level: str
        :param key_filter: str
        :return: list or item
        """
        url = "rest/api/2/application-properties"
        params = {}

        if key:
            params["key"] = key
        if permission_level:
            params["permissionLevel"] = permission_level
        if key_filter:
            params["keyFilter"] = key_filter

        return self.get(url, params=params)

    def set_property(self, property_id, value):
        """
        Modify an application property via PUT. The "value" field present in the PUT will override the existing value.
        :param property_id:
        :param value:
        :return:
        """
        url = "rest/api/2/application-properties/{}".format(property_id)
        data = {"id": property_id, "value": value}

        return self.put(url, data=data)

    def get_advanced_settings(self):
        """
        Returns the properties that are displayed on the "General Configuration > Advanced Settings" page
        :return:
        """
        url = "rest/api/2/application-properties/advanced-settings"

        return self.get(url)

    """
    Application roles. Provides REST access to JIRA's Application Roles.
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/applicationrole
    """

    def get_all_application_roles(self):
        """
        Returns all ApplicationRoles in the system
        :return:
        """
        url = "rest/api/2/applicationrole"
        return self.get(url) or {}

    def get_application_role(self, role_key):
        """
        Returns the ApplicationRole with passed key if it exists
        :param role_key: str
        :return:
        """
        url = "rest/api/2/applicationrole/{}".format(role_key)
        return self.get(url) or {}

    """
    Attachments
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/attachment
    """

    def get_attachment(self, attachment_id):
        """
        Returns the meta-data for an attachment, including the URI of the actual attached file
        :param attachment_id: int
        :return:
        """
        url = "rest/api/2/attachment/{}".format(attachment_id)
        return self.get(url)

    def remove_attachment(self, attachment_id):
        """
        Remove an attachment from an issue
        :param attachment_id: int
        :return: if success, return None
        """
        url = "rest/api/2/attachment/{}".format(attachment_id)
        return self.delete(url)

    def get_attachment_meta(self):
        """
        Returns the meta information for an attachments,
        specifically if they are enabled and the maximum upload size allowed
        :return:
        """
        url = "rest/api/2/attachment/meta"
        return self.get(url)

    def get_attachment_expand_human(self, attachment_id):
        """
        Returns the information for an expandable attachment in human-readable format
        :param attachment_id: int
        :return:
        """
        url = "rest/api/2/attachment/{}/expand/human".format(attachment_id)
        return self.get(url)

    def get_attachment_expand_raw(self, attachment_id):
        """
        Returns the information for an expandable attachment in raw format
        :param attachment_id: int
        :return:
        """
        url = "rest/api/2/attachment/{}/expand/raw".format(attachment_id)
        return self.get(url)

    """
    Audit Records. Resource representing the auditing records
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/auditing
    """

    def get_audit_records(self, offset=None, limit=None, filter=None, from_date=None, to_date=None):
        """
        Returns auditing records filtered using provided parameters
        :param offset: the number of record from which search starts
        :param limit: maximum number of returned results (if is limit is <= 0 or > 1000,
            it will be set do default value: 1000)
        :param str filter: text query; each record that will be returned must contain
            the provided text in one of it's fields.
        :param str from_date: timestamp in past; 'from' must be less or equal 'to',
            otherwise the result set will be empty only records that where created in the same moment or after
            the 'from' timestamp will be provided in response
        :param str to_date: timestamp in past; 'from' must be less or equal 'to',
            otherwise the result set will be empty only records that where created in the same moment or earlier than
            the 'to' timestamp will be provided in response
        :return:
        """
        params = {}
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if filter:
            params["filter"] = filter
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        url = "rest/api/2/auditing/record"
        return self.get(url, params=params) or {}

    def post_audit_record(self, audit_record):
        """
        Store a record in Audit Log
        :param audit_record: json with compat https://docs.atlassian.com/jira/REST/schema/audit-record#
        :return:
        """
        url = "rest/api/2/auditing/record"
        return self.post(url, data=audit_record)

    """
    Avatar
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/avatar
    """

    def get_all_system_avatars(self, avatar_type="user"):
        """
        Returns all system avatars of the given type.
        :param avatar_type:
        :return: Returns a map containing a list of system avatars.
                 A map is returned to be consistent with the shape of the project/KEY/avatars REST end point.
        """
        url = "rest/api/2/avatar/{type}/system".format(type=avatar_type)
        return self.get(url)

    """
    Cluster. (Available for DC) It gives possibility to manage old node in cluster.
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/cluster
    """

    def get_cluster_all_nodes(self):
        url = "rest/api/2/cluster/nodes"
        return self.get(url)

    def delete_cluster_node(self, node_id):
        """
        Delete the node from the cluster if state of node is OFFLINE
        :param node_id: str
        :return:
        """
        url = "rest/api/2/cluster/node/{}".format(node_id)
        return self.delete(url)

    def set_node_to_offline(self, node_id):
        """
        Change the node's state to offline if the node is reporting as active, but is not alive
        :param node_id: str
        :return:
        """
        url = "rest/api/2/cluster/node/{}/offline".format(node_id)
        return self.put(url)

    """
    ZDU (Zero Downtime upgrade) module. (Available for DC)
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/cluster/zdu
    """

    def get_cluster_zdu_state(self):
        url = "rest/api/2/cluster/zdu/state"
        return self.get(url)

    """
    Comments properties
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/comment/{commentId}/properties
    """

    def get_comment_properties_keys(self, comment_id):
        """
        Returns the keys of all properties for the comment identified by the key or by the id.
        :param comment_id:
        :return:
        """
        url = "rest/api/2/comment/{commentId}/properties".format(commentId=comment_id)
        return self.get(url)

    def get_comment_property(self, comment_id, property_key):
        """
        Returns the value a property for a comment
        :param comment_id: int
        :param property_key: str
        :return:
        """
        url = "rest/api/2/comment/{commentId}/properties/{propertyKey}".format(
            commentId=comment_id, propertyKey=property_key
        )
        return self.get(url)

    def set_comment_property(self, comment_id, property_key, value_property):
        """
        Returns the keys of all properties for the comment identified by the key or by the id.
        :param comment_id: int
        :param property_key: str
        :param value_property: object
        :return:
        """
        url = "rest/api/2/comment/{commentId}/properties/{propertyKey}".format(
            commentId=comment_id, propertyKey=property_key
        )
        data = {"value": value_property}
        return self.put(url, data=data)

    def delete_comment_property(self, comment_id, property_key):
        """
        Deletes a property for a comment
        :param comment_id: int
        :param property_key: str
        :return:
        """
        url = "rest/api/2/comment/{commentId}/properties/{propertyKey}".format(
            commentId=comment_id, propertyKey=property_key
        )
        return self.delete(url)

    """
    Component
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/component
    """

    def component(self, component_id):
        return self.get("rest/api/2/component/{component_id}".format(component_id=component_id))

    def get_component_related_issues(self, component_id):
        """
        Returns counts of issues related to this component.
        :param component_id:
        :return:
        """
        url = "rest/api/2/component/{component_id}/relatedIssueCounts".format(component_id=component_id)
        return self.get(url)

    def create_component(self, component):
        log.warning('Creating component "{name}"'.format(name=component["name"]))
        url = "rest/api/2/component/"
        return self.post(url, data=component)

    def delete_component(self, component_id):
        log.warning('Deleting component "{component_id}"'.format(component_id=component_id))
        return self.delete("rest/api/2/component/{component_id}".format(component_id=component_id))

    def update_component_lead(self, component_id, lead):
        data = {"id": component_id, "leadUserName": lead}
        return self.put(
            "rest/api/2/component/{component_id}".format(component_id=component_id),
            data=data,
        )

    """
    Configurations of Jira
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/configuration
    """

    def get_configurations_of_jira(self):
        """
        Returns the information if the optional features in JIRA are enabled or disabled.
        If the time tracking is enabled, it also returns the detailed information about time tracking configuration.
        :return:
        """
        url = "rest/api/2/configuration"
        return self.get(url)

    """
    Custom Field
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/customFieldOption
               https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/customFields
               https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/field
    """

    def get_custom_field_option(self, option_id):
        """
        Returns a full representation of the Custom Field Option that has the given id.
        :param option_id:
        :return:
        """
        url = "rest/api/2/customFieldOption/{id}".format(id=option_id)
        return self.get(url)

    def get_custom_fields(self, search=None, start=1, limit=50):
        """
        Get custom fields. Evaluated on 7.12
        :param search: str
        :param start: long Default: 1
        :param limit: int Default: 50
        :return:
        """
        url = "rest/api/2/customFields"
        params = {}
        if search:
            params["search"] = search
        if start:
            params["startAt"] = start
        if limit:
            params["maxResults"] = limit
        return self.get(url, params=params)

    def get_all_fields(self):
        """
        Returns a list of all fields, both System and Custom
        :return: application/jsonContains a full representation of all visible fields in JSON.
        """
        url = "rest/api/2/field"
        return self.get(url)

    def create_custom_field(self, name, type, search_key=None, description=None):
        """
        Creates a custom field with the given name and type
        :param name: str
        :param type: str, like 'com.atlassian.jira.plugin.system.customfieldtypes:textfield'
        :param search_key: str, like above
        :param description: str
        """
        url = "rest/api/2/field"
        data = {"name": name, "type": type}
        if search_key:
            data["search_key"] = search_key
        if description:
            data["description"] = description
        return self.post(url, data=data)

    """
    Dashboards
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/dashboard
    """

    def get_dashboards(self, filter="", start=0, limit=10):
        """
        Returns a list of all dashboards, optionally filtering them.
        :param filter: OPTIONAL: an optional filter that is applied to the list of dashboards.
                                Valid values include "favourite" for returning only favourite dashboards,
                                and "my" for returning dashboards that are owned by the calling user.
        :param start: the index of the first dashboard to return (0-based). must be 0 or a multiple of maxResults
        :param limit: a hint as to the the maximum number of dashboards to return in each call.
                      Note that the JIRA server reserves the right to impose a maxResults limit that is lower
                      than the value that a client provides, dues to lack or resources or any other condition.
                      When this happens, your results will be truncated.
                      Callers should always check the returned maxResults to determine
                      the value that is effectively being used.
        :return:
        """
        params = {}
        if filter:
            params["filter"] = filter
        if start:
            params["startAt"] = start
        if limit:
            params["maxResults"] = limit
        url = "rest/api/2/dashboard"
        return self.get(url, params=params)

    """
    Filters. Resource for searches
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/filter
    """

    def create_filter(self, name, jql, description=None, favourite=False):
        """
        :param name: str
        :param jql: str
        :param description: str, Optional. Empty string by default
        :param favourite: bool, Optional. False by default
        """
        data = {
            "jql": jql,
            "name": name,
            "description": description if description else "",
            "favourite": "true" if favourite else "false",
        }
        url = "rest/api/2/filter"
        return self.post(url, data=data)

    def get_filter(self, filter_id):
        """
        Returns a full representation of a filter that has the given id.
        :param filter_id:
        :return:
        """
        url = "rest/api/2/filter/{id}".format(id=filter_id)
        return self.get(url)

    def delete_filter(self, filter_id):
        """
        Deletes a filter that has the given id.
        :param filter_id:
        :return:
        """
        url = "rest/api/2/filter/{id}".format(id=filter_id)
        return self.delete(url)

    """
    Group.
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/group
               https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/groups
    """

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
        url = "rest/api/2/groups/picker"
        params = {}
        if query:
            params["query"] = query
        else:
            params["query"] = ""
        if exclude:
            params["exclude"] = exclude
        if limit:
            params["maxResults"] = limit
        return self.get(url, params=params)

    def create_group(self, name):
        """
        Create a group by given group parameter

        :param name: str
        :return: New group params
        """
        url = "rest/api/2/group"
        data = {"name": name}

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
        log.warning("Removing group...")
        url = "rest/api/2/group"
        if swap_group is not None:
            params = {"groupname": name, "swapGroup": swap_group}
        else:
            params = {"groupname": name}

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
        url = "rest/api/2/group/member"
        params = {}
        if group:
            params["groupname"] = group
        params["includeInactiveUsers"] = include_inactive_users
        params["startAt"] = start
        params["maxResults"] = limit
        return self.get(url, params=params)

    def add_user_to_group(self, username, group_name):
        """
        Add given user to a group

        :param username: str
        :param group_name: str
        :return: Current state of the group
        """
        url = "rest/api/2/group/user"
        params = {"groupname": group_name}
        data = {"name": username}

        return self.post(url, params=params, data=data)

    def remove_user_from_group(self, username, group_name):
        """
        Remove given user from a group

        :param username: str
        :param group_name: str
        :return:
        """
        log.warning("Removing user from a group...")
        url = "rest/api/2/group/user"
        params = {"groupname": group_name, "username": username}

        return self.delete(url, params=params)

    """
    Issue
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/issue
    """

    def issue(self, key, fields="*all", expand=None):
        params = {}
        if expand:
            params["expand"] = expand
        return self.get("rest/api/2/issue/{0}?fields={1}".format(key, fields), params=params)

    def get_issue(self, issue_id_or_key, fields=None, properties=None, update_history=True):
        """
        Returns a full representation of the issue for the given issue key
        By default, all fields are returned in this get-issue resource

        :param issue_id_or_key: str
        :param fields: str
        :param properties: str
        :param update_history: bool
        :return: issue
        """
        url = "rest/api/2/issue/{}".format(issue_id_or_key)
        params = {}

        if fields is not None:
            if isinstance(fields, (list, tuple, set)):
                fields = ",".join(fields)
            params["fields"] = fields
        if properties is not None:
            params["properties"] = properties
        if update_history is True:
            params["updateHistory"] = "true"
        if update_history is False:
            params["updateHistory"] = "false"

        return self.get(url, params=params)

    def bulk_issue(self, issue_list, fields="*all"):
        """
        :param fields:
        :param list issue_list:
        :return:
        """
        jira_issue_regex = re.compile(r"[A-Z]{1,10}-\d+")
        missing_issues = list()
        matched_issue_keys = list()
        for key in issue_list:
            if re.match(jira_issue_regex, key):
                matched_issue_keys.append(key)
        jql = "key in ({})".format(", ".join(set(matched_issue_keys)))
        query_result = self.jql(jql, fields=fields)
        if "errorMessages" in query_result.keys():
            for message in query_result["errorMessages"]:
                for key in issue_list:
                    if key in message:
                        missing_issues.append(key)
                        issue_list.remove(key)
            query_result, missing_issues = self.bulk_issue(issue_list, fields)
        return query_result, missing_issues

    def issue_createmeta(self, project, expand="projects.issuetypes.fields"):
        params = {}
        if expand:
            params["expand"] = expand
        url = "rest/api/2/issue/createmeta?projectKeys={}".format(project)
        return self.get(url, params=params)

    def get_issue_changelog(self, issue_key):
        """
        Get issue related change log
        :param issue_key:
        :return:
        """
        url = "rest/api/2/issue/{}?expand=changelog".format(issue_key)
        return (self.get(url) or {}).get("changelog")

    def issue_add_json_worklog(self, key, worklog):
        """

        :param key:
        :param worklog:
        :return:
        """
        url = "rest/api/2/issue/{}/worklog".format(key)
        return self.post(url, data=worklog)

    def issue_worklog(self, key, started, time_sec, comment=None):
        """
        :param key:
        :param time_sec: int: second
        :param started: str: format ``%Y-%m-%dT%H:%M:%S.000+0000%z``
        :param comment:
        :return:
        """
        data = {"started": started, "timeSpentSeconds": time_sec}
        if comment:
            data["comment"] = comment
        return self.issue_add_json_worklog(key=key, worklog=data)

    def issue_get_worklog(self, issue_id_or_key):
        """
        Returns all work logs for an issue.
        Note: Work logs won't be returned if the Log work field is hidden for the project.
        :param issue_id_or_key:
        :return:
        """
        url = "rest/api/2/issue/{issueIdOrKey}/worklog".format(issueIdOrKey=issue_id_or_key)

        return self.get(url)

    def issue_archive(self, issue_id_or_key, notify_users=False):
        """
        Archives an issue.
        :param issue_id_or_key: Issue id or issue key
        :param notify_users: send the email with notification that the issue was updated to users that watch it.
                            Admin or project admin permissions are required to disable the notification.
        :return:
        """
        params = {}
        if notify_users:
            params["notifyUsers"] = "true"
        else:
            params["notifyUsers"] = "false"
        url = "rest/api/2/issue/{issueIdOrKey}/archive".format(issueIdOrKey=issue_id_or_key)
        return self.get(url)

    def issue_field_value(self, key, field, expand=None):
        params = {}
        if expand:
            params["expand"] = expand
        issue = self.get("rest/api/2/issue/{0}?fields={1}".format(key, field), params=params)
        return issue["fields"][field]

    def issue_fields(self, key):
        issue = self.get("rest/api/2/issue/{0}".format(key))
        return issue["fields"]

    def update_issue_field(self, key, fields="*all"):
        return self.put("rest/api/2/issue/{0}".format(key), data={"fields": fields})

    def get_issue_labels(self, issue_key):
        """
        Get issue labels.
        :param issue_key:
        :return:
        """
        url = "rest/api/2/issue/{issue_key}?fields=labels".format(issue_key=issue_key)
        if self.advanced_mode:
            return self.get(url)
        return (self.get(url) or {}).get("fields").get("labels")

    def add_attachment(self, issue_key, filename):
        """
        Add attachment to Issue
        :param issue_key: str
        :param filename: str, name, if file in current directory or full path to file
        """
        log.warning("Adding attachment...")
        url = "rest/api/2/issue/{}/attachments".format(issue_key)
        with open(filename, "rb") as attachment:
            files = {"file": attachment}
            return self.post(url, headers=self.no_check_headers, files=files)

    def issue_exists(self, issue_key):
        original_value = self.advanced_mode
        self.advanced_mode = True
        try:
            resp = self.issue(issue_key, fields="*none")
            if resp.status_code == 404:
                log.info('Issue "{issue_key}" does not exists'.format(issue_key=issue_key))
                return False
            resp.raise_for_status()
            log.info('Issue "{issue_key}" exists'.format(issue_key=issue_key))
            return True
        finally:
            self.advanced_mode = original_value

    def issue_deleted(self, issue_key):
        exists = self.issue_exists(issue_key)
        if exists:
            log.info('Issue "{issue_key}" is not deleted'.format(issue_key=issue_key))
        else:
            log.info('Issue "{issue_key}" is deleted'.format(issue_key=issue_key))
        return not exists

    def delete_issue(self, issue_id_or_key, delete_subtasks=True):
        """
        Delete an issue
        If the issue has subtasks you must set the parameter delete_subtasks = True to delete the issue
        You cannot delete an issue without its subtasks also being deleted
        :param issue_id_or_key:
        :param delete_subtasks:
        :return:
        """
        url = "rest/api/2/issue/{}".format(issue_id_or_key)
        params = {}

        if delete_subtasks is True:
            params["deleteSubtasks"] = "true"
        else:
            params["deleteSubtasks"] = "false"

        log.warning("Removing issue {}...".format(issue_id_or_key))

        return self.delete(url, params=params)

    # @todo merge with edit_issue method
    def issue_update(self, issue_key, fields):
        log.warning('Updating issue "{issue_key}" with "{fields}"'.format(issue_key=issue_key, fields=fields))
        url = "rest/api/2/issue/{0}".format(issue_key)
        return self.put(url, data={"fields": fields})

    def edit_issue(self, issue_id_or_key, fields, notify_users=True):
        """
        Edits an issue from a JSON representation
        The issue can either be updated by setting explicit the field
        value(s) or by using an operation to change the field value

        :param issue_id_or_key: str
        :param fields: JSON
        :param notify_users: bool
        :return:
        """
        url = "rest/api/2/issue/{}".format(issue_id_or_key)
        params = {}
        data = {"update": fields}

        if notify_users is True:
            params["notifyUsers"] = "true"
        else:
            params["notifyUsers"] = "false"
        return self.put(url, data=data, params=params)

    def issue_add_watcher(self, issue_key, user):
        """
        Start watching issue
        :param issue_key:
        :param user:
        :return:
        """
        log.warning('Adding user {user} to "{issue_key}" watchers'.format(issue_key=issue_key, user=user))
        data = user
        return self.post(
            "rest/api/2/issue/{issue_key}/watchers".format(issue_key=issue_key),
            data=data,
        )

    def assign_issue(self, issue, assignee=None):
        """Assign an issue to a user. None will set it to unassigned. -1 will set it to Automatic.
        :param issue: the issue ID or key to assign
        :type issue: int or str
        :param assignee: the user to assign the issue to
        :type assignee: str
        :rtype: bool
        """
        url = "rest/api/2/issue/{issue}/assignee".format(issue=issue)
        data = {"name": assignee}

        return self.put(url, data=data)

    def create_issue(self, fields, update_history=False, update=None):
        """
        Creates an issue or a sub-task from a JSON representation
        :param fields: JSON data
                mandatory keys are issuetype, summary and project
        :param update: JSON data
                Use it to link issues or update worklog
        :param update_history: bool (if true then the user's project history is updated)
        :return:
            example:
                fields = dict(summary='Into The Night',
                              project = dict(key='APA'),
                              issuetype = dict(name='Story')
                              )
                update = dict(issuelinks={
                    "add": {
                        "type": {
                            "name": "Child-Issue"
                            },
                        "inwardIssue": {
                            "key": "ISSUE-KEY"
                            }
                        }
                    }
                )
                jira.create_issue(fields=fields, update=update)
        """
        url = "rest/api/2/issue"
        data = {"fields": fields}
        if update:
            data["update"] = update
        params = {}

        if update_history is True:
            params["updateHistory"] = "true"
        else:
            params["updateHistory"] = "false"
        return self.post(url, params=params, data=data)

    def create_issues(self, list_of_issues_data):
        """
        Creates issues or sub-tasks from a JSON representation
        Creates many issues in one bulk operation
        :param list_of_issues_data: list of JSON data
        :return:
        """
        url = "rest/api/2/issue/bulk"
        data = {"issueUpdates": list_of_issues_data}
        return self.post(url, data=data)

    # @todo refactor and merge with create_issue method
    def issue_create(self, fields):
        log.warning('Creating issue "{summary}"'.format(summary=fields["summary"]))
        url = "rest/api/2/issue"
        return self.post(url, data={"fields": fields})

    def issue_create_or_update(self, fields):
        issue_key = fields.get("issuekey", None)

        if not issue_key or not self.issue_exists(issue_key):
            log.info("IssueKey is not provided or does not exists in destination. Will attempt to create an issue")
            fields.pop("issuekey", None)
            return self.issue_create(fields)

        if self.issue_deleted(issue_key):
            log.warning('Issue "{issue_key}" deleted, skipping'.format(issue_key=issue_key))
            return None

        log.info('Issue "{issue_key}" exists, will update'.format(issue_key=issue_key))
        fields.pop("issuekey", None)
        return self.issue_update(issue_key, fields)

    def issue_add_comment(self, issue_key, comment, visibility=None):
        """
        Add comment into Jira issue
        :param issue_key:
        :param comment:
        :param visibility: OPTIONAL
        :return:
        """
        url = "rest/api/2/issue/{issueIdOrKey}/comment".format(issueIdOrKey=issue_key)
        data = {"body": comment}
        if visibility:
            data["visibility"] = visibility
        return self.post(url, data=data)

    def issue_edit_comment(self, issue_key, comment_id, comment, visibility=None):
        """
        Updates an existing comment
        :param issue_key: str
        :param comment_id: int
        :param comment: str
        :param visibility: OPTIONAL
        :return:
        """
        url = "rest/api/2/issue/{}/comment/{}".format(issue_key, comment_id)
        data = {"body": comment}
        if visibility:
            data["visibility"] = visibility
        return self.put(url, data=data)

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
        url = "rest/api/2/issue/{issue_key}/remotelink".format(issue_key=issue_key)
        params = {}
        if global_id:
            params["globalId"] = global_id
        if internal_id:
            url += "/" + internal_id
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
        url = "rest/api/2/issue/{issue_key}/remotelink".format(issue_key=issue_key)
        data = {"object": {"url": link_url, "title": title}}
        if global_id:
            data["globalId"] = global_id
        if relationship:
            data["relationship"] = relationship
        return self.post(url, data=data)

    def get_issue_remote_link_by_id(self, issue_key, link_id):
        url = "rest/api/2/issue/{issue_key}/remotelink/{link_id}".format(issue_key=issue_key, link_id=link_id)
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
        data = {"object": {"url": url, "title": title}}
        if global_id:
            data["globalId"] = global_id
        if relationship:
            data["relationship"] = relationship
        url = "rest/api/2/issue/{issue_key}/remotelink/{link_id}".format(issue_key=issue_key, link_id=link_id)
        return self.put(url, data=data)

    def delete_issue_remote_link_by_id(self, issue_key, link_id):
        """
        Deletes Remote Link on Issue
        :param issue_key: str
        :param link_id: str
        """
        url = "rest/api/2/issue/{issue_key}/remotelink/{link_id}".format(issue_key=issue_key, link_id=link_id)
        return self.delete(url)

    def get_issue_transitions(self, issue_key):
        if self.advanced_mode:
            return [
                {
                    "name": transition["name"],
                    "id": int(transition["id"]),
                    "to": transition["to"]["name"],
                }
                for transition in (self.get_issue_transitions_full(issue_key).json() or {}).get("transitions")
            ]
        else:
            return [
                {
                    "name": transition["name"],
                    "id": int(transition["id"]),
                    "to": transition["to"]["name"],
                }
                for transition in (self.get_issue_transitions_full(issue_key) or {}).get("transitions")
            ]

    def issue_transition(self, issue_key, status):
        return self.set_issue_status(issue_key, status)

    def set_issue_status(self, issue_key, status_name, fields=None):
        """
        Setting status by status_name. fields defaults to None for transitions without mandatory fields.
        If there are mandatary fields for the transition, these can be set using a dict.
        Example:
            jira.set_issue_status('MY-123','Resolved',{'myfield': 'myvalue'})
        :param issue_key: str
        :param status_name: str
        :param fields: dict, optional
        """
        url = "rest/api/2/issue/{issue_key}/transitions".format(issue_key=issue_key)
        transition_id = self.get_transition_id_to_status_name(issue_key, status_name)
        data = {"transition": {"id": transition_id}}
        if fields is not None:
            data["fields"] = fields
        return self.post(url, data=data)

    def set_issue_status_by_transition_id(self, issue_key, transition_id):
        """
        Setting status by transition_id
        :param issue_key: str
        :param transition_id: int
        """
        url = "rest/api/2/issue/{issue_key}/transitions".format(issue_key=issue_key)
        return self.post(url, data={"transition": {"id": transition_id}})

    def get_issue_status(self, issue_key):
        url = "rest/api/2/issue/{issue_key}?fields=status".format(issue_key=issue_key)
        return (((self.get(url) or {}).get("fields") or {}).get("status") or {}).get("name") or {}

    def get_issue_status_id(self, issue_key):
        url = "rest/api/2/issue/{issue_key}?fields=status".format(issue_key=issue_key)
        return (self.get(url) or {}).get("fields").get("status").get("id")

    def get_issue_transitions_full(self, issue_key, transition_id=None, expand=None):
        """
        Get a list of the transitions possible for this issue by the current user,
        along with fields that are required and their types.
        Fields will only be returned if expand = 'transitions.fields'.
        The fields in the metadata correspond to the fields in the transition screen for that transition.
        Fields not in the screen will not be in the metadata.
        :param issue_key: str
        :param transition_id: str
        :param expand: str
        :return:
        """
        url = "rest/api/2/issue/{issue_key}/transitions".format(issue_key=issue_key)
        params = {}
        if transition_id:
            params["transitionId"] = transition_id
        if expand:
            params["expand"] = expand
        return self.get(url, params=params)

    def get_updated_worklogs(self, since, expand=None):
        """
        Returns a list of IDs and update timestamps for worklogs updated after a date and time.
        :param since: The date and time, as a UNIX timestamp in milliseconds, after which updated worklogs are returned.
        :param expand: Use expand to include additional information about worklogs in the response.
            This parameter accepts properties that returns the properties of each worklog.
        """
        url = "rest/api/3/worklog/updated"
        params = {}
        if since:
            params["since"] = str(int(since * 1000))
        if expand:
            params["expand"] = expand

        return self.get(url, params=params)

    def get_worklogs(self, ids, expand=None):
        """
        Returns worklog details for a list of worklog IDs.
        :param expand: Use expand to include additional information about worklogs in the response.
            This parameter accepts properties that returns the properties of each worklog.
        :param ids: REQUIRED A list of worklog IDs.
        """

        url = "rest/api/3/worklog/list"
        params = {}
        if expand:
            params["expand"] = expand
        data = {"ids": ids}
        return self.post(url, params=params, data=data)

    """
    User
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/user
    """

    def user(self, username=None, key=None, account_id=None, expand=None):
        """
        Returns a user. This resource cannot be accessed anonymously.
        You can use only one parameter: username or key

        :param username:
        :param key: if username and key are different
        :param account_id:
        :param expand: Can be 'groups,applicationRoles'
        :return:
        """
        params = {}
        major_parameter_enabled = False
        if account_id:
            params = {"accountId": account_id}
            major_parameter_enabled = True

        if not major_parameter_enabled and username and not key:
            params = {"username": username}
        elif not major_parameter_enabled and not username and key:
            params = {"key": key}
        elif not major_parameter_enabled and username and key:
            return "You cannot specify both the username and the key parameters"
        elif not account_id and not key and not username:
            return "You must specify at least one parameter: username or key or account_id"
        if expand:
            params["expand"] = expand

        return self.get("rest/api/2/user", params=params)

    def is_active_user(self, username):
        """
        Check status of user
        :param username:
        :return:
        """
        return self.user(username).get("active")

    def user_remove(self, username=None, account_id=None, key=None):
        """
        Remove user from Jira if this user does not have any activity
        :param key:
        :param account_id:
        :param username:
        :return:
        """
        params = {}
        if username:
            params["username"] = username
        if account_id:
            params["accountId"] = account_id
        if key:
            params["key"] = key
        return self.delete("rest/api/2/user", params=params)

    def user_update(self, username, data):
        """
        Update user attributes based on json
        :param username:
        :param data:
        :return:
        """
        url = "rest/api/2/user?username={0}".format(username)
        return self.put(url, data=data)

    def user_update_username(self, old_username, new_username):
        """
        Update username
        :param old_username:
        :param new_username:
        :return:
        """
        data = {"name": new_username}
        return self.user_update(old_username, data=data)

    def user_update_email(self, username, email):
        """
        Update user email for new domain changes
        :param username:
        :param email:
        :return:
        """
        data = {"name": username, "emailAddress": email}
        return self.user_update(username, data=data)

    def user_create(self, username, email, display_name, password=None, notification=None):
        """
        Create a user in Jira
        :param username:
        :param email:
        :param display_name:
        :param password: OPTIONAL: If a password is not set, a random password is generated.
        :param notification: OPTIONAL: Sends the user an email confirmation that they have been added to Jira.
                             Default:false.
        :return:
        """
        log.warning("Creating user {}".format(display_name))
        data = {"name": username, "emailAddress": email, "displayName": display_name}
        if password is not None:
            data["password"] = password
        else:
            data["notification"] = True
        if notification is not None:
            data["notification"] = True
        if notification is False:
            data["notification"] = False
        return self.post("rest/api/2/user", data=data)

    def user_properties(self, username):
        """
        Get user property
        :param username:
        :return:
        """
        return self.get("rest/api/2/user/properties?username={}".format(username))

    def user_property(self, username, key_property):
        """
        Get user property
        :param key_property:
        :param username:
        :return:
        """
        params = {"username": username}
        return self.get("rest/api/2/user/properties/{}".format(key_property), params=params)

    def user_set_property(self, username, key_property, value_property):
        """
        Set property for user
        :param username:
        :param key_property:
        :param value_property:
        :return:
        """
        url = "rest/api/2/user/properties/{key_property}?username={user_name}".format(
            key_property=key_property, user_name=username
        )
        data = {"value": value_property}
        return self.put(url, data=data)

    def user_delete_property(self, username, key_property):
        """
        Delete property for user
        :param username:
        :param key_property:
        :return:
        """
        url = "rest/api/2/user/properties/{}".format(key_property)
        params = {"username": username}
        return self.delete(url, params=params)

    def user_update_or_create_property_through_rest_point(self, username, key, value):
        """
        ATTENTION!
        This method used after configuration of rest endpoint on Jira side
        :param username:
        :param key:
        :param value:
        :return:
        """
        url = "rest/scriptrunner/latest/custom/updateUserProperty"
        params = {"username": username, "property": key, "value": value}
        return self.get(url, params=params)

    def user_deactivate(self, username):
        """
        Disable user. Works from 8.3.0 Release
        https://docs.atlassian.com/software/jira/docs/api/REST/8.3.0/#api/2/user-updateUser
        :param username:
        :return:
        """
        data = {"active": "false", "name": username}
        return self.user_update(username=username, data=data)

    def user_disable(self, username):
        """Override the disable method"""
        return self.user_deactivate(username)

    def user_disable_throw_rest_endpoint(
        self,
        username,
        url="rest/scriptrunner/latest/custom/disableUser",
        param="userName",
    ):
        """The disable method throw own rest endpoint"""
        url = "{}?{}={}".format(url, param, username)
        return self.get(path=url)

    def user_get_websudo(self):
        """ Get web sudo cookies using normal http request"""
        url = "secure/admin/WebSudoAuthenticate.jspa"
        data = {
            "webSudoPassword": self.password,
            "webSudoIsPost": "false",
        }
        answer = self.get("secure/admin/WebSudoAuthenticate.jspa", self.form_token_headers)
        atl_token = None
        if answer:
            atl_token = (
                answer.split('<meta id="atlassian-token" name="atlassian-token" content="')[1]
                .split("\n")[0]
                .split('"')[0]
            )
        if atl_token:
            data["atl_token"] = atl_token

        return self.post(path=url, data=data, headers=self.form_token_headers)

    def invalidate_websudo(self):
        """
        This method invalidates the any current WebSudo session.
        """
        return self.delete("rest/auth/1/websudo")

    def user_find_by_user_string(
        self,
        username,
        start=0,
        limit=50,
        include_inactive_users=False,
        include_active_users=True,
    ):
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
        url = "rest/api/2/user/search"
        params = {
            "username": username,
            "includeActive": include_active_users,
            "includeInactive": include_inactive_users,
            "startAt": start,
            "maxResults": limit,
        }
        return self.get(url, params=params)

    def is_user_in_application(self, username, application_key):
        """
        Utility function to test whether a user has an application role
        :param username: The username of the user to test.
        :param application_key: The application key of the application
        :return: True if the user has the application, else False
        """
        user = self.user(username, "applicationRoles")  # Get applications roles of the user
        if "self" in user:
            for application_role in user.get("applicationRoles").get("items"):
                if application_role.get("key") == application_key:
                    return True
        return False

    def add_user_to_application(self, username, application_key):
        """
        Add a user to an application
        :param username: The username of the user to add.
        :param application_key: The application key of the application
        :return: True if the user was added to the application, else False
        :see: https://docs.atlassian.com/software/jira/docs/api/REST/7.5.3/#api/2/user-addUserToApplication
        """
        params = {"username": username, "applicationKey": application_key}
        return self.post("rest/api/2/user/application", params=params) is None

    """
    Projects
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/project
    """

    def get_all_projects(self, included_archived=None):
        return self.projects(included_archived)

    def projects(self, included_archived=None):
        """Returns all projects which are visible for the currently logged in user.
        If no user is logged in, it returns the list of projects that are visible when using anonymous access.
        :param included_archived: boolean whether to include archived projects in response, default: false
        :return:
        """
        params = {}
        if included_archived:
            params["includeArchived"] = included_archived
        return self.get("rest/api/2/project")

    def create_project_from_raw_json(self, json):
        """
        Creates a new project.
            {
                "key": "EX",
                "name": "Example",
                "projectTypeKey": "business",
                "projectTemplateKey": "com.atlassian.jira-core-project-templates:jira-core-project-management",
                "description": "Example Project description",
                "lead": "Charlie",
                "url": "http://atlassian.com",
                "assigneeType": "PROJECT_LEAD",
                "avatarId": 10200,
                "issueSecurityScheme": 10001,
                "permissionScheme": 10011,
                "notificationScheme": 10021,
                "categoryId": 10120
            }
        :param json:
        :return:
        """
        return self.post("rest/api/2/project", json=json)

    def delete_project(self, key):
        """
        DELETE /rest/api/2/project/<project_key>
        :param key: str
        :return:
        """
        return self.delete("rest/api/2/project/{0}".format(key))

    def project(self, key, expand=None):
        params = {}
        if expand:
            params["expand"] = expand
        return self.get("rest/api/2/project/{0}".format(key), params=params)

    def get_project(self, key, expand):
        """
            Contains a full representation of a project in JSON format.
            All project keys associated with the project will only be returned if expand=projectKeys.
        :param key:
        :param expand:
        :return:
        """
        return self.project(key=key, expand=expand)

    def get_project_components(self, key):
        """
        Get project components using project key
        :param key: str
        :return:
        """
        return self.get("rest/api/2/project/{0}/components".format(key))

    def get_project_versions(self, key, expand=None):
        """
        Contains a full representation of a the specified project's versions.
        :param key:
        :param expand: the parameters to expand
        :return:
        """
        params = {}
        if expand is not None:
            params["expand"] = expand
        return self.get("rest/api/2/project/{}/versions".format(key), params=params)

    def get_project_versions_paginated(
        self,
        key,
        start=None,
        limit=None,
        order_by=None,
        expand=None,
        query=None,
        status=None,
    ):
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
        :param query: Filter the results using a literal string. Versions with matching name or description
            are returned (case insensitive).
        :param status: A list of status values used to filter the results by version status.
            This parameter accepts a comma-separated list. The status values are released, unreleased, and archived.
        :return:
        """
        params = {}
        if start is not None:
            params["startAt"] = int(start)
        if limit is not None:
            params["maxResults"] = int(limit)
        if order_by is not None:
            params["orderBy"] = order_by
        if expand is not None:
            params["expand"] = expand
        if query is not None:
            params["query"] = query
        if status in ["released", "unreleased", "archived"]:
            params["status"] = status
        return self.get("rest/api/2/project/{}/version".format(key), params=params)

    def add_version(self, project_key, project_id, version, is_archived=False, is_released=False):
        """
        Add missing version to project
        :param project_key: the project key
        :param project_id: the project id
        :param version: the new project version to add
        :param is_archived:
        :param is_released:
        :return:
        """
        payload = {
            "name": version,
            "archived": is_archived,
            "released": is_released,
            "project": project_key,
            "projectId": project_id,
        }
        return self.post("rest/api/2/version", data=payload)

    def delete_version(self, version, moved_fixed=None, move_affected=None):
        """
        Delete version from the project
        :param int version: the version id to delete
        :param int moved_fixed: The version to set fixVersion to on issues where the deleted version is the fix version.
                                If null then the fixVersion is removed.
        :param int move_affected: The version to set affectedVersion to on issues where the deleted version is
                                  the affected version, If null then the affectedVersion is removed.
        :return:
        """
        payload = {"moveFixIssuesTo": moved_fixed, "moveAffectedIssuesTo": move_affected}
        return self.delete("rest/api/2/version/{}".format(version), data=payload)

    def get_project_roles(self, project_key):
        """
        Provide associated project roles
        :param project_key:
        :return:
        """
        return self.get("rest/api/2/project/{0}/role".format(project_key))

    def get_project_actors_for_role_project(self, project_key, role_id):
        """
        Returns the details for a given project role in a project.
        :param project_key:
        :param role_id:
        :return:
        """
        url = "rest/api/2/project/{projectIdOrKey}/role/{id}".format(projectIdOrKey=project_key, id=role_id)
        return (self.get(url) or {}).get("actors")

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
        url = "rest/api/2/project/{projectIdOrKey}/role/{roleId}".format(projectIdOrKey=project_key, roleId=role_id)
        params = {}
        if actor_type is not None and actor_type in ["group", "user"]:
            params[actor_type] = actor
        return self.delete(url, params=params)

    def add_user_into_project_role(self, project_key, role_id, user_name):
        """

        :param project_key:
        :param role_id:
        :param user_name:
        :return:
        """
        return self.add_project_actor_in_role(project_key, role_id, user_name, "atlassian-user-role-actor")

    def add_project_actor_in_role(self, project_key, role_id, actor, actor_type):
        """

        :param project_key:
        :param role_id:
        :param actor:
        :param actor_type:
        :return:
        """
        url = "rest/api/2/project/{projectIdOrKey}/role/{roleId}".format(projectIdOrKey=project_key, roleId=role_id)
        data = {}
        if actor_type in ["group", "atlassian-group-role-actor"]:
            data["group"] = [actor]
        elif actor_type in ["user", "atlassian-user-role-actor"]:
            data["user"] = [actor]

        return self.post(url, data=data)

    def update_project(self, project_key, data, expand=None):
        """
        Updates a project.
        Only non null values sent in JSON will be updated in the project.
        Values available for the assigneeType field are: "PROJECT_LEAD" and "UNASSIGNED".
        Update project: /rest/api/2/project/{projectIdOrKey}

        :param project_key: project key of project that needs to be updated
        :param data: dictionary containing the data to be updated
        :param expand: the parameters to expand
        """
        url = "rest/api/2/project/{projectIdOrKey}".format(projectIdOrKey=project_key)
        params = {}
        if expand:
            params["expand"] = expand
        return self.put(url, data, params=params)

    def update_project_category_for_project(self, project_key, new_project_category_id, expand=None):
        """
        Updates a project.
        Update project: /rest/api/2/project/{projectIdOrKey}

        :param project_key: project key of project that needs to be updated
        :param new_project_category_id:
        :param expand: the parameters to expand
        """
        data = {"categoryId": new_project_category_id}
        return self.update_project(project_key, data, expand=expand)

    """
    Resource for associating notification schemes and projects
    Reference:
       https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/project/{projectKeyOrId}/notificationscheme
    """

    def get_notification_scheme_for_project(self, project_id_or_key):
        """
        Gets a notification scheme associated with the project.
        Follow the documentation of /notificationscheme/{id} resource for all details about returned value.
        :param project_id_or_key:
        :return:
        """
        url = "rest/api/2/project/{}/notificationscheme".format(project_id_or_key)
        return self.get(url)

    def assign_project_notification_scheme(self, project_key, new_notification_scheme=""):
        """
        Updates a project.
        Update project: /rest/api/2/project/{projectIdOrKey}

        :param project_key: project key of project that needs to be updated
        :param new_notification_scheme:
        """
        data = {"notificationScheme": new_notification_scheme}
        return self.update_project(project_key, data)

    def get_notification_schemes(self):
        """
        Returns a paginated list of notification schemes
        """
        url = "rest/api/2/notificationscheme"
        return self.get(url)

    def get_all_notification_schemes(self):
        """
        Returns a paginated list of notification schemes
        """
        return self.get_notification_schemes().get("values") or []

    def get_notification_scheme(self, notification_scheme_id, expand=None):
        """
        Returns a full representation of the notification scheme for the given id.
        Use 'expand' to get details
        Returns a full representation of the notification scheme for the given id. This resource will return a
        notification scheme containing a list of events and recipient configured to receive notifications for these
        events. Consumer should allow events without recipients to appear in response. User accessing the data is
        required to have permissions to administer at least one project associated with the requested notification
        scheme.
        Notification recipients can be:

            current assignee - the value of the notificationType is CurrentAssignee
            issue reporter - the value of the notificationType is Reporter
            current user - the value of the notificationType is CurrentUser
            project lead - the value of the notificationType is ProjectLead
            component lead - the value of the notificationType is ComponentLead
            all watchers - the value of the notification type is AllWatchers
            configured user - the value of the notification type is User. Parameter will contain key of the user.
                Information about the user will be provided if user expand parameter is used.
            configured group - the value of the notification type is Group. Parameter will contain name of the group.
                Information about the group will be provided if group expand parameter is used.
            configured email address - the value of the notification type is EmailAddress, additionally
                information about the email will be provided.
            users or users in groups in the configured custom fields - the value of the notification type
                is UserCustomField or GroupCustomField. Parameter will contain id of the custom field.
                Information about the field will be provided if field expand parameter is used.
            configured project role - the value of the notification type is ProjectRole.
                Parameter will contain project role id.
                Information about the project role will be provided if projectRole expand parameter is used.
        Please see the example for reference.
        The events can be JIRA system events or events configured by administrator.
        In case of the system events, data about theirs ids, names and descriptions is provided.
        In case of custom events, the template event is included as well.
        :param notification_scheme_id: Id of scheme u wanna work with
        :param expand: str
        :return: full representation of the notification scheme for the given id
        """
        url = "rest/api/2/notificationscheme/{}".format(notification_scheme_id)
        params = {}
        if expand:
            params["expand"] = expand
        return self.get(url, params=params)

    """
    Resource for associating permission schemes and projects.
    Reference:
       https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/project/{projectKeyOrId}/permissionscheme
    """

    def assign_project_permission_scheme(self, project_id_or_key, permission_scheme_id):
        """
        Assigns a permission scheme with a project.
        :param project_id_or_key:
        :param permission_scheme_id:
        :return:
        """
        url = "rest/api/2/project/{}/permissionscheme".format(project_id_or_key)
        data = {"id": permission_scheme_id}
        return self.put(url, data=data)

    def get_project_permission_scheme(self, project_id_or_key, expand=None):
        """
        Gets a permission scheme assigned with a project
        Use 'expand' to get details

        :param project_id_or_key: str
        :param expand: str
        :return: data of project permission scheme
        """
        url = "rest/api/2/project/{}/permissionscheme".format(project_id_or_key)
        params = {}
        if expand:
            params["expand"] = expand
        return self.get(url, params=params)

    def get_issue_types(self):
        """
        Return all issue types
        """
        return self.get("rest/api/2/issuetype")

    def create_issue_type(self, name, description="", type="standard"):
        """
        Create a new issue type
        :param name:
        :param description:
        :param type: standard or sub-task
        :return:
        """
        data = {"name": name, "description": description, "type": type}
        return self.post("rest/api/2/issuetype", data=data)

    def get_all_custom_fields(self):
        """
        Returns a list of all custom fields
        That method just filtering all fields method
        :return: application/jsonContains a full representation of all visible fields in JSON.
        """
        fields = self.get_all_fields()
        custom_fields = []
        for field in fields:
            if field["custom"]:
                custom_fields.append(field)
        return custom_fields

    def project_leaders(self):
        for project in self.projects():
            key = project["key"]
            project_data = self.project(key)
            lead = self.user(project_data["lead"]["name"])
            yield {
                "project_key": key,
                "project_name": project["name"],
                "lead_name": lead["displayName"],
                "lead_key": lead["name"],
                "lead_email": lead["emailAddress"],
            }

    def get_project_issuekey_last(self, project):
        jql = "project = {project} ORDER BY issuekey DESC".format(project=project)
        return (self.jql(jql).get("issues") or {})[0]["key"]

    def get_project_issuekey_all(self, project):
        jql = "project = {project} ORDER BY issuekey ASC".format(project=project)
        return [issue["key"] for issue in self.jql(jql)["issues"]]

    def get_project_issues_count(self, project):
        jql = 'project = "{project}" '.format(project=project)
        return self.jql(jql, fields="*none")["total"]

    def get_all_project_issues(self, project, fields="*all", start=0, limit=None):
        jql = "project = {project} ORDER BY key".format(project=project)
        return self.jql(jql, fields=fields, start=start, limit=limit)["issues"]

    def get_all_assignable_users_for_project(self, project_key, start=0, limit=50):
        """
        Provide assignable users for project
        :param project_key:
        :param start: OPTIONAL: The start point of the collection to return. Default: 0.
        :param limit: OPTIONAL: The limit of the number of users to return, this may be restricted by
                fixed system limits. Default by built-in method: 50
        :return:
        """
        params = {"project": project_key, "startAt": start, "maxResults": limit}
        url = "rest/api/2/user/assignable/search"
        return self.get(url, params=params)

    def get_assignable_users_for_issue(self, issue_key, username=None, start=0, limit=50):
        """
        Provide assignable users for issue
        :param issue_key:
        :param username: OPTIONAL: Can be used to chaeck if user can be assigned
        :param start: OPTIONAL: The start point of the collection to return. Default: 0.
        :param limit: OPTIONAL: The limit of the number of users to return, this may be restricted by
                fixed system limits. Default by built-in method: 50
        :return:
        """
        params = {"issueKey": issue_key, "startAt": start, "maxResults": limit}
        if username:
            params["username"] = username
        url = "rest/api/2/user/assignable/search"
        return self.get(url)

    def get_status_id_from_name(self, status_name):
        url = "rest/api/2/status/{name}".format(name=status_name)
        return int((self.get(url) or {}).get("id"))

    def get_status_for_project(self, project_key):
        url = "rest/api/2/project/{name}/statuses".format(name=project_key)
        return self.get(url)

    def get_all_time_tracking_providers(self):
        """
        Returns all time tracking providers. By default, Jira only has one time tracking provider: JIRA provided time
        tracking. However, you can install other time tracking providers via apps from the Atlassian Marketplace.
        """
        url = "rest/api/3/configuration/timetracking/list"
        return self.get(url)

    def get_selected_time_tracking_provider(self):
        """
        Returns the time tracking provider that is currently selected. Note that if time tracking is disabled,
        then a successful but empty response is returned.
        """
        url = "rest/api/3/configuration/timetracking"
        return self.get(url)

    def get_time_tracking_settings(self):
        """
        Returns the time tracking settings. This includes settings such as the time format, default time unit,
        and others.
        """

        url = "rest/api/3/configuration/timetracking/options"
        return self.get(url)

    def get_transition_id_to_status_name(self, issue_key, status_name):
        for transition in self.get_issue_transitions(issue_key):
            if status_name.lower() == transition["to"].lower():
                return int(transition["id"])

    """
    The Link Issue Resource provides functionality to manage issue links.
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/issueLink
    """

    def create_issue_link(self, data):
        """
        Creates an issue link between two issues.
        The user requires the link issue permission for the issue which will be linked to another issue.
        The specified link type in the request is used to create the link and will create a link from
        the first issue to the second issue using the outward description. It also create a link from
        the second issue to the first issue using the inward description of the issue link type.
        It will add the supplied comment to the first issue. The comment can have a restriction who can view it.
        If group is specified, only users of this group can view this comment, if roleLevel is specified only users
        who have the specified role can view this comment.
        The user who creates the issue link needs to belong to the specified group or have the specified role.
        :param data: i.e.
        {
            "type": {"name": "Duplicate" },
            "inwardIssue": { "key": "HSP-1"},
            "outwardIssue": {"key": "MKY-1"},
            "comment": { "body": "Linked related issue!",
                         "visibility": { "type": "group", "value": "jira-software-users" }
            }
        }
        :return:
        """
        log.info(
            "Linking issue {inward} and {outward}".format(inward=data["inwardIssue"], outward=data["outwardIssue"])
        )
        url = "rest/api/2/issueLink"
        return self.post(url, data=data)

    def get_issue_link(self, link_id):
        """
        Returns an issue link with the specified id.
        :param link_id: the issue link id.
        :return:
        """
        url = "rest/api/2/issueLink/{}".format(link_id)
        return self.get(url)

    def remove_issue_link(self, link_id):
        """
        Deletes an issue link with the specified id.
        To be able to delete an issue link you must be able to view both issues
        and must have the link issue permission for at least one of the issues.
        :param link_id: the issue link id.
        :return:
        """
        url = "rest/api/2/issueLink/{}".format(link_id)
        return self.delete(url)

    """
    Rest resource to retrieve a list of issue link types.
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/issueLinkType
    """

    def get_issue_link_types(self):
        """Returns a list of available issue link types,
        if issue linking is enabled.
        Each issue link type has an id,
        a name and a label for the outward and inward link relationship.
        """
        url = "rest/api/2/issueLinkType"
        return (self.get(url) or {}).get("issueLinkTypes")

    def get_issue_link_types_names(self):
        """
        Provide issue link type names
        :return:
        """
        return [link_type["name"] for link_type in self.get_issue_link_types()]

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
        url = "rest/api/2/issueLinkType"
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
        data = {"name": link_type_name, "inward": inward, "outward": outward}
        return self.create_issue_link_type_by_json(data=data)

    def get_issue_link_type(self, issue_link_type_id):
        """Returns for a given issue link type id all information about this issue link type."""
        url = "rest/api/2/issueLinkType/{issueLinkTypeId}".format(issueLinkTypeId=issue_link_type_id)
        return self.get(url)

    def delete_issue_link_type(self, issue_link_type_id):
        """Delete the specified issue link type."""
        url = "rest/api/2/issueLinkType/{issueLinkTypeId}".format(issueLinkTypeId=issue_link_type_id)
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
        url = "rest/api/2/issueLinkType/{issueLinkTypeId}".format(issueLinkTypeId=issue_link_type_id)
        return self.put(url, data=data)

    """
    Resolution
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/resolution
    """

    def get_all_resolutions(self):
        """
        Returns a list of all resolutions.
        :return:
        """
        url = "rest/api/2/resolution"
        return self.get(url)

    def get_resolution_by_id(self, resolution_id):
        """
        Get Resolution info by id
        :param resolution_id:
        :return:
        """
        url = "rest/api/2/resolution/{}".format(resolution_id)
        return self.get(url)

    """
    Role
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/role
    """

    def get_all_global_project_roles(self):
        """
        Get all the ProjectRoles available in Jira. Currently this list is global.
        :return:
        """
        url = "rest/api/2/role"
        return self.get(url)

    """
    Screens
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/screens
    """

    def get_all_screens(self):
        """
        Get all available screens from Jira
        :return: list of json elements of screen with field id, name. description
        """
        url = "rest/api/2/screens"
        return self.get(url)

    def get_all_available_screen_fields(self, screen_id):
        """
        Get all available fields by screen id
        :param screen_id:
        :return:
        """
        url = "rest/api/2/screens/{}/availableFields".format(screen_id)
        return self.get(url)

    def get_screen_tabs(self, screen_id):
        """
        Get tabs for the screen id
        :param screen_id:
        :return:
        """
        url = "rest/api/2/screens/{}/tabs".format(screen_id)
        return self.get(url)

    def get_screen_tab_fields(self, screen_id, tab_id):
        """
        Get fields by the tab id and the screen id
        :param tab_id:
        :param screen_id:
        :return:
        """
        url = "rest/api/2/screens/{}/tabs/{}/fields".format(screen_id, tab_id)
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
            tab_id = screen_tab["id"]
            if tab_id:
                tab_fields = self.get_screen_tab_fields(screen_id=screen_id, tab_id=tab_id)
                fields = fields + tab_fields
        return fields

    """
    Search
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/search
    """

    def jql(self, jql, fields="*all", start=0, limit=None, expand=None):
        """
        Get issues from jql search result with all related fields
        :param jql:
        :param fields: list of fields, for example: ['priority', 'summary', 'customfield_10007']
        :param start: OPTIONAL: The start point of the collection to return. Default: 0.
        :param limit: OPTIONAL: The limit of the number of issues to return, this may be restricted by
                fixed system limits. Default by built-in method: 50
        :param expand: OPTIONAL: expand the search result
        :return:
        """
        params = {}
        if start is not None:
            params["startAt"] = int(start)
        if limit is not None:
            params["maxResults"] = int(limit)
        if fields is not None:
            if isinstance(fields, (list, tuple, set)):
                fields = ",".join(fields)
            params["fields"] = fields
        if jql is not None:
            params["jql"] = jql
        if expand is not None:
            params["expand"] = expand
        return self.get("rest/api/2/search", params=params)

    def csv(self, jql, limit=1000, all_fields=True, start=None, delimiter=None):
        """
            Get issues from jql search result with ALL or CURRENT fields
            default will be to return all fields
        :param jql: JQL query
        :param limit: max results in the output file
        :param all_fields: To return all fields or current fields only
        :param start: index value
        :param delimiter:
        :return: CSV file
        """

        params = {"jqlQuery": jql}
        if limit:
            params["tempMax"] = limit
        if start:
            params["pager/start"] = start
        if delimiter:
            params["delimiter"] = delimiter
        # fmt: off
        if all_fields:
            url = "sr/jira.issueviews:searchrequest-csv-all-fields/temp/SearchRequest.csv"
        else:
            url = "sr/jira.issueviews:searchrequest-csv-current-fields/temp/SearchRequest.csv"
        # fmt: on
        return self.get(
            url,
            params=params,
            not_json_response=True,
            headers={"Accept": "application/csv"},
        )

    def excel(self, jql, limit=1000, all_fields=True, start=None):
        """
            Get issues from jql search result with ALL or CURRENT fields
            default will be to return all fields
        :param jql: JQL query
        :param limit: max results in the output file
        :param all_fields: To return all fields or current fields only
        :param start: index value
        :return: CSV file
        """

        params = {"jqlQuery": jql}
        if limit:
            params["tempMax"] = limit
        if start:
            params["pager/start"] = start
        # fmt: off
        if all_fields:
            url = "sr/jira.issueviews:searchrequest-excel-all-fields/temp/SearchRequest.xls"
        else:
            url = "sr/jira.issueviews:searchrequest-excel-current-fields/temp/SearchRequest.xls"
        # fmt: on
        return self.get(
            url,
            params=params,
            not_json_response=True,
            headers={"Accept": "application/vnd.ms-excel"},
        )

    def export_html(self, jql, limit=None, all_fields=True, start=None):
        """
        Get issues from jql search result with ALL or CURRENT fields
            default will be to return all fields
        :param jql: JQL query
        :param limit: max results in the output file
        :param all_fields: To return all fields or current fields only
        :param start: index value
        :return: HTML file
        """

        params = {"jqlQuery": jql}
        if limit:
            params["tempMax"] = limit
        if start:
            params["pager/start"] = start
        # fmt: off
        if all_fields:
            url = "sr/jira.issueviews:searchrequest-html-all-fields/temp/SearchRequest.html"
        else:
            url = "sr/jira.issueviews:searchrequest-html-current-fields/temp/SearchRequest.html"
        # fmt: on
        return self.get(
            url,
            params=params,
            not_json_response=True,
            headers={"Accept": "application/xhtml+xml"},
        )

    def get_all_priorities(self):
        """
        Returns a list of all priorities.
        :return:
        """
        url = "rest/api/2/priority"
        return self.get(url)

    def get_priority_by_id(self, priority_id):
        """
        Get Priority info by id
        :param priority_id:
        :return:
        """
        url = "rest/api/2/priority/{}".format(priority_id)
        return self.get(url)

    """
    Workflow
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/workflow
    """

    def get_all_workflows(self):
        """
        Provide all workflows for application admin
        :return:
        """
        url = "rest/api/2/workflow"
        return self.get(url)

    def get_workflows_paginated(self, startAt=None, maxResults=None, workflowName=None, expand=None):
        """
        Provide all workflows paginated (see https://developer.atlassian.com/cloud/jira/platform/rest/v2/\
api-group-workflows/#api-rest-api-2-workflow-search-get)
        :param expand:
        :param startAt: OPTIONAL The index of the first item to return in a page of results (page offset).
        :param maxResults: OPTIONAL The maximum number of items to return per page.
        :param workflowName: OPTIONAL The name of a workflow to return.
        :param: expand: OPTIONAL Use expand to include additional information in the response. This parameter accepts a
            comma-separated list. Expand options include: transitions, transitions.rules, statuses, statuses.properties
        :return:
        """
        url = "rest/api/2/workflow/search"

        params = {}
        if startAt:
            params["startAt"] = startAt
        if maxResults:
            params["maxResults"] = maxResults
        if workflowName:
            params["workflowName"] = workflowName
        if expand:
            params["expand"] = expand

        return self.get(url, params=params)

    def get_all_statuses(self):
        """
        Returns a list of all statuses
        :return:
        """
        url = "rest/api/2/status"
        return self.get(url)

    def get_plugins_info(self):
        """
        Provide plugins info
        :return a json of installed plugins
        """
        url = "rest/plugins/1.0/"
        return self.get(url, headers=self.no_check_headers)

    def upload_plugin(self, plugin_path):
        """
        Provide plugin path for upload into Jira e.g. useful for auto deploy
        :param plugin_path:
        :return:
        """
        files = {"plugin": open(plugin_path, "rb")}
        upm_token = self.request(
            method="GET",
            path="rest/plugins/1.0/",
            headers=self.no_check_headers,
            trailing=True,
        ).headers["upm-token"]
        url = "rest/plugins/1.0/?token={upm_token}".format(upm_token=upm_token)
        return self.post(url, files=files, headers=self.no_check_headers)

    def delete_plugin(self, plugin_key):
        """
        Delete plugin
        :param plugin_key:
        :return:
        """
        url = "rest/plugins/1.0/{}-key".format(plugin_key)
        return self.delete(url)

    def check_plugin_manager_status(self):
        url = "rest/plugins/latest/safe-mode"
        return self.request(method="GET", path=url, headers=self.safe_mode_headers)

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
        url = "rest/api/2/permissionscheme"
        params = {}
        if expand:
            params["expand"] = expand
        return (self.get(url, params=params) or {}).get("permissionSchemes")

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
        url = "rest/api/2/permissionscheme/{schemeID}".format(schemeID=permission_id)
        params = {}
        if expand:
            params["expand"] = expand
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
        url = "rest/api/2/permissionscheme/{schemeID}/permission".format(schemeID=permission_id)

        return self.post(url, data=new_permission)

    """
    REST resource that allows to view security schemes defined in the product.
    Resource for managing priority schemes.
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/issuesecurityschemes
               https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/priorityschemes
    """

    def get_issue_security_schemes(self):
        """
        Returns all issue security schemes that are defined
        Administrator permission required

        :return: list
        """
        url = "rest/api/2/issuesecurityschemes"

        return self.get(url).get("issueSecuritySchemes")

    def get_issue_security_scheme(self, scheme_id, only_levels=False):
        """
        Returns the issue security scheme along with that are defined

        Returned if the user has the administrator permission or if the scheme is used in a project in which the
        user has the administrative permission

        :param scheme_id: int
        :param only_levels: bool
        :return: list
        """
        url = "rest/api/2/issuesecurityschemes/{}".format(scheme_id)

        if only_levels is True:
            return self.get(url).get("levels")
        else:
            return self.get(url)

    def get_project_issue_security_scheme(self, project_id_or_key, only_levels=False):
        """
        Returns the issue security scheme for project

        Returned if the user has the administrator permission or if the scheme is used in a project in which the
        user has the administrative permission

        :param project_id_or_key: int
        :param only_levels: bool
        :return: list
        """
        url = "rest/api/2/project/{}/issuesecuritylevelscheme".format(project_id_or_key)
        try:
            response = self.get(url)
        except HTTPError as e:
            if e.response.status_code == 401:
                raise ApiPermissionError("Returned if the user is not logged in.", reason=e)
            elif e.response.status_code == 403:
                raise ApiPermissionError("User doesn't have administrative permissions", reason=e)
            elif e.response.status_code == 404:
                raise ApiNotFoundError(
                    "Returned if the project does not exist, or is not visible to the calling user",
                    reason=e,
                )
            raise
        if only_levels is True and response:
            return response.get("levels") or None
        return response

    def get_all_priority_schemes(self, start=0, limit=100, expand=None):
        """
        Returns all priority schemes.
        All project keys associated with the priority scheme will only be returned
        if additional query parameter is provided expand=schemes.projectKeys.
        :param start: the page offset, if not specified then defaults to 0
        :param limit: how many results on the page should be included. Defaults to 100, maximum is 1000.
        :param expand: can be 'schemes.projectKeys'
        :return:
        """
        url = "rest/api/2/priorityschemes"
        params = {}
        if start:
            params["startAt"] = int(start)
        if limit:
            params["maxResults"] = int(limit)
        if expand:
            params["expand"] = expand
        return self.get(url, params=params)

    def create_priority_scheme(self, data):
        """
        Creates new priority scheme.
        :param data:
                {"name": "New priority scheme",
                "description": "Priority scheme for very important projects",
                "defaultOptionId": "3",
                "optionIds": [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5"
                ]}
        :return: Returned if the priority scheme was created.
        """
        return self.post(path="rest/api/2/priorityschemes", data=data)

    """
    Resource for associating priority schemes and projects.
    Reference:
        https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/project/{projectKeyOrId}/priorityscheme
    """

    def get_priority_scheme_of_project(self, project_key_or_id, expand=None):
        """
        Gets a full representation of a priority scheme in JSON format used by specified project.
        Resource for associating priority scheme schemes and projects.
        User must be global administrator or project administrator.
        :param project_key_or_id:
        :param expand: notificationSchemeEvents,user,group,projectRole,field,all
        :return:
        """
        params = {}
        if expand:
            params["expand"] = expand
        url = "rest/api/2/project/{}/priorityscheme".format(project_key_or_id)
        return self.get(url, params=params)

    def assign_priority_scheme_for_project(self, project_key_or_id, priority_scheme_id):
        """
        Assigns project with priority scheme. Priority scheme assign with migration is possible from the UI.
        Operation will fail if migration is needed as a result of operation
        eg. there are issues with priorities invalid in the destination scheme.
        All project keys associated with the priority scheme will only be returned
        if additional query parameter is provided expand=projectKeys.
        :param project_key_or_id:
        :param priority_scheme_id:
        :return:
        """
        url = "rest/api/2/project/{projectKeyOrId}/priorityscheme".format(projectKeyOrId=project_key_or_id)
        data = {"id": priority_scheme_id}
        return self.put(url, data=data)

    """
    Provide security level information of the given project for the current user.
    Reference:
        https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/project/{projectKeyOrId}/securitylevel
    """

    def get_security_level_for_project(self, project_key_or_id):
        """
        Returns all security levels for the project that the current logged in user has access to.
        If the user does not have the Set Issue Security permission, the list will be empty.
        :param project_key_or_id:
        :return: Returns a list of all security levels in a project for which the current user has access.
        """
        url = "rest/api/2/project/{projectKeyOrId}/securitylevel".format(projectKeyOrId=project_key_or_id)
        return self.get(url)

    """
    Provide project type
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/project/type
    """

    def get_all_project_types(self):
        """
        Returns all the project types defined on the Jira instance,
        not taking into account whether the license to use those project types is valid or not.
        :return: Returns a list with all the project types defined on the Jira instance.
        """
        url = "rest/api/2/project/type"
        return self.get(url)

    """
    Provide project categories
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/projectCategory
    """

    def get_all_project_categories(self):
        """
        Returns all project categories
        :return: Returns a list of project categories.
        """
        url = "rest/api/2/projectCategory"
        return self.get(url)

    """
    Project validates
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/projectvalidate
    """

    def get_project_validated_key(self, key):
        """
        Validates a project key.
        :param key: the project key
        :return:
        """
        params = {"key": key}
        url = "rest/api/2/projectvalidate/key"
        return self.get(url, params=params)

    """
    REST resource for starting/stopping/querying indexing.
    Reference: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2/reindex
    """

    def reindex(
        self,
        comments=True,
        change_history=True,
        worklogs=True,
        indexing_type="BACKGROUND_PREFERRED",
    ):
        """
        Reindex the Jira instance
        Kicks off a reindex. Need Admin permissions to perform this reindex.
        Type of re-indexing available:
        FOREGROUND - runs a lock/full reindexing
        BACKGROUND - runs a background reindexing.
                   If Jira fails to finish the background reindexing, respond with 409 Conflict (error message).
        BACKGROUND_PREFERRED  - If possible do a background reindexing.
                   If it's not possible (due to an inconsistent index), do a foreground reindexing.
        :param comments: Indicates that comments should also be reindexed. Not relevant for foreground reindex,
        where comments are always reindexed.
        :param change_history: Indicates that changeHistory should also be reindexed.
        Not relevant for foreground reindex, where changeHistory is always reindexed.
        :param worklogs: Indicates that changeHistory should also be reindexed.
        Not relevant for foreground reindex, where changeHistory is always reindexed.
        :param indexing_type: OPTIONAL: The default value for the type is BACKGROUND_PREFERRED
        :return:
        """
        params = {}
        if not comments:
            params["indexComments"] = comments
        if not change_history:
            params["indexChangeHistory"] = change_history
        if not worklogs:
            params["indexWorklogs"] = worklogs
        if not indexing_type:
            params["type"] = indexing_type
        return self.post("rest/api/2/reindex", params=params)

    def reindex_with_type(self, indexing_type="BACKGROUND_PREFERRED"):
        """
        Reindex the Jira instance
        Type of re-indexing available:
        FOREGROUND - runs a lock/full reindexing
        BACKGROUND - runs a background reindexing.
                   If Jira fails to finish the background reindexing, respond with 409 Conflict (error message).
        BACKGROUND_PREFERRED  - If possible do a background reindexing.
                   If it's not possible (due to an inconsistent index), do a foreground reindexing.
        :param indexing_type: OPTIONAL: The default value for the type is BACKGROUND_PREFERRED
        :return:
        """
        return self.reindex(indexing_type=indexing_type)

    def reindex_status(self):
        """
        Returns information on the system reindexes.
        If a reindex is currently taking place then information about this reindex is returned.
        If there is no active index task, then returns information about the latest reindex task run,
        otherwise returns a 404 indicating that no reindex has taken place.
        :return:
        """
        return self.get("rest/api/2/reindex")

    def reindex_project(self, project_key):
        return self.post(
            "secure/admin/IndexProject.jspa",
            data="confirmed=true&key={}".format(project_key),
            headers=self.form_token_headers,
        )

    def reindex_issue(self, list_of_):
        pass

    def get_server_info(self, do_health_check=False):
        """
        Returns general information about the current Jira server.
        with health checks or not.
        """
        if do_health_check:
            check = True
        else:
            check = False
        return self.get("rest/api/2/serverInfo", params={"doHealthCheck": check})

    #######################################################################
    #                   Tempo Account REST API implements
    #######################################################################
    def tempo_account_get_accounts(self, skip_archived=None, expand=None):
        """
        Get all Accounts that the logged in user has permission to browse.
        :param skip_archived: bool OPTIONAL: skip archived Accounts, either true or false, default value true.
        :param expand: bool OPTIONAL: With expanded data or not
        :return:
        """
        params = {}
        if skip_archived is not None:
            params["skipArchived"] = skip_archived
        if expand is not None:
            params["expand"] = expand
        url = "rest/tempo-accounts/1/account"
        return self.get(url, params=params)

    def tempo_account_get_accounts_by_jira_project(self, project_id):
        """
        Get Accounts by JIRA Project. The Caller must have the Browse Account permission for Account.
        This will return Accounts for which the Caller has Browse Account Permission for.
        :param project_id: str the project id.
        :return:
        """
        url = "rest/tempo-accounts/1/account/project/{}".format(project_id)
        return self.get(url)

    def tempo_account_associate_with_jira_project(
        self, account_id, project_id, default_account=False, link_type="MANUAL"
    ):
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
            data["accountId"] = account_id
        if default_account:
            data["defaultAccount"] = default_account
        if link_type:
            data["linkType"] = link_type
        if project_id:
            data["scope"] = project_id
        data["scopeType"] = "PROJECT"

        url = "rest/tempo-accounts/1/link/"
        return self.post(url, data=data)

    def tempo_account_add_account(self, data=None):
        """
        Creates Account, adding new Account requires the Manage Accounts Permission.
        :param data: String then it will convert to json
        :return:
        """
        url = "rest/tempo-accounts/1/account/"
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
        url = "rest/tempo-accounts/1/account/{id}/".format(id=account_id)
        return self.delete(url)

    def tempo_account_get_rate_table_by_account_id(self, account_id):
        """
        Returns a rate table for the specified account.
        :param account_id: the account id.
        :return:
        """
        params = {"scopeType": "ACCOUNT", "scopeId": account_id}
        url = "rest/tempo-accounts/1/ratetable"
        return self.get(url, params=params)

    def tempo_account_get_all_account_by_customer_id(self, customer_id):
        """
        Get un-archived Accounts by customer. The Caller must have the Browse Account permission for the Account.
        :param customer_id: the Customer id.
        :return:
        """
        url = "rest/tempo-accounts/1/account/customer/{customerId}/".format(customerId=customer_id)
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
            params["query"] = query
        if count_accounts is not None:
            params["countAccounts"] = count_accounts
        url = "rest/tempo-accounts/1/customer"
        return self.get(url, params=params)

    def tempo_account_add_new_customer(self, key, name):
        """
        Gets all or some Attribute whose key or name contain a specific substring.
        Attributes can be a Category or Customer.
        :param key:
        :param name:
        :return: if error will show in error log, like validation unsuccessful. If success will good.
        """
        data = {"name": name, "key": key}
        url = "rest/tempo-accounts/1/customer"
        return self.post(url, data=data)

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
        url = "rest/tempo-accounts/1/customer"
        return self.post(url, data=data)

    def tempo_account_get_customer_by_id(self, customer_id=1):
        """
        Get Account Attribute whose key or name contain a specific substring. Attribute can be a Category or Customer.
        :param customer_id: id of Customer record
        :return: Customer info
        """
        url = "rest/tempo-accounts/1/customer/{id}".format(id=customer_id)
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
        url = "rest/tempo-accounts/1/customer/{id}".format(id=customer_id)
        return self.put(url, data=data)

    def tempo_account_delete_customer_by_id(self, customer_id=1):
        """
        Delete an Attribute. Caller must have Manage Account Permission. Attribute can be a Category or Customer.
        :param customer_id: id of Customer record
        :return: Customer info
        """
        url = "rest/tempo-accounts/1/customer/{id}".format(id=customer_id)
        return self.delete(url)

    def tempo_account_export_accounts(self):
        """
        Get csv export file of Accounts from Tempo
        :return: csv file
        """
        headers = self.form_token_headers
        url = "rest/tempo-accounts/1/export"
        return self.get(url, headers=headers, not_json_response=True)

    def tempo_holiday_get_schemes(self):
        """
        Provide a holiday schemes
        :return:
        """
        url = "rest/tempo-core/2/holidayschemes/"
        return self.get(url)

    def tempo_holiday_get_scheme_info(self, scheme_id):
        """
        Provide a holiday scheme
        :return:
        """
        url = "rest/tempo-core/2/holidayschemes/{}".format(scheme_id)
        return self.get(url)

    def tempo_holiday_get_scheme_members(self, scheme_id):
        """
        Provide a holiday scheme members
        :return:
        """
        url = "rest/tempo-core/2/holidayschemes/{}/members".format(scheme_id)
        return self.get(url)

    def tempo_holiday_put_into_scheme_member(self, scheme_id, username):
        """
        Provide a holiday scheme
        :return:
        """
        url = "rest/tempo-core/2/holidayschemes/{}/member/{}/".format(scheme_id, username)
        data = {"id": scheme_id}
        return self.put(url, data=data)

    def tempo_holiday_scheme_set_default(self, scheme_id):
        """
        Set as default the holiday scheme
        :param scheme_id:
        :return:
        """
        # @deprecated available in private mode the 1 version
        # url = 'rest/tempo-core/1/holidayscheme/setDefault/{}'.format(scheme_id)

        url = "rest/tempo-core/2/holidayscheme/setDefault/{}".format(scheme_id)
        data = {"id": scheme_id}
        return self.post(url, data=data)

    def tempo_workload_scheme_get_members(self, scheme_id):
        """
        Provide a workload scheme members
        :param scheme_id:
        :return:
        """
        url = "rest/tempo-core/1/workloadscheme/users/{}".format(scheme_id)
        return self.get(url)

    def tempo_workload_scheme_set_member(self, scheme_id, member):
        """
        Provide a workload scheme members
        :param member: user name of user
        :param scheme_id:
        :return:
        """
        url = "rest/tempo-core/1/workloadscheme/user/{}".format(member)
        data = {"id": scheme_id}
        return self.put(url, data=data)

    def tempo_timesheets_get_configuration(self):
        """
        Provide the configs of timesheets
        :return:
        """
        url = "rest/tempo-timesheets/3/private/config/"
        return self.get(url)

    def tempo_timesheets_get_team_utilization(self, team_id, date_from, date_to=None, group_by=None):
        """
        Get team utilization. Response in json
        :param team_id:
        :param date_from:
        :param date_to:
        :param group_by:
        :return:
        """
        url = "rest/tempo-timesheets/3/report/team/{}/utilization".format(team_id)
        params = {"dateFrom": date_from, "dateTo": date_to}

        if group_by:
            params["groupBy"] = group_by
        return self.get(url, params=params)

    def tempo_timesheets_get_worklogs(
        self,
        date_from=None,
        date_to=None,
        username=None,
        project_key=None,
        account_key=None,
        team_id=None,
    ):
        """

        :param date_from: yyyy-MM-dd
        :param date_to: yyyy-MM-dd
        :param username: name of the user you wish to get the worklogs for
        :param project_key: key of a project you wish to get the worklogs for
        :param account_key: key of an account you wish to get the worklogs for
        :param team_id: id of the Team you wish to get the worklogs for
        :return:
        """
        params = {}
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        if username:
            params["username"] = username
        if project_key:
            params["projectKey"] = project_key
        if account_key:
            params["accountKey"] = account_key
        if team_id:
            params["teamId"] = team_id
        url = "rest/tempo-timesheets/3/worklogs/"
        return self.get(url, params=params)

    def tempo_4_timesheets_find_worklogs(self, **params):
        """
        Find existing worklogs with searching parameters.
        NOTE: check if you are using correct types for the parameters!
        :param from: string From Date
        :param to: string To Date
        :param worker: Array of strings
        :param taskId: Array of integers
        :param taskKey: Array of strings
        :param projectId: Array of integers
        :param projectKey: Array of strings
        :param teamId: Array of integers
        :param roleId: Array of integers
        :param accountId: Array of integers
        :param accountKey: Array of strings
        :param filterId: Array of integers
        :param customerId: Array of integers
        :param categoryId: Array of integers
        :param categoryTypeId: Array of integers
        :param epicKey: Array of strings
        :param updatedFrom: string
        :param includeSubtasks: boolean
        :param pageNo: integer
        :param maxResults: integer
        :param offset: integer
        """

        url = "rest/tempo-timesheets/4/worklogs/search"
        return self.post(url, data=params)

    def tempo_timesheets_get_worklogs_by_issue(self, issue):
        """
        Get Tempo timesheet worklog by issue key or id.
        :param issue: Issue key or Id
        :return:
        """
        url = "rest/tempo-timesheets/4/worklogs/jira/issue/{issue}".format(issue=issue)
        return self.get(url)

    def tempo_timesheets_write_worklog(self, worker, started, time_spend_in_seconds, issue_id, comment=None):
        """
        Log work for user
        :param worker:
        :param started:
        :param time_spend_in_seconds:
        :param issue_id:
        :param comment:
        :return:
        """
        data = {
            "worker": worker,
            "started": started,
            "timeSpentSeconds": time_spend_in_seconds,
            "originTaskId": str(issue_id),
        }
        if comment:
            data["comment"] = comment
        url = "rest/tempo-timesheets/4/worklogs/"
        return self.post(url, data=data)

    def tempo_timesheets_approval_worklog_report(self, user_key, period_start_date):
        """
        Return timesheets for approval
        :param user_key:
        :param period_start_date:
        :return:
        """
        url = "rest/tempo-timesheets/4/timesheet-approval/current"
        params = {}
        if period_start_date:
            params["periodStartDate"] = period_start_date
        if user_key:
            params["userKey"] = user_key
        return self.get(url, params=params)

    def tempo_timesheets_get_required_times(self, from_date, to_date, user_name):
        """
        Provide time how much should work
        :param from_date:
        :param to_date:
        :param user_name:
        :return:
        """
        url = "rest/tempo-timesheets/3/private/days"
        params = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if user_name:
            params["user"] = user_name
        return self.get(url, params=params)

    def tempo_timesheets_approval_status(self, period_start_date, user_name):
        url = "rest/tempo-timesheets/4/timesheet-approval/approval-statuses"
        params = {}
        if user_name:
            params["userKey"] = user_name
        if period_start_date:
            params["periodStartDate"] = period_start_date
        return self.get(url, params=params)

    def tempo_get_links_to_project(self, project_id):
        """
        Gets all links to a specific project
        :param project_id:
        :return:
        """
        url = "rest/tempo-accounts/1/link/project/{}/".format(project_id)
        return self.get(url)

    def tempo_get_default_link_to_project(self, project_id):
        """
        Gets the default link to a specific project
        :param project_id:
        :return:
        """
        url = "rest/tempo-accounts/1/link/project/{}/default/".format(project_id)
        return self.get(url)

    def tempo_teams_get_all_teams(self, expand=None):
        url = "rest/tempo-teams/2/team"
        params = {}
        if expand:
            params["expand"] = expand
        return self.get(url, params=params)

    def tempo_teams_add_member(self, team_id, member_key):
        """
        Add team member
        :param team_id:
        :param member_key: user_name or user_key of Jira
        :return:
        """
        data = {
            "member": {"key": str(member_key), "type": "USER"},
            "membership": {"availability": "100", "role": {"id": 1}},
        }
        return self.tempo_teams_add_member_raw(team_id, member_data=data)

    def tempo_teams_add_membership(self, team_id, member_id):
        """
        Add team member
        :param team_id:
        :param member_id:
        :return:
        """
        data = {
            "teamMemberId": member_id,
            "teamId": team_id,
            "availability": "100",
            "role": {"id": 1},
        }
        url = "rest/tempo-teams/2/team/{}/member/{}/membership".format(team_id, member_id)
        return self.post(url, data=data)

    def tempo_teams_add_member_raw(self, team_id, member_data):
        """
        Add team member
        :param team_id:
        :param member_data:
        :return:
        """
        url = "rest/tempo-teams/2/team/{}/member/".format(team_id)
        data = member_data
        return self.post(url, data=data)

    def tempo_teams_get_members(self, team_id):
        """
        Get members from team
        :param team_id:
        :return:
        """
        url = "rest/tempo-teams/2/team/{}/member/".format(team_id)
        return self.get(url)

    def tempo_teams_remove_member(self, team_id, member_id, membership_id):
        """
        Remove team membership
        :param team_id:
        :param member_id:
        :param membership_id:
        :return:
        """
        url = "rest/tempo-teams/2/team/{}/member/{}/membership/{}".format(team_id, member_id, membership_id)
        return self.delete(url)

    def tempo_teams_update_member_information(self, team_id, member_id, membership_id, data):
        """
        Update team membership attribute info
        :param team_id:
        :param member_id:
        :param membership_id:
        :param data:
        :return:
        """
        url = "rest/tempo-teams/2/team/{}/member/{}/membership/{}".format(team_id, member_id, membership_id)
        return self.put(url, data=data)

    def tempo_timesheets_get_period_configuration(self):
        return self.get("rest/tempo-timesheets/3/period-configuration")

    def tempo_timesheets_get_private_configuration(self):
        return self.get("rest/tempo-timesheets/3/private/config")

    def tempo_teams_get_memberships_for_member(self, username):
        return self.get("rest/tempo-teams/2/user/{}/memberships".format(username))

    #######################################################################
    #   Agile(Formerly Greenhopper) REST API implements
    #   Resource: https://docs.atlassian.com/jira-software/REST/7.3.1/
    #######################################################################
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
        url = "rest/agile/1.0/board"
        params = {}
        if board_name:
            params["name"] = board_name
        if project_key:
            params["projectKeyOrId"] = project_key
        if board_type:
            params["type"] = board_type
        if start:
            params["startAt"] = int(start)
        if limit:
            params["maxResults"] = int(limit)

        return self.get(url, params=params)

    def get_agile_board(self, board_id):
        """
        Get agile board info by id
        :param board_id:
        :return:
        """
        url = "rest/agile/1.0/board/{}".format(str(board_id))
        return self.get(url)

    def create_agile_board(self, name, type, filter_id, location=None):
        """
        Create an agile board
        :param name: str
        :param type: str, scrum or kanban
        :param filter_id: int
        :param location: dict, Optional. Default is user
        """
        data = {"name": name, "type": type, "filterId": filter_id}
        if location:
            data["location"] = location
        else:
            data["location"] = {"type": "user"}
        url = "rest/agile/1.0/board"
        return self.post(url, data=data)

    def get_agile_board_by_filter_id(self, filter_id):
        """
        Gets an agile board by the filter id
        :param filter_id: int, str
        """
        url = "rest/agile/1.0/board/filter/{filter_id}".format(filter_id=filter_id)
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
        url = "rest/agile/1.0/board/{}/configuration".format(str(board_id))
        return self.get(url)

    def get_issues_for_backlog(self, board_id):
        """
        :param board_id: int, str
        """
        url = "rest/agile/1.0/{board_id}/backlog".format(board_id=board_id)
        return self.get(url)

    def delete_agile_board(self, board_id):
        """
        Delete agile board by id
        :param board_id:
        :return:
        """
        url = "rest/agile/1.0/board/{}".format(str(board_id))
        return self.delete(url)

    def get_agile_board_properties(self, board_id):
        """
        Gets a list of all the board properties
        :param board_id: int, str
        """
        url = "rest/agile/1.0/board/{board_id}/properties".format(board_id=board_id)
        return self.get(url)

    def create_sprint(self, name, board_id, start_date=None, end_date=None, goal=None):
        """
        Create a sprint within a board.
        ! User requires `Manage Sprints` permission for relevant boards.

        :param name: str: Name for the Sprint to be created
        :param board_id: int: The ID for the Board in which the Sprint will be created
        :param start_date: str: The Start Date for Sprint in isoformat
                            example value is "2015-04-11T15:22:00.000+10:00"
        :param end_date: str: The End Date for Sprint in isoformat
                            example value is "2015-04-20T01:22:00.000+10:00"
        :param goal: str: Goal Text for setting for the Sprint
        :return: Dictionary of response received from the API

        https://docs.atlassian.com/jira-software/REST/8.9.0/#agile/1.0/sprint
        isoformat can be created with datetime.datetime.isoformat()
        """
        url = "/rest/agile/1.0/sprint"
        data = dict(name=name, originBoardId=board_id)
        if start_date:
            data["startDate"] = start_date
        if end_date:
            data["endDate"] = end_date
        if goal:
            data["goal"] = goal
        return self.post(url, data=data)

    def add_issues_to_sprint(self, sprint_id, issues):
        """
        Adding Issue(s) to Sprint
        :param sprint_id: int/str:  The ID for the Sprint.
                                    Sprint to be Active or Open only.
                                    eg.  104
        :param issues:       list:  List of Issue Keys
                                    eg. ['APA-1', 'APA-2']
        :return: Dictionary of response received from the API

        https://docs.atlassian.com/jira-software/REST/8.9.0/#agile/1.0/sprint-moveIssuesToSprint
        """
        if not isinstance(issues, list):
            raise ValueError("`issues` param should be List of Issue Keys")
        url = "/rest/agile/1.0/sprint/{sprint_id}/issue".format(sprint_id=sprint_id)
        data = dict(issues=issues)
        return self.post(url, data=data)

    def get_all_sprint(self, board_id, state=None, start=0, limit=50):
        """
        Returns all sprints from a board, for a given board Id.
        This only includes sprints that the user has permission to view.
        :param board_id:
        :param state: Filters results to sprints in specified states.
                      Valid values: future, active, closed.
                      You can define multiple states separated by commas, e.g. state=active,closed
        :param start: The starting index of the returned sprints.
                      Base index: 0.
                      See the 'Pagination' section at the top of this page for more details.
        :param limit: The maximum number of sprints to return per page.
                      Default: 50.
                      See the 'Pagination' section at the top of this page for more details.
        :return:
        """
        params = {}
        if start:
            params["startAt"] = start
        if limit:
            params["maxResults"] = limit
        if state:
            params["state"] = state
        url = "rest/agile/1.0/board/{boardId}/sprint".format(boardId=board_id)
        return self.get(url, params=params)

    def get_sprint(self, sprint_id):
        """
        Returns the sprint for a given sprint Id.
        The sprint will only be returned if the user can view the board that the sprint was created on,
        or view at least one of the issues in the sprint.
        :param sprint_id:
        :return:
        """
        url = "rest/agile/1.0/sprint/{sprintId}".format(sprintId=sprint_id)
        return self.get(url)

    def rename_sprint(self, sprint_id, name, start_date, end_date):
        """

        :param sprint_id:
        :param name:
        :param start_date:
        :param end_date:
        :return:
        """
        return self.put(
            "rest/greenhopper/1.0/sprint/{0}".format(sprint_id),
            data={"name": name, "startDate": start_date, "endDate": end_date},
        )

    def delete_sprint(self, sprint_id):
        """
        Deletes a sprint.
        Once a sprint is deleted, all issues in the sprint will be moved to the backlog.
        Note, only future sprints can be deleted.
        :param sprint_id:
        :return:
        """
        return self.delete("rest/agile/1.0/sprint/{sprintId}".format(sprintId=sprint_id))

    def update_partially_sprint(self, sprint_id, data):
        """
        Performs a partial update of a sprint.
        A partial update means that fields not present in the request JSON will not be updated.
        Notes:

        Sprints that are in a closed state cannot be updated.
        A sprint can be started by updating the state to 'active'.
        This requires the sprint to be in the 'future' state and have a startDate and endDate set.
        A sprint can be completed by updating the state to 'closed'.
        This action requires the sprint to be in the 'active' state.
        This sets the completeDate to the time of the request.
        Other changes to state are not allowed.
        The completeDate field cannot be updated manually.
        :param sprint_id:
        :param data: { "name": "new name"}
        :return:
        """
        return self.post("rest/agile/1.0/sprint/{}".format(sprint_id), data=data)

    def get_sprint_issues(self, sprint_id, start, limit):
        """
        Returns all issues in a sprint, for a given sprint Id.
        This only includes issues that the user has permission to view.
        By default, the returned issues are ordered by rank.
        :param sprint_id:
        :param start: The starting index of the returned issues.
                      Base index: 0.
                      See the 'Pagination' section at the top of this page for more details.
        :param limit: The maximum number of issues to return per page.
                      Default: 50.
                      See the 'Pagination' section at the top of this page for more details.
                      Note, the total number of issues returned is limited by the property
                      'jira.search.views.default.max' in your Jira instance.
                      If you exceed this limit, your results will be truncated.
        :return:
        """
        params = {}
        if start:
            params["startAt"] = start
        if limit:
            params["maxResults"] = limit
        url = "rest/agile/1.0/sprint/{sprintId}/issue".format(sprintId=sprint_id)
        return self.get(url, params=params)

    def update_rank(self, issues_to_rank, rank_before, customfield_number):
        """
        Updates the rank of issues (max 50), placing them before a given issue.
        :param issues_to_rank: List of issues to rank (max 50)
        :param rank_before: Issue that the issues will be put over
        :param customfield_number: The number of the custom field Rank
        :return:
        """
        return self.put(
            "rest/agile/1.0/issue/rank",
            data={
                "issues": issues_to_rank,
                "rankBeforeIssue": rank_before,
                "rankCustomFieldId": customfield_number,
            },
        )

    def health_check(self):
        """
        Get health status
        https://confluence.atlassian.com/jirakb/how-to-retrieve-health-check-results-using-rest-api-867195158.html
        :return:
        """
        # check as Troubleshooting & Support Tools Plugin
        response = self.get("rest/troubleshooting/1.0/check/")
        if not response:
            # check as support tools
            response = self.get("rest/supportHealthCheck/1.0/check/")
        return response
