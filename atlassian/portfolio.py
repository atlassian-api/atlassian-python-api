import logging
from atlassian import AtlassianRestAPI


log = logging.getLogger('atlassian.portfolio')


class Portfolio(AtlassianRestAPI):

    def plan(self, plan_id):
        return self.get('/rest/roadmap/1.0/plans/{0}.json'.format(plan_id))

    def stages(self, plan_id):
        return self.get('/rest/roadmap/1.0/plans/{0}/stages.json'.format(plan_id))

    def teams(self, plan_id):
        return self.get('/rest/roadmap/1.0/plans/{0}/teams.json'.format(plan_id))

    def team_name(self, plan_id, team_id):
        return [team['title'] for team in self.teams(team_id)['collection'] if team['id'] == str(team_id)][0]

    def config(self, plan_id):
        return self.get('/rest/roadmap/1.0/plans/{0}/config.json'.format(plan_id))

    def persons(self, plan_id):
        return self.get('/rest/roadmap/1.0/plans/{0}/persons.json'.format(plan_id))

    def streams(self, plan_id):
        return self.get('/rest/roadmap/1.0/plans/{0}/streams.json'.format(plan_id))

    def releases(self, plan_id):
        return self.streams(plan_id)

    def themes(self, plan_id):
        return self.get('/rest/roadmap/1.0/plans/{0}/themes.json'.format(plan_id))

    def state(self, plan_id, plan_version):
        return self.get('/rest/roadmap/1.0/scheduling/{0}/state.json?planVersion={1}'.format(plan_id, plan_version))

    def filter(self, plan_id, plan_version, limit=500):
        url = '/rest/roadmap/1.0/plans/{0}/workitems/filter.json?planVersion={1}'.format(plan_id, plan_version)
        return self.post(url, data={'limit': limit})

    def dependencies(self, workitem_id, plan_version):
        url = '/rest/roadmap/1.0/workitems/{0}/dependencies.json?planVersion={1}'.format(workitem_id, plan_version)
        return self.get(url)

    def stage_name(self, plan_id, stage_id):
        return [stage['title'] for stage in self.stages(plan_id)['collection'] if stage['id'] == str(stage_id)][0]

    def estimates_dict(self, plan_id, estimates):
        return {self.stage_name(plan_id, stage['targetId']): stage['value'] for stage in estimates['stages']}
