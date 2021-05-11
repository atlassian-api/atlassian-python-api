# coding=utf-8
import logging
import re

from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Xray(AtlassianRestAPI):
    def __init__(self, *args, **kwargs):
        super(Xray, self).__init__(*args, **kwargs)

    # Tests API
    def get_tests(self, test_keys):
        """
        Retrieve information about the provided tests.
        :param test_keys: list of tests (eg. `['TEST-001', 'TEST-002']`) to retrieve.
        :return: Returns the retrieved tests.
        """
        url = "rest/raven/1.0/api/test?keys={0}".format(";".join(test_keys))
        return self.get(url)

    def get_test_statuses(self):
        """
        Retrieve a list of all Test Statuses available in Xray sorted by rank.
        :return: Returns the test statuses.
        """
        url = "rest/raven/1.0/api/settings/teststatuses"
        return self.get(url)

    def get_test_runs(self, test_key):
        """
        Retrieve test runs of a test.
        :param test_key: Test key (eg. 'TEST-001').
        :return: Returns the exported test runs.
        """
        url = "rest/raven/1.0/api/test/{0}/testruns".format(test_key)
        return self.get(url)

    def get_test_runs_with_environment(self, test_key, test_environments):
        # TODO
        """
        Retrieve test runs of a test filtered by tests environments.
        :param test_key: Test key (eg. 'TEST-001').
        :param test_environments: Test execution environments separated by ','.
        :return: Returns the exported test runs.
        """
        env = "?testEnvironments={0}".format(",".join([re.escape(env) for env in test_environments]))
        url = "rest/raven/1.0/api/test/{0}/testruns{1}".format(test_key, env)
        return self.get(url)

    def get_test_preconditions(self, test_key):
        """
        Retrieve pre-conditions of a test.
        :param test_key: Test key (eg. 'TEST-001').
        :return: Returns the test pre-conditions of a given test.
        """
        url = "rest/raven/1.0/api/test/{0}/preconditions".format(test_key)
        return self.get(url)

    def get_test_sets(self, test_key):
        """
        Retrieve test sets associated with a test.
        :param test_key: Test key (eg. 'TEST-001').
        :return: Returns the exported test sets.
        """
        url = "rest/raven/1.0/api/test/{0}/testsets".format(test_key)
        return self.get(url)

    def get_test_executions(self, test_key):
        """
        Retrieve test executions of a test.
        :param test_key: Test key (eg. 'TEST-001').
        :return: Returns the exported test executions.
        """
        url = "rest/raven/1.0/api/test/{0}/testexecutions".format(test_key)
        return self.get(url)

    def get_test_plans(self, test_key):
        """
        Retrieve test plans associated with a test.
        :param test_key: Test key (eg. 'TEST-001').
        :return: Returns the exported test plans.
        """
        url = "rest/raven/1.0/api/test/{0}/testplans".format(test_key)
        return self.get(url)

    # Test Steps API
    def get_test_step_statuses(self):
        """
        Retrieve the test step statuses available in Xray sorted by rank.
        :return: Returns the test step statuses available in Xray sorted by rank.
        """
        url = "rest/raven/1.0/api/settings/teststepstatuses"
        return self.get(url)

    def get_test_step(self, test_key, test_step_id):
        """
        Retrieve the specified test step of a given test.
        :param test_key: Test key (eg. 'TEST-001').
        :param test_step_id: ID of the test step.
        :return: Return the test step with the given id.
        """
        url = "rest/raven/1.0/api/test/{0}/step/{1}".format(test_key, test_step_id)
        return self.get(url)

    def get_test_steps(self, test_key):
        """
        Retrieve the test steps of a given test.
        :param test_key: Test key (eg. 'TEST-001').
        :return: Return the test steps of a given test.
        """
        url = "rest/raven/1.0/api/test/{0}/step".format(test_key)
        return self.get(url)

    def create_test_step(self, test_key, step, data, result):
        """
        Create a new test steps for a given test.
        NOTE: attachments are currently not supported!
        :param test_key: Test key (eg. 'TEST-001').
        :param step: Test Step name (eg. 'Example step').
        :param data: Test Step data (eg. 'Example data').
        :param result: Test Step results (eg. 'Example results').
        :return:
        """
        create = {"step": step, "data": data, "result": result, "attachments": []}
        url = "rest/raven/1.0/api/test/{0}/step".format(test_key)
        return self.put(url, create)

    def update_test_step(self, test_key, test_step_id, step, data, result):
        """
        Update the specified test steps for a given test.
        NOTE: attachments are currently not supported!
        :param test_key: Test key (eg. 'TEST-001').
        :param test_step_id: ID of the test step.
        :param step: Test Step name (eg. 'Example step').
        :param data: Test Step data (eg. 'Example data').
        :param result: Test Step results (eg. 'Example results').
        :return:
        """
        update = {
            "step": step,
            "data": data,
            "result": result,
            "attachments": {"add": [], "remove": []},
        }
        url = "rest/raven/1.0/api/test/{0}/step/{1}".format(test_key, test_step_id)
        return self.post(url, update)

    def delete_test_step(self, test_key, test_step_id):
        """
        Remove the specified test steps from a given test.
        :param test_key: Test key (eg. 'TEST-001').
        :param test_step_id: ID of the test step.
        :return:
        """
        url = "rest/raven/1.0/api/test/{0}/step/{1}".format(test_key, test_step_id)
        return self.delete(url)

    # Pre-Conditions API
    def get_tests_with_precondition(self, precondition_key):
        """
        Retrieve the tests associated with the given pre-condition.
        :param precondition_key: Precondition key (eg. 'TEST-001').
        :return: Return a list of the test associated with the pre-condition.
        """
        url = "rest/raven/1.0/api/precondition/{0}/test".format(precondition_key)
        return self.get(url)

    def update_precondition(self, precondition_key, add=None, remove=None):
        """
        Associate tests with the given pre-condition.
        :param precondition_key: Precondition key (eg. 'TEST-001').
        :param add: OPTIONAL: List of Test Keys to associate with the pre-condition (eg. ['TEST-2', 'TEST-3'])
        :param remove: OPTIONAL: List of Test Keys no longer associate with the pre-condition (eg. ['TEST-4', 'TEST-5'])
        :return:
        """
        if remove is None:
            remove = []
        if add is None:
            add = []
        update = {"add": add, "remove": remove}
        url = "rest/raven/1.0/api/precondition/{0}/test".format(precondition_key)
        return self.post(url, update)

    def delete_test_from_precondition(self, precondition_key, test_key):
        """
        Remove association of the specified tests from the given pre-condition.
        :param precondition_key: Precondition key (eg. 'TEST-001').
        :param test_key: Test Key which should no longer be associate with the pre-condition (eg. 'TEST-100')
        :return:
        """
        url = "rest/raven/1.0/api/precondition/{0}/test/{1}".format(precondition_key, test_key)
        return self.delete(url)

    # Test Set API
    def get_tests_with_test_set(self, test_set_key, limit=None, page=None):
        """
        Retrieve the tests associated with the given test set.
        :param test_set_key: Test set key (eg. 'SET-001').
        :param limit: OPTIONAL: Limits the number of results per page.
        :param page: OPTIONAL: Number of the page to be returned.
        :return: Return a list of the test associated with the test set.
        """
        url = "rest/raven/1.0/api/testset/{0}/test".format(test_set_key)
        params = {}

        if limit:
            params["limit"] = limit
        if page:
            params["page"] = page

        return self.get(url, params=params)

    def update_test_set(self, test_set_key, add=None, remove=None):
        """
        Associate tests with the given test set.
        :param test_set_key: Test set key (eg. 'SET-001').
        :param add: OPTIONAL: List of Test Keys to associate with the test set (eg. ['TEST-002', 'TEST-003'])
        :param remove: OPTIONAL: List of Test Keys no longer associate with the test set (eg. ['TEST-004', 'TEST-005'])
        :return:
        """
        if add is None:
            add = []
        if remove is None:
            remove = []
        update = {"add": add, "remove": remove}
        url = "rest/raven/1.0/api/testset/{0}/test".format(test_set_key)
        return self.post(url, update)

    def delete_test_from_test_set(self, test_set_key, test_key):
        """
        Remove association of the specified tests from the given test set.
        :param test_set_key: Test set key (eg. 'SET-001').
        :param test_key: Test Key which should no longer be associate with the test set (eg. 'TEST-100')
        :return:
        """
        url = "rest/raven/1.0/api/testset/{0}/test/{1}".format(test_set_key, test_key)
        return self.delete(url)

    # Test Plans API
    def get_tests_with_test_plan(self, test_plan_key):
        """
        Retrieve the tests associated with the given test plan.
        :param test_plan_key: Test set key (eg. 'PLAN-001').
        :return: Return a list of the test associated with the test plan.
        """
        url = "rest/raven/1.0/api/testplan/{0}/test".format(test_plan_key)
        return self.get(url)

    def update_test_plan(self, test_plan_key, add=None, remove=None):
        """
        Associate tests with the given test plan.
        :param test_plan_key: Test plan key (eg. 'PLAN-001').
        :param add: OPTIONAL: List of Test Keys to associate with the test plan (eg. ['TEST-002', 'TEST-003'])
        :param remove: OPTIONAL: List of Test Keys no longer associate with the test plan (eg. ['TEST-004', 'TEST-005'])
        :return:
        """
        if add is None:
            add = []
        if remove is None:
            remove = []
        update = {"add": add, "remove": remove}
        url = "rest/raven/1.0/api/testplan/{0}/test".format(test_plan_key)
        return self.post(url, update)

    def delete_test_from_test_plan(self, test_plan_key, test_key):
        """
        Remove association of the specified tests from the given test plan.
        :param test_plan_key: Test plan key (eg. 'PLAN-001').
        :param test_key: Test Key which should no longer be associate with the test plan (eg. 'TEST-100')
        :return:
        """
        url = "rest/raven/1.0/api/testplan/{0}/test/{1}".format(test_plan_key, test_key)
        return self.delete(url)

    def get_test_executions_with_test_plan(self, test_plan_key):
        """
        Retrieve test executions associated with the given test plan.
        :param test_plan_key: Test plan key (eg. 'PLAN-001').
        :return: Return a list of the test executions associated with the test plan.
        """
        url = "rest/raven/1.0/api/testplan/{0}/testexecution".format(test_plan_key)
        return self.get(url)

    def update_test_plan_test_executions(self, test_plan_key, add=None, remove=None):
        """
        Associate test executions with the given test plan.
        :param test_plan_key: Test plan key (eg. 'PLAN-001').
        :param add: OPTIONAL: List of Test Keys to associate with the test plan (eg. ['TEST-002', 'TEST-003'])
        :param remove: OPTIONAL: List of Test Keys no longer associate with the test plan (eg. ['TEST-004', 'TEST-005'])
        :return:
        """
        if add is None:
            add = []
        if remove is None:
            remove = []
        update = {"add": add, "remove": remove}
        url = "rest/raven/1.0/api/testplan/{0}/testexecution".format(test_plan_key)
        return self.post(url, update)

    def delete_test_execution_from_test_plan(self, test_plan_key, test_exec_key):
        """
        Remove association of the specified tests execution from the given test plan.
        :param test_plan_key: Test plan key (eg. 'PLAN-001').
        :param test_exec_key: Test execution Key which should no longer be associate with the test plan (eg. 'TEST-100')
        :return:
        """
        url = "rest/raven/1.0/api/testplan/{0}/testexecution/{1}".format(test_plan_key, test_exec_key)
        return self.delete(url)

    # Test Executions API
    def get_tests_with_test_execution(self, test_exec_key, detailed=False, limit=None, page=None):
        """
        Retrieve the tests associated with the given test execution.
        :param test_exec_key: Test execution key (eg. 'EXEC-001').
        :param detailed: OPTIONAL: (bool) Retrieve detailed information about the testrun
        :param limit: OPTIONAL: Limits the number of results per page.
        :param page: OPTIONAL: Number of the page to be returned.
        :return: Return a list of the test associated with the test execution.
        """
        url = "rest/raven/1.0/api/testexec/{0}/test".format(test_exec_key)
        params = {}

        if detailed:
            params["detailed"] = detailed
        if limit:
            params["limit"] = limit
        if page:
            params["page"] = page

        return self.get(url, params=params)

    def update_test_execution(self, test_exec_key, add=None, remove=None):
        """
        Associate tests with the given test execution.
        :param test_exec_key: Test execution key (eg. 'EXEC-001').
        :param add: OPTIONAL: List of Test Keys to associate with the test execution (eg. ['TEST-2', 'TEST-3'])
        :param remove: OPTIONAL:
            List of Test Keys no longer associate with the test execution (eg. ['TEST-4', 'TEST-5'])
        :return:
        """
        if add is None:
            add = []
        if remove is None:
            remove = []
        update = {"add": add, "remove": remove}
        url = "rest/raven/1.0/api/testexec/{0}/test".format(test_exec_key)
        return self.post(url, update)

    def delete_test_from_test_execution(self, test_exec_key, test_key):
        """
        Remove association of the specified tests from the given test execution.
        :param test_exec_key: Test execution key (eg. 'EXEC-001').
        :param test_key: Test Key which should no longer be associate with the test execution (eg. 'TEST-100')
        :return:
        """
        url = "rest/raven/1.0/api/testexec/{0}/test/{1}".format(test_exec_key, test_key)
        return self.delete(url)

    # Test Runs API
    def get_test_run(self, test_run_id):
        """
        Retrieve detailed information about the given test run.
        :param test_run_id: ID of the test run (eg. 100).
        :return: Returns detailed information about the test run.
        """
        url = "rest/raven/1.0/api/testrun/{0}".format(test_run_id)
        return self.get(url)

    def get_test_run_assignee(self, test_run_id):
        """
        Retrieve the assignee for the given test run.
        :param test_run_id: ID of the test run (eg. 100).
        :return: Returns the assignee for the given test run
        """
        url = "rest/raven/1.0/api/testrun/{0}/assignee".format(test_run_id)
        return self.get(url)

    def update_test_run_assignee(self, test_run_id, assignee):
        """
        Update the assignee for the given test run.
        :param test_run_id: ID of the test run (eg. 100).
        :param assignee: Assignee id (eg. 'bob')
        :return:
        """
        update = {"assignee": assignee}
        url = "rest/raven/1.0/api/testrun/{0}".format(test_run_id)
        return self.put(url, update)

    def get_test_run_status(self, test_run_id):
        """
        Retrieve the status for the given test run.
        :param test_run_id: ID of the test run (eg. 100).
        :return: Returns the status for the given test run
        """
        url = "rest/raven/1.0/api/testrun/{0}/status".format(test_run_id)
        return self.get(url)

    def update_test_run_status(self, test_run_id, status):
        """
        Update the status for the given test run.
        :param test_run_id: ID of the test run (eg. 100).
        :param status: Status id (eg. 'PASS')
        :return:
        """
        update = {"status": status}
        url = "rest/raven/1.0/api/testrun/{0}".format(test_run_id)
        return self.put(url, update)

    def get_test_run_defects(self, test_run_id):
        """
        Retrieve the defects for the given test run.
        :param test_run_id: ID of the test run (eg. 100).
        :return: Returns a list of defects for the given test run
        """
        url = "rest/raven/1.0/api/testrun/{0}/defect".format(test_run_id)
        return self.get(url)

    def update_test_run_defects(self, test_run_id, add=None, remove=None):
        """
        Update the defects associated with the given test run.
        :param test_run_id: ID of the test run (eg. 100).
        :param add: OPTIONAL: List of defects to associate to the test run (eg. ['BUG-001', 'BUG-002'])
        :param remove: OPTIONAL: List of defects which no longer need to be associated to the test run (eg. ['BUG-003'])
        :return:
        """
        if add is None:
            add = []
        if remove is None:
            remove = []
        update = {"defects": {"add": add, "remove": remove}}
        url = "rest/raven/1.0/api/testrun/{0}".format(test_run_id)
        return self.put(url, update)

    def get_test_run_comment(self, test_run_id):
        """
        Retrieve the comment for the given test run.
        :param test_run_id: ID of the test run (eg. 100).
        :return: Returns the comment for the given test run
        """
        url = "rest/raven/1.0/api/testrun/{0}/comment".format(test_run_id)
        return self.get(url)

    def update_test_run_comment(self, test_run_id, comment):
        """
        Update the comment for the given test run.
        :param test_run_id: ID of the test run (eg. 100).
        :param comment: Comment (eg. 'Test needs to be reworked')
        :return:
        """
        update = {"comment": comment}
        url = "rest/raven/1.0/api/testrun/{0}".format(test_run_id)
        return self.put(url, update)

    def get_test_run_steps(self, test_run_id):
        """
        Retrieve the steps for the given test run.
        :param test_run_id: ID of the test run (eg. 100).
        :return: Returns the steps for the given test run
        """
        url = "rest/raven/1.0/api/testrun/{0}/step".format(test_run_id)
        return self.get(url)
