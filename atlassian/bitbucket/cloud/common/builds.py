from ..base import BitbucketCloudBase


class Build(BitbucketCloudBase):
    STATE_FAILED = "FAILED"
    STATE_INPROGRESS = "INPROGRESS"
    STATE_STOPPED = "STOPPED"
    STATE_SUCCESSFUL = "SUCCESSFUL"

    def __init__(self, data, *args, **kwargs):
        super(Build, self).__init__(None, None, *args, data=data, expected_type="build", **kwargs)

    @property
    def key(self):
        """Key of the build."""
        return self.get_data("key")

    @property
    def name(self):
        """Name of the build."""
        return self.get_data("name")

    @property
    def description(self):
        """Build description."""
        return self.get_data("description")

    @property
    def failed(self):
        """True if the build failed."""
        return self.get_data("state") == self.STATE_FAILED

    @property
    def inprogress(self):
        """True if the build is in progress."""
        return self.get_data("state") == self.STATE_INPROGRESS

    @property
    def successful(self):
        """True if the build was successful."""
        return self.get_data("state") == self.STATE_SUCCESSFUL

    @property
    def stopped(self):
        """True if the build was stopped."""
        return self.get_data("state") == self.STATE_STOPPED

    @property
    def created_on(self):
        """Time of creation."""
        return self.get_time("created_on")

    @property
    def updated_on(self):
        """Time of last update."""
        return self.get_time("updated_on")

    @property
    def commit(self):
        """Return the hash key of the commit."""
        return self.get_data("commit")["hash"]

    @property
    def website(self):
        """
        Return the url to the build's webpage.
        This url points to the build's frontend website (Pipelines, Jenkins ...)
        """
        return self.get_data("url")

    @property
    def refname(self):
        """Return the refname.

        This can be used to indicate on which branch/tag the
        build happened.
        """
        return self.get_data("refname")

    def update(self, **kwargs):
        """Update build status.

        See
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-commit-statuses/#api-repositories-workspace-repo-slug-commit-commit-statuses-build-key-put
        """
        return self._update_data(self.put(None, data=kwargs))
