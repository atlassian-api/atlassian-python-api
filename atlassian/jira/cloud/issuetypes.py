"""
Jira Cloud API for working with issue types and field configurations
"""

from atlassian.jira.cloud.cloud import CloudJira


class IssueTypesJira(CloudJira):
    """
    Jira Cloud API for working with issue types and field configurations
    """

    def get_all_issue_types(self):
        """
        Get all issue types from Jira

        :return: List of issue types
        """
        url = "rest/api/3/issuetype"
        return self.get(url)

    def get_issue_type(self, issue_type_id):
        """
        Get issue type by ID

        :param issue_type_id: Issue type ID
        :return: Issue type details
        """
        url = f"rest/api/3/issuetype/{issue_type_id}"
        return self.get(url)

    def create_issue_type(self, name, description=None, type="standard", scope_id=None):
        """
        Create a new issue type

        :param name: Name of the issue type
        :param description: Description of the issue type
        :param type: Type of the issue type (standard, subtask)
        :param scope_id: Project context if this issue type is for a next-gen project
        :return: Created issue type
        """
        url = "rest/api/3/issuetype"
        data = {
            "name": name,
            "type": type,
        }

        if description:
            data["description"] = description

        if scope_id:
            data["scope"] = {"type": "PROJECT", "project": {"id": scope_id}}

        return self.post(url, data=data)

    def update_issue_type(self, issue_type_id, name=None, description=None, avatar_id=None):
        """
        Update an issue type

        :param issue_type_id: Issue type ID
        :param name: New name for the issue type
        :param description: New description for the issue type
        :param avatar_id: New avatar ID for the issue type
        :return: Updated issue type
        """
        url = f"rest/api/3/issuetype/{issue_type_id}"
        data = {}

        if name:
            data["name"] = name

        if description:
            data["description"] = description

        if avatar_id:
            data["avatarId"] = avatar_id

        return self.put(url, data=data)

    def delete_issue_type(self, issue_type_id, alternative_issue_type_id=None):
        """
        Delete an issue type

        :param issue_type_id: ID of the issue type to delete
        :param alternative_issue_type_id: If provided, issues with the deleted issue type are migrated
                                         to this issue type
        :return: None
        """
        params = {}
        if alternative_issue_type_id:
            params["alternativeIssueTypeId"] = alternative_issue_type_id

        url = f"rest/api/3/issuetype/{issue_type_id}"
        return self.delete(url, params=params)

    def get_issue_type_property_keys(self, issue_type_id):
        """
        Get issue type property keys

        :param issue_type_id: Issue type ID
        :return: Property keys for the issue type
        """
        url = f"rest/api/3/issuetype/{issue_type_id}/properties"
        return self.get(url)

    def get_issue_type_property(self, issue_type_id, property_key):
        """
        Get issue type property

        :param issue_type_id: Issue type ID
        :param property_key: Property key
        :return: Property value
        """
        url = f"rest/api/3/issuetype/{issue_type_id}/properties/{property_key}"
        return self.get(url)

    def set_issue_type_property(self, issue_type_id, property_key, value):
        """
        Set issue type property

        :param issue_type_id: Issue type ID
        :param property_key: Property key
        :param value: Property value
        :return: None
        """
        url = f"rest/api/3/issuetype/{issue_type_id}/properties/{property_key}"
        return self.put(url, data=value)

    def delete_issue_type_property(self, issue_type_id, property_key):
        """
        Delete issue type property

        :param issue_type_id: Issue type ID
        :param property_key: Property key
        :return: None
        """
        url = f"rest/api/3/issuetype/{issue_type_id}/properties/{property_key}"
        return self.delete(url)

    def get_issue_type_schemes(self, start_at=0, max_results=50, id=None):
        """
        Get issue type schemes

        :param start_at: Index of the first item to return
        :param max_results: Maximum number of items to return
        :param id: Filter by scheme IDs
        :return: List of issue type schemes
        """
        url = "rest/api/3/issuetypescheme"
        params = {
            "startAt": start_at,
            "maxResults": max_results,
        }

        if id:
            if isinstance(id, list):
                params["id"] = ",".join(map(str, id))
            else:
                params["id"] = str(id)

        return self.get(url, params=params)

    def create_issue_type_scheme(self, name, description=None, default_issue_type_id=None, issue_type_ids=None):
        """
        Create a new issue type scheme

        :param name: Name of the scheme
        :param description: Description of the scheme
        :param default_issue_type_id: Default issue type ID for the scheme
        :param issue_type_ids: List of issue type IDs in the scheme
        :return: Created issue type scheme
        """
        url = "rest/api/3/issuetypescheme"
        data = {
            "name": name,
        }

        if description:
            data["description"] = description

        if default_issue_type_id:
            data["defaultIssueTypeId"] = default_issue_type_id

        if issue_type_ids:
            data["issueTypeIds"] = issue_type_ids

        return self.post(url, data=data)

    def get_issue_type_scheme_mapping(self, scheme_id):
        """
        Get issue type scheme mapping

        :param scheme_id: Issue type scheme ID
        :return: Mapping of issue types in the scheme
        """
        url = f"rest/api/3/issuetypescheme/{scheme_id}/mapping"
        return self.get(url)

    def add_issue_types_to_scheme(self, scheme_id, issue_type_ids):
        """
        Add issue types to a scheme

        :param scheme_id: Issue type scheme ID
        :param issue_type_ids: List of issue type IDs to add
        :return: None
        """
        url = f"rest/api/3/issuetypescheme/{scheme_id}/issuetype"
        data = {"issueTypeIds": issue_type_ids}
        return self.put(url, data=data)

    def remove_issue_type_from_scheme(self, scheme_id, issue_type_id):
        """
        Remove issue type from scheme

        :param scheme_id: Issue type scheme ID
        :param issue_type_id: Issue type ID to remove
        :return: None
        """
        url = f"rest/api/3/issuetypescheme/{scheme_id}/issuetype/{issue_type_id}"
        return self.delete(url)

    def get_field_configurations(self, start_at=0, max_results=50, ids=None):
        """
        Get field configurations

        :param start_at: Index of the first item to return
        :param max_results: Maximum number of items to return
        :param ids: Filter by field configuration IDs
        :return: List of field configurations
        """
        url = "rest/api/3/fieldconfiguration"
        params = {
            "startAt": start_at,
            "maxResults": max_results,
        }

        if ids:
            if isinstance(ids, list):
                params["id"] = ",".join(map(str, ids))
            else:
                params["id"] = str(ids)

        return self.get(url, params=params)

    def create_field_configuration(self, name, description=None):
        """
        Create a field configuration

        :param name: Name of the field configuration
        :param description: Description of the field configuration
        :return: Created field configuration
        """
        url = "rest/api/3/fieldconfiguration"
        data = {
            "name": name,
        }

        if description:
            data["description"] = description

        return self.post(url, data=data)

    def update_field_configuration(self, field_config_id, name, description=None):
        """
        Update a field configuration

        :param field_config_id: Field configuration ID
        :param name: New name for the field configuration
        :param description: New description for the field configuration
        :return: None
        """
        url = f"rest/api/3/fieldconfiguration/{field_config_id}"
        data = {
            "name": name,
        }

        if description:
            data["description"] = description

        return self.put(url, data=data)

    def delete_field_configuration(self, field_config_id):
        """
        Delete a field configuration

        :param field_config_id: Field configuration ID to delete
        :return: None
        """
        url = f"rest/api/3/fieldconfiguration/{field_config_id}"
        return self.delete(url)

    def get_field_configuration_items(self, field_config_id, start_at=0, max_results=50):
        """
        Get field configuration items

        :param field_config_id: Field configuration ID
        :param start_at: Index of the first item to return
        :param max_results: Maximum number of items to return
        :return: List of field configuration items
        """
        url = f"rest/api/3/fieldconfiguration/{field_config_id}/fields"
        params = {
            "startAt": start_at,
            "maxResults": max_results,
        }
        return self.get(url, params=params)

    def update_field_configuration_items(self, field_config_id, field_configurations):
        """
        Update field configuration items

        :param field_config_id: Field configuration ID
        :param field_configurations: List of field configurations to update
        :return: None
        """
        url = f"rest/api/3/fieldconfiguration/{field_config_id}/fields"
        data = {"fieldConfigurationItems": field_configurations}
        return self.put(url, data=data)

    def get_all_fields(self, include_system=True, include_custom=True):
        """
        Get all fields

        :param include_system: Include system fields
        :param include_custom: Include custom fields
        :return: List of fields
        """
        url = "rest/api/3/field"
        params = {}
        if not include_system:
            params["type"] = "custom"
        if not include_custom:
            params["type"] = "system"

        return self.get(url, params=params)

    def create_custom_field(self, name, description, type, search_key=None, project_ids=None, issue_type_ids=None):
        """
        Create a custom field

        :param name: Name of the custom field
        :param description: Description of the custom field
        :param type: Custom field type key
        :param search_key: Search key for the custom field
        :param project_ids: List of project IDs where the field will be available
        :param issue_type_ids: List of issue type IDs where the field will be available
        :return: Created custom field
        """
        url = "rest/api/3/field"
        data = {
            "name": name,
            "description": description,
            "type": type,
        }

        if search_key:
            data["searcherKey"] = search_key

        context_data = {}
        if project_ids:
            context_data["projectIds"] = project_ids

        if issue_type_ids:
            context_data["issueTypeIds"] = issue_type_ids

        if context_data:
            data["scope"] = context_data

        return self.post(url, data=data)
