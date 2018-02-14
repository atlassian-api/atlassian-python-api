import logging
from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Bamboo(AtlassianRestAPI):

    def base_list_call(self, resource, expand, favourite, cloverEnabled, start_index, max_results, **kwargs):
        flags = []
        params = {'start-index': start_index, 'max-results': max_results}
        if expand:
            params['expand'] = expand
        if favourite:
            flags.append('favourite')
        if cloverEnabled:
            flags.append('cloverEnabled')
        params.update(kwargs)
        return self.get(self.resource_url(resource), flags=flags, params=params)

    def projects(self, project_key=None, expand=None, favourite=False, cloverEnabled=False, start_index=0, max_results=25):
        resource = 'project/{}'.format(project_key) if project_key else 'project'
        return self.base_list_call(resource, expand, favourite, cloverEnabled, start_index, max_results)

    def plans(self, expand=None, favourite=False, cloverEnabled=False, start_index=0, max_results=25):
        return self.base_list_call("plan", expand, favourite, cloverEnabled, start_index, max_results)

    def results(self, project_key=None, plan_key=None, job_key=None, build_number=None, expand=None, favourite=False,
                cloverEnabled=False, label=None, issueKey=None, start_index=0, max_results=25):
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
        if issueKey:
            params['issueKey'] = issueKey
        return self.base_list_call(resource, expand, favourite, cloverEnabled, start_index, max_results, **params)

    def latest_results(self, expand=None, favourite=False, cloverEnabled=False, label=None, issueKey=None,
                       start_index=0, max_results=25):
        return self.results(expand=expand, favourite=favourite, cloverEnabled=cloverEnabled,
                            label=label, issueKey=issueKey, start_index=start_index, max_results=max_results)

    def project_latest_results(self, project_key, expand=None, favourite=False, cloverEnabled=False, label=None, issueKey=None,
                               start_index=0, max_results=25):
        return self.results(project_key, expand=expand, favourite=favourite, cloverEnabled=cloverEnabled,
                            label=label, issueKey=issueKey, start_index=start_index, max_results=max_results)

    def plan_results(self, project_key, plan_key, expand=None, favourite=False, cloverEnabled=False, label=None, issueKey=None,
                     start_index=0, max_results=25):
        return self.results(project_key, plan_key, expand=expand, favourite=favourite, cloverEnabled=cloverEnabled,
                            label=label, issueKey=issueKey, start_index=start_index, max_results=max_results)

    def build_result(self, project_key, plan_key, build_key, expand=None, favourite=False, cloverEnabled=False, label=None, issueKey=None,
                     start_index=0, max_results=25):
        return self.results(project_key, plan_key, expand=expand, favourite=favourite, cloverEnabled=cloverEnabled,
                            label=label, issueKey=issueKey, start_index=start_index, max_results=max_results)

    def reports(self, expand=None, start_index=0, max_results=25):
        params = {'start-index': start_index, 'max-results': max_results}
        if expand:
            params['expand'] = expand

        return self.get(self.resource_url('chart/reports'), params=params)

    def chart(self, reportKey, buildKeys, groupByPeriod, dateFilter=None, dateFrom=None, dateTo=None,
              width=None, height=None, start_index=9, max_results=25):
        params = {'reportKey': reportKey, 'buildKeys': buildKeys, 'groupByPeriod': groupByPeriod,
                  'start-index': start_index, 'max-results': max_results}
        if dateFilter:
            params['dateFilter'] = dateFilter
            if dateFilter == 'RANGE':
                params['dateFrom'] = dateFrom
                params['dateTo'] = dateTo
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

    def deployment_project(self, project_id=None):
        resource = 'deploy/project/{}'.format(project_id) if project_id else 'deploy/project/all'
        return self.get(self.resource_url(resource))

    def deployment_environment_results(self, env_id, expand=None):
        resource = 'deploy/environment/{environmentId}/results'.format(environmentId=env_id)
        params = {'expand': expand}
        return self.get(self.resource_url(resource), params=params)

    def deployment_dashboard(self, project_id=None):
        """
        Returns the current status of each deployment environment
        If no project id is provided, returns all projects.
        """
        resource = 'deploy/dashboard/{}'.format(project_id) if project_id else 'deploy/dashboard'
        return self.get(self.resource_url(resource))

    def search_branches(self, plan_key, include_default_branch=True, start_index=0, max_results=25):
        return self.base_list_call('search/branches', expand=None, start_index=start_index, max_results=max_results,
                                   cloverEnabled=False, favourite=False,
                                   masterPlanKey=plan_key,
                                   includeMasterBranch=include_default_branch)
