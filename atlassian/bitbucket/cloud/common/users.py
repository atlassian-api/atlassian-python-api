from ..base import BitbucketCloudBase


class User(BitbucketCloudBase):
    def __init__(self, url, data, *args, **kwargs):
        super(User, self).__init__(url, *args, data=data, expected_type="user", **kwargs)

    @property
    def display_name(self):
        return str(self.get_data("display_name"))

    @property
    def nickname(self):
        return self.get_data("nickname")

    @property
    def account_id(self):
        return self.get_data("account_id")

    @property
    def uuid(self):
        return self.get_data("uuid")


class Participant(BitbucketCloudBase):
    ROLE_REVIEWER = "REVIEWER"
    ROLE_PARTICIPANT = "PARTICIPANT"
    CHANGES_REQUESTED = "changes_requested"

    def __init__(self, data, *args, **kwargs):
        super(Participant, self).__init__(None, None, *args, data=data, expected_type="participant", **kwargs)

    @property
    def user(self):
        """User object with user information of the participant."""
        return User(None, self.get_data("user"), **self._new_session_args)

    @property
    def is_participant(self):
        """True if the user is a pull request participant."""
        return self.get_data("role") == self.ROLE_PARTICIPANT

    @property
    def is_reviewer(self):
        """True if the user is a pull request reviewer."""
        return self.get_data("role") == self.ROLE_REVIEWER

    @property
    def is_default_reviewer(self):
        """True if the user is a default reviewer."""

    @property
    def has_changes_requested(self):
        """True if user requested changes."""
        return str(self.get_data("state")) == self.CHANGES_REQUESTED

    @property
    def has_approved(self):
        """True if user approved the pull request."""
        return self.get_data("approved")

    @property
    def participated_on(self):
        """Time of last participation."""
        return self.get_time("participated_on")
