import logging
from atlassian import AtlassianRestAPI


log = logging.getLogger('atlassian.stash')


class Stash(AtlassianRestAPI):

	def projects_list(self, expand=None, favourite=False, cloverEnabled=False, start=0, limit=25):
		args = ()
		kwargs = {}
		return self.get(self.resource_url('project'), args=args, kwargs=kwargs)

	def plans_list(self, expand=None, favourite=False, cloverEnabled=False, start=0, limit=25):
		pass

	def result_list(self, project_key=None, plan_key=None, build_number=None,
		expand=None, favourite=False, cloverEnabled=False, label=None,
		start=0, limit=25):
		pass

	def get_project_latest_results(self, project, expand=None, favourite=False, cloverEnabled=False, label=None,
		start=0, limit=25):
		return self.result_list(project_key, expand=expand, favourite=favourite, cloverEnabled=cloverEnabled,
			label=label, start=start, limit=limit)

	def get_plan_results(self, project_key, plan_key, expand=None, favourite=False, cloverEnabled=False, label=None,
		start=0, limit=25):
		return self.result_list(project_key, plan_key, expand=expand, favourite=favourite, cloverEnabled=cloverEnabled,
			label=label, start=start, limit=limit)

	def get_result(self, project_key, plan_key, build_key, expand=None, favourite=False, cloverEnabled=False, label=None,
		start=0, limit=25):
		return self.result_list(project_key, plan_key, expand=expand, favourite=favourite, cloverEnabled=cloverEnabled,
			label=label, start=start, limit=limit)

	def chart_list(self, reportKey, buildKeys, groupByPeriod, dateFrom=None, dateTo=None,
		width=None, height=None):
		return self.result_list()

	def reports_list(self, expand=None, start=0, limit=25):
		pass

	def get_comments(self, project_key, plan_key, build_number):
		pass

	def get_labels(self, project_key, plan_key, build_number):
		pass

	def get_server_info(self):
		pass