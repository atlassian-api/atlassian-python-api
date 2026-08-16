Requirement Yogi
================

The Requirement Yogi clients are split by Atlassian product and deployment,
so a Jira URL is never used for a Confluence Data Center endpoint.

.. code-block:: python

    from atlassian import YogiConfluenceCloud, YogiConfluenceDC
    from atlassian import YogiJiraCloud, YogiJiraDC

    cloud_jira = YogiJiraCloud(token="token")
    cloud_confluence = YogiConfluenceCloud(token="token")
    requirements = cloud_jira.get_requirements(application_id="application-id")

    dc_jira = YogiJiraDC("https://jira.example.com", username="admin", password="secret")
    dc_confluence = YogiConfluenceDC("https://confluence.example.com", username="admin", password="secret")

Cloud
-----

``YogiJiraCloud`` and ``YogiConfluenceCloud`` share the complete Cloud API:
128 concrete methods for organizations, applications, containers,
requirements, variants, templates, dashboards, files, external properties,
and user account resources. Methods use named Python arguments for every path
and query parameter and accept ``data=`` for JSON request bodies.

Data Center
-----------

``YogiJiraDC`` implements Jira-specific information, synchronization, and
issue-link endpoints. ``YogiConfluenceDC`` implements requirement search,
baselines, reindexing, and integration endpoints. Data Center API routes are
experimental; methods intentionally cover the public routes documented by
Requirement Yogi and omit routes marked “Do not use”.

The actual installation-specific OpenAPI documents are available from
``/rest/reqs/1/openapi`` in both Jira and Confluence.
