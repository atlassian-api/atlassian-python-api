# coding=utf-8

from ..base import BitbucketCloudBase
from .defaultReviewers import DefaultReviewer
from datetime import datetime


class PullRequests(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(PullRequests, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        if "errors" in data:
            return
        return PullRequest(self.url_joiner(self.url, data["id"]), data, **self._new_session_args)

    def each(self, q=None, sort=None):
        """
        Returns the list of pull requests in this repository.

        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the PullRequest objects
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        for pr in self._get_paged(None, trailing=True, params=params):
            yield self.__get_object(pr)

        return

    def get(self, id):
        """
        Returns the pull requests with the requested id in this repository.

        :param id: int: The requested pull request id

        :return: The requested PullRequest object
        """
        return self.__get_object(super(PullRequests, self).get(id))


class PullRequest(BitbucketCloudBase):
    def __init__(self, url, data, *args, **kwargs):
        super(PullRequest, self).__init__(url, *args, data=data, expected_type="pullrequest", **kwargs)

    @property
    def id(self):
        """ unique pull request id """
        return self.get_data("id")

    @property
    def title(self):
        """ pull request title """
        return self.get_data("title")

    @property
    def description(self):
        """ pull request description """
        return self.get_data("description")

    @property
    def state(self):
        """
        pull request state
        possible values: MERGED, SUPERSEDED, OPEN, DECLINED
        """
        return self.get_data("state")

    @property
    def created_on(self):
        """ time of creation """
        return datetime.strptime(self.get_data("created_on"), "%Y-%m-%dT%H:%M:%S.%f%z")

    @property
    def updated_on(self):
        """ time of last update """
        uo_str = self.get_data("updated_on")
        uo_dt = datetime.strptime(uo_str, "%Y-%m-%dT%H:%M:%S.%f%z") if uo_str else uo_str
        return uo_dt

    @property
    def close_source_branch(self):
        """ close source branch flag """
        return self.get_data("close_source_branch")

    @property
    def source_branch(self):
        """ source branch """
        branch = self.get_data("source").get("branch")
        return branch.get("name")

    @property
    def destination_branch(self):
        """ destination branch """
        branch = self.get_data("destination").get("branch")
        return branch.get("name")

    @property
    def comment_count(self):
        """ number of comments """
        return self.get_data("comment_count")

    @property
    def task_count(self):
        """ number of tasks """
        return self.get_data("task_count")

    @property
    def declined_reason(self):
        """ reason for declining """
        return self.get_data("reason")

    @property
    def author(self):
        """ DefaultReviewer object of the author """
        return DefaultReviewer(None, self.get_data("author"))

    def participants(self):
        """ Returns a generator object of participants """
        for participant in self.get_data("participants"):
            yield Participant(participant)

        return

    def reviewers(self):
        """ Returns a generator object of reviewers """
        for reviewer in self.get_data("reviewers"):
            yield DefaultReviewer(None, reviewer)

        return


class Participant(BitbucketCloudBase):
    def __init__(self, data, *args, **kwargs):
        super(Participant, self).__init__(None, None, *args, data=data, expected_type="participant", **kwargs)

    @property
    def user(self):
        """ DefaultReviewer object with user information of the participant """
        return DefaultReviewer(None, self.get_data("user"))

    @property
    def role(self):
        """ Returns PARTICIPANT or REVIEWER """
        return self.get_data("role")

    @property
    def state(self):
        """ Returns approved, changes_requested or None"""
        return self.get_data("state")

    @property
    def participated_on(self):
        """ time of last participation """
        po_str = self.get_data("participated_on")
        po_dt = datetime.strptime(po_str, "%Y-%m-%dT%H:%M:%S.%f%z") if po_str else po_str
        return po_dt

    @property
    def approved(self):
        """ Returns True if the user approved the pull request, else False """
        return self.get_data("approved")
