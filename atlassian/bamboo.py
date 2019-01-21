# coding: utf8
import logging
from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Bamboo(AtlassianRestAPI):
    def _get_generator(self, path, elements_key='results', element_key='result', data=None, flags=None,
                       params=None, headers=None):
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
        size = 1
        start_index = 0
        while size:
            params['start-index'] = start_index
            response = self.get(path, data, flags, params, headers)
            results = response[elements_key]
            size = results['size']
            # Check if start index was reset when reaching the end of the pages list
            if results['start-index'] < start_index:
                break
            for r in results[element_key]:
                yield r
            start_index += results['max-result']

    def base_list_call(self, resource, expand, favourite, clover_enabled, max_results, start_index=0, **kwargs):
        flags = []
        params = {'max-results': max_results}
        if expand:
            params['expand'] = expand
        if favourite:
            flags.append('favourite')
        if clover_enabled:
            flags.append('cloverEnabled')
        params.update(kwargs)
        if 'elements_key' in kwargs and 'element_key' in kwargs:
            return self._get_generator(self.resource_url(resource), flags=flags, params=params,
                                       elements_key=kwargs['elements_key'],
                                       element_key=kwargs['element_key'])
        params['start-index'] = start_index
        return self.get(self.resource_url(resource), flags=flags, params=params)

    def projects(self, expand=None, favourite=False, clover_enabled=False, max_results=25):
        return self.base_list_call('project', expand, favourite, clover_enabled, max_results,
                                   elements_key='projects', element_key='project')

    def project(self, project_key, expand=None, favourite=False, clover_enabled=False):
        resource = 'project/{}'.format(project_key)
        return self.base_list_call(resource, expand, favourite, clover_enabled, start_index=0, max_results=25)

    def project_plans(self, project_key):
        """
        Returns a generator with the plans in a given project
        :param project_key: Project key
        :return: Generator with plans
        """
        resource = 'project/{}'.format(project_key, max_results=25)
        return self.base_list_call(resource, expand='plans', favourite=False, clover_enabled=False, max_results=25,
                                   elements_key='plans', element_key='plan')

    def plans(self, expand=None, favourite=False, clover_enabled=False, start_index=0, max_results=25):
        return self.base_list_call("plan", expand, favourite, clover_enabled, start_index, max_results,
                                   elements_key='plans', element_key='plan')

    def results(self, project_key=None, plan_key=None, job_key=None, build_number=None, expand=None, favourite=False,
                clover_enabled=False, issue_key=None, start_index=0, max_results=25):
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
        :param start_index:
        :param max_results:
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
            resource += '/' + project_key

        params = {}
        if issue_key:
            params['issueKey'] = issue_key
        return self.base_list_call(resource, expand=expand, favourite=favourite, clover_enabled=clover_enabled,
                                   start_index=start_index, max_results=max_results,
                                   elements_key='results', element_key='result', **params)

    def latest_results(self, expand=None, favourite=False, clover_enabled=False, label=None, issue_key=None,
                       start_index=0, max_results=25):
        """
        Get latest Results
        :param expand:
        :param favourite:
        :param clover_enabled:
        :param label:
        :param issue_key:
        :param start_index:
        :param max_results:
        :return:
        """
        return self.results(expand=expand, favourite=favourite, clover_enabled=clover_enabled,
                            label=label, issue_key=issue_key, start_index=start_index, max_results=max_results)

    def project_latest_results(self, project_key, expand=None, favourite=False, clover_enabled=False, label=None,
                               issue_key=None, start_index=0, max_results=25):
        """
        Get latest Project Results
        :param project_key:
        :param expand:
        :param favourite:
        :param clover_enabled:
        :param label:
        :param issue_key:
        :param start_index:
        :param max_results:
        :return:
        """
        return self.results(project_key, expand=expand, favourite=favourite, clover_enabled=clover_enabled,
                            label=label, issue_key=issue_key, start_index=start_index, max_results=max_results)

    def plan_results(self, project_key, plan_key, expand=None, favourite=False, clover_enabled=False, label=None,
                     issue_key=None, start_index=0, max_results=25):
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
        :return:
        """
        return self.results(project_key, plan_key, expand=expand, favourite=favourite, clover_enabled=clover_enabled,
                            label=label, issue_key=issue_key, start_index=start_index, max_results=max_results)

    def build_result(self, build_key, expand=None):
        """
        Returns details of a specific build result
        :param expand: expands build result details on request. Possible values are: artifacts, comments, labels,
        Jira Issues, stages. stages expand is available only for top level plans. It allows to drill down to job results
        using stages.stage.results.result. All expand parameters should contain results.result prefix.
        :param build_key: Should be in the form XX-YY[-ZZ]-99, that is, the last token should be an integer representing
        the build number
        """
        try:
            int(build_key.split('-')[-1])
            resource = "result/{}".format(build_key)
            return self.base_list_call(resource, expand, favourite=False, clover_enabled=False,
                                       start_index=0, max_results=25)
        except ValueError:
            raise ValueError('The key "{}" does not correspond to a build result'.format(build_key))

    def build_latest_result(self, plan_key, expand=None):
        """
        Returns details of a latest build result
        :param expand: expands build result details on request. Possible values are: artifacts, comments, labels,
        Jira Issues, stages. stages expand is available only for top level plans. It allows to drill down to job results
        using stages.stage.results.result. All expand parameters should contain results.result prefix.
        :param plan_key: Should be in the form XX-YY[-ZZ]
        """
        try:
            resource = "result/{}/latest.json".format(plan_key)
            return self.base_list_call(resource, expand, favourite=False, clover_enabled=False,
                                       start_index=0, max_results=25)
        except ValueError:
            raise ValueError('The key "{}" does not correspond to the latest build result'.format(plan_key))

    def reports(self, max_results=25):
        params = {'max-results': max_results}
        return self._get_generator(self.resource_url('chart/reports'), elements_key='reports', element_key='report',
                                   params=params)

    def chart(self, report_key, build_keys, group_by_period, date_filter=None, date_from=None, date_to=None,
              width=None, height=None, start_index=9, max_results=25):
        params = {'reportKey': report_key, 'buildKeys': build_keys, 'groupByPeriod': group_by_period,
                  'start-index': start_index, 'max-results': max_results}
        if date_filter:
            params['dateFilter'] = date_filter
            if date_filter == 'RANGE':
                params['dateFrom'] = date_from
                params['dateTo'] = date_to
        if width:
            params['width'] = width
        if height:
            params['height'] = height
        return self.get(self.resource_url('chart'), params=params)

    def comments(self, project_key, plan_key, build_number, start_index=0, max_results=25):
        resource = "result/{}-{}-{}/comment".format(project_key, plan_key, build_number)
        params = {'start-index': start_index, 'max-results': max_results}
        return self.get(self.resource_url(resource), params=params)

    def create_comment(self, project_key, plan_key, build_number, comment, author=None):
        resource = "result/{}-{}-{}/comment".format(project_key, plan_key, build_number)
        comment_data = {'author': author if author else self.username, 'content': comment}
        return self.post(self.resource_url(resource), data=comment_data)

    def labels(self, project_key, plan_key, build_number, start_index=0, max_results=25):
        resource = "result/{}-{}-{}/label".format(project_key, plan_key, build_number)
        params = {'start-index': start_index, 'max-results': max_results}
        return self.get(self.resource_url(resource), params=params)

    def create_label(self, project_key, plan_key, build_number, label):
        resource = "result/{}-{}-{}/label".format(project_key, plan_key, build_number)
        return self.post(self.resource_url(resource), data={'name': label})

    def delete_label(self, project_key, plan_key, build_number, label):
        resource = "result/{}-{}-{}/label/{}".format(project_key, plan_key, build_number, label)
        return self.delete(self.resource_url(resource))

    def server_info(self):
        return self.get(self.resource_url('info'))

    def agent_status(self):
        return self.get(self.resource_url('agent'))

    def activity(self):
        return self.get('build/admin/ajax/getDashboardSummary.action')

    def deployment_project(self, project_id):
        resource = 'deploy/project/{}'.format(project_id)
        return self.get(self.resource_url(resource))

    def deployment_projects(self):
        resource = 'deploy/project/all'
        for project in self.get(self.resource_url(resource)):
            yield project

    def deployment_environment_results(self, env_id, expand=None, max_results=25):
        resource = 'deploy/environment/{environmentId}/results'.format(environmentId=env_id)
        params = {'max-result': max_results, 'start-index': 0}
        size = 1
        if expand:
            params['expand'] = expand
        while params['start-index'] < size:
            results = self.get(self.resource_url(resource), params=params)
            size = results['size']
            for r in results['results']:
                yield r
            params['start-index'] += results['max-result']

    def deployment_dashboard(self, project_id=None):
        """
        Returns the current status of each deployment environment
        If no project id is provided, returns all projects.
        """
        resource = 'deploy/dashboard/{}'.format(project_id) if project_id else 'deploy/dashboard'
        return self.get(self.resource_url(resource))

    def search_branches(self, plan_key, include_default_branch=True, max_results=25):
        params = {
            'max-result': max_results,
            'start-index': 0,
            'masterPlanKey': plan_key,
            'includeMasterBranch': include_default_branch
        }
        size = 1
        while params['start-index'] < size:
            results = self.get(self.resource_url('search/branches'), params=params)
            size = results['size']
            for r in results['searchResults']:
                yield r
            params['start-index'] += results['max-result']

    def plan_branches(self, plan_key, expand=None, favourite=False, clover_enabled=False, max_results=25):
        """api/1.0/plan/{projectKey}-{buildKey}/branch"""
        resource = 'plan/{}/branch'.format(plan_key)
        return self.base_list_call(resource, expand, favourite, clover_enabled, max_results,
                                   elements_key='branches', element_key='branch')

    def health_check(self):
        """
        Get health status
        https://confluence.atlassian.com/jirakb/how-to-retrieve-health-check-results-using-rest-api-867195158.html
        :return:
        """
        # check as Troubleshooting & Support Tools Plugin
        response = self.get('rest/troubleshooting/1.0/check/')
        if not response:
            # check as support tools
            response = self.get('rest/supportHealthCheck/1.0/check/')
        return response
