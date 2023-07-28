Xray module
===========

.. note::
   The Xray module only support the Server + Data Center edition
   of the Xray Jira plugin!

Manage Test
-----------

.. code-block:: python

    # Retrieve information about the provided tests
    xray.get_tests(['TEST-001', 'TEST-002'])

    # Retrieve a list of all Test Statuses available in Xray sorted by rank
    xray.get_test_statuses()

    # Retrieve test runs of a test
    xray.get_test_runs('TEST-001')

    # Retrieve test runs of a test filtered by tests environments
    xray.get_test_runs_with_environment('TEST-001', 'Android,iOS')

    # Retrieve pre-conditions of a test
    xray.get_test_preconditions('TEST-001')

    # Retrieve test sets associated with a test
    xray.get_test_sets('TEST-001')

    # Retrieve test executions of a test
    xray.get_test_executions('TEST-001')

    # Retrieve test plans associated with a test
    xray.get_test_plans('TEST-001')

Manage Test Steps
-----------------

.. code-block:: python

    # Retrieve the test step statuses available in Xray sorted by rank
    xray.get_test_step_statuses()

    # Retrieve the specified test step of a given test
    xray.get_test_step('TEST-001', 'STEP-001')

    # Retrieve the test steps of a given test
    xray.get_test_steps('TEST-001')

    # Create a new test steps for a given test
    xray.create_test_step('TEST-001', 'Example Test Step', 'Example Test Data', 'Example Test Result')

    # Update the specified test steps for a given test
    xray.update_test_step('TEST-001', 100, 'Updated Test Step', 'Updated Test Data', 'Updated Test Result')

    # Remove the specified test steps from a given test
    xray.delete_test_step('TEST-001', 100)

Manage Pre-conditions
---------------------

.. code-block:: python

    # Retrieve the tests associated with the given pre-condition
    xray.get_tests_with_precondition('PREC-001')

    # Associate tests with the given pre-condition
    xray.update_precondition('PREC-001', add=['TEST-001','TEST-002'], remove=['TEST-003'])

    # Remove association of the specified tests from the given pre-condition
    xray.delete_test_from_precondition('PREC-001', 'TEST-003')

Manage Test sets
----------------

.. code-block:: python

    # Retrieve the tests associated with the given test set
    xray.get_tests_with_test_set('SET-001', page=1, limit=10)

    # Associate tests with the given test set
    xray.update_test_set('SET-001',add=['TEST-001','TEST-002'], remove=['TEST-003'])

    #  Remove association of the specified tests from the given test set
    xray.delete_test_from_test_set('SET-001', 'TEST-003')

Manage Test plans
-----------------

.. code-block:: python

    # Retrieve the tests associated with the given test plan
    xray.get_tests_with_test_plan('PLAN-001')

    # Associate tests with the given test plan
    xray.update_test_plan('PLAN-001', add=['TEST-001', 'TEST-002'], remove=['TEST-003'])

    # Remove association of the specified tests from the given test plan
    xray.delete_test_from_test_plan('PLAN-001', 'TEST-001'):

    # Retrieve the test executionss associated with the given test plan
    xray.get_test_executions_with_test_plan('PLAN-001')

    # Associate test executionss with the given test plan
    xray.update_test_plan_test_executions('PLAN-001', add=['EXEC-001', 'EXEC-002'], remove=['EXEC-003'])

    # Remove association of the specified test executionss from the given test plan
    xray.delete_test_execution_from_test_plan('PLAN-001', 'EXEC-001'):

Manage Test Executions
----------------------

.. code-block:: python

    # Retrieve the tests associated with the given test execution
    xray.get_tests_with_test_execution('EXEC-001', detailed=True, page=1, limit=10)

    # Associate tests with the given test execution
    xray.update_test_execution('EXEC-001', add=['TEST-001', 'TEST-002'], remove=['TEST-003'])

    # Remove association of the specified tests from the given test execution
    xray.delete_test_from_test_execution('EXEC-001', 'TEST-001')

Manage Test Runs
----------------

.. code-block:: python

    # Retrieve detailed information about the given test run
    xray.get_test_run(100)

    # Retrieve the assignee for the given test run.
    xray.get_test_run_assignee(100)

    # Update the assignee for the given test run
    xray.update_test_run_assignee(100, 'bob')

    # Retrieve the status for the given test run
    xray.get_test_run_status(100)

    # Update the status for the given test run
    xray.update_test_run_status(100, 'PASS')

    # Retrieve the defects for the given test run
    xray.get_test_run_defects(100)

    # Update the defects associated with the given test run
    xray.update_test_run_defects(100, add=['BUG-001', 'BUG-002'], remove=['BUG-003'])

    # Retrieve the comment for the given test run
    xray.get_test_run_comment(100)

    # Update the comment for the given test run
    xray.update_test_run_comment(100, 'Test needs to be reworked')

    # Retrieve the steps for the given test run
    xray.get_test_run_steps(100)

    # Retrieve test repository folders of a project.
    xray.get_test_repo_folders(project_key)

    # Retrieve test repository folder of a project.
    xray.get_test_repo_folder(project_key, folder_id)

    # Create test repository folder for a project.
    xray.create_test_repo_folder(project_key, folder_name, parent_folder_id=-1)
