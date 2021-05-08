# coding=utf-8

from ..base import BitbucketCloudBase
from ..common.users import User


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
            yield self.__get_object(pr)

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

    def comments(self):
        """
        Returns generator object of the comments endpoint

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D/comments#get
        """
        for comment in self._get_paged("comments"):
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


class Participant(BitbucketCloudBase):
    ROLE_REVIEWER = "REVIEWER"
    ROLE_PARTICIPANT = "PARTICIPANT"
    CHANGES_REQUESTED = "changes_requested"

    def __init__(self, data, *args, **kwargs):
        super(Participant, self).__init__(None, None, *args, data=data, expected_type="participant", **kwargs)

    @property
    def user(self):
        """User object with user information of the participant"""
        return User(None, self.get_data("user"), **self._new_session_args)

    @property
    def is_participant(self):
        """True if the user is a pull request participant"""
        return self.get_data("role") == self.ROLE_PARTICIPANT

    @property
    def is_reviewer(self):
        """True if the user is a pull request reviewer"""
        return self.get_data("role") == self.ROLE_REVIEWER

    @property
    def is_default_reviewer(self):
        """True if the user is a default reviewer"""

    @property
    def has_changes_requested(self):
        """True if user requested changes"""
        return str(self.get_data("state")) == self.CHANGES_REQUESTED

    @property
    def has_approved(self):
        """True if user approved the pull request"""
        return self.get_data("approved")

    @property
    def participated_on(self):
        """time of last participation"""
        return self.get_time("participated_on")


class Comment(BitbucketCloudBase):
    def __init__(self, data, *args, **kwargs):
        super(Comment, self).__init__(None, None, *args, data=data, expected_type="pullrequest_comment", **kwargs)

    @property
    def raw(self):
        """The raw comment"""
        return self.get_data("content")["raw"]

    @property
    def html(self):
        """The html comment"""
        return self.get_data("content")["html"]

    @property
    def markup(self):
        """The markup type"""
        return self.get_data("content")["markup"]

    @property
    def user(self):
        """User object with user information of the comment"""
        return User(None, self.get_data("user"), **self._new_session_args)

    def update(self, **kwargs):
        """
        Update the pullrequest properties. Fields not present in the request body are ignored.

        :param kwargs: dict: The data to update.

        :return: The updated repository

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D/comments/%7Bcomment_id%7D#put
        """
        return self._update_data(self.put(None, data=kwargs))

    def delete(self):
        """
        Delete the pullrequest comment.

        :return: The response on success

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D/comments/%7Bcomment_id%7D#delete
        """
        return super(Comment, self).delete(None)


class Build(BitbucketCloudBase):
    STATE_FAILED = "FAILED"
    STATE_INPROGRESS = "INPROGRESS"
    STATE_STOPPED = "STOPPED"
    STATE_SUCCESSFUL = "SUCCESSFUL"

    def __init__(self, data, *args, **kwargs):
        super(Build, self).__init__(None, None, *args, data=data, expected_type="build", **kwargs)

    @property
    def key(self):
        """Key of the build"""
        return self.get_data("key")

    @property
    def name(self):
        """Name of the build"""
        return self.get_data("name")

    @property
    def description(self):
        """Build description"""
        return self.get_data("description")

    @property
    def failed(self):
        """True if the build was stopped"""
        return self.get_data("state") == self.STATE_FAILED

    @property
    def inprogress(self):
        """True if the build is inprogress"""
        return self.get_data("state") == self.STATE_INPROGRESS

    @property
    def successful(self):
        """True if the build was successful"""
        return self.get_data("state") == self.STATE_SUCCESSFUL

    @property
    def stopped(self):
        """True if the build was stopped"""
        return self.get_data("state") == self.STATE_STOPPED

    @property
    def created_on(self):
        """time of creation"""
        return self.get_time("created_on")

    @property
    def updated_on(self):
        """time of last update"""
        return self.get_time("updated_on")

    @property
    def commit(self):
        """Returns the hash key of the commit"""
        return self.get_data("commit")["hash"]

    @property
    def website(self):
        """Returns the url to the builds webpage.
        This url points to the build's frontend website (Pipelines, Jenkins ...)
        """
        return self.get_data("url")

    @property
    def refname(self):
        """Returns the refname"""
        return self.get_data("refname")
