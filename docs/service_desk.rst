Jira Service Desk module
========================

Get info about Service Desk
---------------------------

.. code-block:: python

    sd.get_info()

Create customer
---------------

**EXPERIMENTAL** (may change without notice)

.. code-block:: python

    sd.create_customer(full_name, email)

The Request actions
-------------------

.. code-block:: python

    # Create customer request
    sd.create_customer_request(service_desk_id, request_type_id, values_dict)

    # Get customer request by ID
    sd.get_customer_request(issue_id_or_key)

    # Get customer requests
    sd.get_my_customer_requests()

    # Get customer request status
    sd.get_customer_request_status(issue_id_or_key)

    # Create comment. Optional argument public (True or False), default is True
    sd.create_request_comment(issue_id_or_key, body, public=True)

    # Get request comments
    sd.get_request_comments(issue_id_or_key)

    # Get request comment
    sd.get_request_comment_by_id(issue_id_or_key, comment_id)

Transitions
-----------

**EXPERIMENTAL** (may change without notice)

.. code-block:: python

    # Perform transition. Optional argument comment (string), default is None
    sd.perform_transition(issue_id_or_key, transition_id, comment=None)
