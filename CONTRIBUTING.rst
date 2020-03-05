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

* `Jira Server`_
* `Jira Cloud`_
* `Confluence Server`_
* `Confluence Cloud`_
* `Jira Service Desk Server`_
* `Jira Service Desk Cloud`_
* `Portfolio for Jira`_
* `Portfolio for Jira Teams`_
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
* Others:
    - https://developer.atlassian.com/server/jira/platform/oauth/
    - https://confluence.atlassian.com/cloud/api-tokens-938839638.html

.. _`Jira Server`: https://docs.atlassian.com/software/jira/docs/api/REST/latest
.. _`Jira Cloud`: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
.. _`Confluence Server`: https://developer.atlassian.com/server/confluence/confluence-server-rest-api/
.. _`Confluence Cloud`: https://developer.atlassian.com/cloud/confluence/rest/
.. _`Jira Service Desk Cloud`: https://developer.atlassian.com/cloud/jira/service-desk/rest/
.. _`Jira Service Desk Server`: https://docs.atlassian.com/jira-servicedesk/REST/server
.. _`Portfolio for Jira Teams`: https://docs.atlassian.com/portfolio-for-jira-server/REST/2.13.0/teams/
.. _`Portfolio for Jira`: https://docs.atlassian.com/portfolio-for-jira-server/REST/2.13.0/jpo/


Credits
-------
In addition to all the contributors we would like to thank to these companies:

* Atlassian_ for developing such a powerful ecosystem.
* JetBrains_ for providing us with free licenses of PyCharm_
* Travis_ for hosting our continuous integration
* Insomnia_ for providing the human rest client easy to test the methods
.. _Atlassian: https://www.atlassian.com/
.. _JetBrains: http://www.jetbrains.com
.. _PyCharm: http://www.jetbrains.com/pycharm/
.. _Travis: https://travis-ci.org/
.. _Insomnia: https://insomnia.rest/