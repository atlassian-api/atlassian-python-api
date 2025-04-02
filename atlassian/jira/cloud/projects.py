"""
Jira Cloud API for advanced project configuration operations
"""

from atlassian.jira.cloud.cloud_base import CloudJira


class ProjectsJira(CloudJira):
    """
    Jira Cloud API for working with advanced project configurations
    """

    def get_all_projects(self, expand=None, recent=None, properties=None):
        """
        Get all projects with optional expansion and filtering

        :param expand: List of fields to expand (description, lead, issueTypes, url, projectKeys, etc.)
        :param recent: Limit to projects recently accessed by the current user
        :param properties: List of project properties to include
        :return: List of projects
        """
        url = "rest/api/3/project"
        params = {}
        
        if expand:
            if isinstance(expand, list):
                params["expand"] = ",".join(expand)
            else:
                params["expand"] = expand
        
        if recent is not None:
            params["recent"] = recent
        
        if properties:
            if isinstance(properties, list):
                params["properties"] = ",".join(properties)
            else:
                params["properties"] = properties
        
        return self.get(url, params=params)

    def get_project(self, project_id_or_key, expand=None, properties=None):
        """
        Get project by ID or key

        :param project_id_or_key: Project ID or key
        :param expand: List of fields to expand
        :param properties: List of project properties to include
        :return: Project details
        """
        url = f"rest/api/3/project/{project_id_or_key}"
        params = {}
        
        if expand:
            if isinstance(expand, list):
                params["expand"] = ",".join(expand)
            else:
                params["expand"] = expand
        
        if properties:
            if isinstance(properties, list):
                params["properties"] = ",".join(properties)
            else:
                params["properties"] = properties
        
        return self.get(url, params=params)

    def create_project(self, key, name, project_type_key, project_template_key, 
                       description=None, lead_account_id=None, url=None, 
                       assignee_type=None, avatar_id=None, issue_security_scheme=None, 
                       permission_scheme=None, notification_scheme=None, 
                       category_id=None, workflow_scheme=None, issue_type_scheme=None,
                       issue_type_screen_scheme=None, field_configuration_scheme=None):
        """
        Create a new project

        :param key: Project key
        :param name: Project name
        :param project_type_key: The project type
        :param project_template_key: The project template key
        :param description: Project description
        :param lead_account_id: User account ID for the project lead
        :param url: Project URL
        :param assignee_type: Assignee type (PROJECT_LEAD, UNASSIGNED)
        :param avatar_id: Avatar ID
        :param issue_security_scheme: Issue security scheme ID
        :param permission_scheme: Permission scheme ID
        :param notification_scheme: Notification scheme ID
        :param category_id: Project category ID
        :param workflow_scheme: Workflow scheme ID
        :param issue_type_scheme: Issue type scheme ID
        :param issue_type_screen_scheme: Issue type screen scheme ID
        :param field_configuration_scheme: Field configuration scheme ID
        :return: Created project
        """
        url = "rest/api/3/project"
        data = {
            "key": key,
            "name": name,
            "projectTypeKey": project_type_key,
            "projectTemplateKey": project_template_key,
        }
        
        if description:
            data["description"] = description
        
        if lead_account_id:
            data["leadAccountId"] = lead_account_id
        
        if url:
            data["url"] = url
        
        if assignee_type:
            data["assigneeType"] = assignee_type
        
        if avatar_id:
            data["avatarId"] = avatar_id
        
        if issue_security_scheme:
            data["issueSecurityScheme"] = issue_security_scheme
        
        if permission_scheme:
            data["permissionScheme"] = permission_scheme
        
        if notification_scheme:
            data["notificationScheme"] = notification_scheme
        
        if category_id:
            data["categoryId"] = category_id
            
        if workflow_scheme:
            data["workflowScheme"] = workflow_scheme
            
        if issue_type_scheme:
            data["issueTypeScheme"] = issue_type_scheme
            
        if issue_type_screen_scheme:
            data["issueTypeScreenScheme"] = issue_type_screen_scheme
            
        if field_configuration_scheme:
            data["fieldConfigurationScheme"] = field_configuration_scheme
        
        return self.post(url, data=data)

    def update_project(self, project_id_or_key, name=None, key=None, description=None, 
                      lead_account_id=None, url=None, assignee_type=None, 
                      avatar_id=None, issue_security_scheme=None, permission_scheme=None, 
                      notification_scheme=None, category_id=None):
        """
        Update an existing project

        :param project_id_or_key: Project ID or key
        :param name: New project name
        :param key: New project key
        :param description: New project description
        :param lead_account_id: New project lead account ID
        :param url: New project URL
        :param assignee_type: New assignee type
        :param avatar_id: New avatar ID
        :param issue_security_scheme: New issue security scheme
        :param permission_scheme: New permission scheme
        :param notification_scheme: New notification scheme
        :param category_id: New project category
        :return: Updated project
        """
        url = f"rest/api/3/project/{project_id_or_key}"
        data = {}
        
        if name:
            data["name"] = name
        
        if key:
            data["key"] = key
        
        if description:
            data["description"] = description
        
        if lead_account_id:
            data["leadAccountId"] = lead_account_id
        
        if url:
            data["url"] = url
        
        if assignee_type:
            data["assigneeType"] = assignee_type
        
        if avatar_id:
            data["avatarId"] = avatar_id
        
        if issue_security_scheme:
            data["issueSecurityScheme"] = issue_security_scheme
        
        if permission_scheme:
            data["permissionScheme"] = permission_scheme
        
        if notification_scheme:
            data["notificationScheme"] = notification_scheme
        
        if category_id:
            data["categoryId"] = category_id
        
        return self.put(url, data=data)

    def delete_project(self, project_id_or_key):
        """
        Delete a project

        :param project_id_or_key: Project ID or key
        :return: None
        """
        url = f"rest/api/3/project/{project_id_or_key}"
        return self.delete(url)

    def archive_project(self, project_id_or_key):
        """
        Archive a project

        :param project_id_or_key: Project ID or key
        :return: None
        """
        url = f"rest/api/3/project/{project_id_or_key}/archive"
        return self.put(url, data={})

    def restore_project(self, project_id_or_key):
        """
        Restore an archived project

        :param project_id_or_key: Project ID or key
        :return: Project details
        """
        url = f"rest/api/3/project/{project_id_or_key}/restore"
        return self.put(url, data={})

    def get_project_components(self, project_id_or_key):
        """
        Get all components for a project

        :param project_id_or_key: Project ID or key
        :return: List of components
        """
        url = f"rest/api/3/project/{project_id_or_key}/components"
        return self.get(url)

    def create_component(self, project_key, name, description=None, lead_account_id=None, 
                         assignee_type=None, assignee_account_id=None):
        """
        Create a project component

        :param project_key: Project key
        :param name: Component name
        :param description: Component description
        :param lead_account_id: Lead user account ID
        :param assignee_type: Assignee type (PROJECT_LEAD, COMPONENT_LEAD, UNASSIGNED, PROJECT_DEFAULT)
        :param assignee_account_id: Assignee user account ID
        :return: Created component
        """
        url = "rest/api/3/component"
        data = {
            "project": project_key,
            "name": name,
        }
        
        if description:
            data["description"] = description
        
        if lead_account_id:
            data["leadAccountId"] = lead_account_id
        
        if assignee_type:
            data["assigneeType"] = assignee_type
        
        if assignee_account_id:
            data["assigneeAccountId"] = assignee_account_id
        
        return self.post(url, data=data)

    def get_component(self, component_id):
        """
        Get component by ID

        :param component_id: Component ID
        :return: Component details
        """
        url = f"rest/api/3/component/{component_id}"
        return self.get(url)

    def update_component(self, component_id, name=None, description=None, 
                        lead_account_id=None, assignee_type=None, 
                        assignee_account_id=None, project_key=None):
        """
        Update a component

        :param component_id: Component ID
        :param name: New name
        :param description: New description
        :param lead_account_id: New lead user account ID
        :param assignee_type: New assignee type
        :param assignee_account_id: New assignee user account ID
        :param project_key: New project key
        :return: Updated component
        """
        url = f"rest/api/3/component/{component_id}"
        data = {}
        
        if name:
            data["name"] = name
        
        if description:
            data["description"] = description
        
        if lead_account_id:
            data["leadAccountId"] = lead_account_id
        
        if assignee_type:
            data["assigneeType"] = assignee_type
        
        if assignee_account_id:
            data["assigneeAccountId"] = assignee_account_id
        
        if project_key:
            data["project"] = project_key
        
        return self.put(url, data=data)

    def delete_component(self, component_id, move_issues_to=None):
        """
        Delete a component

        :param component_id: Component ID
        :param move_issues_to: Move issues to this component ID
        :return: None
        """
        url = f"rest/api/3/component/{component_id}"
        params = {}
        
        if move_issues_to:
            params["moveIssuesTo"] = move_issues_to
        
        return self.delete(url, params=params)

    def get_project_versions(self, project_id_or_key, expand=None):
        """
        Get all versions for a project

        :param project_id_or_key: Project ID or key
        :param expand: List of fields to expand (operations)
        :return: List of versions
        """
        url = f"rest/api/3/project/{project_id_or_key}/versions"
        params = {}
        
        if expand:
            if isinstance(expand, list):
                params["expand"] = ",".join(expand)
            else:
                params["expand"] = expand
        
        return self.get(url, params=params)

    def create_version(self, project_id_or_key, name, description=None, 
                       start_date=None, release_date=None, released=None, 
                       archived=None):
        """
        Create a project version

        :param project_id_or_key: Project ID or key
        :param name: Version name
        :param description: Version description
        :param start_date: Start date (ISO format YYYY-MM-DD)
        :param release_date: Release date (ISO format YYYY-MM-DD)
        :param released: Whether the version is released
        :param archived: Whether the version is archived
        :return: Created version
        """
        url = "rest/api/3/version"
        data = {
            "project": project_id_or_key,
            "name": name,
        }
        
        if description:
            data["description"] = description
        
        if start_date:
            data["startDate"] = start_date
        
        if release_date:
            data["releaseDate"] = release_date
        
        if released is not None:
            data["released"] = released
        
        if archived is not None:
            data["archived"] = archived
        
        return self.post(url, data=data)

    def get_version(self, version_id, expand=None):
        """
        Get version by ID

        :param version_id: Version ID
        :param expand: List of fields to expand
        :return: Version details
        """
        url = f"rest/api/3/version/{version_id}"
        params = {}
        
        if expand:
            if isinstance(expand, list):
                params["expand"] = ",".join(expand)
            else:
                params["expand"] = expand
        
        return self.get(url, params=params)

    def update_version(self, version_id, name=None, description=None, 
                      project_id=None, start_date=None, release_date=None, 
                      released=None, archived=None):
        """
        Update a version

        :param version_id: Version ID
        :param name: New name
        :param description: New description
        :param project_id: New project ID
        :param start_date: New start date (ISO format YYYY-MM-DD)
        :param release_date: New release date (ISO format YYYY-MM-DD)
        :param released: New released status
        :param archived: New archived status
        :return: Updated version
        """
        url = f"rest/api/3/version/{version_id}"
        data = {}
        
        if name:
            data["name"] = name
        
        if description:
            data["description"] = description
        
        if project_id:
            data["projectId"] = project_id
        
        if start_date:
            data["startDate"] = start_date
        
        if release_date:
            data["releaseDate"] = release_date
        
        if released is not None:
            data["released"] = released
        
        if archived is not None:
            data["archived"] = archived
        
        return self.put(url, data=data)

    def delete_version(self, version_id, move_fix_issues_to=None, 
                      move_affected_issues_to=None):
        """
        Delete a version

        :param version_id: Version ID
        :param move_fix_issues_to: Move fix version issues to this version ID
        :param move_affected_issues_to: Move affected version issues to this version ID
        :return: None
        """
        url = f"rest/api/3/version/{version_id}"
        params = {}
        
        if move_fix_issues_to:
            params["moveFixIssuesTo"] = move_fix_issues_to
        
        if move_affected_issues_to:
            params["moveAffectedIssuesTo"] = move_affected_issues_to
        
        return self.delete(url, params=params)

    def get_project_roles(self, project_id_or_key):
        """
        Get all roles for a project

        :param project_id_or_key: Project ID or key
        :return: Dictionary of roles
        """
        url = f"rest/api/3/project/{project_id_or_key}/role"
        return self.get(url)

    def get_project_role(self, project_id_or_key, role_id):
        """
        Get a project role

        :param project_id_or_key: Project ID or key
        :param role_id: Role ID
        :return: Role details
        """
        url = f"rest/api/3/project/{project_id_or_key}/role/{role_id}"
        return self.get(url)

    def set_actors_to_project_role(self, project_id_or_key, role_id, 
                                  user_account_ids=None, group_ids=None):
        """
        Set actors to a project role

        :param project_id_or_key: Project ID or key
        :param role_id: Role ID
        :param user_account_ids: List of user account IDs
        :param group_ids: List of group IDs
        :return: Role details
        """
        url = f"rest/api/3/project/{project_id_or_key}/role/{role_id}"
        data = {}
        
        if user_account_ids:
            data["categorisedActors"] = {"atlassian-user-role-actor": user_account_ids}
        
        if group_ids:
            if "categorisedActors" not in data:
                data["categorisedActors"] = {}
            data["categorisedActors"]["atlassian-group-role-actor"] = group_ids
        
        return self.put(url, data=data)

    def add_actors_to_project_role(self, project_id_or_key, role_id, 
                                  user_account_ids=None, group_ids=None):
        """
        Add actors to a project role

        :param project_id_or_key: Project ID or key
        :param role_id: Role ID
        :param user_account_ids: List of user account IDs to add
        :param group_ids: List of group IDs to add
        :return: Role details
        """
        url = f"rest/api/3/project/{project_id_or_key}/role/{role_id}"
        data = {}
        
        if user_account_ids:
            data["categorisedActors"] = {"atlassian-user-role-actor": user_account_ids}
        
        if group_ids:
            if "categorisedActors" not in data:
                data["categorisedActors"] = {}
            data["categorisedActors"]["atlassian-group-role-actor"] = group_ids
        
        return self.post(url, data=data)

    def remove_actor_from_project_role(self, project_id_or_key, role_id, 
                                      user_account_id=None, group_id=None):
        """
        Remove an actor from a project role

        :param project_id_or_key: Project ID or key
        :param role_id: Role ID
        :param user_account_id: User account ID to remove
        :param group_id: Group ID to remove
        :return: None
        """
        url = f"rest/api/3/project/{project_id_or_key}/role/{role_id}"
        params = {}
        
        if user_account_id:
            params["user"] = user_account_id
        
        if group_id:
            params["group"] = group_id
        
        return self.delete(url, params=params) 