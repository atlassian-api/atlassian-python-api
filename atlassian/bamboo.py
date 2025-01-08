# coding=utf-8
import logging

from requests.exceptions import HTTPError
from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Bamboo(AtlassianRestAPI):
    """Private methods"""

    def _get_generator(
        self,
        path,
        elements_key="results",
        element_key="result",
        data=None,
        flags=None,
        params=None,
        headers=None,
        max_results=None,
    ):
        """
        Generic method to return a generator with the results returned from Bamboo. It is intended to work for
        responses in the form:
        {
            'results':
            {
                'size': 5,
                'start-index': 0,
                'max-result': 5,
                'result': []
            },
            ...
        }
        In this case we would have elements_key='results' element_key='result'.
        The only reason to use this generator is to abstract dealing with response pagination from the client

        :param path: URI for the resource
        :return: generator with the contents of response[elements_key][element_key]
        """
        response = self.get(path, data, flags, params, headers)
        if self.advanced_mode:
            try:
                response.raise_for_status()
                response = response.json()
            except HTTPError as e:
                logging.error("Broken response: {}".format(e))
                yield e
        try:
            results = response[elements_key]
            size = 0
            # Check if we still can get results
            if size > max_results or results["size"] == 0:
                return
            for r in results[element_key]:
                size += 1
                yield r
        except TypeError:
            logging.error("Broken response: {}".format(response))
            yield response

    def base_list_call(
        self,
        resource,
        expand,
        favourite,
        clover_enabled,
        max_results,
        label=None,
        start_index=0,
        **kwargs
    ):  # fmt: skip
        flags = []
        params = {"max-results": max_results}
        if expand:
            params["expand"] = expand
        if favourite:
            flags.append("favourite")
        if clover_enabled:
            flags.append("cloverEnabled")
        if label:
            params["label"] = label
        params.update(kwargs)
        if "elements_key" in kwargs and "element_key" in kwargs:
            return self._get_generator(
                self.resource_url(resource),
                flags=flags,
                params=params,
                elements_key=kwargs["elements_key"],
                element_key=kwargs["element_key"],
                max_results=max_results,
            )
        params["start-index"] = start_index
        return self.get(self.resource_url(resource), flags=flags, params=params)

    """ Projects & Plans """

    def projects(
        self,
        expand=None,
        favourite=False,
        clover_enabled=False,
        max_results=25,
    ):
        """
        Get all Projects
        :param expand:
        :param favourite:
        :param clover_enabled:
        :param max_results:
        :return:
        """
        return self.base_list_call(
            "project",
            expand=expand,
            favourite=favourite,
            clover_enabled=clover_enabled,
            max_results=max_results,
            elements_key="projects",
            element_key="project",
        )

    def project(self, project_key, expand=None, favourite=False, clover_enabled=False):
        """
        Get a single project by the key
        :param project_key:
        :param expand:
        :param favourite:
        :param clover_enabled:
        :return:
        """
        resource = "project/{}".format(project_key)
        return self.base_list_call(
            resource=resource,
            expand=expand,
            favourite=favourite,
            clover_enabled=clover_enabled,
            start_index=0,
            max_results=25,
        )

    def get_project(self, project_key):
        """Method used to retrieve information for project specified as project key.
        Possible expand parameters: plans, list of plans for project. plans.plan, list of plans with plan details
        (only plans visible - READ permission for user)"""
        resource = "project/{}?showEmpty".format(project_key)
        return self.get(self.resource_url(resource))

    def delete_project(self, project_key):
        """Marks project for deletion. Project will be deleted by a batch job."""
        resource = "project/{}".format(project_key)
        return self.delete(self.resource_url(resource))

    def project_plans(self, project_key, start_index=0, max_results=25):
        """
        Get all build plans in a project
        Returns a generator with the plans in a given project.
        :param project_key: project key
        :param start_index:
        :param max_results:
        :return: Generator with plans
        """
        resource = "project/{}".format(project_key)
        return self.base_list_call(
            resource,
            expand="plans",
            favourite=False,
            clover_enabled=False,
            start_index=start_index,
            max_results=max_results,
            elements_key="plans",
            element_key="plan",
        )

    def plans(
        self,
        expand=None,
        favourite=False,
        clover_enabled=False,
        start_index=0,
        max_results=25,
    ):
        """
        Get all build plans
        :param expand:
        :param favourite:
        :param clover_enabled:
        :param start_index:
        :param max_results:
        :return:
        """
        return self.base_list_call(
            "plan",
            expand=expand,
            favourite=favourite,
            clover_enabled=clover_enabled,
            start_index=start_index,
            max_results=max_results,
            elements_key="plans",
            element_key="plan",
        )

    def plan_directory_info(self, plan_key):
        """
        Returns information about the directories where artifacts, build logs, and build results will be stored.
        Disabled by default.
        See https://confluence.atlassian.com/display/BAMBOO/Plan+directory+information+REST+API for more information.
        :param plan_key:
        :return:
        """
        resource = "planDirectoryInfo/{}".format(plan_key)
        return self.get(self.resource_url(resource))

    def get_plan(self, plan_key, expand=None):
        """
        Get plan information.
        :param plan_key:
        :param expand: optional
        :return:
        """
        params = {}
        if expand:
            params["expand"] = expand
        resource = "rest/api/latest/plan/{}".format(plan_key)
        return self.get(resource, params=params)

    def search_plans(self, search_term, fuzzy=True, start_index=0, max_results=25):
        """
        Search plans by name
        :param search_term: str
        :param fuzzy: bool optional
        :param start_index: optional
        :param max_results: optional
        :return: GET request
        """

        resource = "rest/api/latest/search/plans"
        return self.get(
            resource,
            params={"fuzzy": fuzzy, "searchTerm": search_term, "max-results": max_results, "start-index": start_index},
        )

    def delete_plan(self, plan_key):
        """
        Marks plan for deletion. Plan will be deleted by a batch job.
        :param plan_key:
        :return:
        """
        resource = "rest/api/latest/plan/{}".format(plan_key)
        return self.delete(resource)

    def disable_plan(self, plan_key):
        """
        Disable plan.
        :param plan_key: str TST-BLD
        :return: DELETE request
        """
        resource = "plan/{plan_key}/enable".format(plan_key=plan_key)
        return self.delete(self.resource_url(resource))

    def enable_plan(self, plan_key):
        """
        Enable plan.
        :param plan_key: str TST-BLD
        :return: POST request
        """
        resource = "plan/{plan_key}/enable".format(plan_key=plan_key)
        return self.post(self.resource_url(resource))

    """ Branches """

    def search_branches(self, plan_key, include_default_branch=True, max_results=25, start=0):
        """
        Search Branches
        :param plan_key:
        :param include_default_branch:
        :param max_results:
        :param start:
        :return:
        """
        params = {
            "max-result": max_results,
            "start-index": start,
            "masterPlanKey": plan_key,
            "includeMasterBranch": include_default_branch,
        }
        size = 1
        while params["start-index"] < size:
            results = self.get(self.resource_url("search/branches"), params=params)
            size = results["size"]
            for r in results["searchResults"]:
                yield r
            params["start-index"] += results["max-result"]

    def plan_branches(
        self,
        plan_key,
        expand=None,
        favourite=False,
        clover_enabled=False,
        max_results=25,
    ):
        """
        Get all plan Branches
        api/1.0/plan/{projectKey}-{buildKey}/branch
        :param plan_key:
        :param expand:
        :param favourite:
        :param clover_enabled:
        :param max_results:
        :return:
        """
        resource = "plan/{}/branch".format(plan_key)
        return self.base_list_call(
            resource,
            expand,
            favourite,
            clover_enabled,
            max_results,
            elements_key="branches",
            element_key="branch",
        )

    def get_branch_info(self, plan_key, branch_name):
        """
        Get information about a plan branch
        :param plan_key:
        :param branch_name:
        :return:
        """
        resource = "plan/{plan_key}/branch/{branch_name}".format(plan_key=plan_key, branch_name=branch_name)
        return self.get(self.resource_url(resource))

    def create_branch(
        self,
        plan_key,
        branch_name,
        vcs_branch=None,
        enabled=False,
        cleanup_enabled=False,
    ):
        """
        Method for creating branch for a specified plan.
        You can use vcsBranch query param to define which vcsBranch should newly created branch use.
        If not specified it will not override vcsBranch from the main plan.

        :param plan_key: str TST-BLD
        :param branch_name: str new-shiny-branch
        :param vcs_branch: str feature/new-shiny-branch, /refs/heads/new-shiny-branch
        :param enabled: bool
        :param cleanup_enabled: bool - enable/disable automatic cleanup of branch
        :return: PUT request
        """
        resource = "plan/{plan_key}/branch/{branch_name}".format(plan_key=plan_key, branch_name=branch_name)
        params = {}
        if vcs_branch:
            params = dict(
                vcsBranch=vcs_branch,
                enabled="true" if enabled else "false",
                cleanupEnabled="true" if cleanup_enabled else "false",
            )
        return self.put(self.resource_url(resource), params=params)

    def get_vcs_branches(self, plan_key, max_results=25):
        """
        Get all vcs names for the current plan
        :param plan_key: str TST-BLD
        :param max_results
        :return:
        """
        resource = "plan/{plan_key}/vcsBranches".format(plan_key=plan_key)
        return self.base_list_call(
            resource,
            start_index=0,
            max_results=max_results,
            clover_enabled=None,
            expand=None,
            favourite=None,
        )

    """ Build results """

    def results(
        self,
        project_key=None,
        plan_key=None,
        job_key=None,
        build_number=None,
        expand=None,
        favourite=False,
        clover_enabled=False,
        issue_key=None,
        label=None,
        start_index=0,
        max_results=25,
        include_all_states=False,
    ):
        """
        Get results as generic method
        :param project_key:
        :param plan_key:
        :param job_key:
        :param build_number:
        :param expand:
        :param favourite:
        :param clover_enabled:
        :param issue_key:
        :param label:
        :param start_index:
        :param max_results:
        :param include_all_states:
        :return:
        """
        resource = "result"
        if project_key and plan_key and job_key and build_number:
            resource += "/{}-{}-{}/{}".format(project_key, plan_key, job_key, build_number)
        elif project_key and plan_key and build_number:
            resource += "/{}-{}/{}".format(project_key, plan_key, build_number)
        elif project_key and plan_key:
            resource += "/{}-{}".format(project_key, plan_key)
        elif project_key:
            resource += "/" + project_key

        params = {}
        if issue_key:
            params["issueKey"] = issue_key
        if include_all_states:
            params["includeAllStates"] = include_all_states
        return self.base_list_call(
            resource,
            expand=expand,
            favourite=favourite,
            clover_enabled=clover_enabled,
            start_index=start_index,
            max_results=max_results,
            elements_key="results",
            element_key="result",
            label=label,
            **params
        )  # fmt: skip

    def latest_results(
        self,
        expand=None,
        favourite=False,
        clover_enabled=False,
        label=None,
        issue_key=None,
        start_index=0,
        max_results=25,
        include_all_states=False,
    ):
        """
        Get the latest Results
        :param expand:
        :param favourite:
        :param clover_enabled:
        :param label:
        :param issue_key:
        :param start_index:
        :param max_results:
        :param include_all_states:
        :return:
        """
        return self.results(
            expand=expand,
            favourite=favourite,
            clover_enabled=clover_enabled,
            label=label,
            issue_key=issue_key,
            start_index=start_index,
            max_results=max_results,
            include_all_states=include_all_states,
        )

    def project_latest_results(
        self,
        project_key,
        expand=None,
        favourite=False,
        clover_enabled=False,
        label=None,
        issue_key=None,
        start_index=0,
        max_results=25,
        include_all_states=False,
    ):
        """
        Get the latest Project Results
        :param project_key:
        :param expand:
        :param favourite:
        :param clover_enabled:
        :param label:
        :param issue_key:
        :param start_index:
        :param max_results:
        :param include_all_states:
        :return:
        """
        return self.results(
            project_key,
            expand=expand,
            favourite=favourite,
            clover_enabled=clover_enabled,
            label=label,
            issue_key=issue_key,
            start_index=start_index,
            max_results=max_results,
            include_all_states=include_all_states,
        )

    def plan_results(
        self,
        project_key,
        plan_key,
        expand=None,
        favourite=False,
        clover_enabled=False,
        label=None,
        issue_key=None,
        start_index=0,
        max_results=25,
        include_all_states=False,
    ):
        """
        Get Plan results
        :param project_key:
        :param plan_key:
        :param expand:
        :param favourite:
        :param clover_enabled:
        :param label:
        :param issue_key:
        :param start_index:
        :param max_results:
        :param include_all_states:
        :return:
        """
        return self.results(
            project_key,
            plan_key,
            expand=expand,
            favourite=favourite,
            clover_enabled=clover_enabled,
            label=label,
            issue_key=issue_key,
            start_index=start_index,
            max_results=max_results,
            include_all_states=include_all_states,
        )

    def build_result(
        self,
        build_key,
        expand=None,
        include_all_states=False,
        start=0,
        max_results=25,
    ):
        """
        Returns details of a specific build result
        :param expand: expands build result details on request. Possible values are: artifacts, comments, labels,
        Jira Issues, stages. stages expand is available only for top level plans. It allows to drill down to job results
        using stages.stage.results.result. All expand parameters should contain results. Result prefix.
        :param build_key: Should be in the form XX-YY[-ZZ]-99, that is, the last token should be an integer representing
        the build number
        :param include_all_states
        :param start:
        :param max_results:
        """
        try:
            int(build_key.split("-")[-1])
            resource = "result/{}".format(build_key)
            return self.base_list_call(
                resource,
                expand,
                favourite=False,
                clover_enabled=False,
                start_index=start,
                max_results=max_results,
                include_all_states=include_all_states,
            )
        except ValueError:
            raise ValueError('The key "{}" does not correspond to a build result'.format(build_key))

    def build_latest_result(self, plan_key, expand=None, include_all_states=False):
        """
        Returns details of the latest build result
        :param expand: expands build result details on request. Possible values are: artifacts, comments, labels,
        Jira Issues, stages. stages expand is available only for top level plans. It allows to drill down to job results
        using stages.stage.results.result. All expand parameters should contain results. Result prefix.
        :param plan_key: Should be in the form XX-YY[-ZZ]
        :param include_all_states:
        """
        try:
            resource = "result/{}/latest.json".format(plan_key)
            return self.base_list_call(
                resource,
                expand,
                favourite=False,
                clover_enabled=False,
                start_index=0,
                max_results=25,
                include_all_states=include_all_states,
            )
        except ValueError:
            raise ValueError('The key "{}" does not correspond to the latest build result'.format(plan_key))

    def delete_build_result(self, build_key):
        """
        Deleting result for specific build
        :param build_key: Take full build key, example: PROJECT-PLAN-8
        """
        custom_resource = "/build/admin/deletePlanResults.action"
        build_key = build_key.split("-")
        plan_key = "{}-{}".format(build_key[0], build_key[1])
        build_number = build_key[2]
        params = {"buildKey": plan_key, "buildNumber": build_number}
        return self.post(custom_resource, params=params, headers=self.form_token_headers)

    def execute_build(
        self,
        plan_key,
        stage=None,
        execute_all_stages=True,
        custom_revision=None,
        **bamboo_variables
    ):  # fmt: skip
        """
        Fire build execution for specified plan.
        !IMPORTANT! NOTE: for some reason, this method always execute all stages
        :param plan_key: str TST-BLD
        :param stage: str stage-name
        :param execute_all_stages: bool
        :param custom_revision: str revisionName
        :param bamboo_variables: dict {variable=value}
        :return: POST request
        """
        resource = "queue/{plan_key}".format(plan_key=plan_key)
        params = {}
        if stage:
            execute_all_stages = False
            params["stage"] = stage
        if custom_revision:
            params["customRevision"] = custom_revision
        params["executeAllStages"] = "true" if execute_all_stages else "false"
        if bamboo_variables:
            for key, value in bamboo_variables.items():
                params["bamboo.variable.{}".format(key)] = value

        return self.post(self.resource_url(resource), params=params)

    def stop_build(self, plan_key):
        """
        Stop the build which is in progress at the moment.
        :param plan_key: str TST-BLD
        :return: GET request
        """
        resource = "/build/admin/stopPlan.action?planKey={}".format(plan_key)
        return self.post(path=resource, headers=self.no_check_headers)

    """ Comments & Labels """

    def comments(
        self,
        project_key,
        plan_key,
        build_number,
        start_index=0,
        max_results=25,
    ):
        """
        Get comments for a specific build
        :param project_key:
        :param plan_key:
        :param build_number:
        :param start_index:
        :param max_results:
        :return:
        """
        resource = "result/{}-{}-{}/comment".format(project_key, plan_key, build_number)
        params = {"start-index": start_index, "max-results": max_results}
        return self.get(self.resource_url(resource), params=params)

    def create_comment(self, project_key, plan_key, build_number, comment):
        """
        Create a comment for a specific build
        :param project_key:
        :param plan_key:
        :param build_number:
        :param comment:
        :return:
        """
        resource = "result/{}-{}-{}/comment".format(project_key, plan_key, build_number)
        comment_data = {
            "content": comment,
        }
        return self.post(self.resource_url(resource), data=comment_data)

    def labels(
        self,
        project_key,
        plan_key,
        build_number,
        start_index=0,
        max_results=25,
    ):
        """
        Get labels for a build
        :param project_key:
        :param plan_key:
        :param build_number:
        :param start_index:
        :param max_results:
        :return:
        """
        resource = "result/{}-{}-{}/label".format(project_key, plan_key, build_number)
        params = {"start-index": start_index, "max-results": max_results}
        return self.get(self.resource_url(resource), params=params)

    def create_label(self, project_key, plan_key, build_number, label):
        """
        Create a label for a specific build
        :param project_key:
        :param plan_key:
        :param build_number:
        :param label:
        :return:
        """
        resource = "result/{}-{}-{}/label".format(project_key, plan_key, build_number)
        return self.post(self.resource_url(resource), data={"name": label})

    def delete_label(self, project_key, plan_key, build_number, label):
        """
        Delete a label for a specific build
        :param project_key:
        :param plan_key:
        :param build_number:
        :param label:
        :return:
        """
        resource = "result/{}-{}-{}/label/{}".format(project_key, plan_key, build_number, label)
        return self.delete(self.resource_url(resource))

    def get_projects(self):
        """Method used to list all projects defined in Bamboo.
        Projects without any plan are not listed."""
        start_idx = 0
        max_results = 25

        while True:
            resource = "project?start-index={}&max-result={}".format(start_idx, max_results)

            r = self.get(self.resource_url(resource))

            if r is None:
                break

            if start_idx > r["projects"]["size"]:
                break

            start_idx += max_results

            for project in r["projects"]["project"]:
                yield project

    """ Deployments """

    def deployment_projects(self):
        """
        Returns all deployment projects.
        :return:
        """
        resource = "deploy/project/all"
        for project in self.get(self.resource_url(resource)):
            yield project

    def deployment_project(self, project_id):
        """
        Returns a deployment project.
        :param project_id:
        :return:
        """
        resource = "deploy/project/{}".format(project_id)
        return self.get(self.resource_url(resource))

    def delete_deployment_project(self, project_id):
        """
        Deletes a deployment project.
        :param project_id:
        :return:
        """
        resource = "deploy/project/{}".format(project_id)
        return self.delete(self.resource_url(resource))

    def deployment_environment_results(self, env_id, expand=None, max_results=25):
        """
        Get deployment environment results
        :param env_id:
        :param expand:
        :param max_results:
        :return:
        """
        resource = "deploy/environment/{environmentId}/results".format(environmentId=env_id)
        params = {"max-result": max_results, "start-index": 0}
        size = 1
        if expand:
            params["expand"] = expand
        while params["start-index"] < size:
            results = self.get(self.resource_url(resource), params=params)
            size = results["size"]
            for r in results["results"]:
                yield r
            params["start-index"] += results["max-result"]

    def deployment_dashboard(self, project_id=None):
        """
        Returns the current status of each deployment environment
        If no project id is provided, returns all projects.
        """
        resource = "deploy/dashboard/{}".format(project_id) if project_id else "deploy/dashboard"
        return self.get(self.resource_url(resource))

    def get_deployment_projects_for_plan(self, plan_key):
        """
        Returns deployment projects associated with a build plan.
        :param plan_key: The key of the plan.
        """
        resource = "deploy/project/forPlan"
        params = {"planKey": plan_key}
        for deployment_project in self.get(self.resource_url(resource), params=params):
            yield deployment_project

    def trigger_deployment_for_version_on_environment(self, version_id, environment_id):
        """
        Triggers a deployment for a release version on the given environment.
        Example: trigger_deployment_for_version_on_environment(version_id='3702785', environment_id='3637249')
        :param version_id: str or int id of the release version.
        :param environment_id: str or int id of the deployment environment.
        :return:
        """
        resource = "queue/deployment"
        params = {"versionId": version_id, "environmentId": environment_id}
        return self.post(self.resource_url(resource), params=params)

    """ Users & Groups """

    def get_users_in_global_permissions(self, start=0, limit=25):
        """
        Provide users in global permissions configuration
        :param start:
        :param limit:
        :return:
        """
        params = {"limit": limit, "start": start}
        url = "rest/api/latest/permissions/global/users"
        return self.get(url, params=params)

    def get_groups(self, start=0, limit=25):
        """
        Retrieve a paginated list of groups.
        The authenticated user must have restricted administrative permission or higher to use this resource.
        :param start:
        :param limit:
        :return:
        """
        params = {"limit": limit, "start": start}
        url = "rest/api/latest/admin/groups"
        return self.get(url, params=params)

    def create_group(self, group_name):
        """
        Create a new group.
        The authenticated user must have restricted administrative permission or higher to use this resource.
        :param group_name:
        :return:
        """
        url = "rest/api/latest/admin/groups"
        data = {"name": group_name}
        return self.post(url, data=data)

    def delete_group(self, group_name):
        """
        Deletes the specified group, removing it from the system.
        The authenticated user must have restricted administrative permission or higher to use this resource.
        :param group_name:
        :return:
        """
        url = "rest/api/latest/admin/groups/{}".format(group_name)
        return self.delete(url)

    def add_users_into_group(self, group_name, users):
        """
        Add multiple users to a group.
        The list of usernames should be passed as request body.
        The authenticated user must have restricted administrative permission or higher to use this resource.
        :param group_name:
        :param users: list
        :return:
        """
        url = "rest/api/latest/admin/groups/{}/add-users".format(group_name)
        return self.post(url, data=users)

    def remove_users_from_group(self, group_name, users):
        """
        Remove multiple users from a group.
        The list of usernames should be passed as request body.
        The authenticated user must have restricted administrative permission or higher to use this resource.
        :param group_name:
        :param users: list
        :return:
        """
        url = "rest/api/latest/admin/groups/{}/remove-users".format(group_name)
        return self.delete(url, data=users)

    def get_users_from_group(self, group_name, filter_users=None, start=0, limit=25):
        """
        Retrieves a list of users that are members of a specified group.
        The authenticated user must have restricted administrative permission or higher to use this resource.
        :param filter_users:
        :param group_name:
        :param start:
        :param limit:
        :return:
        """
        params = {"limit": limit, "start": start}
        if filter_users:
            params = {"filter": filter_users}
        url = "rest/api/latest/admin/groups/{}/more-members".format(group_name)
        return self.get(url, params=params)

    def get_users_not_in_group(self, group_name, filter_users="", start=0, limit=25):
        """
        Retrieves a list of users that are not members of a specified group.
        The authenticated user must have restricted administrative permission or higher to use this resource.
        :param filter_users:
        :param group_name:
        :param start:
        :param limit:
        :return:
        """
        params = {"limit": limit, "start": start}
        if filter_users:
            params = {"filter": filter_users}

        url = "rest/api/latest/admin/groups/{}/more-non-members".format(group_name)
        return self.get(url, params=params)

    def get_deployment_users(self, deployment_id, filter_name=None, start=0, limit=25):
        """
        Retrieve a list of users with their explicit permissions to given resource.
        The list can be filtered by some attributes.
        This resource is paged and returns a single page of results.
        :param deployment_id:
        :param filter_name:
        :param start:
        :param limit:
        :return:
        """
        params = {"limit": limit, "start": start}
        if filter_name:
            params = {"name": filter_name}
        resource = "permissions/deployment/{}/users".format(deployment_id)
        return self.get(self.resource_url(resource), params=params)

    def revoke_user_from_deployment(self, deployment_id, user, permissions=["READ", "WRITE", "BUILD"]):
        """
        Revokes deployment project permissions from a given user.
        :param deployment_id:
        :param user:
        :param permissions:
        :return:
        """
        resource = "permissions/deployment/{}/users/{}".format(deployment_id, user)
        return self.delete(self.resource_url(resource), data=permissions)

    def grant_user_to_deployment(self, deployment_id, user, permissions):
        """
        Grants deployment project permissions to a given user.
        :param deployment_id:
        :param user:
        :param permissions:
        :return:
        """
        resource = "permissions/deployment/{}/users/{}".format(deployment_id, user)
        return self.put(self.resource_url(resource), data=permissions)

    def get_deployment_groups(self, deployment_id, filter_name=None, start=0, limit=25):
        """
        Retrieve a list of groups with their deployment project permissions.
        The list can be filtered by some attributes.
        This resource is paged returns a single page of results.
        :param deployment_id:
        :param filter_name:
        :param start:
        :param limit:
        :return:
        """
        params = {"limit": limit, "start": start}
        if filter_name:
            params = {"name": filter_name}
        resource = "permissions/deployment/{}/groups".format(deployment_id)
        return self.get(self.resource_url(resource), params=params)

    def revoke_group_from_deployment(self, deployment_id, group, permissions=["READ", "WRITE", "BUILD"]):
        """
        Revokes deployment project permissions from a given group.
        :param deployment_id:
        :param group:
        :param permissions:
        :return:
        """
        resource = "permissions/deployment/{}/groups/{}".format(deployment_id, group)
        return self.delete(self.resource_url(resource), data=permissions)

    def grant_group_to_deployment(self, deployment_id, group, permissions):
        """
        Grants deployment project permissions to a given group.
        :param deployment_id:
        :param group:
        :param permissions:
        :return:
        """
        resource = "permissions/deployment/{}/groups/{}".format(deployment_id, group)
        return self.put(self.resource_url(resource), data=permissions)

    def get_environment_users(self, environment_id, filter_name=None, start=0, limit=25):
        """
        Retrieve a list of users with their explicit permissions to given resource.
        The list can be filtered by some attributes.
        This resource is paged and returns a single page of results.
        :param environment_id:
        :param filter_name:
        :param start:
        :param limit:
        :return:
        """
        params = {"limit": limit, "start": start}
        if filter_name:
            params = {"name": filter_name}
        resource = "permissions/environment/{}/users".format(environment_id)
        return self.get(self.resource_url(resource), params=params)

    def revoke_user_from_environment(self, environment_id, user, permissions=["READ", "WRITE", "BUILD"]):
        """
        Revokes deployment environment permissions from a given user.
        :param environment_id:
        :param user:
        :param permissions:
        :return:
        """
        resource = "permissions/environment/{}/users/{}".format(environment_id, user)
        return self.delete(self.resource_url(resource), data=permissions)

    def grant_user_to_environment(self, environment_id, user, permissions):
        """
        Grants deployment environment permissions to a given user.
        :param environment_id:
        :param user:
        :param permissions:
        :return:
        """
        resource = "permissions/environment/{}/users/{}".format(environment_id, user)
        return self.put(self.resource_url(resource), data=permissions)

    def get_environment_groups(self, environment_id, filter_name=None, start=0, limit=25):
        """
        Retrieve a list of groups with their deployment environment permissions.
        The list can be filtered by some attributes.
        This resource is paged returns a single page of results.
        :param environment_id:
        :param filter_name:
        :param start:
        :param limit:
        :return:
        """
        params = {"limit": limit, "start": start}
        if filter_name:
            params = {"name": filter_name}
        resource = "permissions/environment/{}/groups".format(environment_id)
        return self.get(self.resource_url(resource), params=params)

    def revoke_group_from_environment(self, environment_id, group, permissions=["READ", "WRITE", "BUILD"]):
        """
        Revokes deployment environment permissions from a given group.
        :param environment_id:
        :param group:
        :param permissions:
        :return:
        """
        resource = "permissions/environment/{}/groups/{}".format(environment_id, group)
        return self.delete(self.resource_url(resource), data=permissions)

    def grant_group_to_environment(self, environment_id, group, permissions):
        """
        Grants deployment environment permissions to a given group.
        :param environment_id:
        :param group:
        :param permissions:
        :return:
        """
        resource = "permissions/environment/{}/groups/{}".format(environment_id, group)
        return self.put(self.resource_url(resource), data=permissions)

    """Other actions"""

    def server_info(self):
        return self.get(self.resource_url("info"))

    def get_build_queue(self, expand="queuedBuilds"):
        """
        Lists all the builds waiting in the build queue, adds or removes a build from the build queue.
        May be used also to resume build on manual stage or rerun failed jobs.
        :return:
        """
        params = {"expand": expand}
        return self.get("rest/api/latest/queue", params=params)

    def get_deployment_queue(self, expand="queuedDeployments"):
        """
        Provide list of deployment results scheduled for execution and waiting in queue.
        :return:
        """
        params = {"expand": expand}
        return self.get("rest/api/latest/queue/deployment", params=params)

    def agent_status(self, online=False):
        """
        Provides a list of all agents.

        :param online:  filter only online agents (default False = all)
        :return:
        """
        return self.get(self.resource_url("agent"), params={"online": online})

    def agent_is_online(self, agent_id):
        """
        Get agent online status.

        :param agent_id:  Bamboo agent ID (integer number)
        :return: True/False
        """
        response = self.get(self.resource_url("agent/{}/status".format(agent_id)))
        return response["online"]

    def agent_enable(self, agent_id):
        """
        Enable agent

        :param agent_id:  Bamboo agent ID (integer number)
        :return: None
        """
        self.put(self.resource_url("agent/{}/enable".format(agent_id)))

    def agent_disable(self, agent_id):
        """
        Disable agent

        :param agent_id:  Bamboo agent ID (integer number)
        :return: None
        """
        self.put(self.resource_url("agent/{}/disable".format(agent_id)))

    def agent_remote(self, online=False):
        """
        Provides a list of all agent authentication statuses.

        :param online: list only online agents (default False = all)
        :return: list of agent-describing dictionaries
        """
        return self.get(self.resource_url("agent/remote"), params={"online": online})

    def agent_details(self, agent_id, expand=None):
        """
        Provides details of an agent with given id.

        :param agent_id:  Bamboo agent ID (integer number)
        :param expand:    Expand fields (None, capabilities, executableEnvironments, executableJobs)
        :return:
        """
        params = None
        if expand:
            params = {"expand": expand}
        return self.get(self.resource_url("agent/{}".format(agent_id)), params=params)

    def agent_capabilities(self, agent_id, include_shared=True):
        """
        List agent's capabilities.

        :param agent_id:        Bamboo agent ID (integer number)
        :param include_shared:  Include shared capabilities
        :return: agents
        """
        return self.get(
            self.resource_url("agent/{}/capability".format(agent_id)),
            params={"includeShared": include_shared},
        )

    def activity(self):
        return self.get("build/admin/ajax/getDashboardSummary.action")

    def get_custom_expiry(self, limit=25):
        """
        Get list of all plans where user has admin permission and which override global expiry settings.
        If global expiry is not enabled it returns empty response.
        :param limit:
        """
        url = "rest/api/latest/admin/expiry/custom/plan?limit={}".format(limit)
        return self.get(url)

    def reports(self, max_results=25):
        params = {"max-results": max_results}
        return self._get_generator(
            self.resource_url("chart/reports"),
            elements_key="reports",
            element_key="report",
            params=params,
        )

    def chart(
        self,
        report_key,
        build_keys,
        group_by_period,
        date_filter=None,
        date_from=None,
        date_to=None,
        width=None,
        height=None,
        start_index=9,
        max_results=25,
    ):
        """
        Get chart data
        :param report_key:
        :param build_keys:
        :param group_by_period:
        :param date_filter:
        :param date_from:
        :param date_to:
        :param width:
        :param height:
        :param start_index:
        :param max_results:
        :return:
        """
        params = {
            "reportKey": report_key,
            "buildKeys": build_keys,
            "groupByPeriod": group_by_period,
            "start-index": start_index,
            "max-results": max_results,
        }
        if date_filter:
            params["dateFilter"] = date_filter
            if date_filter == "RANGE":
                params["dateFrom"] = date_from
                params["dateTo"] = date_to
        if width:
            params["width"] = width
        if height:
            params["height"] = height
        return self.get(self.resource_url("chart"), params=params)

    def reindex(self):
        """
        Returns status of the current indexing operation.
        reindexInProgress - reindex is currently performed in background reindexPending - reindex is required
        (i.e. it failed before or some upgrade task asked for it)
        """
        return self.get(self.resource_url("reindex"))

    def stop_reindex(self):
        """
        Kicks off a reindex. Requires system admin permissions to perform this reindex.
        """
        return self.post(self.resource_url("reindex"))

    def health_check(self):
        """
        Get health status
        https://confluence.atlassian.com/jirakb/how-to-retrieve-health-check-results-using-rest-api-867195158.html
        :return:
        """
        # check as Troubleshooting & Support Tools Plugin
        response = self.get("rest/troubleshooting/1.0/check/")
        if not response:
            # check as support tools
            response = self.get("rest/supportHealthCheck/1.0/check/")
        return response

    """Elastic Bamboo"""

    def get_elastic_instance_logs(self, instance_id):
        """
        Get logs from an EC2 instance
        :param instance_id:
        :return:
        """
        resource = "/elasticInstances/instance/{instance_id}/logs".format(instance_id=instance_id)
        return self.get(self.resource_url(resource))

    def get_elastic_configurations(self):
        """
        Get list of all elastic configurations
        :return:
        """
        resource = "elasticConfiguration"
        return self.get(self.resource_url(resource))

    def create_elastic_configuration(self, json):
        """
        Create an elastic configuration
        :param json:
        :return:
        """
        resource = "elasticConfiguration"
        return self.post(self.resource_url(resource), json=json)

    def get_elastic_configuration(self, configuration_id):
        """
        Get information of an elastic configuration
        :param configuration_id:
        :return:
        """

        resource = "elasticConfiguration/{configuration_id}".format(configuration_id=configuration_id)
        return self.get(self.resource_url(resource))

    def update_elastic_configuration(self, configuration_id, data):
        """
        Update an elastic configuration
        :param configuration_id:
        :param data:
        :return:
        """

        resource = "elasticConfiguration/{configuration_id}".format(configuration_id=configuration_id)
        return self.put(self.resource_url(resource), data=data)

    def delete_elastic_configuration(self, configuration_id):
        """
        Delete an elastic configuration
        :param configuration_id:
        :return:
        """

        resource = "elasticConfiguration/{configuration_id}".format(configuration_id=configuration_id)
        return self.delete(self.resource_url(resource))

    def get_elastic_bamboo(self):
        """
        Get elastic bamboo configuration
        :return:
        """
        response = self.get("rest/admin/latest/elastic/config")
        return response

    def set_elastic_bamboo(self, data):
        """
        Set elastic bamboo configuration
        :return:
        """
        response = self.put("rest/admin/latest/elastic/config", data=data)
        return response

    def get_plugins_info(self):
        """
        Provide plugins info
        :return a json of installed plugins
        """
        url = "rest/plugins/1.0/"
        return self.get(url, headers=self.no_check_headers, trailing=True)

    def get_plugin_info(self, plugin_key):
        """
        Provide plugin info
        :return a json of installed plugins
        """
        url = "rest/plugins/1.0/{plugin_key}-key".format(plugin_key=plugin_key)
        return self.get(url, headers=self.no_check_headers, trailing=True)

    def get_plugin_license_info(self, plugin_key):
        """
        Provide plugin license information
        :return a json specific License query
        """
        url = "rest/plugins/1.0/{plugin_key}-key/license".format(plugin_key=plugin_key)
        return self.get(url, headers=self.no_check_headers, trailing=True)

    def upload_plugin(self, plugin_path):
        """
        Provide plugin path for upload into Jira e.g. useful for auto deploy
        :param plugin_path:
        :return:
        """
        files = {"plugin": open(plugin_path, "rb")}
        upm_token = self.request(
            method="GET",
            path="rest/plugins/1.0/",
            headers=self.no_check_headers,
            trailing=True,
        ).headers["upm-token"]
        url = "rest/plugins/1.0/?token={upm_token}".format(upm_token=upm_token)
        return self.post(url, files=files, headers=self.no_check_headers)

    def disable_plugin(self, plugin_key):
        """
        Disable a plugin
        :param plugin_key:
        :return:
        """
        app_headers = {
            "X-Atlassian-Token": "nocheck",
            "Content-Type": "application/vnd.atl.plugins+json",
        }
        url = "rest/plugins/1.0/{plugin_key}-key".format(plugin_key=plugin_key)
        data = {"status": "disabled"}
        return self.put(url, data=data, headers=app_headers)

    def enable_plugin(self, plugin_key):
        """
        Enable a plugin
        :param plugin_key:
        :return:
        """
        app_headers = {
            "X-Atlassian-Token": "nocheck",
            "Content-Type": "application/vnd.atl.plugins+json",
        }
        url = "rest/plugins/1.0/{plugin_key}-key".format(plugin_key=plugin_key)
        data = {"status": "enabled"}
        return self.put(url, data=data, headers=app_headers)

    def delete_plugin(self, plugin_key):
        """
        Delete plugin
        :param plugin_key:
        :return:
        """
        url = "rest/plugins/1.0/{}-key".format(plugin_key)
        return self.delete(url)

    def check_plugin_manager_status(self):
        """
        Check plugin manager status
        :return:
        """
        url = "rest/plugins/latest/safe-mode"
        return self.request(method="GET", path=url, headers=self.safe_mode_headers)

    def update_plugin_license(self, plugin_key, raw_license):
        """
        Update license for plugin
        :param plugin_key:
        :param raw_license:
        :return:
        """
        app_headers = {
            "X-Atlassian-Token": "nocheck",
            "Content-Type": "application/vnd.atl.plugins+json",
        }
        url = "/plugins/1.0/{plugin_key}/license".format(plugin_key=plugin_key)
        data = {"rawLicense": raw_license}
        return self.put(url, data=data, headers=app_headers)
