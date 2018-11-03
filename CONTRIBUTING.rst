How to contribute
=================

You’re very welcome to make bug fixes or enhancements to this library.
This document lays out the guidelines for how to get those changes into
the main package repository.

Getting Started
---------------

1. Fork the repository on GitHub:
   https://github.com/atlassian-api/atlassian-python-api
2. Make changes
3. Send pull request

Mandatory conditions
--------------------

1. If you adding new method - add description to docs
2. If you make changes in current methods - add changes to docs

Please follow the code style in the docs.

Using your changes before they’re live
--------------------------------------

You may want to use the changes you’ve made to this library before the
merging/review process has been completed. To do this you can install it
into the global python environment by running this command from the top
level directory.

::

   pip install . --upgrade

The following command builds a package and uploads it to PIP repository.

::

   python setup.py sdist upload


References
----------

All methods based on docs from: https://developer.atlassian.com/docs/

1. Jira:
    - https://docs.atlassian.com/software/jira/docs/api/REST/latest
2. Confluence:
    - https://developer.atlassian.com/server/confluence/confluence-server-rest-api/
3. Jira Service Desk:
    - https://developer.atlassian.com/cloud/jira/service-desk/rest/
    - https://docs.atlassian.com/jira-servicedesk/REST/server
4. Portfolio for Jira:
    - https://docs.atlassian.com/portfolio-for-jira-server/REST/2.13.0/teams/
    - https://docs.atlassian.com/portfolio-for-jira-server/REST/2.13.0/jpo/
5. Bitbucket:
    - https://developer.atlassian.com/server/bitbucket/reference/rest-api/
    - https://developer.atlassian.com/server/bitbucket/how-tos/command-line-rest/
6. Bamboo:
    - https://docs.atlassian.com/atlassian-bamboo/REST/latest/
7. Tempo:
    - https://www.tempo.io/server-api-documentation
    - http://tempo.io/doc/core/api/rest/latest/