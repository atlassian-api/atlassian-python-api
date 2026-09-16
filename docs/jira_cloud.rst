Jira Cloud API clients
======================

The clients are organized under ``atlassian.jira``.  ``Jira`` is the retained
Server/Data Center-compatible client (also available explicitly as
``JiraServer``); ``ServiceDesk`` remains available for established
integrations.
New Cloud work should use the module-specific clients:

.. code-block:: python

    from atlassian.jira import JiraCloud, JiraSoftware, JiraServiceManagement

    # Jira Cloud platform (Core), REST v3 by default; v2 is also supported.
    core = JiraCloud("https://example.atlassian.net", token="...", api_version=3)
    issue = core.get(core.endpoint("issue/ABC-1"))

    # Jira Software has several independently versioned roots.
    software = JiraSoftware("https://example.atlassian.net", token="...")
    sprints = software.get(software.endpoint("agile", "board/42/sprint"))

    # The public JSM API has the servicedeskapi root and keeps ServiceDesk APIs.
    jsm = JiraServiceManagement("https://example.atlassian.net", token="...")
    request = jsm.get(jsm.endpoint("request/ABC-1"))

Core API versioning
-------------------

``JiraCloud`` validates Core REST versions 2 and 3.  It defaults to v3 for new
integrations.  Use v2 only where its response or request payload is part of an
existing contract.  ``Jira`` still defaults to its historical string version
``"2"`` and does not automatically enable Cloud mode; this is intentional
backward compatibility.

Enhanced JQL search
-------------------

Both ``JiraCloud`` and the legacy ``Jira(..., cloud=True)`` client provide
``enhanced_jql()``. The method always uses Jira Cloud's v3
``/search/jql`` endpoint, regardless of the Core client's selected version.
Pass the returned ``nextPageToken`` to fetch another page, or use
``enhanced_jql_get_list_of_tickets()`` to collect cursor-paginated results.

.. code-block:: python

    issues = core.enhanced_jql_get_list_of_tickets(
        'project = EXAMPLE ORDER BY updated DESC',
        fields=["summary", "description"],
        limit=100,
        expand="names",
    )

Software API roots
------------------

``JiraSoftware.endpoint(api, resource)`` selects the supplied API's current
documented root/version. Supported API names are ``agile``, ``software``,
``devinfo``, ``featureflags``, ``deployments``, ``builds``, ``remotelinks``,
``security``, ``operations``, and ``devopscomponents``.  The separate roots
avoid incorrectly treating Jira Software as Core v1.

Issue ranking
-------------

Jira Software exposes ranking through the Agile API. ``rank_issues`` accepts
multiple issue keys or IDs and placement fields supported by Jira:

.. code-block:: python

    software.rank_issues({
        "issues": ["EXAMPLE-1", "EXAMPLE-2"],
        "rankAfterIssue": "EXAMPLE-10",
    })

Use ``rank_epics`` for ranking epics. These methods are available on Cloud and
on Jira Software Server/Data Center installations exposing the Agile REST API.

Plans (Advanced Roadmaps)
-------------------------

The official Plans REST API (released December 2024) is available on
``JiraCloud``: ``get_plans``, ``create_plan``, ``get_plan``, ``update_plan``,
``duplicate_plan``, ``archive_plan``, and ``trash_plan``, plus the team
operations listed in :doc:`jira_cloud_api`. Plans are identified by numeric ID
and the caller needs the Plans admin permission.

``update_plan`` takes a JSON Patch document, which the RFC notes appends
``add`` operations rather than honouring array indexes. The
``add_custom_field_to_plan`` helper wraps the common case:

.. code-block:: python

    plan = core.create_plan(data={
        "name": "Q3 Delivery Plan",
        "leadAccountId": "5b10a2844c20165700ede21g",
        "issueSources": [{"sourceType": "BOARD", "id": "42"}],
    })
    core.add_custom_field_to_plan(plan["id"], custom_field_id=10071, filter=True)

Plan *views* are not part of the official API yet; there is no supported
endpoint to create, list, or delete them.

Generated OpenAPI operations
----------------------------

The supplied API descriptions provide 619 Core operations across 423 paths,
105 Software operations across 78 paths, and 75 Service Management operations
across 50 paths.  Every operation is implemented as an ordinary snake_case
Python method, grouped in ``core_methods.py``, ``software_methods.py``, or
``service_management_methods.py``.  For example:

.. code-block:: python

    issue = core.get_issue("ABC-1")
    boards = software.get_all_boards(project_key_or_id="ABC")
    request = jsm.get_customer_request_by_id_or_key("ABC-1")

Methods have explicit path and query arguments, plus ``data`` for the JSON
body and the same request options supported by the shared REST client. A few
JSM operation IDs are duplicated by Atlassian; their method names include a
deterministic endpoint suffix so no endpoint is lost.

Compatibility and migration
---------------------------

``Jira`` and ``JiraServer`` are the same legacy-compatible implementation.
Their imports, constructor options, and existing method names remain unchanged:

.. code-block:: python

    from atlassian import Jira

    jira = Jira("https://jira.example.org", username="admin", password="...")
    jira.issue("ABC-1")

Use the new Cloud classes only for new integrations or an intentional Cloud
migration. They force ``cloud=True`` and accept the ordinary connection
arguments such as ``token``, ``oauth2``, ``session``, ``verify_ssl``,
``timeout``, and retry settings. ``JiraCloud`` supports Core ``api_version=2``
and ``api_version=3``; its concrete Core methods build routes for the selected
version. Jira Software and JSM select their documented fixed roots.

For a complete method-to-endpoint reference, see :doc:`jira_cloud_api`.

Core generated operations use the selected ``JiraCloud(api_version=2|3)``
version in their route.  Existing snake_case ``Jira`` and ``ServiceDesk``
methods retain their endpoint selection and behavior; they are neither renamed
nor overwritten by the generated Cloud surface.
Workflow scheme project associations
------------------------------------

Use :class:`atlassian.jira.JiraCloud` to inspect or assign classic-project
workflow schemes. Team-managed projects are not returned by Jira for this
endpoint. Both operations require the Administer Jira global permission.

.. code-block:: python

    from atlassian.jira import JiraCloud

    jira = JiraCloud("https://your-domain.atlassian.net", username=email, password=api_token)

    associations = jira.get_project_workflow_scheme_associations(["10001", "10002"])
    jira.assign_project_workflow_scheme(project_id="10001", workflow_scheme_id="10032")
