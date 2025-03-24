# coding=utf-8
import logging
import re
from requests import HTTPError
from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Xray(AtlassianRestAPI):
    def __init__(self, *args, **kwargs):
        if "api_version" not in kwargs:
            kwargs["api_version"] = "1.0"
        kwargs["api_root"] = "rest/raven"
        super(Xray, self).__init__(*args, **kwargs)

    def raise_for_status(self, response):
        """
        Checks the response for an error status and raises an exception with the error message provided by the server
        :param response:
        :return:
        """
        if response.status_code == 401 and response.headers.get("Content-Type") != "application/json;charset=UTF-8":
            raise HTTPError("Unauthorized (401)", response=response)

        if 400 <= response.status_code < 600:
            try:
                j = response.json()
                error_msg = j["message"]
            except Exception as e:
                log.error(e)
                response.raise_for_status()
            else:
                raise HTTPError(error_msg, response=response)

    def resource_url(self, resource, api_root=None, api_version=None):
        """
        Overloading the method from AtlassianRestAPI to be compatible with the "middle man" version used by Xray.
        """
        if api_root is None:
            api_root = self.api_root
        if api_version is None:
            api_version = self.api_version
        return "/".join(s.strip("/") for s in [api_root, api_version, "api", resource] if s is not None)

    # Tests API
    def get_tests(self, test_keys):
        """
        Retrieve information about the provided tests.
        :param test_keys: list of tests (eg. `['TEST-001', 'TEST-002']`) to retrieve.
        :return: Returns the retrieved tests.
        """
        url = self.resource_url(f"test?keys={';'.join(test_keys)}")
        return self.get(url)

    def get_test_statuses(self):
        """
        Retrieve a list of all Test Statuses available in Xray sorted by rank.
        :return: Returns the test statuses.
        """
        url = self.resource_url("settings/teststatuses")
        return self.get(url)

    def get_test_runs(self, test_key):
        """
        Retrieve test runs of a test.
        :param test_key: Test key (eg. 'TEST-001').
        :return: Returns the exported test runs.
        """
        url = self.resource_url(f"test/{test_key}/testruns")
        return self.get(url)

    def get_test_runs_in_context(
        self,
        test_exec_key=None,
        test_key=None,
        test_plan_key=None,
        include_test_fields=None,
        saved_filter_id=None,
        limit=None,
        page=None,
    ):
        """
        Retrieves all the Test Runs from a given context.
        With this endpoint you can obtain all the Test Runs (paginated)
        in one of the following contexts:
        * In a Test Execution issue (use testKey to limit to single test)
        * In a Test Plan issue
        * In a JQL filter that returns several Test Execution issue
        In case the Test Run has iterations, steps will not appear.
        However, if the Test has parameters but executed one time,
        it will show the steps and the parameters' info
        :param test_exec_key: The Test Execution issue key
        :param test_key: The Test issue key
        (may only be used when using the "test_exec_key" param)
        :param test_plan_key: The Test Plan issue key
        :param include_test_fields: List of custom fields of the Test issue
        to be return in the responde
        (several custom fields can be requested by separating them with ',')
        :param saved_filter_id: The Jira JQL filter ID or
        name containing Test Executions issues
        :param limit: The number of maximum Test Runs to be returned
        :param page: The number of the results page
        :return: Returns the exported test runs.
        """
        if self.api_version == "1.0":
            raise Exception("Not supported in API version 1.0")
        params = {}
        if test_exec_key:
            params["testExecKey"] = test_exec_key
        if test_key:
            params["testKey"] = test_key
        if test_plan_key:
            params["testPlanKey"] = test_plan_key
        if include_test_fields:
            params["includeTestFields"] = include_test_fields
        if saved_filter_id:
            params["savedFilterId"] = saved_filter_id
        if limit:
            params["limit"] = limit
        if page:
            params["page"] = page
        url = self.resource_url("testruns")
        return self.get(url, params=params)

    def get_test_runs_with_environment(self, test_key, test_environments):
        # TODO
        """
        Retrieve test runs of a test filtered by tests environments.
        :param test_key: Test key (eg. 'TEST-001').
        :param test_environments: Test execution environments separated by ','.
        :return: Returns the exported test runs.
        """
        env = f"?testEnvironments={','.join([re.escape(env) for env in test_environments])}"
        url = self.resource_url(f"test/{test_key}/testruns{env}")
        return self.get(url)

    def get_test_preconditions(self, test_key):
        """
        Retrieve pre-conditions of a test.
        :param test_key: Test key (eg. 'TEST-001').
        :return: Returns the test pre-conditions of a given test.
        """
        url = self.resource_url(f"test/{test_key}/preconditions")
        return self.get(url)

    def get_test_sets(self, test_key):
        """
        Retrieve test sets associated with a test.
        :param test_key: Test key (eg. 'TEST-001').
        :return: Returns the exported test sets.
        """
        url = self.resource_url(f"test/{test_key}/testsets")
        return self.get(url)

    def get_test_executions(self, test_key):
        """
        Retrieve test executions of a test.
        :param test_key: Test key (eg. 'TEST-001').
        :return: Returns the exported test executions.
        """
        url = self.resource_url(f"test/{test_key}/testexecutions")
        return self.get(url)

    def get_test_plans(self, test_key):
        """
        Retrieve test plans associated with a test.
        :param test_key: Test key (eg. 'TEST-001').
        :return: Returns the exported test plans.
        """
        url = self.resource_url(f"test/{test_key}/testplans")
        return self.get(url)

    # Test Steps API
    def get_test_step_statuses(self):
        """
        Retrieve the test step statuses available in Xray sorted by rank.
        :return: Returns the test step statuses available in Xray sorted by rank.
        """
        url = self.resource_url("settings/teststepstatuses")
        return self.get(url)

    def get_test_step(self, test_key, test_step_id):
        """
        Retrieve the specified test step of a given test.
        :param test_key: Test key (eg. 'TEST-001').
        :param test_step_id: ID of the test step.
        :return: Return the test step with the given id.
        """
        url = self.resource_url(f"test/{test_key}/step/{test_step_id}")
        return self.get(url)

    def get_test_steps(self, test_key):
        """
        Retrieve the test steps of a given test.
        :param test_key: Test key (eg. 'TEST-001').
        :return: Return the test steps of a given test.
        """
        url = self.resource_url(f"test/{test_key}/step")
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
        url = self.resource_url(f"test/{test_key}/step")
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
        url = self.resource_url(f"test/{test_key}/step/{test_step_id}")
        return self.post(url, update)

    def delete_test_step(self, test_key, test_step_id):
        """
        Remove the specified test steps from a given test.
        :param test_key: Test key (eg. 'TEST-001').
        :param test_step_id: ID of the test step.
        :return:
        """
        url = self.resource_url(f"test/{test_key}/step/{test_step_id}")
        return self.delete(url)

    # Pre-Conditions API
    def get_tests_with_precondition(self, precondition_key):
        """
        Retrieve the tests associated with the given pre-condition.
        :param precondition_key: Precondition key (eg. 'TEST-001').
        :return: Return a list of the test associated with the pre-condition.
        """
        url = self.resource_url(f"precondition/{precondition_key}/test")
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
        url = self.resource_url(f"precondition/{precondition_key}/test")
        return self.post(url, update)

    def delete_test_from_precondition(self, precondition_key, test_key):
        """
        Remove association of the specified tests from the given pre-condition.
        :param precondition_key: Precondition key (eg. 'TEST-001').
        :param test_key: Test Key which should no longer be associate with the pre-condition (eg. 'TEST-100')
        :return:
        """
        url = self.resource_url(f"precondition/{precondition_key}/test/{test_key}")
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
        url = self.resource_url(f"testset/{test_set_key}/test")
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
        url = self.resource_url(f"testset/{test_set_key}/test")
        return self.post(url, update)

    def delete_test_from_test_set(self, test_set_key, test_key):
        """
        Remove association of the specified tests from the given test set.
        :param test_set_key: Test set key (eg. 'SET-001').
        :param test_key: Test Key which should no longer be associate with the test set (eg. 'TEST-100')
        :return:
        """
        url = self.resource_url(f"testset/{test_set_key}/test/{test_key}")
        return self.delete(url)

    # Test Plans API
    def get_tests_with_test_plan(self, test_plan_key, limit=None, page=None):
        """
        Retrieve the tests associated with the given test plan.
        :param test_plan_key: Test set key (eg. 'PLAN-001').
        :param limit: OPTIONAL: Limits the number of results per page.
        :param page: OPTIONAL: Number of the page to be returned.
        :return: Return a list of the test associated with the test plan.
        """
        url = self.resource_url(f"testplan/{test_plan_key}/test")
        params = {}

        if limit:
            params["limit"] = limit
        if page:
            params["page"] = page

        return self.get(url, params=params)

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
        url = self.resource_url(f"testplan/{test_plan_key}/test")
        return self.post(url, update)

    def delete_test_from_test_plan(self, test_plan_key, test_key):
        """
        Remove association of the specified tests from the given test plan.
        :param test_plan_key: Test plan key (eg. 'PLAN-001').
        :param test_key: Test Key which should no longer be associate with the test plan (eg. 'TEST-100')
        :return:
        """
        url = self.resource_url(f"testplan/{test_plan_key}/test/{test_key}")
        return self.delete(url)

    def get_test_executions_with_test_plan(self, test_plan_key):
        """
        Retrieve test executions associated with the given test plan.
        :param test_plan_key: Test plan key (eg. 'PLAN-001').
        :return: Return a list of the test executions associated with the test plan.
        """
        url = self.resource_url(f"testplan/{test_plan_key}/testexecution")
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
        url = self.resource_url(f"testplan/{test_plan_key}/testexecution")
        return self.post(url, update)

    def delete_test_execution_from_test_plan(self, test_plan_key, test_exec_key):
        """
        Remove association of the specified tests execution from the given test plan.
        :param test_plan_key: Test plan key (eg. 'PLAN-001').
        :param test_exec_key: Test execution Key which should no longer be associate with the test plan (eg. 'TEST-100')
        :return:
        """
        url = self.resource_url(f"testplan/{test_plan_key}/testexecution/{test_exec_key}")
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
        url = self.resource_url(f"testexec/{test_exec_key}/test")
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
        url = self.resource_url(f"testexec/{test_exec_key}/test")
        return self.post(url, update)

    def delete_test_from_test_execution(self, test_exec_key, test_key):
        """
        Remove association of the specified tests from the given test execution.
        :param test_exec_key: Test execution key (eg. 'EXEC-001').
        :param test_key: Test Key which should no longer be associate with the test execution (eg. 'TEST-100')
        :return:
        """
        url = self.resource_url(f"testexec/{test_exec_key}/test/{test_key}")
        return self.delete(url)

    # Test Runs API
    def get_test_run(self, test_run_id):
        """
        Retrieve detailed information about the given test run.
        :param test_run_id: ID of the test run (e.g. 100).
        :return: Returns detailed information about the test run.
        """
        url = self.resource_url(f"testrun/{test_run_id}")
        return self.get(url)

    def get_test_run_assignee(self, test_run_id):
        """
        Retrieve the assignee for the given test run.
        :param test_run_id: ID of the test run (e.g. 100).
        :return: Returns the assignee for the given test run
        """
        url = self.resource_url(f"testrun/{test_run_id}/assignee")
        return self.get(url)

    def update_test_run_assignee(self, test_run_id, assignee):
        """
        Update the assignee for the given test run.
        :param test_run_id: ID of the test run (eg. 100).
        :param assignee: Assignee id (eg. 'bob')
        :return:
        """
        update = {"assignee": assignee}
        url = self.resource_url(f"testrun/{test_run_id}")
        return self.put(url, update)

    def get_test_run_iteration(self, test_run_id, iteration_id):
        """
        Retrieve the specified iteration for the given test run.
        :param test_run_id: ID of the test run (e.g. 100).
        :param iteration_id: ID of the iteration.
        :return: Returns the specified iteration for the given test run.
        """
        url = self.resource_url(f"testrun/{test_run_id}/iteration/{iteration_id}")
        return self.get(url)

    def get_test_run_status(self, test_run_id):
        """
        Retrieve the status for the given test run.
        :param test_run_id: ID of the test run (e.g. 100).
        :return: Returns the status for the given test run
        """
        url = self.resource_url(f"testrun/{test_run_id}/status")
        return self.get(url)

    def update_test_run_status(self, test_run_id, status):
        """
        Update the status for the given test run.
        :param test_run_id: ID of the test run (e.g. 100).
        :param status: Status id (eg. 'PASS')
        :return:
        """
        update = {"status": status}
        url = self.resource_url(f"testrun/{test_run_id}")
        return self.put(url, update)

    def get_test_run_defects(self, test_run_id):
        """
        Retrieve the defects for the given test run.
        :param test_run_id: ID of the test run (e.g. 100).
        :return: Returns a list of defects for the given test run
        """
        url = self.resource_url(f"testrun/{test_run_id}/defect")
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
        url = self.resource_url(f"testrun/{test_run_id}")
        return self.put(url, update)

    def get_test_run_comment(self, test_run_id):
        """
        Retrieve the comment for the given test run.
        :param test_run_id: ID of the test run (e.g. 100).
        :return: Returns the comment for the given test run
        """
        url = self.resource_url(f"testrun/{test_run_id}/comment")
        return self.get(url)

    def update_test_run_comment(self, test_run_id, comment):
        """
        Update the comment for the given test run.
        :param test_run_id: ID of the test run (eg. 100).
        :param comment: Comment (e.g. 'Test needs to be reworked')
        :return:
        """
        update = {"comment": comment}
        url = self.resource_url(f"testrun/{test_run_id}")
        return self.put(url, update)

    def get_test_run_steps(self, test_run_id):
        """
        Retrieve the steps for the given test run.
        :param test_run_id: ID of the test run (e.g. 100).
        :return: Returns the steps for the given test run
        """
        url = self.resource_url(f"testrun/{test_run_id}/step")
        return self.get(url)

    def get_test_repo_folders(self, project_key):
        """
        Retrieve test repository folders of a project.
        :param project_key: Project key (eg. 'FOO').
        :return: Returns the list of test repository folders.
        """
        url = self.resource_url(f"testrepository/{project_key}/folders")
        return self.get(url)

    def get_test_repo_folder(self, project_key, folder_id):
        """
        Retrieve test repository folder of a project.
        :param project_key: Project key (eg. 'FOO').
        :param folder_id: Internal folder ID.
        :return: Returns the test repository folder.
        """
        url = self.resource_url(f"testrepository/{project_key}/folders/{folder_id}")
        return self.get(url)

    def create_test_repo_folder(self, project_key, folder_name, parent_folder_id=-1):
        """
        Create test repository folder for a project.
        :param project_key: Project key (eg. 'FOO').
        :param folder_name: Name of folder.
        :param parent_folder_id: Internal folder ID; "-1" corresponds to the root folder of the test repository.
        :return: Returns the created test repository folder.
        """
        data = {"name": folder_name}
        url = self.resource_url(f"testrepository/{project_key}/folders/{parent_folder_id}")
        return self.post(url, data=data)

    def update_test_repo_folder(self, project_key, folder_id, folder_name, rank=1):
        """
        Update test repository folder for a project.
        :param project_key: Project key (eg. 'FOO').
        :param folder_id: Internal folder ID.
        :param folder_name: Name of folder.
        :param rank: Rank within the parent folder.
        :return: Returns the updated test repository folder.
        """
        data = {"name": folder_name, "rank": rank}
        url = self.resource_url(f"testrepository/{project_key}/folders/{folder_id}")
        return self.put(url, data=data)

    def delete_test_repo_folder(self, project_key, folder_id):
        """
        Delete test repository folder for a project.
        :param project_key: Project key (eg. 'FOO').
        :param folder_id: Internal folder Id.
        :return: Returns the delete results.
        """
        url = self.resource_url(f"testrepository/{project_key}/folders/{folder_id}")
        return self.delete(url)

    def get_test_repo_folder_tests(self, project_key, folder_id, all_descendants=False, page=1, limit=50):
        """
        Retrieve tests of a test repository folder.
        :param project_key: Project key (eg. 'FOO').
        :param folder_id: Internal folder ID.
        :param all_descendants: Include all descendants (i.e. all child Tests); "false", by default.
        :param page: Page of paginated data (first 1)
        :param limit: Amount of Tests per paginated data.
        :return: Returns list of the Tests contained in a given folder of the test repository.
        Note: param "page" and "limit" must coexist, otherwise rest api will raise 400
        """
        url = self.resource_url(f"testrepository/{project_key}/folders/{folder_id}/tests")
        params = {}

        if all_descendants:
            params["allDescendants"] = all_descendants
        if page:
            params["page"] = page
        if limit:
            params["limit"] = limit

        return self.get(url, params=params)

    def update_test_repo_folder_tests(self, project_key, folder_id, add=None, remove=None):
        """
        Update tests of a test repository folder.
        :param project_key: Project key (eg. 'FOO').
        :param folder_id: Internal folder Id.
        :param add: OPTIONAL: List of tests to be added (eg. ['TEST-001', 'TEST-002'])
        :param remove: OPTIONAL: List of tests to be removed (eg. ['TEST-003'])
        :return: Returns the update result.
        """
        if add is None:
            add = []
        if remove is None:
            remove = []
        data = {"add": add, "remove": remove}
        url = self.resource_url(f"testrepository/{project_key}/folders/{folder_id}/tests")
        return self.put(url, data=data)
