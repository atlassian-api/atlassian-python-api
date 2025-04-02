"""
Adapter for Jira Projects providing backward compatibility with the original Jira client
"""

import logging
import warnings
from typing import Optional, List, Dict, Any, Union

from atlassian.jira.cloud.projects import ProjectsJira


class ProjectsJiraAdapter(ProjectsJira):
    """
    Adapter for Jira Projects providing backward compatibility with the original Jira client
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._legacy_method_map = {
            "projects": "get_all_projects",
            "project": "get_project",
            "project_components": "get_project_components",
            "component": "get_component",
            "create_component": "create_component",
            "update_component": "update_component",
            "delete_component": "delete_component",
            "project_versions": "get_project_versions",
            "create_version": "create_version",
            "update_version": "update_version",
            "delete_version": "delete_version",
            "project_roles": "get_project_roles",
            "project_role": "get_project_role",
        }

    def projects(self, expand=None):
        """
        Get all projects with optional expansion

        Deprecated in favor of get_all_projects
        
        :param expand: List of fields to expand
        :return: List of projects
        """
        warnings.warn(
            "Method projects is deprecated, use get_all_projects instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_all_projects(expand=expand)

    def project(self, key):
        """
        Get project by key

        Deprecated in favor of get_project
        
        :param key: Project key
        :return: Project details
        """
        warnings.warn(
            "Method project is deprecated, use get_project instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_project(key)

    def create_project(self, key, name, project_type=None, template_name=None, description=""):
        """
        Create project

        Deprecated in favor of the newer create_project method with more parameters
        
        :param key: Project key
        :param name: Project name
        :param project_type: Project type key
        :param template_name: Project template key
        :param description: Project description
        :return: Created project
        """
        warnings.warn(
            "This version of create_project is deprecated, use the newer method with additional parameters",
            DeprecationWarning,
            stacklevel=2,
        )
        return super().create_project(
            key=key,
            name=name,
            project_type_key=project_type or "software",
            project_template_key=template_name or "com.pyxis.greenhopper.jira:gh-scrum-template",
            description=description,
        )

    def delete_project(self, key):
        """
        Delete project

        Equivalent to the new delete_project method
        
        :param key: Project key
        :return: None
        """
        return super().delete_project(key)

    def project_components(self, key):
        """
        Get project components

        Deprecated in favor of get_project_components
        
        :param key: Project key
        :return: List of components
        """
        warnings.warn(
            "Method project_components is deprecated, use get_project_components instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_project_components(key)

    def component(self, component_id):
        """
        Get component by ID

        Deprecated in favor of get_component
        
        :param component_id: Component ID
        :return: Component details
        """
        warnings.warn(
            "Method component is deprecated, use get_component instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_component(component_id)

    def create_component(self, component):
        """
        Create component

        Deprecated in favor of the more explicit create_component method
        
        :param component: Dictionary containing component details
        :return: Created component
        """
        warnings.warn(
            "Method create_component with dictionary parameter is deprecated, use the newer method with explicit parameters",
            DeprecationWarning,
            stacklevel=2,
        )
        
        project_key = component.get("project")
        name = component.get("name")
        description = component.get("description")
        lead_account_id = component.get("leadAccountId") or component.get("lead")
        assignee_type = component.get("assigneeType")
        assignee_account_id = component.get("assigneeAccountId")
        
        return super().create_component(
            project_key=project_key,
            name=name,
            description=description,
            lead_account_id=lead_account_id,
            assignee_type=assignee_type,
            assignee_account_id=assignee_account_id,
        )

    def update_component(self, component_id, component):
        """
        Update component

        Deprecated in favor of the more explicit update_component method
        
        :param component_id: Component ID
        :param component: Dictionary containing component details to update
        :return: Updated component
        """
        warnings.warn(
            "Method update_component with dictionary parameter is deprecated, use the newer method with explicit parameters",
            DeprecationWarning,
            stacklevel=2,
        )
        
        name = component.get("name")
        description = component.get("description")
        lead_account_id = component.get("leadAccountId") or component.get("lead")
        assignee_type = component.get("assigneeType")
        assignee_account_id = component.get("assigneeAccountId")
        project_key = component.get("project")
        
        return super().update_component(
            component_id=component_id,
            name=name,
            description=description,
            lead_account_id=lead_account_id,
            assignee_type=assignee_type,
            assignee_account_id=assignee_account_id,
            project_key=project_key,
        )

    def delete_component(self, component_id):
        """
        Delete component

        Equivalent to the new delete_component method
        
        :param component_id: Component ID
        :return: None
        """
        return super().delete_component(component_id)

    def project_versions(self, key):
        """
        Get project versions

        Deprecated in favor of get_project_versions
        
        :param key: Project key
        :return: List of versions
        """
        warnings.warn(
            "Method project_versions is deprecated, use get_project_versions instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_project_versions(key)

    def create_version(self, version):
        """
        Create version

        Deprecated in favor of the more explicit create_version method
        
        :param version: Dictionary containing version details
        :return: Created version
        """
        warnings.warn(
            "Method create_version with dictionary parameter is deprecated, use the newer method with explicit parameters",
            DeprecationWarning,
            stacklevel=2,
        )
        
        project = version.get("project")
        name = version.get("name")
        description = version.get("description")
        start_date = version.get("startDate")
        release_date = version.get("releaseDate")
        released = version.get("released")
        archived = version.get("archived")
        
        return super().create_version(
            project_id_or_key=project,
            name=name,
            description=description,
            start_date=start_date,
            release_date=release_date,
            released=released,
            archived=archived,
        )

    def update_version(self, version_id, version):
        """
        Update version

        Deprecated in favor of the more explicit update_version method
        
        :param version_id: Version ID
        :param version: Dictionary containing version details to update
        :return: Updated version
        """
        warnings.warn(
            "Method update_version with dictionary parameter is deprecated, use the newer method with explicit parameters",
            DeprecationWarning,
            stacklevel=2,
        )
        
        name = version.get("name")
        description = version.get("description")
        project_id = version.get("projectId")
        start_date = version.get("startDate")
        release_date = version.get("releaseDate")
        released = version.get("released")
        archived = version.get("archived")
        
        return super().update_version(
            version_id=version_id,
            name=name,
            description=description,
            project_id=project_id,
            start_date=start_date,
            release_date=release_date,
            released=released,
            archived=archived,
        )

    def delete_version(self, version_id):
        """
        Delete version

        Equivalent to the new delete_version method
        
        :param version_id: Version ID
        :return: None
        """
        return super().delete_version(version_id)

    def project_roles(self, project_key):
        """
        Get project roles

        Deprecated in favor of get_project_roles
        
        :param project_key: Project key
        :return: Dictionary of roles
        """
        warnings.warn(
            "Method project_roles is deprecated, use get_project_roles instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_project_roles(project_key)

    def project_role(self, project_key, role_id):
        """
        Get project role

        Deprecated in favor of get_project_role
        
        :param project_key: Project key
        :param role_id: Role ID
        :return: Role details
        """
        warnings.warn(
            "Method project_role is deprecated, use get_project_role instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_project_role(project_key, role_id)

    def add_user_to_project_role(self, project_key, role_id, user_id, user_type="atlassian-user-role-actor"):
        """
        Add user to project role

        Deprecated in favor of add_actors_to_project_role
        
        :param project_key: Project key
        :param role_id: Role ID
        :param user_id: User ID or account ID
        :param user_type: User type
        :return: Role details
        """
        warnings.warn(
            "Method add_user_to_project_role is deprecated, use add_actors_to_project_role instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.add_actors_to_project_role(project_key, role_id, user_account_ids=[user_id])

    def add_group_to_project_role(self, project_key, role_id, group_name):
        """
        Add group to project role

        Deprecated in favor of add_actors_to_project_role
        
        :param project_key: Project key
        :param role_id: Role ID
        :param group_name: Group name or ID
        :return: Role details
        """
        warnings.warn(
            "Method add_group_to_project_role is deprecated, use add_actors_to_project_role instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.add_actors_to_project_role(project_key, role_id, group_ids=[group_name])

    def delete_user_from_project_role(self, project_key, role_id, user_id):
        """
        Delete user from project role

        Deprecated in favor of remove_actor_from_project_role
        
        :param project_key: Project key
        :param role_id: Role ID
        :param user_id: User ID
        :return: None
        """
        warnings.warn(
            "Method delete_user_from_project_role is deprecated, use remove_actor_from_project_role instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.remove_actor_from_project_role(project_key, role_id, user_account_id=user_id)

    def delete_group_from_project_role(self, project_key, role_id, group_name):
        """
        Delete group from project role

        Deprecated in favor of remove_actor_from_project_role
        
        :param project_key: Project key
        :param role_id: Role ID
        :param group_name: Group name
        :return: None
        """
        warnings.warn(
            "Method delete_group_from_project_role is deprecated, use remove_actor_from_project_role instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.remove_actor_from_project_role(project_key, role_id, group_id=group_name) 