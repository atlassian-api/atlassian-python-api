from ..base import BitbucketCloudBase


class DiffStat(BitbucketCloudBase):
    """
    Bitbucket Cloud repository diffstat entry.

    This represents the changes for one specific file in a diff.

    See https://developer.atlassian.com/cloud/bitbucket/rest/api-group-commits/#api-repositories-workspace-repo-slug-diffstat-spec-get
    """

    MODIFIED = "modified"
    ADDED = "added"
    REMOVED = "removed"
    LOCAL_DELETED = "local deleted"
    REMOTE_DELETED = "remote deleted"
    MERGE_CONFLICT = "merge conflict"
    RENAME_CONFLICT = "rename conflict"
    RENAME_DELETE_CONFLICT = "rename/delete conflict"
    SUBREPO_CONFLICT = "subrepo conflict"

    def __init__(self, data, *args, **kwargs):
        """See BitbucketCloudBase."""
        super(DiffStat, self).__init__(None, None, *args, data=data, expected_type="diffstat", **kwargs)

    @property
    def lines_removed(self):
        """Lines removed."""
        return self.get_data("lines_removed")

    @property
    def lines_added(self):
        """Lines added."""
        return self.get_data("lines_added")

    @property
    def old(self):
        """A CommitFile object, representing a file at a commit in a repository."""
        return CommitFile(self.get_data("old"), **self._new_session_args)

    @property
    def new(self):
        """A CommitFile object, representing a file at a commit in a repository."""
        return CommitFile(self.get_data("new"), **self._new_session_args)

    @property
    def has_conflict(self):
        """True if the change causes a conflict."""
        return str(self.get_data("status")) in [
            self.MERGE_CONFLICT,
            self.RENAME_CONFLICT,
            self.RENAME_DELETE_CONFLICT,
            self.SUBREPO_CONFLICT,
            self.LOCAL_DELETED,
            self.REMOTE_DELETED,
        ]


class CommitFile(BitbucketCloudBase):
    """
    Bitbucket Cloud repository diffstat file.

    File reference from a diffstat entry.

    See https://developer.atlassian.com/cloud/bitbucket/rest/api-group-commits/#api-repositories-workspace-repo-slug-diffstat-spec-get
    """

    def __init__(self, data, *args, **kwargs):
        """See BitbucketCloudBase."""
        if data is None:  # handles add/remove
            data = {
                "path": None,
                "escaped_path": None,
                "links": {},
                "type": "commit_file",
            }
        super(CommitFile, self).__init__(None, None, *args, data=data, expected_type="commit_file", **kwargs)

    @property
    def path(self):
        """The path in the repository."""
        return self.get_data("path")

    @property
    def escaped_path(self):
        """
        The escaped version of the path as it appears in a diff.

        If the path does not require escaping this will be the same as path.
        """
        return self.get_data("escaped_path")
