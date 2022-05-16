How to contribute
=================

You’re very welcome to make bug fixes or enhancements to this library.
This document lays out the guidelines for how to get those changes into
the main package repository.

Getting Started
---------------

* Fork_ repository
* Keep it sync_'ed while you are developing
* Install pyenv_
* Install related atlassian product for testing through SDK_ or use the cloud instance
* ``pip install -r requirements-dev.txt``
* Start up related product:
  - Standalone product atlas-run-standalone_
  - For cloud product, just do registration
* Run the quality checks with `make qa` or if you have docker installed with `make docker-qa`
* Send pull request

.. _Fork: https://help.github.com/articles/fork-a-repo/
.. _sync: https://help.github.com/articles/syncing-a-fork/
.. _pyenv: https://amaral.northwestern.edu/resources/guides/pyenv-tutorial
.. _SDK: https://developer.atlassian.com/server/framework/atlassian-sdk/downloads/
.. _atlas-run-standalone: https://developer.atlassian.com/server/framework/atlassian-sdk/atlas-run-standalone/

Mandatory conditions
--------------------

1. If you adding new method - add description to docs
2. If you make changes in current methods - add changes to docs
3. If you sent the PR, please validate via black_

Please follow the code style in the docs.

.. _black:  https://black.readthedocs.io/en/stable/integrations/editors.html

Connect on Chat for any queries
---------------------------------

Please message on chat-group link present in `README.rst`_ badge for any queries.

.. _README.rst: README.rst


Before you raise a PR
---------------------

Create the **Commit Header** with the relevant Service Name pre-fixed, examples below,

* Jira: review user module           :heavy_check_mark:
* [JIRA] Issues Move to Sprint       :heavy_check_mark:
* Confluence: update_page_property method     :heavy_check_mark:

An example of a commit message header,

* Addition of parameters for start & limit in the function of `get_all_project_issues`      :x:

could be better written as,

* [JIRA] Project Issues parameter addition for start and limit      :heavy_check_mark:

with the commit body have a detail about where/what changes introduced.

This will help the reviewer or log-viewers to better identify what a particular commit is for.


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

An alternative way you can use next command

::

   python3 -m pip install git+https://github.com/atlassian-api/atlassian-python-api.git


References
----------

All methods based on docs from: https://developer.atlassian.com/docs/

* Jira
    - `Jira Server`_
    - `Jira Cloud`_
* Jira Service Desk
    - `Jira Service Desk Server`_
    - `Jira Service Desk Cloud`_
* Confluence
    - `Confluence Server`_
    - `Confluence Cloud`_
* Crowd
    - `Crowd Server`_
* Advanced Roadmaps (formerly Portfolio for Jira)
    - `Portfolio for Jira`_
    - `Portfolio for Jira Teams`_
* Insight
    _`Insight Server`_
    _`Insight Cloud`_
*  Bitbucket:
    - https://developer.atlassian.com/server/bitbucket/reference/rest-api/
    - https://developer.atlassian.com/server/bitbucket/how-tos/command-line-rest/
    - https://developer.atlassian.com/bitbucket/api/2/reference/resource/
* Bamboo:
    - https://docs.atlassian.com/atlassian-bamboo/REST/latest/
* Tempo:
    - https://www.tempo.io/server-api-documentation
    - http://tempo.io/doc/core/api/rest/latest/
* Marketplace:
    - https://developer.atlassian.com/platform/marketplace/rest
* Crowd:
    - https://developer.atlassian.com/server/crowd/crowd-rest-apis/
* Xray:
    - https://docs.getxray.app/display/XRAY/REST+API
* Others:
    - https://developer.atlassian.com/server/jira/platform/oauth/
    - https://confluence.atlassian.com/cloud/api-tokens-938839638.html
    - (OpsGenie) https://docs.opsgenie.com/docs/api-overview
    - (Status Page) https://developer.statuspage.io/

.. _`Jira Server`: https://docs.atlassian.com/software/jira/docs/api/REST/latest
.. _`Jira Cloud`: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
.. _`Confluence Server`: https://developer.atlassian.com/server/confluence/confluence-server-rest-api/
.. _`Confluence Cloud`: https://developer.atlassian.com/cloud/confluence/rest/
.. _`Crowd Server`: https://developer.atlassian.com/server/crowd/crowd-rest-apis/
.. _`Jira Service Desk Cloud`: https://developer.atlassian.com/cloud/jira/service-desk/rest/
.. _`Jira Service Desk Server`: https://docs.atlassian.com/jira-servicedesk/REST/server
.. _`Portfolio for Jira Teams`: https://docs.atlassian.com/portfolio-for-jira-server/REST/2.13.0/teams/
.. _`Portfolio for Jira`: https://docs.atlassian.com/portfolio-for-jira-server/REST/2.13.0/jpo/
.. _`Insight Server`: https://insight-javadoc.riada.io/insight-javadoc-8.6/insight-rest/
.. _`Insight Cloud`: https://developer.atlassian.com/cloud/insight/rest/api-group-objectschema/#api-objectschema-list-get

Credits
-------
In addition to all the contributors we would like to thank to these companies:

* Atlassian_ for developing such a powerful ecosystem.
* JetBrains_ for providing us with free licenses of PyCharm_
* GitHub_ for hosting our repository and continuous integration
* Insomnia_ for providing the human rest client easy to test the methods
.. _Atlassian: https://www.atlassian.com/
.. _JetBrains: http://www.jetbrains.com
.. _PyCharm: http://www.jetbrains.com/pycharm/
.. _GitHub: https://github.com/
.. _Insomnia: https://insomnia.rest/
