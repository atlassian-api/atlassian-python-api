# coding=utf-8
import logging

from .rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class Portfolio(AtlassianRestAPI):
    def __init__(self, plan_id, *args, **kwargs):
        self.plan_id = plan_id
        super(Portfolio, self).__init__(*args, **kwargs)

    def get_epic(self, epic):
        key = [x.get("link", None) for x in epic.get("links", [])]
        estimates = self.get_estimates_dict(epic["estimates"])
        estimates.update(Total=sum(estimates.values()))
        team_id = epic.get("teamId", None)
        return {
            "title": epic.get("title", None),
            "team": self.get_team_name(team_id) if team_id else None,
            "description": epic.get("description", None),
            "issuekey": key[0] if key else None,
            "estimates": estimates,
        }

    def get_plan(self):
        url = f"rest/roadmap/1.0/plans/{self.plan_id}.json"
        return self.get(url)

    def get_stages(self):
        url = f"rest/roadmap/1.0/plans/{self.plan_id}/stages.json"
        return self.get(url)

    def get_teams(self):
        url = f"rest/roadmap/1.0/plans/{self.plan_id}/teams.json"
        return self.get(url)

    def get_team_name(self, team_id):
        all_teams = self.get_teams()["collection"]
        return [team["title"] for team in all_teams if team["id"] == str(team_id)][0]

    def get_config(self):
        url = f"rest/roadmap/1.0/plans/{self.plan_id}/config.json"
        return self.get(url)

    def get_persons(self):
        url = f"rest/roadmap/1.0/plans/{self.plan_id}/persons.json"
        return self.get(url)

    def get_streams(self):
        url = f"rest/roadmap/1.0/plans/{self.plan_id}/streams.json"
        return self.get(url)

    def get_releases(self):
        return self.get_streams()

    def get_themes(self):
        url = f"rest/roadmap/1.0/plans/{self.plan_id}/themes.json"
        return self.get(url)

    def get_state(self):
        url = f"rest/roadmap/1.0/scheduling/{self.plan_id}/state.json"
        return self.get(url)

    def get_filter(self, limit=500):
        url = f"rest/roadmap/1.0/plans/{self.plan_id}/workitems/filter.json"
        return self.post(url, data={"limit": limit})

    def get_filters(self, query_string):
        url = f"rest/roadmap/1.0/system/filters.json?queryString={query_string}"
        return self.get(url)

    def get_dependencies(self, workitem_id, plan_version):
        url = f"rest/roadmap/1.0/workitems/{workitem_id}/dependencies.json?planVersion={plan_version}"
        return self.get(url)

    def get_stage_name(self, stage_id):
        all_stages = self.get_stages()["collection"]
        return [stage["title"] for stage in all_stages if stage["id"] == str(stage_id)][0]

    def get_estimates_dict(self, estimates):
        return {self.get_stage_name(stage["targetId"]): stage["value"] for stage in estimates["stages"]}

    def import_workitem(self, data):
        url = f"rest/roadmap/1.0/plans/bulk/{self.plan_id}/workitems.json"
        return self.post(url, data=data)

    def get_jql_issues(
        self,
        jql,
        limit=500,
        exclude_linked=True,
        estimation_method="estimates",
        epic_fetch_enabled=True,
        load_story_points=True,
    ):
        url = "rest/roadmap/1.0/system/import.json"
        data = {
            "planId": str(self.plan_id),
            "query": jql,
            "excludeLinked": exclude_linked,
            "epicFetchEnabled": epic_fetch_enabled,
            "maxResults": limit,
            "estimationMethod": estimation_method,
            "loadStoryPoints": load_story_points,
        }
        return self.post(url, data=data)["data"]["items"]
