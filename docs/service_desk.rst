Jira Service Desk module
========================

Get info about Service Desk
---------------------------

.. code-block:: python

    # Get info about Service Desk app
    sd.get_info()

    # Get all service desks in the JIRA Service Desk application with the option to include archived service desks
    sd.get_service_desks()

    # Get the service desk for a given service desk ID
    sd.get_service_desk_by_id(service_desk_id)

Create customer
---------------

**EXPERIMENTAL** (may change without notice)

.. code-block:: python

    sd.create_customer(full_name, email)

The Request actions
-------------------

.. code-block:: python

    # Create customer request
    sd.create_customer_request(service_desk_id, request_type_id, values_dict, raise_on_behalf_of=None, request_participants=None)

    # Get customer request by ID
    sd.get_customer_request(issue_id_or_key)

    # Get customer requests
    sd.get_my_customer_requests()

    # Get customer request status
    sd.get_customer_request_status(issue_id_or_key)

    # Create comment. Optional argument public (True or False), default is True
    sd.create_request_comment(issue_id_or_key, body, public=True)

    # Get request comments
    sd.get_request_comments(issue_id_or_key, start=0, limit=50, public=True, internal=True)

    # Get request comment
    sd.get_request_comment_by_id(issue_id_or_key, comment_id)

Manage a Participants
---------------------

.. code-block:: python

    # Get request participants
    sd.get_request_participants(issue_id_or_key, start=0, limit=50)

    # Add request participants
    # The calling user must have permission to manage participants for this customer request
    sd.add_request_participants(issue_id_or_key, users_list)

    # Remove request participants
    # The calling user must have permission to manage participants for this customer request
    sd.remove_request_participants(issue_id_or_key, users_list)

Transitions
-----------

**EXPERIMENTAL** (may change without notice)

.. code-block:: python

    # Get customer transitions. A list of transitions that customers can perform on the request
    sd.get_customer_transitions(issue_id_or_key)

    # Perform transition. Optional argument comment (string), default is None
    sd.perform_transition(issue_id_or_key, transition_id, comment=None)

Manage the Organizations
------------------------

**EXPERIMENTAL** (may change without notice)

.. code-block:: python

    # Get a list of organizations in the JIRA instance
    # If the user is not an agent, the resource returns a list of organizations the user is a member of
    # If service_desk_id is None, request returns all organizations
    # In service_desk_id is ID, request returns organizations from given Service Desk ID
    sd.get_organisations(service_desk_id=None, start=0, limit=50)

    # Get an organization for a given organization ID
    sd.get_organization(organization_id)

    # Get all the users of a specified organization
    sd.get_users_in_organization(organization_id, start=0, limit=50)

    # Create organization
    sd.create_organization(name)

    # Add an organization to a servicedesk for a given servicedesk ID (str) and organization ID (int)
    sd.add_organization(service_desk_id, organization_id)

    # Remove an organization from a servicedesk for a given servicedesk ID (str) and organization ID (int)
    sd.remove_organization(service_desk_id, organization_id)

    # Delete organization
    sd.delete_organization(organization_id)

    # Add users to organization
    sd.add_users_to_organization(organization_id, users_list=[], account_list=[])

    # Remove users from organization
    sd.remove_users_from_organization(organization_id, , users_list=[], account_list=[])

Attachment actions
------------------

**EXPERIMENTAL** (may change without notice)

.. code-block:: python

    # Create attachment (only single file) as a comment
    # You can choose type of attachment. public=True is Public attachment, public=False is Internal attachment
    # Customers can only create public attachments
    # An additional comment may be provided which will be prepended to the attachments
    sd.create_attachment(service_desk_id, issue_id_or_key, filename, public=True, comment=None)

    # Create temporary attachment, which can later be converted into permanent attachment
    sd.attach_temporary_file(service_desk_id, filename)

    # Add temporary attachment that were created using attach_temporary_file function to a customer request
    sd.add_attachment(issue_id_or_key, temp_attachment_id, public=True, comment=None)

SLA actions
-----------

.. code-block:: python

    # Get the SLA information for a customer request for a given request ID or key
    # IMPORTANT: The calling user must be an agent
    sd.get_sla(issue_id_or_key, start=0, limit=50)

    # Get the SLA information for a customer request for a given request ID or key and SLA metric ID
    # IMPORTANT: The calling user must be an agent
    sd.get_sla_by_id(issue_id_or_key, sla_id)

Approvals
---------

.. code-block:: python

    # Get all approvals on a request, for a given request ID/Key
    sd.get_approvals(issue_id_or_key, start=0, limit=50)

    # Get an approval for a given approval ID
    sd.get_approval_by_id(issue_id_or_key, approval_id)

    # Answer a pending approval
    sd.answer_approval(issue_id_or_key, approval_id, decision)

Queues
------

.. code-block:: python

    # Get queue settings on project
    sd.get_queue_settings(project_key)

**EXPERIMENTAL** (may change without notice)

.. code-block:: python

    # Returns a page of queues defined inside a service desk, for a given service desk ID.
    # The returned queues will include an issue count for each queue (represented in issueCount field)
    # if the query param includeCount is set to true (defaults to false).
    # Permissions: The calling user must be an agent of the given service desk.
    sd.get_queues(service_desk_id, include_count=False, start=0, limit=50)

    # Returns a page of issues inside a queue for a given queue ID.
    # Only fields that the queue is configured to show are returned.
    # For example, if a queue is configured to show only Description and Due Date,
    # then only those two fields are returned for each issue in the queue.
    # Permissions: The calling user must have permission to view the requested queue,
    # i.e. they must be an agent of the service desk that the queue belongs to.
    sd.get_issues_in_queue(service_desk_id, queue_id, start=0, limit=50)

Add customers to given Service Desk
-----------------------------------

**EXPERIMENTAL** (may change without notice)

.. code-block:: python

    # Adds one or more existing customers to the given service desk.
    # If you need to create a customer, see Create customer method.
    # Administer project permission is required, or agents if public signups
    # and invites are enabled for the Service Desk project.
    sd.add_customers(service_desk_id, list_of_usernames)
