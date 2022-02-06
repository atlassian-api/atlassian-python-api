# coding=utf-8
import logging

from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class ServiceDesk(AtlassianRestAPI):
    """
    JIRA ServiceDesk API object
    """

    # Information actions
    def get_info(self):
        """Get info about Service Desk app"""

        return self.get("rest/servicedeskapi/info", headers=self.experimental_headers)

    def get_service_desks(self):
        """
        Returns all service desks in the Jira Service Desk application
        with the option to include archived service desks

        :return: Service Desks
        """
        service_desks_list = self.get("rest/servicedeskapi/servicedesk", headers=self.experimental_headers)
        if self.advanced_mode:
            return service_desks_list
        else:
            return (service_desks_list or {}).get("values")

    def get_service_desk_by_id(self, service_desk_id):
        """
        Returns the service desk for a given service desk ID

        :param service_desk_id: str
        :return: Service Desk
        """

        return self.get(
            "rest/servicedeskapi/servicedesk/{}".format(service_desk_id),
            headers=self.experimental_headers,
        )

    # Customers actions
    def create_customer(self, full_name, email):
        """
        Creating customer user

        :param full_name: str
        :param email: str
        :return: New customer
        """
        log.warning("Creating customer...")
        data = {"fullName": full_name, "email": email}

        return self.post("rest/servicedeskapi/customer", headers=self.experimental_headers, data=data)

    def get_customer_request(self, issue_id_or_key):
        """
        Get single request

        :param issue_id_or_key: str
        :return: Customer request
        """

        return self.get(
            "rest/servicedeskapi/request/{}".format(issue_id_or_key),
            headers=self.experimental_headers,
        )

    def get_my_customer_requests(self):
        """Returning requests where you are the assignee"""
        response = self.get("rest/servicedeskapi/request", headers=self.experimental_headers)
        if self.advanced_mode:
            return response
        return (response or {}).get("values")

    def create_customer_request(
        self,
        service_desk_id,
        request_type_id,
        values_dict,
        raise_on_behalf_of=None,
        request_participants=None,
    ):
        """
        Creating customer request

        :param service_desk_id: str
        :param request_type_id: str
        :param values_dict: str/dict
        :param raise_on_behalf_of: str
        :param request_participants: list
        :return: New request
        """
        log.warning("Creating request...")
        data = {
            "serviceDeskId": service_desk_id,
            "requestTypeId": request_type_id,
            "requestFieldValues": values_dict,
        }

        if raise_on_behalf_of:
            data["raiseOnBehalfOf"] = raise_on_behalf_of

        if request_participants:
            data["requestParticipants"] = request_participants

        param_map = {"headers": self.experimental_headers}

        if isinstance(values_dict, dict):
            param_map["json"] = data
        elif isinstance(values_dict, str):
            param_map["data"] = data

        return self.post("rest/servicedeskapi/request", **param_map)

    def get_customer_request_status(self, issue_id_or_key):
        """
        Get customer request status name

        :param issue_id_or_key: str
        :return: Status name
        """
        request = self.get(
            "rest/servicedeskapi/request/{}/status".format(issue_id_or_key),
            headers=self.experimental_headers,
        )
        if self.advanced_mode:
            return request
        if request:
            if request.get("values", []):
                return request.get("values", [])[0].get("status", {})
        return {}

    def get_customer_transitions(self, issue_id_or_key):
        """
        Returns a list of transitions that customers can perform on the request

        :param issue_id_or_key: str
        :return:
        """
        url = "rest/servicedeskapi/request/{}/transition".format(issue_id_or_key)

        return self.get(url, headers=self.experimental_headers)

    def get_request_types(self, service_desk_id):
        """
        Gets request types

        :param service_desk_id: str
        :return: all service desk request types
        """

        return self.get(
            "rest/servicedeskapi/servicedesk/{}/requesttype".format(service_desk_id),
            headers=self.experimental_headers,
        )

    # Participants actions
    def get_request_participants(self, issue_id_or_key, start=0, limit=50):
        """
        Get request participants

        :param issue_id_or_key: str
        :param start: OPTIONAL: int
        :param limit: OPTIONAL: int
        :return: Request participants
        """
        url = "rest/servicedeskapi/request/{}/participant".format(issue_id_or_key)
        params = {}
        if start is not None:
            params["start"] = int(start)
        if limit is not None:
            params["limit"] = int(limit)

        response = self.get(url, params=params, headers=self.experimental_headers)
        if self.advanced_mode:
            return response
        return (response or {}).get("values")

    def add_request_participants(self, issue_id_or_key, users_list):
        """
        Add users as participants to an existing customer request
        The calling user must have permission to manage participants for this customer request

        :param issue_id_or_key: str
        :param users_list: list
        :return:
        """
        url = "rest/servicedeskapi/request/{}/participant".format(issue_id_or_key)
        data = {"usernames": users_list}

        return self.post(url, data=data, headers=self.experimental_headers)

    def remove_request_participants(self, issue_id_or_key, users_list):
        """
        Remove participants from an existing customer request
        The calling user must have permission to manage participants for this customer request

        :param issue_id_or_key: str
        :param users_list: list
        :return:
        """
        url = "rest/servicedeskapi/request/{}/participant".format(issue_id_or_key)
        data = {"usernames": users_list}

        return self.delete(url, data=data, headers=self.experimental_headers)

    # Transitions actions
    def perform_transition(self, issue_id_or_key, transition_id, comment=None):
        """
        Perform a customer transition for a given request and transition ID.
        An optional comment can be included to provide a reason for the transition.

        :param issue_id_or_key: str
        :param transition_id: str
        :param comment: OPTIONAL: str
        :return: None
        """
        log.warning("Performing transition...")
        data = {"id": transition_id, "additionalComment": {"body": comment}}
        url = "rest/servicedeskapi/request/{}/transition".format(issue_id_or_key)

        return self.post(url, headers=self.experimental_headers, data=data)

    # Comments actions
    def create_request_comment(self, issue_id_or_key, body, public=True):
        """
        Creating request comment

        :param issue_id_or_key: str
        :param body: str
        :param public: OPTIONAL: bool (default is True)
        :return: New comment
        """
        log.warning("Creating comment...")
        data = {"body": body, "public": public}
        url = "rest/servicedeskapi/request/{}/comment".format(issue_id_or_key)

        return self.post(path=url, data=data, headers=self.experimental_headers)

    def get_request_comments(self, issue_id_or_key):
        """
        Get all comments in issue

        :param issue_id_or_key: str
        :return: Issue comments
        """

        return self.get(
            "rest/servicedeskapi/request/{}/comment".format(issue_id_or_key),
            headers=self.experimental_headers,
        )

    def get_request_comment_by_id(self, issue_id_or_key, comment_id):
        """
        Get single comment by ID

        :param issue_id_or_key: str
        :param comment_id: str
        :return: Single comment
        """

        return self.get(
            "rest/servicedeskapi/request/{}/comment/{}".format(issue_id_or_key, comment_id),
            headers=self.experimental_headers,
        )

    # Organizations actions
    def get_organisations(self, service_desk_id=None, start=0, limit=50):
        """
        Returns a list of organizations in the Jira instance. If the user is not an agent,
        the resource returns a list of organizations the user is a member of.

        :param service_desk_id: OPTIONAL: str Get organizations from single Service Desk
        :param start: OPTIONAL: int The starting index of the returned objects.
                     Base index: 0. See the Pagination section for more details.
        :param limit: OPTIONAL: int The maximum number of users to return per page.
                     Default: 50. See the Pagination section for more details.
        :return:
        """
        url_without_sd_id = "rest/servicedeskapi/organization"
        url_with_sd_id = "rest/servicedeskapi/servicedesk/{}/organization".format(service_desk_id)
        params = {}
        if start is not None:
            params["start"] = int(start)
        if limit is not None:
            params["limit"] = int(limit)

        if service_desk_id is None:
            return self.get(url_without_sd_id, headers=self.experimental_headers, params=params)
        return self.get(url_with_sd_id, headers=self.experimental_headers, params=params)

    def get_organization(self, organization_id):
        """
        Get an organization for a given organization ID

        :param organization_id: str
        :return: Organization
        """
        url = "rest/servicedeskapi/organization/{}".format(organization_id)

        return self.get(url, headers=self.experimental_headers)

    def get_users_in_organization(self, organization_id, start=0, limit=50):
        """
        Get all the users of a specified organization

        :param organization_id: str
        :param start: OPTIONAL: int
        :param limit: OPTIONAL: int
        :return: Users list in organization
        """
        url = "rest/servicedeskapi/organization/{}/user".format(organization_id)
        params = {}
        if start is not None:
            params["start"] = int(start)
        if limit is not None:
            params["limit"] = int(limit)

        return self.get(url, headers=self.experimental_headers, params=params)

    def create_organization(self, name):
        """
        To create an organization Jira administrator global or agent
        permission is required depending on the settings

        :param name: str
        :return: Organization data
        """
        log.warning("Creating organization...")
        url = "rest/servicedeskapi/organization"
        data = {"name": name}

        return self.post(url, headers=self.experimental_headers, data=data)

    def add_organization(self, service_desk_id, organization_id):
        """
        Adds an organization to a servicedesk for a given servicedesk ID and organization ID

        :param service_desk_id: str
        :param organization_id: int
        :return:
        """
        log.warning("Adding organization...")
        url = "rest/servicedeskapi/servicedesk/{}/organization".format(service_desk_id)
        data = {"organizationId": organization_id}

        return self.post(url, headers=self.experimental_headers, data=data)

    def remove_organization(self, service_desk_id, organization_id):
        """
        Removes an organization from a servicedesk for a given servicedesk ID and organization ID

        :param service_desk_id: str
        :param organization_id: int
        :return:
        """
        log.warning("Removing organization...")
        url = "rest/servicedeskapi/servicedesk/{}/organization".format(service_desk_id)
        data = {"organizationId": organization_id}

        return self.delete(url, headers=self.experimental_headers, data=data)

    def delete_organization(self, organization_id):
        """
        Deletes an organization for a given organization ID

        :param organization_id:
        :return:
        """
        log.warning("Deleting organization...")
        url = "rest/servicedeskapi/organization/{}".format(organization_id)

        return self.delete(url, headers=self.experimental_headers)

    def add_users_to_organization(self, organization_id, users_list=[], account_list=[]):
        """
        Adds users to an organization
        users_list is a list of strings
        account_list is a list of accountIds

        :param account_list:
        :param organization_id: str
        :param users_list: list
        :return:
        """
        log.warning("Adding users...")
        url = "rest/servicedeskapi/organization/{}/user".format(organization_id)
        data = {"usernames": users_list, "accountIds": account_list}

        return self.post(url, headers=self.experimental_headers, data=data)

    def remove_users_from_organization(self, organization_id, users_list=[], account_list=[]):
        """
        Removes users from an organization
        users_list is a list of strings
        account_list is a list of accountIds

        :param organization_id: str
        :param users_list: list
        :param account_list: list
        :return:
        """
        log.warning("Removing users...")
        url = "rest/servicedeskapi/organization/{}/user".format(organization_id)
        data = {"usernames": users_list, "accountIds": account_list}

        return self.delete(url, headers=self.experimental_headers, data=data)

    # Attachments actions
    def create_attachments(self, service_desk_id, issue_id_or_key, filenames, public=True, comment=None):
        """
        Add attachment as a comment.
        Setting attachment visibility is dependent on the user's permission. For example,
        Agents can create either public or internal attachments,
        while Unlicensed users can only create internal attachments,
        and Customers can only create public attachments.
        An additional comment may be provided which will be prepended to the attachments.
        :param service_desk_id: str
        :param issue_id_or_key: str
        :param filenames: Union(List[str], str), name, if file in current directory or full path to file
        :param public: OPTIONAL: bool (default is True)
        :param comment: OPTIONAL: str (default is None)
        :return: Request info
        """
        # Create temporary attachment
        temp_attachment_ids = []
        if not isinstance(filenames, list):
            filenames = [filenames]

        for filename in filenames:
            temp_attachment_id = self.attach_temporary_file(service_desk_id, filename)
            temp_attachment_ids.append(temp_attachment_id)

        # Add attachments
        return self.add_attachments(issue_id_or_key, temp_attachment_ids, public, comment)

    def create_attachment(self, service_desk_id, issue_id_or_key, filename, public=True, comment=None):
        """
        Add attachment as a comment.
        Setting attachment visibility is dependent on the user's permission. For example,
        Agents can create either public or internal attachments,
        while Unlicensed users can only create internal attachments,
        and Customers can only create public attachments.
        An additional comment may be provided which will be prepended to the attachments.
        :param service_desk_id: str
        :param issue_id_or_key: str
        :param filename: str, name, if file in current directory or full path to file
        :param public: OPTIONAL: bool (default is True)
        :param comment: OPTIONAL: str (default is None)
        :return: Request info
        """
        log.info("Creating attachment...")
        return self.create_attachments(service_desk_id, issue_id_or_key, filename, public=public, comment=comment)

    def attach_temporary_file(self, service_desk_id, filename):
        """
        Create temporary attachment, which can later be converted into permanent attachment
        :param service_desk_id: str
        :param filename: str
        :return: Temporary Attachment ID
        """
        url = "rest/servicedeskapi/servicedesk/{}/attachTemporaryFile".format(service_desk_id)

        # no application/json content type and an additional X-Atlassian-Token header
        # https://docs.atlassian.com/jira-servicedesk/REST/4.14.1/#servicedeskapi/servicedesk/{serviceDeskId}/attachTemporaryFile-attachTemporaryFile
        experimental_headers = self.experimental_headers.copy()
        del experimental_headers["Content-Type"]
        experimental_headers["X-Atlassian-Token"] = "no-check"

        with open(filename, "rb") as file:
            result = self.post(path=url, headers=experimental_headers, files={"file": file}).get("temporaryAttachments")
            temp_attachment_id = result[0].get("temporaryAttachmentId")

            return temp_attachment_id

    def add_attachments(self, issue_id_or_key, temp_attachment_ids, public=True, comment=None):
        """
        Adds temporary attachment to customer request using attach_temporary_file function
        :param issue_id_or_key: str
        :param temp_attachment_ids: List[str], ID from result attach_temporary_file function
        :param public: bool (default is True)
        :param comment: str (default is None)
        :return:
        """
        data = {
            "temporaryAttachmentIds": temp_attachment_ids,
            "public": public,
            "additionalComment": {"body": comment},
        }
        url = "rest/servicedeskapi/request/{}/attachment".format(issue_id_or_key)

        return self.post(url, headers=self.experimental_headers, data=data)

    def add_attachment(self, issue_id_or_key, temp_attachment_id, public=True, comment=None):
        """
        Adds temporary attachment to customer request using attach_temporary_file function
        :param issue_id_or_key: str
        :param temp_attachment_id: str, ID from result attach_temporary_file function
        :param public: bool (default is True)
        :param comment: str (default is None)
        :return:
        """
        log.info("Adding attachment")
        return self.add_attachments(issue_id_or_key, [temp_attachment_id], public=public, comment=comment)

    # SLA actions
    def get_sla(self, issue_id_or_key, start=0, limit=50):
        """
        Get the SLA information for a customer request for a given request ID or key
        A request can have zero or more SLA values
        IMPORTANT: The calling user must be an agent

        :param issue_id_or_key: str
        :param start: OPTIONAL: int
        :param limit: OPTIONAL: int
        :return: SLA information
        """
        url = "rest/servicedeskapi/request/{}/sla".format(issue_id_or_key)
        params = {}
        if start is not None:
            params["start"] = int(start)
        if limit is not None:
            params["limit"] = int(limit)

        response = self.get(url, params=params, headers=self.experimental_headers)
        if self.advanced_mode:
            return response
        return (response or {}).get("values")

    def get_sla_by_id(self, issue_id_or_key, sla_id):
        """
        Get customer request SLA information for given request ID or key and SLA metric ID
        IMPORTANT: The calling user must be an agent

        :param issue_id_or_key: str
        :param sla_id: str
        :return: SLA information
        """
        url = "rest/servicedeskapi/request/{0}/sla/{1}".format(issue_id_or_key, sla_id)

        return self.get(url, headers=self.experimental_headers)

    # Approvals

    def get_approvals(self, issue_id_or_key, start=0, limit=50):
        """
        Get all approvals on a request, for a given request ID/Key

        :param issue_id_or_key: str
        :param start: OPTIONAL: int
        :param limit: OPTIONAL: int
        :return:
        """
        url = "rest/servicedeskapi/request/{}/approval".format(issue_id_or_key)
        params = {}
        if start is not None:
            params["start"] = int(start)
        if limit is not None:
            params["limit"] = int(limit)

        response = self.get(url, headers=self.experimental_headers, params=params)
        if self.advanced_mode:
            return response
        return (response or {}).get("values")

    def get_approval_by_id(self, issue_id_or_key, approval_id):
        """
        Get an approval for a given approval ID

        :param issue_id_or_key: str
        :param approval_id: str
        :return:
        """
        url = "rest/servicedeskapi/request/{0}/approval/{1}".format(issue_id_or_key, approval_id)

        return self.get(url, headers=self.experimental_headers)

    def answer_approval(self, issue_id_or_key, approval_id, decision):
        """
        Answer a pending approval

        :param issue_id_or_key: str
        :param approval_id: str
        :param decision: str
        :return:
        """
        url = "rest/servicedeskapi/request/{0}/approval/{1}".format(issue_id_or_key, approval_id)
        data = {"decision": decision}

        return self.post(url, headers=self.experimental_headers, data=data)

    def get_queue_settings(self, project_key):
        """
        Get queue settings on project

        :param project_key: str
        :return:
        """
        url = "rest/servicedeskapi/queues/{}".format(project_key)

        return self.get(url, headers=self.experimental_headers)

    def get_customers(self, service_desk_id, query=None, start=0, limit=50):
        """
        Returns a list of the customers on a service desk.

        The returned list of customers can be filtered using the query parameter.
        The parameter is matched against customers' displayName, name, or email.
        For example, searching for "John", "Jo", "Smi", or "Smith" will match a
        user with display name "John Smith"..

        :param query:
        :param start:
        :param limit:
        :param service_desk_id: str
        :return: the customers added to the service desk
        """
        url = "rest/servicedeskapi/servicedesk/{}/customer".format(service_desk_id)
        params = {}
        if start is not None:
            params["start"] = int(start)
        if limit is not None:
            params["limit"] = int(limit)
        if query is not None:
            params["query"] = query

        return self.get(url, headers=self.experimental_headers, params=params)

    def add_customers(self, service_desk_id, list_of_usernames=[], list_of_accountids=[]):
        """
        Adds one or more existing customers to the given service desk.
        If you need to create a customer, see Create customer method.

        Administer project permission is required, or agents if public signups
        and invites are enabled for the Service Desk project.

        :param service_desk_id: str
        :param list_of_usernames: list
        :param list_of_accountids: list
        :return: the customers added to the service desk
        """
        url = "rest/servicedeskapi/servicedesk/{}/customer".format(service_desk_id)
        data = {"usernames": list_of_usernames, "accountIds": list_of_accountids}

        log.info("Adding customers...")
        return self.post(url, headers=self.experimental_headers, data=data)

    def remove_customers(self, service_desk_id, list_of_usernames=[], list_of_accountids=[]):
        """
        Removes one or more customers from a service desk. The service
        desk must have closed access. If any of the passed customers are
        not associated with the service desk, no changes will be made for
        those customers and the resource returns a 204 success code.

        :param service_desk_id: str
        :param list_of_usernames: list
        :param list_of_accountids: list
        :return: the customers added to the service desk
        """
        url = "rest/servicedeskapi/servicedesk/{}/customer".format(service_desk_id)
        data = {"usernames": list_of_usernames, "accountIds": list_of_accountids}

        log.info("Removing customers...")
        return self.delete(url, headers=self.experimental_headers, data=data)

    def get_queues(self, service_desk_id, include_count=False, start=0, limit=50):
        """
        Returns a page of queues defined inside a service desk, for a given service desk ID.
        The returned queues will include issue counts for each queue (issueCount field)
        if the query param includeCount is set to true (default=false).

        Permissions: The calling user must be an agent of the given service desk.

        :param service_desk_id: str
        :param include_count: bool
        :param start: int
        :param limit: int
        :return: a page of queues
        """
        url = "rest/servicedeskapi/servicedesk/{}/queue".format(service_desk_id)
        params = {}

        if include_count is not None:
            params["includeCount"] = bool(include_count)
        if start is not None:
            params["start"] = int(start)
        if limit is not None:
            params["limit"] = int(limit)

        return self.get(url, headers=self.experimental_headers, params=params)

    def get_issues_in_queue(self, service_desk_id, queue_id, start=0, limit=50):
        """
        Returns a page of issues inside a queue for a given queue ID.
        Only fields that the queue is configured to show are returned.
        For example, if a queue is configured to show only Description and Due Date,
        then only those two fields are returned for each issue in the queue.

        Permissions: The calling user must have permission to view the requested queue,
        i.e. they must be an agent of the service desk that the queue belongs to.

        :param service_desk_id: str
        :param queue_id: str
        :param start: int
        :param limit: int
        :return: a page of issues
        """
        url = "rest/servicedeskapi/servicedesk/{0}/queue/{1}/issue".format(service_desk_id, queue_id)
        params = {}

        if start is not None:
            params["start"] = int(start)
        if limit is not None:
            params["limit"] = int(limit)

        return self.get(url, headers=self.experimental_headers, params=params)

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

    def create_request_type(
        self,
        service_desk_id,
        request_type_id,
        request_name,
        request_description,
        request_help_text,
    ):
        """
        Creating a request type
        :param request_type_id:
        :param request_help_text:
        :param service_desk_id: str
        :param request_name: str
        :param request_description: str
        """
        log.warning("Creating request type...")
        data = {
            "issueTypeId": request_type_id,
            "name": request_name,
            "description": request_description,
            "helpText": request_help_text,
        }

        url = "rest/servicedeskapi/servicedesk/{}/requesttype".format(service_desk_id)
        return self.post(url, headers=self.experimental_headers, data=data)
