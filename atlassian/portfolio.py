import logging
from atlassian import AtlassianRestAPI


log = logging.getLogger('atlassian.portfolio')


class Portfolio(AtlassianRestAPI):

    def __init__(self, plan_id, *args, **kwargs):
        self.plan_id = plan_id
        super(Portfolio, self).__init__(*args, **kwargs)

    def get_epic(self, epic):
        key = [x.get('link', None) for x in epic.get('links', [])]
        estimates = self.estimates_dict(epic['estimates'])
        estimates.update(Total=sum(estimates.values()))
        return {
            'title': epic.get('title', None),
            'team': self.team_name(epic.get('teamId')) if epic.get('teamId', None) else None,
            'description': epic.get('description', None),
            'issuekey': key[0] if key else None,
            'estimates': estimates}

    def plan(self):
        url = '/rest/roadmap/1.0/plans/{0}.json'.format(self.plan_id)
        return self.get(url)

    def stages(self):
        url = '/rest/roadmap/1.0/plans/{0}/stages.json'.format(self.plan_id)
        return self.get(url)

    def teams(self):
        url = '/rest/roadmap/1.0/plans/{0}/teams.json'.format(self.plan_id)
        return self.get(url)

    def team_name(self, team_id):
        return [team['title'] for team in self.teams()['collection'] if team['id'] == str(team_id)][0]

    def config(self):
        url = '/rest/roadmap/1.0/plans/{0}/config.json'.format(self.plan_id)
        return self.get(url)

    def persons(self):
        url = '/rest/roadmap/1.0/plans/{0}/persons.json'.format(self.plan_id)
        return self.get(url)

    def streams(self):
        url = '/rest/roadmap/1.0/plans/{0}/streams.json'.format(self.plan_id)
        return self.get(url)

    def releases(self):
        return self.streams()

    def themes(self):
        url = '/rest/roadmap/1.0/plans/{0}/themes.json'.format(self.plan_id)
        return self.get(url)

    def state(self, plan_version):
        url = '/rest/roadmap/1.0/scheduling/{0}/state.json?planVersion={1}'.format(self.plan_id, plan_version)
        return self.get(url)

    def filter(self, plan_version, limit=500):
        url = '/rest/roadmap/1.0/plans/{0}/workitems/filter.json?planVersion={1}'.format(self.plan_id, plan_version)
        return self.post(url, data={'limit': limit})

    def filters(self, query_string):
        url = '/rest/roadmap/1.0/system/filters.json?queryString={0}'.format(query_string)
        return self.get(url)

    def import_issues(self, jql, limit=100):
        url = '/rest/roadmap/1.0/system/import.json'
        data = {'planId': str(self.plan_id),
                'query': jql,
                'excludeLinked': False,
                'epicFetchEnabled': True,
                'maxResults': limit,
                'estimationMethod': 'estimates',
                'loadStoryPoints': True}
        self.post(url, data=data)

    def dependencies(self, workitem_id, plan_version):
        url = '/rest/roadmap/1.0/workitems/{0}/dependencies.json?planVersion={1}'.format(workitem_id, plan_version)
        return self.get(url)

    def stage_name(self, stage_id):
        return [stage['title'] for stage in self.stages()['collection'] if stage['id'] == str(stage_id)][0]

    def estimates_dict(self, estimates):
        return {self.stage_name(stage['targetId']): stage['value'] for stage in estimates['stages']}
