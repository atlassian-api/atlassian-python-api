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
                logging.error(f"Broken response: {e}")
                yield e
                return
        try:
            results = response[elements_key]
            size = 0
            # Check if we still can get results
            if results["size"] == 0:
                return
            for r in results[element_key]:
                if max_results is not None and size >= max_results:
                    return
                size += 1
                yield r
        except TypeError:
            logging.error(f"Broken response: {response}")
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
        **kwargs,
    ):
        flags = []
        params = {"max-results": max_results}
        if expand:
            params["expand"] = expand
        if favourite:
            flags.append("favourite")
        if clover_enabled:
            flags.append("cloverEnabled")
        if label:
            # Requests serializes a sequence value as repeated query
            # parameters (``label=one&label=two``), which is the Bamboo REST
            # API representation for filtering by multiple labels.
            params["label"] = label if isinstance(label, str) else list(label)
        params.update(kwargs)
        params["start-index"] = start_index
        elements_key = params.pop("elements_key", None)
        element_key = params.pop("element_key", None)
        if elements_key and element_key:
            return self._get_generator(
                self.resource_url(resource),
                flags=flags,
                params=params,
                elements_key=elements_key,
                element_key=element_key,
                max_results=max_results,
            )
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
        resource = f"project/{project_key}"
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
        resource = f"project/{project_key}?showEmpty"
        return self.get(self.resource_url(resource))

    def delete_project(self, project_key):
        """Marks project for deletion. Project will be deleted by a batch job."""
        resource = f"project/{project_key}"
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
        resource = f"project/{project_key}"
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
        resource = f"planDirectoryInfo/{plan_key}"
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
        resource = f"rest/api/latest/plan/{plan_key}"
        return self.get(resource, params=params)

    def get_plan_specs(self, plan_key, package=None, format="YAML"):
        """Export a plan as Bamboo Specs source code.

        Bamboo does not provide a repositories-only REST endpoint. The
        response's ``spec.code`` field contains the plan definition, including
        its ``repositories`` section. ``YAML`` is the most convenient format
        for repository audits; Bamboo also supports ``JAVA`` on compatible
        releases.

        :param plan_key: Full plan key, for example ``PROJECT-PLAN``.
        :param package: Optional Java package name when exporting Java Specs.
        :param format: Export format, normally ``YAML`` or ``JAVA``.
        :return: The ``RestPlanSpec`` response containing ``spec.code``.
        """
        params = {"format": format}
        if package is not None:
            params["package"] = package
        return self.get(self.resource_url(f"plan/{plan_key}/specs"), params=params)

    def search_linked_repositories(self, search_term=None):
        """Search globally configured Bamboo linked repositories.

        The public Bamboo REST API can search existing linked repositories but
        does not create or update their connection configuration. Create those
        connections in Bamboo administration, then use the returned repository
        ID with :meth:`link_repository_to_project`.

        :param search_term: Optional repository-name fragment.
        :return: Bamboo's paged linked-repository response.
        """
        params = {}
        if search_term is not None:
            params["searchTerm"] = search_term
        return self.get(self.resource_url("repository"), params=params)

    def get_project_linked_repositories(self, project_key):
        """Return linked repositories authorized for Bamboo Specs in a project."""
        return self.get(self.resource_url(f"project/{project_key}/repository"))

    def link_repository_to_project(self, project_key, repository_id):
        """Authorize an existing linked repository for Bamboo Specs in a project.

        This grants a repository-stored Bamboo Specs repository permission to
        create or edit plans in ``project_key``. It does not change the
        repositories checked out by an existing plan; update and apply that
        plan's Bamboo Specs for plan-level repository changes.
        """
        return self.post(self.resource_url(f"project/{project_key}/repository"), data={"id": repository_id})

    def unlink_repository_from_project(self, project_key, repository_id):
        """Remove a project-level Bamboo Specs repository authorization."""
        return self.delete(self.resource_url(f"project/{project_key}/repository/{repository_id}"))

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
        resource = f"rest/api/latest/plan/{plan_key}"
        return self.delete(resource)

    def disable_plan(self, plan_key):
        """
        Disable plan.
        :param plan_key: str TST-BLD
        :return: DELETE request
        """
        resource = f"plan/{plan_key}/enable"
        return self.delete(self.resource_url(resource))

    def enable_plan(self, plan_key):
        """
        Enable plan.
        :param plan_key: str TST-BLD
        :return: POST request
        """
        resource = f"plan/{plan_key}/enable"
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
            page_size = results["max-result"]
            if page_size <= 0:
                break
            for r in results["searchResults"]:
                yield r
            params["start-index"] += page_size

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
        resource = f"plan/{plan_key}/branch"
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
        resource = f"plan/{plan_key}/branch/{branch_name}"
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
        resource = f"plan/{plan_key}/branch/{branch_name}"
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
        resource = f"plan/{plan_key}/vcsBranches"
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
        build_state=None,
        **kwargs,
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
        :param label: A label string or an iterable of labels.
        :param start_index:
        :param max_results:
        :param include_all_states:
        :param build_state: Optional Bamboo result state, such as
            ``Successful`` or ``Failed``.
        :param kwargs: Additional query parameters forwarded to the Bamboo
            REST API.
        :return:
        """
        resource = "result"
        if project_key and plan_key and job_key and build_number:
            resource += f"/{project_key}-{plan_key}-{job_key}/{build_number}"
        elif project_key and plan_key and build_number:
            resource += f"/{project_key}-{plan_key}/{build_number}"
        elif project_key and plan_key:
            resource += f"/{project_key}-{plan_key}"
        elif project_key:
            resource += "/" + project_key

        params = {}
        if issue_key:
            params["issueKey"] = issue_key
        if include_all_states:
            params["includeAllStates"] = include_all_states
        if build_state is not None:
            params["buildstate"] = build_state
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
            **kwargs,
            **params,
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
        build_state=None,
        **kwargs,
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
        :param build_state: Optional Bamboo result state, such as
            ``Successful`` or ``Failed``.
        :param kwargs: Additional query parameters passed to the Bamboo REST
            API (for example ``issueStatus`` or ``jobKey`` filters).
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
            build_state=build_state,
            **kwargs,
        )

    def ordered_plan_results(
        self,
        project_key,
        plan_key,
        order="descending",
        build_state=None,
        max_results=25,
        **kwargs,
    ):
        """Return retrieved plan results ordered by completion time.

        Bamboo's result API does not expose a server-side sort parameter. This
        helper orders the result page client-side by ``buildCompletedTime``.
        Set ``max_results`` high enough to include the history being compared;
        this method returns a list rather than the lazy generator returned by
        :meth:`plan_results`.

        :param order: ``"ascending"`` for oldest first or ``"descending"``
            for newest first.
        :param build_state: Optional ``Successful`` or ``Failed`` filter.
        :param max_results: Number of results Bamboo should return to sort.
        :return: A list of build results ordered by completion time.
        """
        if order not in {"ascending", "descending"}:
            raise ValueError("order must be 'ascending' or 'descending'")

        results = self.plan_results(
            project_key,
            plan_key,
            build_state=build_state,
            max_results=max_results,
            **kwargs,
        )
        return sorted(
            results,
            key=lambda result: result.get("buildCompletedTime") or "",
            reverse=order == "descending",
        )

    def latest_successful_plan_result(self, project_key, plan_key, max_results=25, **kwargs):
        """Return the newest successful plan result, or ``None`` when absent."""
        results = self.ordered_plan_results(
            project_key,
            plan_key,
            build_state="Successful",
            max_results=max_results,
            **kwargs,
        )
        return results[0] if results else None

    def oldest_failed_plan_result(self, project_key, plan_key, max_results=25, **kwargs):
        """Return the oldest failed plan result, or ``None`` when absent."""
        results = self.ordered_plan_results(
            project_key,
            plan_key,
            order="ascending",
            build_state="Failed",
            max_results=max_results,
            **kwargs,
        )
        return results[0] if results else None

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
            resource = f"result/{build_key}"
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
            raise ValueError(f'The key "{build_key}" does not correspond to a build result')

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
            resource = f"result/{plan_key}/latest.json"
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
            raise ValueError(f'The key "{plan_key}" does not correspond to the latest build result')

    def delete_build_result(self, build_key):
        """
        Deleting result for specific build
        :param build_key: Take full build key, example: PROJECT-PLAN-8
        """
        custom_resource = "/build/admin/deletePlanResults.action"
        build_key = build_key.split("-")
        plan_key = f"{build_key[0]}-{build_key[1]}"
        build_number = build_key[2]
        params = {"buildKey": plan_key, "buildNumber": build_number}
        return self.post(custom_resource, params=params, headers=self.form_token_headers)

    def execute_build(
        self,
        plan_key,
        stage=None,
        execute_all_stages=True,
        custom_revision=None,
        **bamboo_variables,
    ):
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
        resource = f"queue/{plan_key}"
        params = {}
        if stage:
            execute_all_stages = False
            params["stage"] = stage
        if custom_revision:
            params["customRevision"] = custom_revision
        params["executeAllStages"] = "true" if execute_all_stages else "false"
        if bamboo_variables:
            for key, value in list(bamboo_variables.items()):
                params[f"bamboo.variable.{key}"] = value

        return self.post(self.resource_url(resource), params=params)

    def queue_build(self, plan_key, params=None):
        """Add a plan to the Bamboo build queue.

        ``params`` maps directly to Bamboo's queue request parameters. For
        example, pass ``{"bamboo.variable.release": "1.2.3"}`` to set a
        custom plan variable. Builds execute all stages by default; provide an
        explicit ``executeAllStages`` or ``stage`` value to override that
        behavior. The supplied mapping is never modified.

        :param plan_key: Full plan key, for example ``PROJECT-PLAN``.
        :param params: Optional queue parameters and custom variables.
        :return: The queued build response.
        """
        queue_params = dict(params or {})
        queue_params.setdefault("executeAllStages", "true")
        return self.post(self.resource_url(f"queue/{plan_key}"), params=queue_params)

    def stop_build(self, plan_key):
        """
        Stop the build which is in progress at the moment.
        :param plan_key: str TST-BLD
        :return: GET request
        """
        resource = f"/build/admin/stopPlan.action?planKey={plan_key}"
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
        resource = f"result/{project_key}-{plan_key}-{build_number}/comment"
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
        resource = f"result/{project_key}-{plan_key}-{build_number}/comment"
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
        resource = f"result/{project_key}-{plan_key}-{build_number}/label"
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
        resource = f"result/{project_key}-{plan_key}-{build_number}/label"
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
        resource = f"result/{project_key}-{plan_key}-{build_number}/label/{label}"
        return self.delete(self.resource_url(resource))

    @property
    def get_projects(self, start=0, limit=25):
        """Method used to list all projects defined in Bamboo.
        Projects without any plan are not listed.
        :return: GET request
        """
        start_idx = start
        max_results = limit

        while True:
            resource = f"project?start-index={start_idx}&max-result={max_results}"

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
        resource = f"deploy/project/{project_id}"
        return self.get(self.resource_url(resource))

    def delete_deployment_project(self, project_id):
        """
        Deletes a deployment project.
        :param project_id:
        :return:
        """
        resource = f"deploy/project/{project_id}"
        return self.delete(self.resource_url(resource))

    def deployment_environment_results(self, env_id, expand=None, max_results=25):
        """
        Get deployment environment results
        :param env_id:
        :param expand:
        :param max_results:
        :return:
        """
        resource = f"deploy/environment/{env_id}/results"
        params = {"max-result": max_results, "start-index": 0}
        size = 1
        if expand:
            params["expand"] = expand
        while params["start-index"] < size:
            results = self.get(self.resource_url(resource), params=params)
            size = results["size"]
            page_size = results["max-result"]
            if page_size <= 0:
                break
            for r in results["results"]:
                yield r
            params["start-index"] += page_size

    def deployment_dashboard(self, project_id=None):
        """
        Returns the current status of each deployment environment
        If no project id is provided, returns all projects.
        """
        resource = f"deploy/dashboard/{project_id}" if project_id else "deploy/dashboard"
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
        url = f"rest/api/latest/admin/groups/{group_name}"
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
        url = f"rest/api/latest/admin/groups/{group_name}/add-users"
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
        url = f"rest/api/latest/admin/groups/{group_name}/remove-users"
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
            params["filter"] = filter_users
        url = f"rest/api/latest/admin/groups/{group_name}/more-members"
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
            params["filter"] = filter_users

        url = f"rest/api/latest/admin/groups/{group_name}/more-non-members"
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
            params["name"] = filter_name
        resource = f"permissions/deployment/{deployment_id}/users"
        return self.get(self.resource_url(resource), params=params)

    def revoke_user_from_deployment(self, deployment_id, user, permissions=["READ", "WRITE", "BUILD"]):
        """
        Revokes deployment project permissions from a given user.
        :param deployment_id:
        :param user:
        :param permissions:
        :return:
        """
        resource = f"permissions/deployment/{deployment_id}/users/{user}"
        return self.delete(self.resource_url(resource), data=permissions)

    def grant_user_to_deployment(self, deployment_id, user, permissions):
        """
        Grants deployment project permissions to a given user.
        :param deployment_id:
        :param user:
        :param permissions:
        :return:
        """
        resource = f"permissions/deployment/{deployment_id}/users/{user}"
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
            params["name"] = filter_name
        resource = f"permissions/deployment/{deployment_id}/groups"
        return self.get(self.resource_url(resource), params=params)

    def revoke_group_from_deployment(self, deployment_id, group, permissions=["READ", "WRITE", "BUILD"]):
        """
        Revokes deployment project permissions from a given group.
        :param deployment_id:
        :param group:
        :param permissions:
        :return:
        """
        resource = f"permissions/deployment/{deployment_id}/groups/{group}"
        return self.delete(self.resource_url(resource), data=permissions)

    def grant_group_to_deployment(self, deployment_id, group, permissions):
        """
        Grants deployment project permissions to a given group.
        :param deployment_id:
        :param group:
        :param permissions:
        :return:
        """
        resource = f"permissions/deployment/{deployment_id}/groups/{group}"
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
            params["name"] = filter_name
        resource = f"permissions/environment/{environment_id}/users"
        return self.get(self.resource_url(resource), params=params)

    def revoke_user_from_environment(self, environment_id, user, permissions=["READ", "WRITE", "BUILD"]):
        """
        Revokes deployment environment permissions from a given user.
        :param environment_id:
        :param user:
        :param permissions:
        :return:
        """
        resource = f"permissions/environment/{environment_id}/users/{user}"
        return self.delete(self.resource_url(resource), data=permissions)

    def grant_user_to_environment(self, environment_id, user, permissions):
        """
        Grants deployment environment permissions to a given user.
        :param environment_id:
        :param user:
        :param permissions:
        :return:
        """
        resource = f"permissions/environment/{environment_id}/users/{user}"
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
            params["name"] = filter_name
        resource = f"permissions/environment/{environment_id}/groups"
        return self.get(self.resource_url(resource), params=params)

    def revoke_group_from_environment(self, environment_id, group, permissions=["READ", "WRITE", "BUILD"]):
        """
        Revokes deployment environment permissions from a given group.
        :param environment_id:
        :param group:
        :param permissions:
        :return:
        """
        resource = f"permissions/environment/{environment_id}/groups/{group}"
        return self.delete(self.resource_url(resource), data=permissions)

    def grant_group_to_environment(self, environment_id, group, permissions):
        """
        Grants deployment environment permissions to a given group.
        :param environment_id:
        :param group:
        :param permissions:
        :return:
        """
        resource = f"permissions/environment/{environment_id}/groups/{group}"
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
        response = self.get(self.resource_url(f"agent/{agent_id}/status"))
        return response["online"]

    def agent_enable(self, agent_id):
        """
        Enable agent

        :param agent_id:  Bamboo agent ID (integer number)
        :return: None
        """
        self.put(self.resource_url(f"agent/{agent_id}/enable"))

    def agent_disable(self, agent_id):
        """
        Disable agent

        :param agent_id:  Bamboo agent ID (integer number)
        :return: None
        """
        self.put(self.resource_url(f"agent/{agent_id}/disable"))

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
        return self.get(self.resource_url(f"agent/{agent_id}"), params=params)

    def agent_capabilities(self, agent_id, include_shared=True):
        """
        List agent's capabilities.

        :param agent_id:        Bamboo agent ID (integer number)
        :param include_shared:  Include shared capabilities
        :return: agents
        """
        return self.get(
            self.resource_url(f"agent/{agent_id}/capability"),
            params={"includeShared": include_shared},
        )

    def add_agent_capability(self, agent_id, data):
        """Add a capability to an agent using Bamboo's capability payload."""
        return self.post(self.resource_url(f"agent/{agent_id}/capability"), data=data)

    def delete_agent_capability(self, agent_id, capability_key):
        """Delete one agent capability by its Bamboo capability key."""
        return self.delete(self.resource_url(f"agent/{agent_id}/capability/{capability_key}"))

    def delete_all_agent_capabilities(self, agent_id):
        """Delete every capability assigned directly to an agent."""
        return self.delete(self.resource_url(f"agent/{agent_id}/capability"))

    def get_plan_variables(self, plan_key):
        """Return variables configured for a plan."""
        return self.get(self.resource_url(f"plan/{plan_key}/variables"))

    def get_plan_variable(self, plan_key, variable_name):
        """Return one plan variable by name."""
        return self.get(self.resource_url(f"plan/{plan_key}/variables/{variable_name}"))

    def create_plan_variable(self, plan_key, data):
        """Create a plan variable from Bamboo's variable request body."""
        return self.post(self.resource_url(f"plan/{plan_key}/variables"), data=data)

    def update_plan_variable(self, plan_key, variable_name, data):
        """Update a plan variable."""
        return self.put(self.resource_url(f"plan/{plan_key}/variables/{variable_name}"), data=data)

    def delete_plan_variable(self, plan_key, variable_name):
        """Delete a plan variable."""
        return self.delete(self.resource_url(f"plan/{plan_key}/variables/{variable_name}"))

    def activity(self, busy=None):
        """Return active online agents and their current build activity.

        The former dashboard AJAX endpoint was an internal Bamboo UI endpoint
        and is not present in current Bamboo releases.  The supported agent
        REST resource exposes ``active`` and ``busy`` for each online agent.

        :param busy: Optional filter for busy (``True``) or idle (``False``)
                     agents. By default, return all active online agents.
        :return: List of active agent dictionaries, including ``busy``.
        """
        agents = self.agent_status(online=True)
        if not isinstance(agents, list):
            return agents

        active_agents = [agent for agent in agents if agent.get("active", agent.get("online", False))]
        if busy is None:
            return active_agents
        return [agent for agent in active_agents if agent.get("busy") is busy]

    def get_custom_expiry(self, limit=25):
        """
        Get list of all plans where user has admin permission and which override global expiry settings.
        If global expiry is not enabled it returns empty response.
        :param limit:
        """
        url = f"rest/api/latest/admin/expiry/custom/plan?limit={limit}"
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

    """Responsibility"""

    def get_broken_builds_by_user(self, username):
        """
        Get broken builds for which a user has taken responsibility.
        :param username: str - username
        :return: list of broken builds
        """
        return self.get(f"rest/responsibility/latest/brokenBuild/byUser/{username}")

    def get_my_broken_builds(self):
        """Get broken builds for which the current user has taken responsibility."""
        return self.get("rest/responsibility/latest/brokenBuild/myBrokenBuilds")

    def get_broken_build(self, plan_result_key_or_plan_key):
        """
        Get responsibility information for a broken build or plan.
        :param plan_result_key_or_plan_key: str - plan result key or plan key
        :return: responsibility info
        """
        return self.get(f"rest/responsibility/latest/brokenBuild/{plan_result_key_or_plan_key}")

    def take_responsibility(self, plan_result_key_or_plan_key, username):
        """
        Take responsibility for a broken build.
        :param plan_result_key_or_plan_key: str - plan result key or plan key
        :param username: str - username taking responsibility
        :return:
        """
        return self.post(f"rest/responsibility/latest/brokenBuild/{plan_result_key_or_plan_key}/{username}")

    def remove_responsibility(self, plan_result_key_or_plan_key, username):
        """
        Remove responsibility for a broken build.
        :param plan_result_key_or_plan_key: str - plan result key or plan key
        :param username: str - username
        :return:
        """
        return self.delete(f"rest/responsibility/latest/brokenBuild/{plan_result_key_or_plan_key}/{username}")

    """Triggers"""

    def remote_trigger_change_detection(self):
        """Trigger remote repository change detection for all linked repositories."""
        return self.post("rest/triggers/latest/remote/changeDetection")

    """Access tokens"""

    def get_access_tokens(self):
        """Get all access tokens for the current user."""
        return self.get(self.resource_url("access-token"))

    def create_access_token(self):
        """Create a new access token for the current user."""
        return self.post(self.resource_url("access-token"))

    def delete_access_token(self, token_id):
        """
        Delete an access token.
        :param token_id: str - token id
        :return:
        """
        return self.delete(self.resource_url(f"access-token/{token_id}"))

    """Deployments"""

    def create_deployment_project(self, data):
        """
        Create a new deployment project.
        :param data: dict - deployment project representation
        :return: created deployment project
        """
        return self.put(self.resource_url("deploy/project"), data=data)

    def update_deployment_project(self, project_id, data):
        """
        Update a deployment project.
        :param project_id: str - deployment project id
        :param data: dict - deployment project representation
        :return:
        """
        return self.post(self.resource_url(f"deploy/project/{project_id}"), data=data)

    def create_deployment_environment(self, project_id, data):
        """
        Create a deployment environment in a deployment project.
        :param project_id: str - deployment project id
        :param data: dict - environment representation
        :return: created environment
        """
        return self.post(self.resource_url(f"deploy/project/{project_id}/environment"), data=data)

    def get_deployment_environment(self, environment_id):
        """
        Get a deployment environment.
        :param environment_id: str - environment id
        :return: environment
        """
        return self.get(self.resource_url(f"deploy/environment/{environment_id}"))

    def update_deployment_environment(self, environment_id, data):
        """
        Update a deployment environment.
        :param environment_id: str - environment id
        :param data: dict - environment representation
        :return:
        """
        return self.put(self.resource_url(f"deploy/environment/{environment_id}"), data=data)

    def delete_deployment_environment(self, environment_id):
        """
        Delete a deployment environment.
        :param environment_id: str - environment id
        :return:
        """
        return self.delete(self.resource_url(f"deploy/environment/{environment_id}"))

    def get_deployment_versions(self, project_id, start=0, limit=25):
        """
        Get versions for a deployment project.
        :param project_id: str - deployment project id
        :param start: int - start index for paging
        :param limit: int - maximum number of results
        :return: versions
        """
        return self.get(
            self.resource_url(f"deploy/project/{project_id}/versions"),
            params={"start": start, "limit": limit},
        )

    def create_deployment_version(self, project_id, data):
        """
        Create a deployment version.
        :param project_id: str - deployment project id
        :param data: dict - version representation
        :return: created version
        """
        return self.post(self.resource_url(f"deploy/project/{project_id}/version"), data=data)

    def get_deployment_version(self, version_id):
        """
        Get a deployment version.
        :param version_id: str - version id
        :return: version
        """
        return self.get(self.resource_url(f"deploy/version/{version_id}"))

    def delete_deployment_version(self, version_id):
        """
        Delete a deployment version.
        :param version_id: str - version id
        :return:
        """
        return self.delete(self.resource_url(f"deploy/version/{version_id}"))

    def get_deployment_dashboard_paginate(self, project_id=None, start=0, limit=25):
        """
        Get paginated deployment dashboard.
        :param project_id: str - optional deployment project id
        :param start: int - start index
        :param limit: int - maximum number of results
        :return: dashboard data
        """
        resource = f"deploy/dashboard/paginate/{project_id}" if project_id else "deploy/dashboard/paginate"
        return self.get(self.resource_url(resource), params={"start": start, "limit": limit})

    def get_deployment_dashboard_status(self, data):
        """
        Get deployment dashboard status for given environments.
        :param data: dict - request body with environment ids
        :return: dashboard status
        """
        return self.post(self.resource_url("deploy/dashboard/status"), data=data)

    """Admin configuration"""

    def _admin_url(self, resource):
        return f"rest/admin/latest/{resource}"

    def get_artifact_handler_config(self, handler_name):
        """
        Get configuration for an artifact handler.
        :param handler_name: str - handler name (agentLocal, bambooRemote, s3, sftp)
        :return: configuration
        """
        return self.get(self._admin_url(f"artifactHandlers/{handler_name}"))

    def update_artifact_handler_config(self, handler_name, data):
        """
        Update configuration for an artifact handler.
        :param handler_name: str - handler name
        :param data: dict - handler configuration
        :return:
        """
        return self.put(self._admin_url(f"artifactHandlers/{handler_name}"), data=data)

    def get_agent_config(self):
        """Get agent configuration list."""
        return self.get(self._admin_url("config/agents"))

    def get_offline_agent_removal_config(self):
        """Get offline agent removal configuration."""
        return self.get(self._admin_url("config/agents/offlineAgentRemoval"))

    def update_offline_agent_removal_config(self, data):
        """
        Update offline agent removal configuration.
        :param data: dict - configuration
        :return:
        """
        return self.put(self._admin_url("config/agents/offlineAgentRemoval"), data=data)

    def get_build_concurrency_config(self):
        """Get build concurrency configuration."""
        return self.get(self._admin_url("config/build/concurrency"))

    def update_build_concurrency_config(self, data):
        """
        Update build concurrency configuration.
        :param data: dict - configuration
        :return:
        """
        return self.put(self._admin_url("config/build/concurrency"), data=data)

    def get_build_monitoring_config(self):
        """Get build monitoring configuration."""
        return self.get(self._admin_url("config/build/monitoring"))

    def update_build_monitoring_config(self, data):
        """
        Update build monitoring configuration.
        :param data: dict - configuration
        :return:
        """
        return self.put(self._admin_url("config/build/monitoring"), data=data)

    def get_general_config(self):
        """Get general configuration."""
        return self.get(self._admin_url("config/general"))

    def update_general_config(self, data):
        """
        Update general configuration.
        :param data: dict - configuration
        :return:
        """
        return self.put(self._admin_url("config/general"), data=data)

    def get_mail_server_config(self):
        """Get mail server configuration."""
        return self.get(self._admin_url("config/mailServer"))

    def update_mail_server_config(self, data):
        """
        Update mail server configuration.
        :param data: dict - configuration
        :return:
        """
        return self.put(self._admin_url("config/mailServer"), data=data)

    def delete_mail_server_config(self):
        """Delete mail server configuration."""
        return self.delete(self._admin_url("config/mailServer"))

    def get_im_server_config(self):
        """Get instant messaging server configuration."""
        return self.get(self._admin_url("config/imServer"))

    def update_im_server_config(self, data):
        """
        Update instant messaging server configuration.
        :param data: dict - configuration
        :return:
        """
        return self.put(self._admin_url("config/imServer"), data=data)

    def delete_im_server_config(self):
        """Delete instant messaging server configuration."""
        return self.delete(self._admin_url("config/imServer"))

    def get_remote_agent_support_config(self):
        """Get remote agent support configuration."""
        return self.get(self._admin_url("config/remoteAgentSupport"))

    def update_remote_agent_support_config(self, data):
        """
        Update remote agent support configuration.
        :param data: dict - configuration
        :return:
        """
        return self.put(self._admin_url("config/remoteAgentSupport"), data=data)

    def get_quarantine_config(self):
        """Get quarantine configuration."""
        return self.get(self._admin_url("config/quarantine"))

    def update_quarantine_config(self, data):
        """
        Update quarantine configuration.
        :param data: dict - configuration
        :return:
        """
        return self.put(self._admin_url("config/quarantine"), data=data)

    def get_audit_log_config(self):
        """Get audit log configuration."""
        return self.get(self._admin_url("config/auditLog"))

    def update_audit_log_config(self, data):
        """
        Update audit log configuration.
        :param data: dict - configuration
        :return:
        """
        return self.put(self._admin_url("config/auditLog"), data=data)

    def get_dark_features(self):
        """Get all dark features."""
        return self.get(self._admin_url("darkFeatures"))

    def get_dark_feature(self, key):
        """
        Get a dark feature.
        :param key: str - feature key
        :return: feature status
        """
        return self.get(self._admin_url(f"darkFeatures/{key}"))

    def update_dark_feature(self, key, enabled):
        """
        Enable or disable a dark feature.
        :param key: str - feature key
        :param enabled: bool - enabled status
        :return:
        """
        return self.put(self._admin_url(f"darkFeatures/{key}"), data={"enabled": enabled})

    def get_dark_feature_user(self, key, username):
        """
        Get dark feature status for a user.
        :param key: str - feature key
        :param username: str - username
        :return: feature status
        """
        return self.get(self._admin_url(f"darkFeatures/{key}/user/{username}"))

    def update_dark_feature_user(self, key, username, enabled):
        """
        Enable or disable a dark feature for a user.
        :param key: str - feature key
        :param username: str - username
        :param enabled: bool - enabled status
        :return:
        """
        return self.put(self._admin_url(f"darkFeatures/{key}/user/{username}"), data={"enabled": enabled})

    def get_global_variables(self):
        """Get all global variables."""
        return self.get(self._admin_url("globalVariables"))

    def create_global_variable(self, data):
        """
        Create a global variable.
        :param data: dict - variable representation
        :return: created variable
        """
        return self.post(self._admin_url("globalVariables"), data=data)

    def get_global_variable(self, variable_id):
        """
        Get a global variable.
        :param variable_id: str - variable id
        :return: variable
        """
        return self.get(self._admin_url(f"globalVariables/{variable_id}"))

    def update_global_variable(self, variable_id, data):
        """
        Update a global variable.
        :param variable_id: str - variable id
        :param data: dict - variable representation
        :return:
        """
        return self.put(self._admin_url(f"globalVariables/{variable_id}"), data=data)

    def delete_global_variable(self, variable_id):
        """
        Delete a global variable.
        :param variable_id: str - variable id
        :return:
        """
        return self.delete(self._admin_url(f"globalVariables/{variable_id}"))

    def verify_global_variables(self, data):
        """
        Verify global variables.
        :param data: dict - variables to verify
        :return: verification result
        """
        return self.put(self._admin_url("globalVariables/verify"), data=data)

    def get_security_settings(self):
        """Get security settings."""
        return self.get(self._admin_url("security/settings"))

    def update_security_settings(self, data):
        """
        Update security settings.
        :param data: dict - security settings
        :return:
        """
        return self.put(self._admin_url("security/settings"), data=data)

    def get_security_groups(self):
        """Get security groups."""
        return self.get(self._admin_url("security/groups"))

    def create_security_group(self, data):
        """
        Create a security group.
        :param data: dict - group representation
        :return: created group
        """
        return self.post(self._admin_url("security/groups"), data=data)

    def get_trusted_keys(self):
        """Get trusted keys."""
        return self.get(self._admin_url("security/trustedKey"))

    def add_trusted_key(self, data):
        """
        Add a trusted key.
        :param data: dict - key representation
        :return: created key
        """
        return self.post(self._admin_url("security/trustedKey"), data=data)

    def delete_trusted_key(self, key_id):
        """
        Delete a trusted key.
        :param key_id: str - key id
        :return:
        """
        return self.delete(self._admin_url(f"security/trustedKey/{key_id}"))

    """Permissions"""

    def _permission_url(self, resource_type, resource_id):
        return f"permissions/{resource_type}/{resource_id}"

    def get_available_users_for_permission(self, resource_type, resource_id, start=0, limit=25):
        """
        Get users available for granting permission to a resource.
        :param resource_type: str - deployment, environment, project, plan, repository
        :param resource_id: str - resource id
        :param start: int - start index
        :param limit: int - maximum number of results
        :return: available users
        """
        return self.get(
            self.resource_url(self._permission_url(resource_type, resource_id) + "/available-users"),
            params={"start": start, "limit": limit},
        )

    def get_available_groups_for_permission(self, resource_type, resource_id, start=0, limit=25):
        """
        Get groups available for granting permission to a resource.
        :param resource_type: str - deployment, environment, project, plan, repository
        :param resource_id: str - resource id
        :param start: int - start index
        :param limit: int - maximum number of results
        :return: available groups
        """
        return self.get(
            self.resource_url(self._permission_url(resource_type, resource_id) + "/available-groups"),
            params={"start": start, "limit": limit},
        )

    def get_roles_for_permission(self, resource_type, resource_id):
        """
        Get roles with permissions for a resource.
        :param resource_type: str - deployment, environment, project, plan, repository
        :param resource_id: str - resource id
        :return: roles
        """
        return self.get(self.resource_url(self._permission_url(resource_type, resource_id) + "/roles"))

    def grant_role_permission(self, resource_type, resource_id, role_name, permissions):
        """
        Grant permissions to a role for a resource.
        :param resource_type: str - deployment, environment, project, plan, repository
        :param resource_id: str - resource id
        :param role_name: str - role name
        :param permissions: list - list of permissions
        :return:
        """
        return self.put(
            self.resource_url(self._permission_url(resource_type, resource_id) + f"/roles/{role_name}"),
            data=permissions,
        )

    def revoke_role_permission(self, resource_type, resource_id, role_name, permissions):
        """
        Revoke permissions from a role for a resource.
        :param resource_type: str - deployment, environment, project, plan, repository
        :param resource_id: str - resource id
        :param role_name: str - role name
        :param permissions: list - list of permissions
        :return:
        """
        return self.delete(
            self.resource_url(self._permission_url(resource_type, resource_id) + f"/roles/{role_name}"),
            data=permissions,
        )

    def get_permission_users(self, resource_type, resource_id, filter_name=None, start=0, limit=25):
        """
        Get users with explicit permissions to a resource.
        :param resource_type: str - deployment, environment, project, plan, repository
        :param resource_id: str - resource id
        :param filter_name: str - optional name filter
        :param start: int - start index
        :param limit: int - maximum number of results
        :return: users
        """
        params = {"start": start, "limit": limit}
        if filter_name:
            params["name"] = filter_name
        return self.get(
            self.resource_url(self._permission_url(resource_type, resource_id) + "/users"),
            params=params,
        )

    def grant_user_permission(self, resource_type, resource_id, user_name, permissions):
        """
        Grant permissions to a user for a resource.
        :param resource_type: str - deployment, environment, project, plan, repository
        :param resource_id: str - resource id
        :param user_name: str - username
        :param permissions: list - list of permissions
        :return:
        """
        return self.put(
            self.resource_url(self._permission_url(resource_type, resource_id) + f"/users/{user_name}"),
            data=permissions,
        )

    def revoke_user_permission(self, resource_type, resource_id, user_name, permissions):
        """
        Revoke permissions from a user for a resource.
        :param resource_type: str - deployment, environment, project, plan, repository
        :param resource_id: str - resource id
        :param user_name: str - username
        :param permissions: list - list of permissions
        :return:
        """
        return self.delete(
            self.resource_url(self._permission_url(resource_type, resource_id) + f"/users/{user_name}"),
            data=permissions,
        )

    def get_permission_groups(self, resource_type, resource_id, filter_name=None, start=0, limit=25):
        """
        Get groups with explicit permissions to a resource.
        :param resource_type: str - deployment, environment, project, plan, repository
        :param resource_id: str - resource id
        :param filter_name: str - optional name filter
        :param start: int - start index
        :param limit: int - maximum number of results
        :return: groups
        """
        params = {"start": start, "limit": limit}
        if filter_name:
            params["name"] = filter_name
        return self.get(
            self.resource_url(self._permission_url(resource_type, resource_id) + "/groups"),
            params=params,
        )

    def grant_group_permission(self, resource_type, resource_id, group_name, permissions):
        """
        Grant permissions to a group for a resource.
        :param resource_type: str - deployment, environment, project, plan, repository
        :param resource_id: str - resource id
        :param group_name: str - group name
        :param permissions: list - list of permissions
        :return:
        """
        return self.put(
            self.resource_url(self._permission_url(resource_type, resource_id) + f"/groups/{group_name}"),
            data=permissions,
        )

    def revoke_group_permission(self, resource_type, resource_id, group_name, permissions):
        """
        Revoke permissions from a group for a resource.
        :param resource_type: str - deployment, environment, project, plan, repository
        :param resource_id: str - resource id
        :param group_name: str - group name
        :param permissions: list - list of permissions
        :return:
        """
        return self.delete(
            self.resource_url(self._permission_url(resource_type, resource_id) + f"/groups/{group_name}"),
            data=permissions,
        )

    """Admin users and groups"""

    def get_users(self, start=0, limit=25):
        """
        Get a paginated list of users.
        :param start: int - start index
        :param limit: int - maximum number of results
        :return: users
        """
        return self.get(self.resource_url("admin/users"), params={"start": start, "limit": limit})

    def create_user(self, data):
        """
        Create a new user.
        :param data: dict - user representation
        :return: created user
        """
        return self.post(self.resource_url("admin/users"), data=data)

    def delete_user(self, username):
        """
        Delete a user.
        :param username: str - username
        :return:
        """
        return self.delete(self.resource_url(f"admin/users/{username}"))

    def update_user_credentials(self, data):
        """
        Update user credentials.
        :param data: dict - credentials request
        :return:
        """
        return self.put(self.resource_url("admin/users/credentials"), data=data)

    def rename_user(self, data):
        """
        Rename a user.
        :param data: dict - rename request
        :return:
        """
        return self.put(self.resource_url("admin/users/rename"), data=data)

    def get_user_access_tokens(self, username):
        """
        Get access tokens for a user.
        :param username: str - username
        :return: access tokens
        """
        return self.get(self.resource_url(f"admin/users/{username}/access-token"))

    def delete_user_access_token(self, username, token_id):
        """
        Delete an access token for a user.
        :param username: str - username
        :param token_id: str - token id
        :return:
        """
        return self.delete(self.resource_url(f"admin/users/{username}/access-token/{token_id}"))

    def get_user_alias(self, username):
        """
        Get a user's alias.
        :param username: str - username
        :return: alias
        """
        return self.get(self.resource_url(f"admin/users/{username}/alias"))

    def set_user_alias(self, username, data):
        """
        Set a user's alias.
        :param username: str - username
        :param data: dict - alias request
        :return:
        """
        return self.post(self.resource_url(f"admin/users/{username}/alias"), data=data)

    def delete_user_alias(self, username):
        """
        Delete a user's alias.
        :param username: str - username
        :return:
        """
        return self.delete(self.resource_url(f"admin/users/{username}/alias"))

    """Server and queue"""

    def get_server(self):
        """Get Bamboo server information."""
        return self.get(self.resource_url("server"))

    def get_server_nodes(self):
        """Get Bamboo server nodes."""
        return self.get(self.resource_url("server/nodes"))

    def pause_server(self):
        """Pause the Bamboo server."""
        return self.post(self.resource_url("server/pause"))

    def resume_server(self):
        """Resume the Bamboo server."""
        return self.post(self.resource_url("server/resume"))

    def prepare_for_restart(self):
        """Prepare the Bamboo server for restart."""
        return self.put(self.resource_url("server/prepareForRestart"))

    def get_current_user(self):
        """Get information about the current user."""
        return self.get(self.resource_url("currentUser"))

    def remove_build_from_queue(self, project_key, build_key, build_number):
        """
        Remove a build from the queue.
        :param project_key: str - project key
        :param build_key: str - build key
        :param build_number: int - build number
        :return:
        """
        return self.delete(self.resource_url(f"queue/{project_key}-{build_key}-{build_number}"))

    def pause_build_in_queue(self, project_key, build_key, build_number):
        """
        Pause a build in the queue.
        :param project_key: str - project key
        :param build_key: str - build key
        :param build_number: int - build number
        :return:
        """
        return self.put(self.resource_url(f"queue/{project_key}-{build_key}-{build_number}"))

    def remove_deployment_from_queue(self, deployment_result_id):
        """
        Remove a deployment from the queue.
        :param deployment_result_id: str - deployment result id
        :return:
        """
        return self.delete(self.resource_url(f"queue/deployment/{deployment_result_id}"))

    """Quick filters"""

    def get_quick_filters(self):
        """Get all quick filters."""
        return self.get(self.resource_url("quickFilter"))

    def create_quick_filter(self, data):
        """
        Create a quick filter.
        :param data: dict - filter representation
        :return: created filter
        """
        return self.post(self.resource_url("quickFilter"), data=data)

    def get_active_quick_filters(self):
        """Get active quick filters."""
        return self.get(self.resource_url("quickFilter/active"))

    def get_visible_quick_filters(self):
        """Get visible quick filters."""
        return self.get(self.resource_url("quickFilter/visible"))

    def set_visible_quick_filters(self, data):
        """
        Set visible quick filters.
        :param data: dict - filter ids
        :return:
        """
        return self.put(self.resource_url("quickFilter/visible"), data=data)

    def deactivate_quick_filters(self, data):
        """
        Deactivate quick filters.
        :param data: dict - filter ids
        :return:
        """
        return self.put(self.resource_url("quickFilter/deactivate"), data=data)

    def get_quick_filter(self, filter_id):
        """
        Get a quick filter.
        :param filter_id: str - filter id
        :return: filter
        """
        return self.get(self.resource_url(f"quickFilter/{filter_id}"))

    def update_quick_filter(self, filter_id, data):
        """
        Update a quick filter.
        :param filter_id: str - filter id
        :param data: dict - filter representation
        :return:
        """
        return self.put(self.resource_url(f"quickFilter/{filter_id}"), data=data)

    def delete_quick_filter(self, filter_id):
        """
        Delete a quick filter.
        :param filter_id: str - filter id
        :return:
        """
        return self.delete(self.resource_url(f"quickFilter/{filter_id}"))

    def activate_quick_filter(self, filter_id):
        """
        Activate a quick filter.
        :param filter_id: str - filter id
        :return:
        """
        return self.put(self.resource_url(f"quickFilter/{filter_id}/activate"))

    """Elastic Bamboo"""

    def get_elastic_instance_logs(self, instance_id):
        """
        Get logs from an EC2 instance
        :param instance_id:
        :return:
        """
        resource = f"/elasticInstances/instance/{instance_id}/logs"
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

        resource = f"elasticConfiguration/{configuration_id}"
        return self.get(self.resource_url(resource))

    def update_elastic_configuration(self, configuration_id, data):
        """
        Update an elastic configuration
        :param configuration_id:
        :param data:
        :return:
        """

        resource = f"elasticConfiguration/{configuration_id}"
        return self.put(self.resource_url(resource), data=data)

    def delete_elastic_configuration(self, configuration_id):
        """
        Delete an elastic configuration
        :param configuration_id:
        :return:
        """

        resource = f"elasticConfiguration/{configuration_id}"
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
        url = f"rest/plugins/1.0/{plugin_key}-key"
        return self.get(url, headers=self.no_check_headers, trailing=True)

    def get_plugin_license_info(self, plugin_key):
        """
        Provide plugin license information
        :return a json specific License query
        """
        url = f"rest/plugins/1.0/{plugin_key}-key/license"
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
        url = f"rest/plugins/1.0/?token={upm_token}"
        return self.post(url, files=files, headers=self.no_check_headers)

    def disable_plugin(self, plugin_key):
        """
        Disable a plugin
        :param plugin_key:
        :return:
        """
        app_headers = {
            "X-Atlassian-Token": "no-check",
            "Content-Type": "application/vnd.atl.plugins+json",
        }
        url = f"rest/plugins/1.0/{plugin_key}-key"
        data = {"status": "disabled"}
        return self.put(url, data=data, headers=app_headers)

    def enable_plugin(self, plugin_key):
        """
        Enable a plugin
        :param plugin_key:
        :return:
        """
        app_headers = {
            "X-Atlassian-Token": "no-check",
            "Content-Type": "application/vnd.atl.plugins+json",
        }
        url = f"rest/plugins/1.0/{plugin_key}-key"
        data = {"status": "enabled"}
        return self.put(url, data=data, headers=app_headers)

    def delete_plugin(self, plugin_key):
        """
        Delete plugin
        :param plugin_key:
        :return:
        """
        url = f"rest/plugins/1.0/{plugin_key}-key"
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
            "X-Atlassian-Token": "no-check",
            "Content-Type": "application/vnd.atl.plugins+json",
        }
        url = f"/plugins/1.0/{plugin_key}/license"
        data = {"rawLicense": raw_license}
        return self.put(url, data=data, headers=app_headers)


    """Admin (root API)"""

    def invalidate_user_sessions(self, name, user):
        """Invalidate active sessions of the given user
        :param name: name path parameter
        :param user: user path parameter
        :return:
        """
        return self.delete(self._admin_url(f"session/{name}"))

    def get_configuration(self):
        """Retrieves ephemeral agents configuration.
        :return:
        """
        return self.get(self._admin_url("ephemeral/config"))

    def get_configuration_1(self):
        """Retrieves global build and deployment expiry configuration for this Bamboo instance.
        :return:
        """
        return self.get(self._admin_url("expiry/configuration"))

    def get_status(self):
        """Retrieves build and deployment expiry status.
        :return:
        """
        return self.get(self._admin_url("expiry/status"))

    def get_jobs(self):
        """Gets the collection of jobs currently scheduled to run.
        :return:
        """
        return self.get(self._admin_url("scheduler/jobs"))

    def get_system_info(self):
        """Read system information.
        :return:
        """
        return self.get(self._admin_url("systemInfo"))

    def test_connection(self, data):
        """Test connection to ephemeral agents provider.
        :param data: request body (dict or list)
        :return:
        """
        return self.post(self._admin_url("ephemeral/config/test-connection"), data=data)

    def trigger_job(self, data):
        """Trigger background job execution.
        :param data: request body (dict or list)
        :return:
        """
        return self.post(self._admin_url("scheduler/jobs/trigger"), data=data)

    def rename_user_post(self, data, external_rename=None):
        """Renames specified user.
        :param external_rename: externalRename query parameter
        :param data: request body (dict or list)
        :return:
        """
        params = {}
        if external_rename is not None:
            params["externalRename"] = external_rename
        return self.post(self._admin_url("user"), params=params, data=data)

    def save_configuration(self, data):
        """Modify ephemeral agents configuration.
        :param data: request body (dict or list)
        :return:
        """
        return self.put(self._admin_url("ephemeral/config"), data=data)

    def set_configuration(self, data):
        """Update global build and deployment expiry configuration for this Bamboo instance. Partial configuration is not allowed (it will fail validation).
        :param data: request body (dict or list)
        :return:
        """
        return self.put(self._admin_url("expiry/configuration"), data=data)

    def run(self):
        """Executes build and deployment expiry process. Will only start each process if it's not currently running.
        :return:
        """
        return self.put(self._admin_url("expiry/run"))

    def rename_user_put(self, new_user_name, data, external_rename=None):
        """Renames specified user.
        :param new_user_name: newUserName path parameter
        :param external_rename: externalRename query parameter
        :param data: request body (dict or list)
        :return:
        """
        params = {}
        if external_rename is not None:
            params["externalRename"] = external_rename
        return self.put(self._admin_url(f"user/{new_user_name}"), params=params, data=data)



    """Admin (users)"""

    def remove_plan_custom_expiry_settings(self, plan_key):
        """Delete custom plan expiry settings.
        :param plan_key: planKey path parameter
        :return:
        """
        return self.delete(self.resource_url(f"admin/expiry/custom/plan/{plan_key}"))

    def unassign_groups(self, name, data):
        """Remove a user from multiple groups.  The authenticated user must have restricted administrative permission or higher to use this resource.
        :param name: name path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.delete(self.resource_url(f"admin/users/{name}/groups"), data=data)

    def find_assigned_groups(self, name, filter=None, limit=None, start=None):
        """Retrieves a list of groups to which the user belongs. The authenticated user must have restricted administrative permission or higher to use this resource.
        :param name: name path parameter
        :param filter: filter query parameter
        :param limit: limit query parameter
        :param start: start query parameter
        :return:
        """
        params = {}
        if filter is not None:
            params["filter"] = filter
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        return self.get(self.resource_url(f"admin/users/{name}/assigned-groups"), params=params)

    def find_unassigned_user_repository_aliases(self, name, filter=None, limit=None, start=None):
        """Retrieves a list of unlinked aliases to which the user does not belong. The authenticated user must have restricted administrative permission or higher to use this resource.
        :param name: name path parameter
        :param filter: filter query parameter
        :param limit: limit query parameter
        :param start: start query parameter
        :return:
        """
        params = {}
        if filter is not None:
            params["filter"] = filter
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        return self.get(self.resource_url(f"admin/users/{name}/unassigned-aliases"), params=params)

    def find_unassigned_groups(self, name, filter=None, limit=None, start=None):
        """Retrieves a list of groups to which the user does not belong. The authenticated user must have restricted administrative permission or higher to use this resource.
        :param name: name path parameter
        :param filter: filter query parameter
        :param limit: limit query parameter
        :param start: start query parameter
        :return:
        """
        params = {}
        if filter is not None:
            params["filter"] = filter
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        return self.get(self.resource_url(f"admin/users/{name}/unassigned-groups"), params=params)

    def assign_groups(self, name, data):
        """Add a user to multiple groups. The authenticated user must have restricted administrative permission or higher to use this resource.
        :param name: name path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.post(self.resource_url(f"admin/users/{name}/groups"), data=data)



    """Agents & assignments"""

    def delete_agent(self, agent_id):
        """Remove build agent.
        :param agent_id: agentId path parameter
        :return:
        """
        return self.delete(self.resource_url(f"agent/{agent_id}"))

    def remove_assignment(self, executor_type=None, executor_id=None, entity_id=None, assignment_type=None):
        """Remove agent's assignment.
        :param executor_type: executorType query parameter
        :param executor_id: executorId query parameter
        :param entity_id: entityId query parameter
        :param assignment_type: assignmentType query parameter
        :return:
        """
        params = {}
        if executor_type is not None:
            params["executorType"] = executor_type
        if executor_id is not None:
            params["executorId"] = executor_id
        if entity_id is not None:
            params["entityId"] = entity_id
        if assignment_type is not None:
            params["assignmentType"] = assignment_type
        return self.delete(self.resource_url("agent/assignment"), params=params)

    def remove_agent_assignment_from_job(self, job_key, executor_key):
        """Remove agent/image from list of dedicated executors for given job.
        :param job_key: jobKey path parameter
        :param executor_key: executorKey path parameter
        :return:
        """
        return self.delete(self.resource_url(f"config/job/{job_key}/agent-assignment/{executor_key}"))

    def search_entity_for_agent(self, max_result=None, executor_type=None, search_term=None, executor_id=None, entity_type=None, start_index=None, assignment_type=None):
        """Search for assignments in specified entity's agents
        :param max_result: max-result query parameter
        :param executor_type: executorType query parameter
        :param search_term: searchTerm query parameter
        :param executor_id: executorId query parameter
        :param entity_type: entityType query parameter
        :param start_index: start-index query parameter
        :param assignment_type: assignmentType query parameter
        :return:
        """
        params = {}
        if max_result is not None:
            params["max-result"] = max_result
        if executor_type is not None:
            params["executorType"] = executor_type
        if search_term is not None:
            params["searchTerm"] = search_term
        if executor_id is not None:
            params["executorId"] = executor_id
        if entity_type is not None:
            params["entityType"] = entity_type
        if start_index is not None:
            params["start-index"] = start_index
        if assignment_type is not None:
            params["assignmentType"] = assignment_type
        return self.get(self.resource_url("agent/assignment/search"), params=params)

    def find_assigned_agents_by_job(self, job_key):
        """Get a list of agents/images assigned to given job.
        :param job_key: jobKey path parameter
        :return:
        """
        return self.get(self.resource_url(f"config/job/{job_key}/agent-assignment"))

    def find_possible_agents_for_job(self, job_key, max_result=None, search_term=None, start_index=None):
        """Get a list of agents/images/templates which can be dedicated for given job.
        :param job_key: jobKey path parameter
        :param max_result: max-result query parameter
        :param search_term: searchTerm query parameter
        :param start_index: start-index query parameter
        :return:
        """
        params = {}
        if max_result is not None:
            params["max-result"] = max_result
        if search_term is not None:
            params["searchTerm"] = search_term
        if start_index is not None:
            params["start-index"] = start_index
        return self.get(
            self.resource_url(f"config/job/{job_key}/agent-assignment/possible-agent-assignment"),
            params=params,
        )

    def add_agent_assignment(self, executor_type=None, executor_id=None, entity_id=None, assignment_type=None):
        """Dedicate agent, elastic image or ephemeral template.
        :param executor_type: executorType query parameter
        :param executor_id: executorId query parameter
        :param entity_id: entityId query parameter
        :param assignment_type: assignmentType query parameter
        :return:
        """
        params = {}
        if executor_type is not None:
            params["executorType"] = executor_type
        if executor_id is not None:
            params["executorId"] = executor_id
        if entity_id is not None:
            params["entityId"] = entity_id
        if assignment_type is not None:
            params["assignmentType"] = assignment_type
        return self.post(self.resource_url("agent/assignment"), params=params)

    def add_agent_assignment_for_job(self, job_key, data):
        """Add agent assignment for job. agentAssignmentKey is a map with one key-value: name - agentAssignmentKey. 
        :param job_key: jobKey path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.post(self.resource_url(f"config/job/{job_key}/agent-assignment"), data=data)

    def update_agent_capability(self, agent_id, capability_key, data):
        """Update existing agent capability. It's allowed to skip capability key at request payload.
        :param agent_id: agentId path parameter
        :param capability_key: capabilityKey path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.put(self.resource_url(f"agent/{agent_id}/capability/{capability_key}"), data=data)



    """Avatars"""

    def delete_avatar(self):
        """Deletes the current avatar for the currently authenticated user.
        :return:
        """
        return self.delete(self.resource_url("avatar/user/avatar.png"))

    def retrieve_avatar(self, user_name, s=None):
        """Returns either the avatar file for a specified user or the gravatar URL. The priority order: custom user avatar as a file, gravatar URL, default avatar as a file. The endpoint supports Last-Modified/If-Modified-Since headers and sets cache policy with expiration equal by default to 90 seconds.
        :param user_name: userName path parameter
        :param s: s query parameter
        :return:
        """
        params = {}
        if s is not None:
            params["s"] = s
        return self.get(self.resource_url(f"avatar/user/{user_name}/avatar.png"), params=params)

    def upload_avatar(self, data):
        """Updated the avatar for the currently authenticated user.
        :param data: request body (dict or list)
        :return:
        """
        return self.put(self.resource_url("avatar/user/avatar.png"), data=data)



    """Deployments"""

    def remove_agent_assignment_from_environment(self, environment_id, executor_key):
        """Remove agent/image from list of dedicated executors for given environment.
        :param environment_id: environmentId path parameter
        :param executor_key: executorKey path parameter
        :return:
        """
        return self.delete(
            self.resource_url(f"deploy/environment/{environment_id}/agent-assignment/{executor_key}"),
        )

    def remove_requirement_from_environment(self, environment_id, requirement_id):
        """Removes a requirement for an environment.
        :param environment_id: environmentId path parameter
        :param requirement_id: requirementId path parameter
        :return:
        """
        return self.delete(
            self.resource_url(f"deploy/environment/{environment_id}/requirement/{requirement_id}"),
        )

    def delete_environment_variable(self, environment_id, variable_name):
        """Delete the environment variable.
        :param environment_id: environmentId path parameter
        :param variable_name: variableName path parameter
        :return:
        """
        return self.delete(self.resource_url(f"deploy/environment/{environment_id}/variable/{variable_name}"))

    def delete_repository_mapping(self, deployment_project_id, repository_id):
        """Remove approval to create plans in given deployment project by given repository.
        :param deployment_project_id: deploymentProjectId path parameter
        :param repository_id: repositoryId path parameter
        :return:
        """
        return self.delete(
            self.resource_url(f"deploy/project/{deployment_project_id}/repository/{repository_id}"),
        )

    def get_all_deployment_projects(self):
        """Get all deployment projects. This method fetch all deployment projects visible to user. It's not optimized for instances with large count of deployment projects and environments, use paged versions instead.
        :return:
        """
        return self.get(self.resource_url("deploy/dashboard"))

    def get_deployment_project(self, project_id):
        """Get deployment project environments with deployment status. It's not optimized for instances with large count of deployment projects and environments, use paged versions instead.
        :param project_id: projectId path parameter
        :return:
        """
        return self.get(self.resource_url(f"deploy/dashboard/{project_id}"))

    def get_deployment_projects(self, filter=None, limit=None, start=None):
        """Get paginated deployment projects with environments list.
        :param filter: filter query parameter
        :param limit: limit query parameter
        :param start: start query parameter
        :return:
        """
        params = {}
        if filter is not None:
            params["filter"] = filter
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        return self.get(self.resource_url("deploy/dashboard/paginate"), params=params)

    def get_paginate_deployment_project(self, project_id, filter=None, limit=None, start=None):
        """Get deployment project environments.
        :param project_id: projectId path parameter
        :param filter: filter query parameter
        :param limit: limit query parameter
        :param start: start query parameter
        :return:
        """
        params = {}
        if filter is not None:
            params["filter"] = filter
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        return self.get(self.resource_url(f"deploy/dashboard/paginate/{project_id}"), params=params)

    def find_assigned_agents_by_environment(self, environment_id):
        """Get a list of agents/images assigned to given environment.
        :param environment_id: environmentId path parameter
        :return:
        """
        return self.get(self.resource_url(f"deploy/environment/{environment_id}/agent-assignment"))

    def get_docker_pipelines_configuration(self, environment_id):
        """Get Docker configuration for given environment.
        :param environment_id: environmentId path parameter
        :return:
        """
        return self.get(self.resource_url(f"deploy/environment/{environment_id}/docker"))

    def find_possible_agents_for_environment(self, environment_id, max_result=None, search_term=None, start_index=None):
        """Get a list of agents/images/templates which can be dedicated for given environment.
        :param environment_id: environmentId path parameter
        :param max_result: max-result query parameter
        :param search_term: searchTerm query parameter
        :param start_index: start-index query parameter
        :return:
        """
        params = {}
        if max_result is not None:
            params["max-result"] = max_result
        if search_term is not None:
            params["searchTerm"] = search_term
        if start_index is not None:
            params["start-index"] = start_index
        return self.get(
            self.resource_url(f"deploy/environment/{environment_id}/possible-agent-assignment"),
            params=params,
        )

    def get_requirements_for_environment(self, environment_id):
        """Gets all the requirements of an environment.
        :param environment_id: environmentId path parameter
        :return:
        """
        return self.get(self.resource_url(f"deploy/environment/{environment_id}/requirement"))

    def get_requirement_for_environment(self, environment_id, requirement_id):
        """Gets the details of a requirement for a given environment.
        :param environment_id: environmentId path parameter
        :param requirement_id: requirementId path parameter
        :return:
        """
        return self.get(
            self.resource_url(f"deploy/environment/{environment_id}/requirement/{requirement_id}"),
        )

    def get_detailed_agent_matches_for_environment(self, environment_id):
        """Gets a detailed summary of the agents that are capable of running an environment, based of its requirements.
        :param environment_id: environmentId path parameter
        :return:
        """
        return self.get(self.resource_url(f"deploy/environment/{environment_id}/requirement/detailedSummary"))

    def get_agent_matches_for_environment(self, environment_id):
        """Gets a summary of the agents that are capable of running an environment, based of its requirements.
        :param environment_id: environmentId path parameter
        :return:
        """
        return self.get(self.resource_url(f"deploy/environment/{environment_id}/requirement/summary"))

    def get_environment_variable(self, environment_id, variable_name):
        """Get the environment variable by its name.
        :param environment_id: environmentId path parameter
        :param variable_name: variableName path parameter
        :return:
        """
        return self.get(self.resource_url(f"deploy/environment/{environment_id}/variable/{variable_name}"))

    def get_all_environment_variables(self, environment_id):
        """Get a list of environment variables.
        :param environment_id: environmentId path parameter
        :return:
        """
        return self.get(self.resource_url(f"deploy/environment/{environment_id}/variables"))

    def get_jira_issue_status_for_project(self, issue_key):
        """Get all deployment projects associated with Jira issue key
        :param issue_key: issueKey path parameter
        :return:
        """
        return self.get(self.resource_url(f"deploy/issue-status/{issue_key}"))

    def get_jira_issue_status_for_project_1(self, issue_key, deployment_project_id):
        """Get deployment project environments and versions associated with Jira issue
        :param issue_key: issueKey path parameter
        :param deployment_project_id: deploymentProjectId path parameter
        :return:
        """
        return self.get(self.resource_url(f"deploy/issue-status/{issue_key}/{deployment_project_id}"))

    def get_possible_results(self, plan_key, deployment_project_id=None):
        """Get possible deployment results.
        :param deployment_project_id: deploymentProjectId query parameter
        :param plan_key: planKey query parameter
        :return:
        """
        params = {}
        if deployment_project_id is not None:
            params["deploymentProjectId"] = deployment_project_id
        if plan_key is not None:
            params["planKey"] = plan_key
        return self.get(self.resource_url("deploy/preview/possibleResults"), params=params)

    def get_version_preview_1(self, previous_version_id=None, deployment_project_id=None, plan_key=None, result_key=None, build_number=None):
        """Get a preview of the deployment version.
        :param previous_version_id: previousVersionId query parameter
        :param deployment_project_id: deploymentProjectId query parameter
        :param plan_key: planKey query parameter
        :param result_key: resultKey query parameter
        :param build_number: buildNumber query parameter
        :return:
        """
        params = {}
        if previous_version_id is not None:
            params["previousVersionId"] = previous_version_id
        if deployment_project_id is not None:
            params["deploymentProjectId"] = deployment_project_id
        if plan_key is not None:
            params["planKey"] = plan_key
        if result_key is not None:
            params["resultKey"] = result_key
        if build_number is not None:
            params["buildNumber"] = build_number
        return self.get(self.resource_url("deploy/preview/result"), params=params)

    def get_version_preview(self, previous_version_id=None, version_id=None, deployment_project_id=None, version_name=None):
        """Get a preview of the deployment version.
        :param previous_version_id: previousVersionId query parameter
        :param version_id: versionId query parameter
        :param deployment_project_id: deploymentProjectId query parameter
        :param version_name: versionName query parameter
        :return:
        """
        params = {}
        if previous_version_id is not None:
            params["previousVersionId"] = previous_version_id
        if version_id is not None:
            params["versionId"] = version_id
        if deployment_project_id is not None:
            params["deploymentProjectId"] = deployment_project_id
        if version_name is not None:
            params["versionName"] = version_name
        return self.get(self.resource_url("deploy/preview/version"), params=params)

    def get_version_name(self, deployment_project_id, result_key=None):
        """Get version name.
        :param result_key: resultKey query parameter
        :param deployment_project_id: deploymentProjectId query parameter
        :return:
        """
        params = {}
        if result_key is not None:
            params["resultKey"] = result_key
        if deployment_project_id is not None:
            params["deploymentProjectId"] = deployment_project_id
        return self.get(self.resource_url("deploy/preview/versionName"), params=params)

    def list_assigned_repositories(self, deployment_project_id):
        """List of repositories which granted to create/edit environment in given deployment project by Repository stored Bamboo Specs.
        :param deployment_project_id: deploymentProjectId path parameter
        :return:
        """
        return self.get(self.resource_url(f"deploy/project/{deployment_project_id}/repository"))

    def search_available_repositories(self, deployment_project_id, max_result=None, search_term=None, start_index=None):
        """Search for linked repositories which can be granted to create/modify environment by Repository stored Bamboo Specs in given deployment project.
        :param deployment_project_id: deploymentProjectId path parameter
        :param max_result: max-result query parameter
        :param search_term: searchTerm query parameter
        :param start_index: start-index query parameter
        :return:
        """
        params = {}
        if max_result is not None:
            params["max-result"] = max_result
        if search_term is not None:
            params["searchTerm"] = search_term
        if start_index is not None:
            params["start-index"] = start_index
        return self.get(
            self.resource_url(f"deploy/project/{deployment_project_id}/repository/search"),
            params=params,
        )

    def export_deployment_spec(self, deployment_project_id, package=None, format=None):
        """Export a deployment project to Bamboo Specs.
        :param deployment_project_id: deploymentProjectId path parameter
        :param package: package query parameter
        :param format: format query parameter
        :return:
        """
        params = {}
        if package is not None:
            params["package"] = package
        if format is not None:
            params["format"] = format
        return self.get(self.resource_url(f"deploy/project/{deployment_project_id}/specs"), params=params)

    def get_deployment_project_versions(self, deployment_project_id, branch_key=None):
        """Get list of deployment versions.
        :param deployment_project_id: deploymentProjectId path parameter
        :param branch_key: branchKey query parameter
        :return:
        """
        params = {}
        if branch_key is not None:
            params["branchKey"] = branch_key
        return self.get(self.resource_url(f"deploy/project/{deployment_project_id}/version"), params=params)

    def get_deployment_naming_preview(self, deployment_project_id, next_version_name, incrementable_variables=None, increment_numbers=None):
        """Get deployment version name preview.
        :param deployment_project_id: deploymentProjectId path parameter
        :param next_version_name: nextVersionName query parameter
        :param incrementable_variables: incrementableVariables query parameter
        :param increment_numbers: incrementNumbers query parameter
        :return:
        """
        params = {}
        if next_version_name is not None:
            params["nextVersionName"] = next_version_name
        if incrementable_variables is not None:
            params["incrementableVariables"] = incrementable_variables
        if increment_numbers is not None:
            params["incrementNumbers"] = increment_numbers
        return self.get(
            self.resource_url(f"deploy/projectVersioning/{deployment_project_id}/namingPreview"),
            params=params,
        )

    def get_next_deployment_versions(self, deployment_project_id, result_key=None):
        """Get next deployment version name.
        :param deployment_project_id: deploymentProjectId path parameter
        :param result_key: resultKey query parameter
        :return:
        """
        params = {}
        if result_key is not None:
            params["resultKey"] = result_key
        return self.get(
            self.resource_url(f"deploy/projectVersioning/{deployment_project_id}/nextVersion"),
            params=params,
        )

    def get_variables_from_name(self, deployment_project_id, next_version_name):
        """Extract variables value from version name.
        :param deployment_project_id: deploymentProjectId path parameter
        :param next_version_name: nextVersionName query parameter
        :return:
        """
        params = {}
        if next_version_name is not None:
            params["nextVersionName"] = next_version_name
        return self.get(
            self.resource_url(f"deploy/projectVersioning/{deployment_project_id}/parseVariables"),
            params=params,
        )

    def get_deployment_project_variables(self, deployment_project_id):
        """Get variables associated with deployment project.
        :param deployment_project_id: deploymentProjectId path parameter
        :return:
        """
        return self.get(self.resource_url(f"deploy/projectVersioning/{deployment_project_id}/variables"))

    def get_deployment_result(self, deployment_result_id, include_logs=None):
        """Get result of version deployment to environment.
        :param deployment_result_id: deploymentResultId path parameter
        :param include_logs: includeLogs query parameter
        :return:
        """
        params = {}
        if include_logs is not None:
            params["includeLogs"] = include_logs
        return self.get(self.resource_url(f"deploy/result/{deployment_result_id}"), params=params)

    def get_version_and_plan_result(self, deployment_version_id):
        """Get associated build result of deployment version.
        :param deployment_version_id: deploymentVersionId path parameter
        :return:
        """
        return self.get(self.resource_url(f"deploy/version/{deployment_version_id}/build-result"))

    def get_latest_version_statuses(self, deployment_version_id):
        """Get the all users' latest statuses of deployment version.
        :param deployment_version_id: deploymentVersionId path parameter
        :return:
        """
        return self.get(self.resource_url(f"deploy/version/{deployment_version_id}/status"))

    def add_agent_assignment_for_environment(self, environment_id, data):
        """Add agent assignment for environment. agentAssignmentKey is a map with one key-value: name - agentAssignmentKey. 
        :param environment_id: environmentId path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.post(
            self.resource_url(f"deploy/environment/{environment_id}/agent-assignment"),
            data=data,
        )

    def move_environment(self, environment_id, position, relative_environment_id):
        """Change environment position within deployment project.
        :param environment_id: environmentId path parameter
        :param position: position path parameter
        :param relative_environment_id: relativeEnvironmentId path parameter
        :return:
        """
        return self.post(
            self.resource_url(f"deploy/environment/{environment_id}/move/{position}/{relative_environment_id}"),
        )

    def add_requirement_for_environment(self, environment_id, data):
        """Adds a requirement for a given environment.
        :param environment_id: environmentId path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.post(self.resource_url(f"deploy/environment/{environment_id}/requirement"), data=data)

    def create_environment_variable(self, environment_id, data):
        """Create the environment variable.
        :param environment_id: environmentId path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.post(self.resource_url(f"deploy/environment/{environment_id}/variable"), data=data)

    def add_assigned_repository(self, deployment_project_id, data):
        """Grant permission to create/edit plan in given deployment project by Bamboo Specs from given repository.
        :param deployment_project_id: deploymentProjectId path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.post(self.resource_url(f"deploy/project/{deployment_project_id}/repository"), data=data)

    def update_version_status(self, deployment_version_id, new_status):
        """Update deployment version status.
        :param deployment_version_id: deploymentVersionId path parameter
        :param new_status: newStatus path parameter
        :return:
        """
        return self.post(self.resource_url(f"deploy/version/{deployment_version_id}/status/{new_status}"))

    def save_docker_pipelines_configuration(self, environment_id, data):
        """Save Docker configuration for given environment.
        :param environment_id: environmentId path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.put(self.resource_url(f"deploy/environment/{environment_id}/docker"), data=data)

    def update_environment_prerequisites(self, environment_id, data):
        """Updates the environment prerequisites.
        :param environment_id: environmentId path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.put(self.resource_url(f"deploy/environment/{environment_id}/prerequisites"), data=data)

    def update_requirement_for_environment(self, environment_id, requirement_id, data):
        """Updates a requirement for a given environment.
        :param environment_id: environmentId path parameter
        :param requirement_id: requirementId path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.put(
            self.resource_url(f"deploy/environment/{environment_id}/requirement/{requirement_id}"),
            data=data,
        )

    def update_environment_variable(self, environment_id, variable_name, data):
        """Update the environment variable.
        :param environment_id: environmentId path parameter
        :param variable_name: variableName path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.put(
            self.resource_url(f"deploy/environment/{environment_id}/variable/{variable_name}"),
            data=data,
        )



    """Ephemeral agents"""

    def delete_template_configuration(self, configuration_id):
        """Delete ephemeral template configuration.
        :param configuration_id: configurationId path parameter
        :return:
        """
        return self.delete(self.resource_url(f"ephemeral/templateConfiguration/{configuration_id}"))

    def delete_capability(self, configuration_id, name):
        """Remove ephemeral agent template capability.
        :param configuration_id: configurationId path parameter
        :param name: name path parameter
        :return:
        """
        return self.delete(
            self.resource_url(f"ephemeral/templateConfiguration/{configuration_id}/capability/{name}"),
        )

    def get_ephemeral_agent_pod_logs(self, pod, container_name=None, limit=None, after_timestamp=None):
        """Gets either pod or container related logs.
        :param pod: pod path parameter
        :param container_name: containerName query parameter
        :param limit: limit query parameter
        :param after_timestamp: afterTimestamp query parameter
        :return:
        """
        params = {}
        if container_name is not None:
            params["containerName"] = container_name
        if limit is not None:
            params["limit"] = limit
        if after_timestamp is not None:
            params["afterTimestamp"] = after_timestamp
        return self.get(self.resource_url(f"ephemeral/pod/{pod}/logs"), params=params)

    def get_ephemeral_agent_pod_raw_logs(self, pod, container_name=None):
        """Gets either pod or container all logs in the raw, plain text form.
        :param pod: pod path parameter
        :param container_name: containerName query parameter
        :return:
        """
        params = {}
        if container_name is not None:
            params["containerName"] = container_name
        return self.get(self.resource_url(f"ephemeral/pod/{pod}/logs/raw"), params=params)

    def get_template_configurations_page(self, filter=None, limit=None, start=None):
        """Fetch page of ephemeral templates.
        :param filter: filter query parameter
        :param limit: limit query parameter
        :param start: start query parameter
        :return:
        """
        params = {}
        if filter is not None:
            params["filter"] = filter
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        return self.get(self.resource_url("ephemeral/templateConfiguration"), params=params)

    def get_template_configuration(self, configuration_id):
        """Gets ephemeral template configuration details.
        :param configuration_id: configurationId path parameter
        :return:
        """
        return self.get(self.resource_url(f"ephemeral/templateConfiguration/{configuration_id}"))

    def get_capabilities(self, configuration_id, limit=None, start=None):
        """Fetch page of ephemeral agent template capabilities.
        :param configuration_id: configurationId path parameter
        :param limit: limit query parameter
        :param start: start query parameter
        :return:
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        return self.get(
            self.resource_url(f"ephemeral/templateConfiguration/{configuration_id}/capability"),
            params=params,
        )

    def create_template_configuration(self, data):
        """Create ephemeral template configuration.
        :param data: request body (dict or list)
        :return:
        """
        return self.post(self.resource_url("ephemeral/templateConfiguration"), data=data)

    def add_capability(self, configuration_id, data):
        """Add ephemeral agent template capability.
        :param configuration_id: configurationId path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.post(
            self.resource_url(f"ephemeral/templateConfiguration/{configuration_id}/capability"),
            data=data,
        )

    def update_template_configuration(self, configuration_id, data):
        """Update ephemeral agent template.
        :param configuration_id: configurationId path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.put(self.resource_url(f"ephemeral/templateConfiguration/{configuration_id}"), data=data)

    def update_capability(self, configuration_id, data):
        """Update ephemeral agent template capability.
        :param configuration_id: configurationId path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.put(
            self.resource_url(f"ephemeral/templateConfiguration/{configuration_id}/capability"),
            data=data,
        )



    """Global permissions"""

    def remove_permissions_for_group_2(self, name, data, ignore=None):
        """Revokes global permissions from a given group.
        :param name: name path parameter
        :param ignore: ignore query parameter
        :param data: request body (dict or list)
        :return:
        """
        params = {}
        if ignore is not None:
            params["ignore"] = ignore
        return self.delete(self.resource_url(f"permissions/global/groups/{name}"), params=params, data=data)

    def remove_permissions_for_role_2(self, name, data, ignore=None):
        """Revokes global permissions from a given role.
        :param name: name path parameter
        :param ignore: ignore query parameter
        :param data: request body (dict or list)
        :return:
        """
        params = {}
        if ignore is not None:
            params["ignore"] = ignore
        return self.delete(self.resource_url(f"permissions/global/roles/{name}"), params=params, data=data)

    def remove_permissions_for_user_2(self, name, data, ignore=None):
        """Revokes global permissions from a given user.
        :param name: name path parameter
        :param ignore: ignore query parameter
        :param data: request body (dict or list)
        :return:
        """
        params = {}
        if ignore is not None:
            params["ignore"] = ignore
        return self.delete(self.resource_url(f"permissions/global/users/{name}"), params=params, data=data)

    def get_available_groups_2(self, limit=None, start=None, name=None, ignore=None):
        """Returns list of groups which weren't granted explicitly any permissions. Resource is paged, returns single page of resources.
        :param limit: limit query parameter
        :param start: start query parameter
        :param name: name query parameter
        :param ignore: ignore query parameter
        :return:
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        if name is not None:
            params["name"] = name
        if ignore is not None:
            params["ignore"] = ignore
        return self.get(self.resource_url("permissions/global/available-groups"), params=params)

    def get_available_users_2(self, limit=None, start=None, name=None, ignore=None):
        """Returns list of users which weren't granted explicitly any permissions. Resource is paged, returns single page of resources.
        :param limit: limit query parameter
        :param start: start query parameter
        :param name: name query parameter
        :param ignore: ignore query parameter
        :return:
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        if name is not None:
            params["name"] = name
        if ignore is not None:
            params["ignore"] = ignore
        return self.get(self.resource_url("permissions/global/available-users"), params=params)

    def list_group_permissions_2(self, limit=None, start=None, name=None, ignore=None):
        """Retrieve a list of groups with their global permissions. The list can be filtered by some attributes. This resource is paged returns a single page of results.
        :param limit: limit query parameter
        :param start: start query parameter
        :param name: name query parameter
        :param ignore: ignore query parameter
        :return:
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        if name is not None:
            params["name"] = name
        if ignore is not None:
            params["ignore"] = ignore
        return self.get(self.resource_url("permissions/global/groups"), params=params)

    def list_role_permissions_2(self, limit=None, start=None, ignore=None):
        """Retrieve a list of roles with their global permissions. This resource is paged returns a single page of results, although only 2 roles are supported: LOGGED IN users, ANONYMOUS users
        :param limit: limit query parameter
        :param start: start query parameter
        :param ignore: ignore query parameter
        :return:
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        if ignore is not None:
            params["ignore"] = ignore
        return self.get(self.resource_url("permissions/global/roles"), params=params)

    def add_permissions_for_group_2(self, name, data, ignore=None):
        """Grants global permissions to a given group.
        :param name: name path parameter
        :param ignore: ignore query parameter
        :param data: request body (dict or list)
        :return:
        """
        params = {}
        if ignore is not None:
            params["ignore"] = ignore
        return self.put(self.resource_url(f"permissions/global/groups/{name}"), params=params, data=data)

    def add_permissions_for_role_2(self, name, data, ignore=None):
        """Grants global permissions to a given role.
        :param name: name path parameter
        :param ignore: ignore query parameter
        :param data: request body (dict or list)
        :return:
        """
        params = {}
        if ignore is not None:
            params["ignore"] = ignore
        return self.put(self.resource_url(f"permissions/global/roles/{name}"), params=params, data=data)

    def add_permissions_for_user_2(self, name, data, ignore=None):
        """Grants global permissions to a given user.
        :param name: name path parameter
        :param ignore: ignore query parameter
        :param data: request body (dict or list)
        :return:
        """
        params = {}
        if ignore is not None:
            params["ignore"] = ignore
        return self.put(self.resource_url(f"permissions/global/users/{name}"), params=params, data=data)



    """Plans"""

    def unmark_plan_favourite(self, project_key, build_key):
        """Remove plan from favorites.
        :param project_key: projectKey path parameter
        :param build_key: buildKey path parameter
        :return:
        """
        return self.delete(self.resource_url(f"plan/{project_key}-{build_key}/favourite"))

    def remove_plan_label(self, project_key, build_key, label_name):
        """Remove label from plan.
        :param project_key: projectKey path parameter
        :param build_key: buildKey path parameter
        :param label_name: labelName path parameter
        :return:
        """
        return self.delete(self.resource_url(f"plan/{project_key}-{build_key}/label/{label_name}"))

    def get_plan_artifact_definition(self, project_key, build_key, max_result=None, start_index=None):
        """Fetch plan's shared artifact definitions.
        :param project_key: projectKey path parameter
        :param build_key: buildKey path parameter
        :param max_result: max-result query parameter
        :param start_index: start-index query parameter
        :return:
        """
        params = {}
        if max_result is not None:
            params["max-result"] = max_result
        if start_index is not None:
            params["start-index"] = start_index
        return self.get(self.resource_url(f"plan/{project_key}-{build_key}/artifact"), params=params)

    def get_issue_details(self, project_key, build_key, issue_key):
        """Fetch linked Jira issue details.
        :param project_key: projectKey path parameter
        :param build_key: buildKey path parameter
        :param issue_key: issueKey path parameter
        :return:
        """
        return self.get(self.resource_url(f"plan/{project_key}-{build_key}/issue/{issue_key}"))

    def get_plan_labels(self, project_key, build_key):
        """List of labels for plan.
        :param project_key: projectKey path parameter
        :param build_key: buildKey path parameter
        :return:
        """
        return self.get(self.resource_url(f"plan/{project_key}-{build_key}/label"))

    def enable_specs_for_branches(self, project_key, build_key):
        """Enable specs scanning for all branches.
        :param project_key: projectKey path parameter
        :param build_key: buildKey path parameter
        :return:
        """
        return self.post(self.resource_url(f"plan/{project_key}-{build_key}/branch/enableSpecsForBranches"))

    def mark_plan_favourite(self, project_key, build_key):
        """Add plan to favourite.
        :param project_key: projectKey path parameter
        :param build_key: buildKey path parameter
        :return:
        """
        return self.post(self.resource_url(f"plan/{project_key}-{build_key}/favourite"))

    def add_plan_label(self, project_key, build_key, data):
        """Add new label to plan.
        :param project_key: projectKey path parameter
        :param build_key: buildKey path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.post(self.resource_url(f"plan/{project_key}-{build_key}/label"), data=data)

    def quarantine_test(self, project_key, build_key, test_id):
        """Quarantine plan's test.
        :param project_key: projectKey path parameter
        :param build_key: buildKey path parameter
        :param test_id: testId path parameter
        :return:
        """
        return self.post(self.resource_url(f"plan/{project_key}-{build_key}/test/{test_id}/quarantine"))

    def unleash_test(self, project_key, build_key, test_id):
        """Unleash plan's test from quarantine.
        :param project_key: projectKey path parameter
        :param build_key: buildKey path parameter
        :param test_id: testId path parameter
        :return:
        """
        return self.post(self.resource_url(f"plan/{project_key}-{build_key}/test/{test_id}/unleash"))



    """Projects & repositories"""

    def delete_project_shared_credentials(self, project_key, shared_credential_id):
        """Deletes shared project credentials specified by id.
        :param project_key: projectKey path parameter
        :param shared_credential_id: sharedCredentialId path parameter
        :return:
        """
        return self.delete(
            self.resource_url(f"project/{project_key}/sharedCredentials/{shared_credential_id}"),
        )

    def delete_project_variable(self, project_key, variable_name):
        """Delete the project variable.
        :param project_key: projectKey path parameter
        :param variable_name: variableName path parameter
        :return:
        """
        return self.delete(self.resource_url(f"project/{project_key}/variable/{variable_name}"))

    def get_paginated_project_repositories(self, project_key, filter=None, limit=None, start=None):
        """Retrieves paginated project repositories specified by the project key.
        :param project_key: projectKey path parameter
        :param filter: filter query parameter
        :param limit: limit query parameter
        :param start: start query parameter
        :return:
        """
        params = {}
        if filter is not None:
            params["filter"] = filter
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        return self.get(self.resource_url(f"project/{project_key}/repositories"), params=params)

    def search_available_repositories_1(self, project_key, search_term=None):
        """Search for linked repositories which can be granted to create plans by Repository stored Bamboo Specs in given project
        :param project_key: projectKey path parameter
        :param search_term: searchTerm query parameter
        :return:
        """
        params = {}
        if search_term is not None:
            params["searchTerm"] = search_term
        return self.get(self.resource_url(f"project/{project_key}/repository/search"), params=params)

    def get_paginated_project_shared_credentials(self, project_key, filter=None, limit=None, start=None):
        """Retrieves paginated shared credentials for the project specified by the project key.
        :param project_key: projectKey path parameter
        :param filter: filter query parameter
        :param limit: limit query parameter
        :param start: start query parameter
        :return:
        """
        params = {}
        if filter is not None:
            params["filter"] = filter
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        return self.get(self.resource_url(f"project/{project_key}/sharedCredentials"), params=params)

    def export_project_specs(self, project_key, package=None, format=None):
        """Export all of the plans for a project to Bamboo specs.
        :param project_key: projectKey path parameter
        :param package: package query parameter
        :param format: format query parameter
        :return:
        """
        params = {}
        if package is not None:
            params["package"] = package
        if format is not None:
            params["format"] = format
        return self.get(self.resource_url(f"project/{project_key}/specs"), params=params)

    def get_project_variable(self, project_key, variable_name):
        """Retrieve the project variable by given name.
        :param project_key: projectKey path parameter
        :param variable_name: variableName path parameter
        :return:
        """
        return self.get(self.resource_url(f"project/{project_key}/variable/{variable_name}"))

    def get_project_variables(self, project_key):
        """Retrieve the list of all variables for a project.
        :param project_key: projectKey path parameter
        :return:
        """
        return self.get(self.resource_url(f"project/{project_key}/variables"))

    def create_project(self, data):
        """Create project.
        :param data: request body (dict or list)
        :return:
        """
        return self.post(self.resource_url("project"), data=data)

    def create_or_update_variable(self, project_key, data):
        """Create or update project variable.
        :param project_key: projectKey path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.post(self.resource_url(f"project/{project_key}/variable"), data=data)

    def enable_all_repositories_access(self, project_key, repository_id, data):
        """Enables access (i.e. allowing usage) to all project's repositories by the Bamboo Specs code stored in this repository.
        :param project_key: projectKey path parameter
        :param repository_id: repositoryId path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.put(
            self.resource_url(f"project/{project_key}/repository/{repository_id}/enableAllRepositoriesAccess"),
            data=data,
        )



    """Repositories"""

    def revoke_permission_to_use_repository_by_rss_repo(self, target_repository_id, repository_id):
        """Revoke access of RSS code stored in repository defined by repositoryId from repository defined by targetRepositoryId. Use this method when need to prevent usage of target repository by RSS code stored in repository referenced by repositoryId.
        :param target_repository_id: targetRepositoryId path parameter
        :param repository_id: repositoryId path parameter
        :return:
        """
        return self.delete(
            self.resource_url(f"repository/{target_repository_id}/rssrepository/{repository_id}"),
        )

    def search_specs_branches(self, repository_id, search_term=None):
        """Search for divergent branches names (i.e. vcs branches that have RSS execution results).
        :param repository_id: repositoryId path parameter
        :param search_term: searchTerm query parameter
        :return:
        """
        params = {}
        if search_term is not None:
            params["searchTerm"] = search_term
        return self.get(self.resource_url(f"repository/{repository_id}/rssBranches"), params=params)

    def get_rss_repositories_allowed_to_access_repository(self, repository_id):
        """Fetch list of RSS repositories which can use given repository by RSS code.
        :param repository_id: repositoryId path parameter
        :return:
        """
        return self.get(self.resource_url(f"repository/{repository_id}/rssrepository"))

    def search_available_repositories_2(self, repository_id, search_term=None):
        """Search for existing linked repositories which can be granted to use given repository by RSS.
        :param repository_id: repositoryId path parameter
        :param search_term: searchTerm query parameter
        :return:
        """
        params = {}
        if search_term is not None:
            params["searchTerm"] = search_term
        return self.get(self.resource_url(f"repository/{repository_id}/rssrepository/search"), params=params)

    def get_specs_detection_status(self, repository_id, max_result=None, branch=None):
        """Resource providing status of RSS processing for a given repository and optional branch.
        :param repository_id: repositoryId path parameter
        :param max_result: max-result query parameter
        :param branch: branch query parameter
        :return:
        """
        params = {}
        if max_result is not None:
            params["max-result"] = max_result
        if branch is not None:
            params["branch"] = branch
        return self.get(self.resource_url(f"repository/{repository_id}/scan/status"), params=params)

    def find_usage(self, repository_id, max_plans=None, max_environments=None):
        """Search for usages of given repository.
        :param repository_id: repositoryId path parameter
        :param max_plans: max-plans query parameter
        :param max_environments: max-environments query parameter
        :return:
        """
        params = {}
        if max_plans is not None:
            params["max-plans"] = max_plans
        if max_environments is not None:
            params["max-environments"] = max_environments
        return self.get(self.resource_url(f"repository/{repository_id}/usage"), params=params)

    def grant_rss_repository_access(self, repository_id, data):
        """Grant repository with RSS code to use target repository in build plans and deployments. If permission is not granted RSS import will fail when code tries to use target repository.
        :param repository_id: repositoryId path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.post(self.resource_url(f"repository/{repository_id}/rssrepository"), data=data)

    def trigger_specs_scanning(self, repository_id, branch=None):
        """Resource for triggering Repository-stored Bamboo Specs in a 'forced' way. Successful requests to this resource will trigger Bamboo Specs execution even if standard processing would have been skipped (e.g. no new commits to process).
        :param repository_id: repositoryId path parameter
        :param branch: branch query parameter
        :return:
        """
        params = {}
        if branch is not None:
            params["branch"] = branch
        return self.post(self.resource_url(f"repository/{repository_id}/scanNow"), params=params)

    def trigger_specs_scanning_1(self, name=None, repository_id=None, id=None, repository_name=None):
        """Webhook resource for triggering Repository-stored Bamboo Specs. Either repository ID or name must be provided via query parameters to identify the linked repository in which Bamboo Specs are defined.
        :param name: name query parameter
        :param repository_id: repositoryId query parameter
        :param id: id query parameter
        :param repository_name: repositoryName query parameter
        :return:
        """
        params = {}
        if name is not None:
            params["name"] = name
        if repository_id is not None:
            params["repositoryId"] = repository_id
        if id is not None:
            params["id"] = id
        if repository_name is not None:
            params["repositoryName"] = repository_name
        return self.post(self.resource_url("repository/scan"), params=params)

    def enable_all_projects_access(self, repository_id, data):
        """Enables access (i.e. allowing modifications) for all Bamboo projects by the Bamboo Specs code stored in this repository. Changes in Bamboo Specs detected will trigger execution of Specs and thus an update of corresponding entities (such as build plans or deployments).
        :param repository_id: repositoryId path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.put(self.resource_url(f"repository/{repository_id}/enableAllProjectsAccess"), data=data)

    def enable_all_repositories_access_1(self, repository_id, data):
        """Enables access (i.e. allowing usage in plans or deployment projects) for all Bamboo linked repositories by the Bamboo Specs code stored in this repository.
        :param repository_id: repositoryId path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.put(
            self.resource_url(f"repository/{repository_id}/enableAllRepositoriesAccess"),
            data=data,
        )

    def enable_ci(self, repository_id, data):
        """Enables or disables detection of Bamboo Specs stored in the repository. If enabled, code changes detected in Bamboo Specs in new commits will trigger execution of Bamboo Specs and thus an update of corresponding entities (such as build plans, deployments or permissions).
        :param repository_id: repositoryId path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.put(self.resource_url(f"repository/{repository_id}/enableCi"), data=data)

    def enable_project_creation(self, repository_id, data):
        """Enables build and deployment project creation by the Bamboo Specs code stored in this repository.
        :param repository_id: repositoryId path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.put(self.resource_url(f"repository/{repository_id}/enableProjectCreation"), data=data)

    def test_connection_1(self, data):
        """Tests connection to a repository if the repository type supports connection testing. Request payload should contain repository configuration.
        :param data: request body (dict or list)
        :return:
        """
        return self.put(self.resource_url("repository/testConnection"), data=data)



    """Build results"""

    def remove_build_comment(self, project_key, build_key, build_number, comment_id):
        """Removes a comment from a build result.
        :param project_key: projectKey path parameter
        :param build_key: buildKey path parameter
        :param build_number: buildNumber path parameter
        :param comment_id: commentId path parameter
        :return:
        """
        return self.delete(
            self.resource_url(f"result/{project_key}-{build_key}-{build_number}/comment/{comment_id}"),
        )

    def get_branch_history(self, project_key, build_key, branch_name, include_all_states=None, continuable=None, issue_key=None, max_results=None, start_index=None, label=None, buildstate=None, favourite=None, expand=None, life_cycle_state=None):
        """Provide list of build results for specified plan's branch. Plan might be top level plan (projectKey-planKey) or job plan (projectKey-planKey-jobKey).
        :param project_key: projectKey path parameter
        :param build_key: buildKey path parameter
        :param branch_name: branchName path parameter
        :param include_all_states: includeAllStates query parameter
        :param continuable: continuable query parameter
        :param issue_key: issueKey query parameter
        :param max_results: max-results query parameter
        :param start_index: start-index query parameter
        :param label: label query parameter
        :param buildstate: buildstate query parameter
        :param favourite: favourite query parameter
        :param expand: expand query parameter
        :param life_cycle_state: lifeCycleState query parameter
        :return:
        """
        params = {}
        if include_all_states is not None:
            params["includeAllStates"] = include_all_states
        if continuable is not None:
            params["continuable"] = continuable
        if issue_key is not None:
            params["issueKey"] = issue_key
        if max_results is not None:
            params["max-results"] = max_results
        if start_index is not None:
            params["start-index"] = start_index
        if label is not None:
            params["label"] = label
        if buildstate is not None:
            params["buildstate"] = buildstate
        if favourite is not None:
            params["favourite"] = favourite
        if expand is not None:
            params["expand"] = expand
        if life_cycle_state is not None:
            params["lifeCycleState"] = life_cycle_state
        return self.get(
            self.resource_url(f"result/{project_key}-{build_key}/branch/{branch_name}"),
            params=params,
        )



    """Web sudo"""

    def remove_web_sudo_from_session(self):
        """Remove web sudo from session.
        :return:
        """
        return self.delete(self.resource_url("websudo-session"))

    def get_expiry(self):
        """Get the web sudo expiry from session.
        :return:
        """
        return self.get(self.resource_url("websudo-session"))

    def refresh_web_sudo_session(self):
        """Refresh the web sudo expiry for the current session.
        :return:
        """
        return self.put(self.resource_url("websudo-session"))



    """General"""

    def get_all_services(self):
        """Provides list of available REST resources in Bamboo
        :return:
        """
        return self.get(self.resource_url(""))



    """Build numbers & clone"""

    def get_next_build_number(self, project_key, build_key):
        """Retrieve the next build number for a given plan or plan branch.
        :param project_key: projectKey path parameter
        :param build_key: buildKey path parameter
        :return:
        """
        return self.get(self.resource_url(f"buildNumber/{project_key}-{build_key}"))

    def bump_build_number(self, project_key, build_key, data):
        """Bump the next build number for a given plan or plan branch to the specified value.
        :param project_key: projectKey path parameter
        :param build_key: buildKey path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.put(self.resource_url(f"buildNumber/{project_key}-{build_key}/bump"), data=data)

    def get_clone(self, project_key, build_key, to_project_key, to_build_key):
        """Clone an existing Plan into a new one, possibly into different project.
        :param project_key: projectKey path parameter
        :param build_key: buildKey path parameter
        :param to_project_key: toProjectKey path parameter
        :param to_build_key: toBuildKey path parameter
        :return:
        """
        return self.put(self.resource_url(f"clone/{project_key}-{build_key}:{to_project_key}-{to_build_key}"))



    """Server capabilities"""

    def get_all_capabilities_on_server(self, max_result=None, search_term=None, last_group=None, start_index=None):
        """Provides a list of capabilities for a select list in the UI.  Filterable and paginable.
        :param max_result: max-result query parameter
        :param search_term: searchTerm query parameter
        :param last_group: lastGroup query parameter
        :param start_index: start-index query parameter
        :return:
        """
        params = {}
        if max_result is not None:
            params["max-result"] = max_result
        if search_term is not None:
            params["searchTerm"] = search_term
        if last_group is not None:
            params["lastGroup"] = last_group
        if start_index is not None:
            params["start-index"] = start_index
        return self.get(self.resource_url("capability/groupedListing"), params=params)



    """Plan summary charts"""

    def get_plan_summary(self, build_keys=None):
        """Get plan summary.
        :param build_keys: buildKeys query parameter
        :return:
        """
        params = {}
        if build_keys is not None:
            params["buildKeys"] = build_keys
        return self.get(self.resource_url("chart/planSummary"), params=params)



    """Plan dependencies"""

    def search_for_available_plan_child_dependencies(self, project_key, build_key, search_term, max_result=None, start_index=None):
        """Search for available plan child dependencies
        :param project_key: projectKey path parameter
        :param build_key: buildKey path parameter
        :param max_result: max-result query parameter
        :param search_term: searchTerm query parameter
        :param start_index: start-index query parameter
        :return:
        """
        params = {}
        if max_result is not None:
            params["max-result"] = max_result
        if search_term is not None:
            params["searchTerm"] = search_term
        if start_index is not None:
            params["start-index"] = start_index
        return self.get(
            self.resource_url(f"dependency/search/{project_key}-{build_key}/child"),
            params=params,
        )

    def search_for_available_plan_parent_dependencies(self, project_key, build_key, search_term, max_result=None, start_index=None):
        """Search for available plan parent dependencies
        :param project_key: projectKey path parameter
        :param build_key: buildKey path parameter
        :param max_result: max-result query parameter
        :param search_term: searchTerm query parameter
        :param start_index: start-index query parameter
        :return:
        """
        params = {}
        if max_result is not None:
            params["max-result"] = max_result
        if search_term is not None:
            params["searchTerm"] = search_term
        if start_index is not None:
            params["start-index"] = start_index
        return self.get(
            self.resource_url(f"dependency/search/{project_key}-{build_key}/parent"),
            params=params,
        )



    """Job configuration"""

    def get_docker_pipeline_configuration(self, job_key):
        """Retrieves Docker configuration for given job.
        :param job_key: jobKey path parameter
        :return:
        """
        return self.get(self.resource_url(f"job/{job_key}/docker"))

    def set_docker_pipeline_configuration(self, job_key, data):
        """Updates Docker configuration for given job.
        :param job_key: jobKey path parameter
        :param data: request body (dict or list)
        :return:
        """
        return self.put(self.resource_url(f"job/{job_key}/docker"), data=data)



    """Global search"""

    def search(self, search_term=None, search_entity=None):
        """Performs a starts with search against projects, plans, plan branches, deployment projects
        :param search_term: searchTerm query parameter
        :param search_entity: searchEntity query parameter
        :return:
        """
        params = {}
        if search_term is not None:
            params["searchTerm"] = search_term
        if search_entity is not None:
            params["searchEntity"] = search_entity
        return self.get(self.resource_url("quicksearch"), params=params)

    def search_authors(self, search_term, max_result=None, unlinked_only=None, start_index=None):
        """A starts-with search of authors based on their author name.
        :param max_result: max-result query parameter
        :param unlinked_only: unlinkedOnly query parameter
        :param search_term: searchTerm query parameter
        :param start_index: start-index query parameter
        :return:
        """
        params = {}
        if max_result is not None:
            params["max-result"] = max_result
        if unlinked_only is not None:
            params["unlinkedOnly"] = unlinked_only
        if search_term is not None:
            params["searchTerm"] = search_term
        if start_index is not None:
            params["start-index"] = start_index
        return self.get(self.resource_url("search/authors"), params=params)

    def search_deployments(self, max_result=None, search_term=None, start_index=None, permission=None):
        """Performs a contains search against deployment project name.
        :param max_result: max-result query parameter
        :param search_term: searchTerm query parameter
        :param start_index: start-index query parameter
        :param permission: permission query parameter
        :return:
        """
        params = {}
        if max_result is not None:
            params["max-result"] = max_result
        if search_term is not None:
            params["searchTerm"] = search_term
        if start_index is not None:
            params["start-index"] = start_index
        if permission is not None:
            params["permission"] = permission
        return self.get(self.resource_url("search/deployments"), params=params)

    def search_jobs(self, plan_key, max_result=None, search_term=None, start_index=None):
        """Performs a "starts with" search against full job name and full job key.
        :param plan_key: planKey path parameter
        :param max_result: max-result query parameter
        :param search_term: searchTerm query parameter
        :param start_index: start-index query parameter
        :return:
        """
        params = {}
        if max_result is not None:
            params["max-result"] = max_result
        if search_term is not None:
            params["searchTerm"] = search_term
        if start_index is not None:
            params["start-index"] = start_index
        return self.get(self.resource_url(f"search/jobs/{plan_key}"), params=params)

    def search_projects(self, max_result=None, search_term=None, start_index=None, permission=None):
        """Performs a contains search against project name.
        :param max_result: max-result query parameter
        :param search_term: searchTerm query parameter
        :param start_index: start-index query parameter
        :param permission: permission query parameter
        :return:
        """
        params = {}
        if max_result is not None:
            params["max-result"] = max_result
        if search_term is not None:
            params["searchTerm"] = search_term
        if start_index is not None:
            params["start-index"] = start_index
        if permission is not None:
            params["permission"] = permission
        return self.get(self.resource_url("search/projects"), params=params)

    def search_stages(self, plan_key, max_result=None, search_term=None, start_index=None, stage_id=None):
        """Performs a "starts with" search against full stage name.
        :param plan_key: planKey path parameter
        :param max_result: max-result query parameter
        :param search_term: searchTerm query parameter
        :param start_index: start-index query parameter
        :param stage_id: stageId query parameter
        :return:
        """
        params = {}
        if max_result is not None:
            params["max-result"] = max_result
        if search_term is not None:
            params["searchTerm"] = search_term
        if start_index is not None:
            params["start-index"] = start_index
        if stage_id is not None:
            params["stageId"] = stage_id
        return self.get(self.resource_url(f"search/stages/{plan_key}"), params=params)

    def search_users(self, search_term, max_result=None, start_index=None):
        """A starts-with search of users based on their username, full-name and if allowed email address.
        :param max_result: max-result query parameter
        :param search_term: searchTerm query parameter
        :param start_index: start-index query parameter
        :return:
        """
        params = {}
        if max_result is not None:
            params["max-result"] = max_result
        if search_term is not None:
            params["searchTerm"] = search_term
        if start_index is not None:
            params["start-index"] = start_index
        return self.get(self.resource_url("search/users"), params=params)

    def search_versions(self, deployment_project_id, max_result=None, branch_key=None, search_term=None, start_index=None, chronological_order=None):
        """Performs a contains search against a version name.
        :param max_result: max-result query parameter
        :param branch_key: branchKey query parameter
        :param search_term: searchTerm query parameter
        :param start_index: start-index query parameter
        :param deployment_project_id: deploymentProjectId query parameter
        :param chronological_order: chronologicalOrder query parameter
        :return:
        """
        params = {}
        if max_result is not None:
            params["max-result"] = max_result
        if branch_key is not None:
            params["branchKey"] = branch_key
        if search_term is not None:
            params["searchTerm"] = search_term
        if start_index is not None:
            params["start-index"] = start_index
        if deployment_project_id is not None:
            params["deploymentProjectId"] = deployment_project_id
        if chronological_order is not None:
            params["chronologicalOrder"] = chronological_order
        return self.get(self.resource_url("search/versions"), params=params)



    """Server status"""

    def get_status_2(self):
        """Returns the current status of the Bamboo node. This endpoint enables a basic status check on the status of a Bamboo node.
        :return:
        """
        return self.get(self.resource_url("status"))



    """Utility"""

    def encrypt(self, data):
        """Encrypts a given text based on the instance specific cipher. Encrypted data can be used i.a. in Repository-stored Specs. Feature can be enabled or disabled in Bamboo security configuration. Number of allowed requests per user is limited and can be modified in Bamboo security configuration.
        :param data: request body (dict or list)
        :return:
        """
        return self.post(self.resource_url("encrypt"), data=data)



    """Elastic configuration"""

    def update_all_image_ids(self, image_id, new_image_id):
        """Bulk update of all images AMI id.
        :param image_id: imageId path parameter
        :param new_image_id: newImageId query parameter
        :return:
        """
        params = {}
        if new_image_id is not None:
            params["newImageId"] = new_image_id
        return self.put(self.resource_url(f"elasticConfiguration/image-id/{image_id}"), params=params)



    """Quick filters"""

    def deactivate_filter(self, id):
        """Deactivates a quick filter for currently logged in user.
        :param id: id path parameter
        :return:
        """
        return self.put(self.resource_url(f"quickFilter/{id}/deactivate"))
