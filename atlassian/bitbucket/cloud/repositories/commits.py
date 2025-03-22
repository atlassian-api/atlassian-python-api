# coding=utf-8

from ..base import BitbucketCloudBase
from ..common.builds import Build
from ..common.comments import Comment
from ..common.users import Participant, User


class Commits(BitbucketCloudBase):
    """Bitbucket Cloud commits."""

    def __init__(self, url, *args, **kwargs):
        super(Commits, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        return Commit(data, **self._new_session_args)

    def each(self, top=None, q=None, sort=None):
        """
        Return the list of commits in this repository.

        :param top: string: Hash of commit to get the history for.
        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the Commit objects

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-commits/#api-repositories-workspace-repo-slug-commits-get
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        trailing = True
        if top is not None:
            trailing = False
        for commit in self._get_paged(top, trailing=trailing, params=params):
            yield self.__get_object(commit)

    def get(self, commit_hash):
        """
        Return the commit with the requested commit id in this repository.

        :param commit_hash: str: The requested commit id

        :return: The requested Commit object

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-commits/#api-repositories-workspace-repo-slug-commit-commit-get
        """
        return self.__get_object(
            super(Commits, self).get(
                self.url_joiner(self.get_link("commit"), commit_hash),
                absolute=True,
            )
        )


class Commit(BitbucketCloudBase):
    """
    Bitbucket Cloud commit endpoint.

    See
    https://developer.atlassian.com/cloud/bitbucket/rest/api-group-commits/#api-repositories-workspace-repo-slug-commit-commit-get
    """

    def __init__(self, data, *args, **kwargs):
        super(Commit, self).__init__(None, *args, data=data, expected_type="commit", **kwargs)

    @property
    def hash(self):
        """Commit id."""
        return self.get_data("hash")

    @property
    def message(self):
        """Commit message."""
        return self.get_data("message")

    @property
    def date(self):
        """Commit date."""
        return self.get_time("date")

    @property
    def author(self):
        """User object of the author."""
        return User(None, self.get_data("author").get("user"))

    def parents(self):
        """Return a generator object of parent commits."""
        for commit in self.get_data("parents"):
            yield Commit(commit, **self._new_session_args)

    def statuses(self):
        """
        Return generator object of the status's endpoint.
        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-commit-statuses/#api-repositories-workspace-repo-slug-commit-commit-statuses-get
        """
        return self._get_paged("statuses")

    def participants(self):
        """Return a generator object of participants."""
        for participant in self.get_data("participants"):
            yield Participant(participant, **self._new_session_args)

    def builds(self):
        """Return the Build objects for the commit."""
        builds = [b for b in self.statuses() if b["type"] == "build"]
        for build in builds:
            yield Build(build, **self._new_session_args)

    def add_build(
        self,
        key,
        url=None,
        description=None,
        refname=None,
        state=Build.STATE_INPROGRESS,
    ):
        """
        Add new build status to commit.

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-commit-statuses/#api-repositories-workspace-repo-slug-commit-commit-statuses-build-post
        """
        data = {
            "key": key,
            "state": state,
            "description": description,
            "url": url,
            "refname": refname,
        }

        return self.post("statuses/build", data)

    def get_build(self, key):
        """
        Return a specific build for the commit.

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-commit-statuses/#api-repositories-workspace-repo-slug-commit-commit-statuses-build-key-get
        """
        return Build(
            super(Commit, self).get(self.url_joiner("statuses/build", key)),
            **self._new_session_args
        )  # fmt: skip

    def comments(self):
        """
        Return generator object endpoint of the comment.
        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-commits/#api-repositories-workspace-repo-slug-commit-commit-comments-get
        """
        for comment in self._get_paged("comments"):
            yield Comment(comment, **self._new_session_args)

    def comment(self, raw_message):
        """
        Add a comment to the pull request in raw format.

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-commits/#api-repositories-workspace-repo-slug-commit-commit-comments-post
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
        Approve a commit.

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-commits/#api-repositories-workspace-repo-slug-commit-commit-approve-post
        """
        data = {"approved": True}
        return self.post("approve", data)

    def unapprove(self):
        """
        Unapprove a commit.

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-commits/#api-repositories-workspace-repo-slug-commit-commit-approve-delete
        """
        return super(BitbucketCloudBase, self).delete("approve")

    def get_pull_requests(self, start=0, pagelen=0):
        """
        Retrieves pull requests associated with the current commit.

        Pull Request Commit Links app must be installed first before using this API;
        installation automatically occurs when 'Go to pull request' is clicked
        from the web interface for a commit's details.

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pullrequests/#api-repositories-workspace-repo-slug-commit-commit-pullrequests-get

        :param start: int, OPTIONAL: The starting page of pull requests to retrieve. Defaults to 0.
        :param pagelen: int, OPTIONAL: The number of pull requests to retrieve per page. Defaults to 0.
        :return: Generator[PullRequest]: A generator that yields `PullRequest` objects.
        """
        # NOTE: Import moved inside the method to avoid circular import issues
        from ...cloud.repositories.pullRequests import PullRequest

        params = {}
        if start:
            params["page"] = start
        if pagelen:
            params["pagelen"] = pagelen

        for pull_request in self._get_paged(url="pullrequests", params=params):
            yield PullRequest(pull_request, **self._new_session_args)
