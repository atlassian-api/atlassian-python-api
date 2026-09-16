Jira Service Desk module
========================

Jira Service Management Cloud authentication and access
-------------------------------------------------------

For Jira Service Management Cloud, authenticate with an Atlassian account
email and an API token. ``password`` below is the API token, not the account
password; the client sends the required HTTP Basic authentication header.

.. code-block:: python

    from atlassian import ServiceDesk

    sd = ServiceDesk(
        url="https://your-domain.atlassian.net",
        username="agent@example.com",
        password="your_atlassian_api_token",
        cloud=True,
    )

    # Fetch all accessible service desks (following every API page).
    service_desks = sd.get_service_desks(start=0, limit=50)

    # Fetch one bounded page only when controlling pagination manually.
    first_page = sd.get_service_desks(start=0, limit=50, fetch_all=False)
    customers = sd.get_customers(service_desk_id="1", query="Ada", start=0, limit=50)

Use an account that can access the relevant service desk. A portal-only
customer can work with its own customer requests, such as through
``get_my_customer_requests()``, but cannot enumerate a service desk's
customers. A ``401`` indicates invalid or absent authentication; a ``403``
indicates that valid credentials lack permission for the requested resource.

Get info about Service Desk
---------------------------

.. code-block:: python

    # Get info about Service Desk app
    sd.get_info()

    # Get every service desk accessible to the authenticated user
    sd.get_service_desks(start=0, limit=50)

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

    # Create customer request. ``values_dict`` must contain the fields required
    # by the request type (for example, summary and description).
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
    sd.add_request_participants(issue_id_or_key, users_list=None, account_list=None)

    # Remove request participants
    # The calling user must have permission to manage participants for this customer request
    sd.remove_request_participants(issue_id_or_key, users_list=None, account_list=None)


Request types
---------------------

.. code-block:: python

    # Get all request types in a service desk project
    sd.get_request_types(service_desk_id)

    # Get single request type in a given service desk project
    sd.get_request_type(service_desk_id, request_type_id)

    # Get field composition of a given request type
    sd.get_request_type_fields(service_desk_id, request_type_id)

    # Create a request type
    sd.create_request_type(service_desk_id, request_type_id, request_name, request_description, request_help_text)

    # Update a request type. Only the provided fields are changed. The calling
    # user must be an admin of the service desk project.
    sd.update_request_type(service_desk_id, request_type_id, request_name=None, request_description=None, request_help_text=None)

    # Delete a request type. The calling user must be an admin of the service desk project.
    sd.delete_request_type(service_desk_id, request_type_id)

    # Get the request type groups of a service desk
    sd.get_request_type_groups(service_desk_id, start=0, limit=50)

    # Get or upsert the customer-facing permission allowlist of a request type.
    # The upsert overwrites existing permissions; entries use
    # {"entityType": "USER" | "GROUP" | "ORGANIZATION", "entityId": str}.
    sd.get_request_type_permission(service_desk_id, request_type_id)
    sd.upsert_request_type_permission(service_desk_id, request_type_id, [{"entityType": "GROUP", "entityId": "jira-users"}])


Transitions
---------------------

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

    # Preview the organizations that would be removed by an organization cleanup
    sd.preview_organization_cleanup(delete_detached_organizations=False, delete_organizations_with_inactive_users=False)

    # Remove service desk organizations that are no longer in use.
    # The calling user must be an instance admin.
    sd.cleanup_organizations(delete_detached_organizations=False, delete_organizations_with_inactive_users=False)

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

    # Get SLA metric configuration for a service desk/project.
    # This uses an internal agent endpoint and may vary by Jira release.
    sd.get_sla_metrics(service_desk_id)

    # Update one SLA metric. Pass the metric definition/goals payload required
    # by your Jira release; this is an internal agent endpoint.
    sd.update_sla_metric(service_desk_id, sla_id, metric_payload)

Approvals
---------

.. code-block:: python

    # Get all approvals on a request, for a given request ID/Key
    sd.get_approvals(issue_id_or_key, start=0, limit=50)

    # Get an approval for a given approval ID
    sd.get_approval_by_id(issue_id_or_key, approval_id)

    # Answer a pending approval
    sd.answer_approval(issue_id_or_key, approval_id, decision)

    # Get the comment configuration of an approval
    sd.get_approval_comment_config(issue_id_or_key, approval_id)

Portals
-------

.. code-block:: python

    # Get the portals visible to the authenticated user
    sd.get_portals(start=0, limit=50)

    # Get a portal by ID
    sd.get_portal(portal_id)

    # Get the portal configured for a project
    sd.get_portal_by_project(project_key)

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

    # Get a single queue inside a service desk. Optionally include its issue count.
    # Permissions: The calling user must be an agent of the service desk.
    sd.get_queue(service_desk_id, queue_id, include_count=False)

    # Returns a page of issues inside a queue for a given queue ID.
    # Only fields that the queue is configured to show are returned.
    # For example, if a queue is configured to show only Description and Due Date,
    # then only those two fields are returned for each issue in the queue.
    # Permissions: The calling user must be an agent of the service desk that the queue belongs to.
    sd.get_issues_in_queue(service_desk_id, queue_id, start=0, limit=50)

    # Create, update, and delete queues. The calling user must be an admin of
    # the service desk project.
    sd.create_queue(service_desk_id, name, jql=None, fields=None)
    sd.update_queue(service_desk_id, queue_id, name=None, jql=None, fields=None)
    sd.delete_queue(service_desk_id, queue_id)

    # Reorder the queues of a service desk. ``queue_order`` is every queue ID in
    # the desired order, e.g. [3, 1, 2]. The calling user must be an admin of
    # the service desk project.
    sd.reorder_queues(service_desk_id, [3, 1, 2])

    # Global and per-project queue display settings. The global settings require
    # an instance admin; the per-project settings require a project admin.
    sd.set_should_queues_use_count_cache_globally(True)
    sd.set_should_queues_include_count_globally(False)
    sd.set_should_queues_use_count_cache_on_project(project_key, True)
    sd.set_should_queues_include_count_on_project(project_key, False)

Add customers to given Service Desk
-----------------------------------

**EXPERIMENTAL** (may change without notice)

.. code-block:: python

    # Adds one or more existing customers to the given service desk.
    # If you need to create a customer, see Create customer method.
    # Administer project permission is required, or agents if public signups
    # and invites are enabled for the Service Desk project.
    sd.add_customers(service_desk_id, list_of_usernames)
