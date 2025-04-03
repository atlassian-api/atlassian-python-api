Cloud Admin module
==================

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
