from ..base import BitbucketCloudBase
from datetime import datetime


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

    def delete(self):
        """
        Deletes the default reviewer
        """
        data = super(User, self).delete(None)
        if "errors" in data:
            return
        return User(self.url, data, **self._new_session_args)


class Participant(BitbucketCloudBase):
    def __init__(self, data, *args, **kwargs):
        super(Participant, self).__init__(None, None, *args, data=data, expected_type="participant", **kwargs)

    @property
    def user(self):
        """ User object with user information of the participant """
        return User(None, self.get_data("user"))

    @property
    def is_participant(self):
        """ True if the user is a pull request participant """
        return self.get_data("role") == "PARTICIPANT"

    @property
    def is_reviewer(self):
        """ True if the user is a pull request reviewer """
        return self.get_data("role") == "REVIEWER"

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
