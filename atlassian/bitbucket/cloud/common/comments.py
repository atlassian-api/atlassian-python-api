from ..base import BitbucketCloudBase
from ..common.users import User


class Comment(BitbucketCloudBase):
    def __init__(self, data, *args, **kwargs):
        super(Comment, self).__init__(
            None,
            None,
            *args,
            data=data,
            expected_type="pullrequest_comment",
            **kwargs
        )  # fmt: skip

    @property
    def raw(self):
        """The raw comment."""
        return self.get_data("content")["raw"]

    @property
    def html(self):
        """The html comment."""
        return self.get_data("content")["html"]

    @property
    def markup(self):
        """The markup type."""
        return self.get_data("content")["markup"]

    @property
    def user(self):
        """User object with user information of the comment."""
        return User(None, self.get_data("user"), **self._new_session_args)

    def update(self, **kwargs):
        """Update the comment properties. Fields not present in the request body are ignored.

        :param kwargs: dict: The data to update.

        :return: The updated comment
        """
        return self._update_data(self.put(None, data=kwargs))

    def delete(self):
        """Delete the comment.

        :return: The response on success
        """
        return super(Comment, self).delete(None)
