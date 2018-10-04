# coding: utf8
import logging
from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class ServiceDesk(AtlassianRestAPI):
    def get_info(self):
        """ Get info about Service Desk app """
        return self.get('rest/servicedeskapi/info')

    def create_customer(self, full_name, email):
        """
        Creating customer user

        :param full_name: str
        :param email: str
        :return: New customer
        """
        log.warning('Creating customer...')
        data = {'fullName': full_name, 'email': email}
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'X-ExperimentalApi': 'opt-in'
                   }
        return self.post('rest/servicedeskapi/customer', headers=headers, data=data)

    def get_customer_request(self, issue_id_or_key):
        """
        Get single request

        :param issue_id_or_key: str
        :return: Customer request
        """
        return self.get('rest/servicedeskapi/request/{}'.format(issue_id_or_key))

    def get_my_customer_requests(self):
        """ Returning requests where you are the assignee """
        requests = self.get('rest/servicedeskapi/request')
        requests_values = requests.get('values')
        return requests_values

    def create_customer_request(self, service_desk_id, request_type_id, values_dict):
        """
        Creating customer request

        :param service_desk_id: str
        :param request_type_id: str
        :param values_dict: str
        :return: New request
        """
        log.warning('Creating request...')
        data = {"serviceDeskId": service_desk_id,
                "requestTypeId": request_type_id,
                "requestFieldValues": values_dict
                }
        return self.post('rest/servicedeskapi/request', data=data)

    def get_customer_request_status(self, issue_id_or_key):
        """
        Get customer request status name

        :param issue_id_or_key: str
        :return: Status name
        """
        request = self.get('rest/servicedeskapi/request/{}/status'.format(issue_id_or_key)).get('values')
        status = request[0].get('status')
        return status

    def perform_transition(self, issue_id_or_key, transition_id, comment=None):
        """
        Perform a customer transition for a given request and transition ID.
        An optional comment can be included to provide a reason for the transition.

        :param issue_id_or_key: str
        :param transition_id: str
        :param comment: OPTIONAL: str
        :return: None
        """
        log.warning('Performing transition...')
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'X-ExperimentalApi': 'opt-in'
                   }
        data = {'id': transition_id, 'additionalComment': {'body': comment}}
        url = 'rest/servicedeskapi/request/{}/transition'.format(issue_id_or_key)
        return self.post(url, headers=headers, data=data)

    def create_request_comment(self, issue_id_or_key, body, public=True):
        """
        Creating request comment

        :param issue_id_or_key: str
        :param body: str
        :param public: OPTIONAL: bool (default is True)
        :return: New comment
        """
        log.warning('Creating comment...')
        data = {"body": body, "public": public}
        return self.post('rest/servicedeskapi/request/{}/comment'.format(issue_id_or_key), data=data)

    def get_request_comments(self, issue_id_or_key):
        """
        Get all comments in issue

        :param issue_id_or_key: str
        :return: Issue comments
        """
        return self.get('rest/servicedeskapi/request/{}/comment'.format(issue_id_or_key))

    def get_request_comment_by_id(self, issue_id_or_key, comment_id):
        """
        Get single comment by ID

        :param issue_id_or_key: str
        :param comment_id: str
        :return: Single comment
        """
        return self.get('rest/servicedeskapi/request/{0}/comment/{1}'.format(issue_id_or_key, comment_id))

    def get_organisations(self, start=0, limit=50):
        """
        Returns a list of organizations in the JIRA instance. If the user is not an agent, the resource returns a list of organizations the user is a member of.
        :param start: OPTIONAL: int The starting index of the returned objects.
                     Base index: 0. See the Pagination section for more details.
        :param limit: OPTIONAL: int The maximum number of users to return per page.
                     Default: 50. See the Pagination section for more details.
        :return:
        """
        params = {}
        if start is not None:
            params["start"] = int(start)
        if limit is not None:
            params["limit"] = int(limit)

        return self.get('rest/servicedeskapi/organization', params=params)
