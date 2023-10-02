# coding=utf-8

from ..base import BitbucketCloudBase
from .diffstat import DiffStat
from ...cloud.repositories.commits import Commit
from ..common.builds import Build
from ..common.comments import Comment
from ..common.users import User, Participant


class PullRequests(BitbucketCloudBase):
    """
    Bitbucket Cloud pull requests
    """

    def __init__(self, url, *args, **kwargs):
        super(PullRequests, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        return PullRequest(data, **self._new_session_args)

    def create(
        self,
        title,
        source_branch,
        destination_branch=None,
        description=None,
        close_source_branch=None,
        reviewers=None,
    ):
        """
        Creates a new pull requests for a given source branch
        Be careful, adding this multiple times for the same source branch updates the pull request!

        :param title: string: pull request title
        :param source_branch: string: name of the source branch
        :param destination_branch: string: name of the destination branch, if None the repository main branch is used
        :param description: string: pull request description
        :param close_source_branch: bool: specifies if the source branch should be closed upon merging
        :param reviewers: list: list of user uuids in curly brackets

        :return: Pull Request Object

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests#post
        """

        rv = [{"uuid": x} for x in reviewers] if reviewers else []
        data = {
            "title": title,
            "source": {"branch": {"name": source_branch}},
            "description": description,
            "close_source_branch": close_source_branch,
            "reviewers": rv,
        }
        if destination_branch:
            data["destination"] = {"branch": {"name": destination_branch}}

        return self.__get_object(self.post(None, data))

    def each(self, q=None, sort=None):
        """
        Returns the list of pull requests in this repository.

        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the PullRequest objects

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests#get
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        for pr in self._get_paged(None, trailing=True, params=params):
            yield self.__get_object(super(PullRequests, self).get(pr.get("id")))

        return

    def get(self, id):
        """
        Returns the pull requests with the requested id in this repository.

        :param id: int: The requested pull request id

        :return: The requested PullRequest object

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D#get
        """
        return self.__get_object(super(PullRequests, self).get(id))


class PullRequest(BitbucketCloudBase):
    """
    Bitbucket Cloud pull request endpoint

    See https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D
    """

    MERGE_COMMIT = "merge_commit"
    MERGE_SQUASH = "squash"
    MERGE_FF = "fast_forward"
    MERGE_STRATEGIES = [
        MERGE_COMMIT,
        MERGE_SQUASH,
        MERGE_FF,
    ]
    STATE_OPEN = "OPEN"
    STATE_DECLINED = "DECLINED"
    STATE_MERGED = "MERGED"
    STATE_SUPERSEDED = "SUPERSEDED"

    def __init__(self, data, *args, **kwargs):
        super(PullRequest, self).__init__(None, *args, data=data, expected_type="pullrequest", **kwargs)

    def _check_if_open(self):
        if not self.is_open:
            raise Exception("Pull Request isn't open")
        return

    @property
    def id(self):
        """unique pull request id"""
        return self.get_data("id")

    @property
    def title(self):
        """pull request title"""
        return self.get_data("title")

    @property
    def description(self):
        """pull request description"""
        return self.get_data("description")

    @property
    def is_declined(self):
        """True if the pull request was declined"""
        return self.get_data("state") == self.STATE_DECLINED

    @property
    def is_merged(self):
        """True if the pull request was merged"""
        return self.get_data("state") == self.STATE_MERGED

    @property
    def is_open(self):
        """True if the pull request is open"""
        return self.get_data("state") == self.STATE_OPEN

    @property
    def is_superseded(self):
        """True if the pull request was superseded"""
        return self.get_data("state") == self.STATE_SUPERSEDED

    @property
    def created_on(self):
        """time of creation"""
        return self.get_time("created_on")

    @property
    def updated_on(self):
        """time of last update"""
        return self.get_time("updated_on")

    @property
    def close_source_branch(self):
        """close source branch flag"""
        return self.get_data("close_source_branch")

    @property
    def source_branch(self):
        """source branch"""
        return self.get_data("source")["branch"]["name"]

    @property
    def destination_branch(self):
        """destination branch"""
        return self.get_data("destination")["branch"]["name"]

    @property
    def source_commit(self):
        """Source commit."""
        return self.get_data("source")["commit"]["hash"]

    @property
    def destination_commit(self):
        """Destination commit."""
        return self.get_data("destination")["commit"]["hash"]

    @property
    def comment_count(self):
        """number of comments"""
        return self.get_data("comment_count")

    @property
    def task_count(self):
        """number of tasks"""
        return self.get_data("task_count")

    @property
    def declined_reason(self):
        """reason for declining"""
        return self.get_data("reason")

    @property
    def author(self):
        """User object of the author"""
        return User(None, self.get_data("author"))

    @property
    def has_conflict(self):
        """Returns True if any of the changes in the PR cause conflicts."""
        for diffstat in self.diffstat():
            if diffstat.has_conflict:
                return True
        return False

    def diffstat(self):
        """
        Returns a generator object of diffstats

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D/diffstat
        """
        for diffstat in self._get_paged("diffstat"):
            yield DiffStat(diffstat, **self._new_session_args)

        return

    def diff(self, encoding="utf-8"):
        """
        Returns PR diff

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D/diff
        """
        return str(self.get("diff", not_json_response=True), encoding=encoding)

    def patch(self, encoding="utf-8"):
        """
        Returns PR patch

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D/patch
        """
        return str(self.get("patch", not_json_response=True), encoding=encoding)

    def statuses(self):
        """
        Returns generator object of the statuses endpoint

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D/statuses
        """
        return self._get_paged("statuses")

    def participants(self):
        """Returns a generator object of participants"""
        for participant in self.get_data("participants"):
            yield Participant(participant, **self._new_session_args)

        return

    def reviewers(self):
        """Returns a generator object of reviewers"""
        for reviewer in self.get_data("reviewers"):
            yield User(None, reviewer, **self._new_session_args)

        return

    def builds(self):
        """Returns the latest Build objects for the pull request."""
        builds = [b for b in self.statuses() if b["type"] == "build"]
        for build in builds:
            yield Build(build, **self._new_session_args)

        return

    def comments(self, q=None, sort=None):
        """
        Returns generator object of the comments endpoint

        :param q: string: Query string to narrow down the response.
        :param sort: string: Name of a response property to sort results.
            See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering
            for details on filtering and sorting.

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D/comments#get
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        for comment in self._get_paged("comments", params=params):
            yield Comment(comment, **self._new_session_args)

    def comment(self, raw_message):
        """
        Commenting the pull request in raw format

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D/comments#post
        """
        if not raw_message:
            raise ValueError("No message set")

        data = {
            "content": {
                "raw": raw_message,
            }
        }

        return self.post("comments", data)

    @property
    def commits(self):
        """Returns generator object for the Commits in the PullRequest"""
        for commit in self._get_paged("commits"):
            yield Commit(commit, **self._new_session_args)

    def tasks(self):
        """
        Returns generator object of the tasks endpoint

        This is feature currently undocumented.
        But confirmed by an Atlassian employee (BCLOUD-16682).
        """
        for task in self._get_paged("tasks"):
            yield Task(task, **self._new_session_args)

    def add_task(self, raw_message):
        """
        Adding a task to the pull request in raw format.

        This is feature currently undocumented.
        But confirmed by an Atlassian employee (BCLOUD-16682).
        """
        if not raw_message:
            raise ValueError("No message set")

        data = {
            "content": {
                "raw": raw_message,
            }
        }

        return Task(self.post("tasks", data), **self._new_session_args)

    def approve(self):
        """
        Approve a pull request if open

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D/approve#post
        """
        self._check_if_open()
        data = {"approved": True}
        return self.post("approve", data)

    def unapprove(self):
        """
        Unapprove a pull request if open

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D/approve#delete
        """
        self._check_if_open()
        return super(BitbucketCloudBase, self).delete("approve")

    def request_changes(self):
        """
        Request changes for the pull request if open

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D/request-changes#post
        """
        self._check_if_open()
        data = {"request-changes": True}
        return self.post("request-changes", data)

    def unrequest_changes(self):
        """
        Unrequest changes for the pull request if open

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D/request-changes#delete
        """
        self._check_if_open()
        return super(BitbucketCloudBase, self).delete("request-changes")

    def decline(self):
        """
        Decline a pull request

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D/decline
        """
        self._check_if_open()
        # decline endpoint needs data, but it's not possible to set a decline reason by api (frontend only)
        data = {"id": self.id}
        return self.post("decline", data)

    def merge(self, merge_strategy=None, close_source_branch=None):
        """
        Merges the pull request if it's open
        :param merge_strategy: string:  Merge strategy (one of PullRequest.MERGE_COMMIT, PullRequest.MERGE_SQUASH, PullRequest.MERGE_FF), if None default merge strategy will be used
        :param close_source_branch: boolean: Close the source branch after merge, default PR option

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D/merge
        """
        self._check_if_open()

        if merge_strategy is not None and merge_strategy not in self.MERGE_STRATEGIES:
            raise ValueError("merge_strategy must be {}".format(self.MERGE_STRATEGIES))

        data = {
            "close_source_branch": close_source_branch or self.close_source_branch,
            "merge_strategy": merge_strategy,
        }

        return self.post("merge", data)


class Task(BitbucketCloudBase):
    STATE_RESOLVED = "RESOLVED"
    STATE_UNRESOLVED = "UNRESOLVED"

    def __init__(self, data, *args, **kwargs):
        super().__init__(None, None, *args, data=data, **kwargs)

    @property
    def id(self):
        """Task id."""
        return self.get_data("id")

    @property
    def description(self):
        """The task description."""
        return self.get_data("content")["raw"]

    @property
    def created_on(self):
        """time of creation"""
        return self.get_time("created_on")

    @property
    def resolved_on(self):
        """resolve timestamp"""
        return self.get_time("resolved_on")

    @property
    def is_resolved(self):
        """True if the task was already resolved."""
        return self.get_data("state") == self.STATE_RESOLVED

    @property
    def creator(self):
        """User object with user information of the task creator"""
        return User(None, self.get_data("creator"), **self._new_session_args)

    @property
    def resolved_by(self):
        """User object with user information of the task resolver"""
        return User(None, self.get_data("resolved_by"), **self._new_session_args)

    def update(self, raw_message):
        """
        Update a task in raw format

        This is feature currently undocumented.
        """
        if not raw_message:
            raise ValueError("No message set")

        data = {
            "content": {
                "raw": raw_message,
            }
        }
        return self._update_data(self.put(None, data=data))

    def delete(self):
        """
        Delete the pullrequest task.

        This is feature currently undocumented.
        """
        return super(Task, self).delete(None)
