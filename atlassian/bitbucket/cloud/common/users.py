from ..base import BitbucketCloudBase


class User(BitbucketCloudBase):
    def __init__(self, url, data, *args, **kwargs):
        super(User, self).__init__(url, *args, data=data, expected_type="user", **kwargs)

    @property
    def display_name(self):
        """ Display name used by Bitbucket Cloud """
        return str(self.get_data("display_name"))

    @property
    def nickname(self):
        """ Username used by Bitbucket Cloud """
        return self.get_data("nickname")

    @property
    def account_id(self):
        """ Account id used by Bitbucket Cloud """
        return self.get_data("account_id")

    @property
    def uuid(self):
        """ User id used by Bitbucket Cloud """
        return self.get_data("uuid")

    @property
    def avatar(self):
        """ URL to user avatar on Bitbucket Cloud """
        return self.get_data("links")["avatar"]["href"]
