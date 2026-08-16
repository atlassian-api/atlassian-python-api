Cloud Admin module
==================

API reference
-------------

.. autoclass:: atlassian.cloud_admin.CloudAdmin
   :members:
   :undoc-members:

.. autoclass:: atlassian.cloud_admin.CloudAdminOrgs
   :members:
   :undoc-members:

.. autoclass:: atlassian.cloud_admin.CloudAdminUsers
   :members:
   :undoc-members:

CloudAdmin
----------

``CloudAdmin`` is the modern organization-administration client for
``https://api.atlassian.com/admin``. It requires an Atlassian Administration
API key, not a Jira or Confluence API token. Give the key the scopes required
by each operation.

.. code-block:: python

    from atlassian import CloudAdmin

    admin = CloudAdmin(admin_api_key="<admin-api-key>")
    organizations = admin.get_organizations()
    directories = admin.get_directories("<org-id>", search_term="engineering")
    users = admin.search_directory_users(
        "<org-id>", "<directory-id>", {"searchTerm": "ada", "limit": 50}
    )
    domains = admin.get_domains("<org-id>")
    events = admin.get_events("<org-id>", limit=100)

    # User Management API: check privileges before a lifecycle change.
    permissions = admin.get_user_management_permissions("<account-id>")
    admin.update_user_profile("<account-id>", {"nickname": "Ada"})
    admin.set_user_email("<account-id>", "ada@example.com")
    admin.deactivate_user("<account-id>", message="Offboarding")
    admin.activate_user("<account-id>")
    admin.delete_user_api_token("<account-id>", "<token-id>")

It also exposes directory user/group details and counts, verified domains, and
individual audit events. ``CloudAdminOrgs`` and ``CloudAdminUsers`` remain for
backwards compatibility with the older Administration API endpoints.

The User Management methods expose permissions, profile reads/updates, email
updates, user API-token revocation, and deactivate/activate/delete/cancel-delete
lifecycle operations. Deletion is destructive after Atlassian's grace period;
prefer deactivation when account recovery may be needed.

User provisioning (SCIM)
~~~~~~~~~~~~~~~~~~~~~~~~

The same client supports the directory-scoped SCIM 2.0 provisioning API.
SCIM resource bodies and PATCH operations are passed through unchanged.

.. code-block:: python

    users = admin.get_scim_users(
        "<directory-id>", filter='userName eq "ada@example.com"', count=10
    )
    user = admin.create_scim_user("<directory-id>", {"userName": "ada@example.com", "active": True})
    admin.patch_scim_group(
        "<directory-id>", "<group-id>",
        [{"op": "add", "path": "members", "value": [{"value": user["id"]}]}],
    )

``delete_scim_user`` and ``delete_scim_group`` delete directory resources.
``delete_scim_user_from_database`` is a repair-only operation and deletes only
the SCIM database record; use it only with a documented recovery procedure.

Data Loss Prevention (DLP)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Classification-level management is available through the DLP API. These
operations require ``read:classification-levels:admin`` or
``write:classification-levels:admin`` on the administration API key.

.. code-block:: python

    levels = admin.get_classification_levels("<org-id>")
    level = admin.create_classification_level("<org-id>", {"name": "Restricted"})
    admin.publish_classification_levels("<org-id>", [level["id"]])
    admin.reorder_classification_levels("<org-id>", [level["id"]])

Archiving a published level makes associated pages and issues unclassified.
Restoring creates a draft, which must be published again before it is usable.

Admin Control
~~~~~~~~~~~~~

Admin Control policies and their resources use V2 by default. Use ``version``
for compatible V1 calls. Publishing draft policies applies pending
organization controls; resource and policy deletion remove existing controls.

.. code-block:: python

    policy = admin.create_control_policy("<org-id>", {"name": "Require MFA"})
    admin.add_control_policy_resource("<org-id>", policy["id"], {"resourceId": "<resource-ari>"})
    admin.publish_control_draft_policies("<org-id>")

Authentication-policy user assignment returns an asynchronous task. Poll it
with ``get_auth_policy_task(org_id, task_id)`` until completion.

API Access
~~~~~~~~~~

API Access management covers organization API tokens and keys, OAuth clients,
and service accounts. Listing and count methods are read-only; revoke and
delete methods immediately affect credentials or accounts.

.. code-block:: python

    tokens = admin.get_org_api_tokens("<org-id>", limit=100)
    service_account = admin.create_service_account("<org-id>", {"name": "automation"})
    client = admin.create_oauth_client("<org-id>", {"name": "integration"})
    admin.revoke_org_api_key("<org-id>", "<api-key-id>")

CloudAdminOrgs
--------------

.. code-block:: python

    # Returns a list of your organizations
    cloud_admin_orgs.get_organizations()

    # Returns information about a single organization by ID
    cloud_admin_orgs.get_organization(org_id)

    # Returns a list of accounts managed by the organization
    cloud_admin_orgs.get_managed_accounts_in_organization(org_id, cursor=None)

    # Returns a list of accounts in the organization that match the search criteria.
    cloud_admin_orgs.search_users_in_organization(org_id, account_ids=None, account_types=None,account_statuses=None,
                                     name_or_nicknames=None, email_usernames=None, email_domains=None, is_suspended=None,
                                     cursor=None, limit=10000, expand=None)

    #

CloudAdminUsers
---------------

.. code-block:: python

    # Returns information about a single Atlassian account by ID
    cloud_admin_users.get_profile(account_id)
