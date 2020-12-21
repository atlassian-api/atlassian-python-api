# coding=utf-8

import json
from ..base import BitbucketCloudBase
from .users import User, Participant
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

    def _check_if_open(self):
        if not self.is_open:
            raise Exception("Pull Request isn't open")
        return

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
    def is_declined(self):
        """ True if the pull request was declined """
        return self.get_data("state").upper() == "DECLINED"

    @property
    def is_merged(self):
        """ True if the pull request was merged """
        return self.get_data("state").upper() == "MERGED"

    @property
    def is_open(self):
        """ True if the pull request is open """
        return self.get_data("state").upper() == "OPEN"

    @property
    def is_superseded(self):
        """ True if the pull request was superseded """
        return self.get_data("state").upper() == "SUPERSEDED"

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
        return self.get_data("source")["name"]["branch"]

    @property
    def destination_branch(self):
        """ destination branch """
        return self.get_data("destination")["branch"]["name"]

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
        """ User object of the author """
        return User(None, self.get_data("author"))

    def participants(self):
        """ Returns a generator object of participants """
        for participant in self.get_data("participants"):
            yield Participant(participant)

        return

    def reviewers(self):
        """ Returns a generator object of reviewers """
        for reviewer in self.get_data("reviewers"):
            yield User(None, reviewer)

        return

    def comment(self, raw_message):
        """ Commenting the pull request in raw format """
        markupstrings = ["markdown", "creole", "plaintext"]
        if not raw_message:
            raise ValueError("No message set")

        data = {
            "content": {
                "raw": raw_message,
            }
        }

        return self.post("comments", data)

    def approve(self):
        """ Approve a pull request if open """
        self._check_if_open()
        data = {"approved": True}
        return self.post("approve", data)

    def unapprove(self):
        """ Unapporve a pull request if open """
        self._check_if_open()
        return self.delete("approve")

    def merge(self, merge_strategy="merge_commit", close_source_branch=None):
        """
        Merges the pull request if it's open
        :param merge_strategy: string:  Merge strategy (one of "merge_commit", "squash", "fast_forward")
        :param close_source_branch: boolean: Close the source branch after merge, default PR option
        """
        self._check_if_open()
        merge_strategies = ["merge_commit", "squash", "fast_forward"]

        if merge_strategy not in merge_strategies:
            raise ValueError("merge_stragegy must be {}".format(merge_strategies))

        data = {
            "close_source_branch": close_source_branch or self.close_source_branch,
            "merge_strategy": merge_strategy,
        }

        return self.post("merge", data)
