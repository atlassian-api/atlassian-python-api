import logging
from atlassian import AtlassianRestAPI


log = logging.getLogger("atlassian.portfolio")


class Portfolio(AtlassianRestAPI):
    
    def plan(self, portfolio_id):
        return self.get('/rest/roadmap/1.0/plans/{0}.json'.format(portfolio_id))

    def stages(self, portfolio_id):
        return self.get('/rest/roadmap/1.0/plans/{0}/stages.json'.format(portfolio_id))

    def teams(self, portfolio_id):
        return self.get('/rest/roadmap/1.0/plans/{0}/teams.json'.format(portfolio_id))

    def config(self, portfolio_id):
        return self.get('/rest/roadmap/1.0/plans/{0}/config.json'.format(portfolio_id))

    def persons(self, portfolio_id):
        return self.get('/rest/roadmap/1.0/plans/{0}/persons.json'.format(portfolio_id))

    def streams(self, portfolio_id):
        return self.get('/rest/roadmap/1.0/plans/{0}/streams.json'.format(portfolio_id))

    def releases(self, portfolio_id):
        return self.streams(portfolio_id)

    def themes(self, portfolio_id):
        return self.get('/rest/roadmap/1.0/plans/{0}/themes.json'.format(portfolio_id))

    def state(self, portfolio_id, plan_version):
        return self.get('/rest/roadmap/1.0/scheduling/{0}/state.json?planVersion={1}'.format(portfolio_id, plan_version))

    def filter(self, portfolio_id, plan_version):
        return self.get('/rest/roadmap/1.0/plans/{0}/workitems/filter.json?planVersion={1}'.format(portfolio_id, plan_version))

    def stage_name(self, portfolio_id, stage_id):
        return [stage['title'] for stage in self.stages(portfolio_id)['collection'] if stage['id'] == str(stage_id)][0]

    def estimates_dict(self, portfolio_id, estimates):
        return {self.stage_name(portfolio_id, stage['targetId']): stage['value'] for stage in estimates['stages']}
