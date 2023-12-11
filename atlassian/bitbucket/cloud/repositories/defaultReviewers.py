# coding=utf-8

from requests import HTTPError

from ..base import BitbucketCloudBase
from ..common.users import User


class DefaultReviewers(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(DefaultReviewers, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        return DefaultReviewer(
            self.url_joiner(self.url, data["uuid"]),
            data,
            **self._new_session_args
        )  # fmt: skip

    def add(self, user):
        """
        Adds the specified user to the repository's list of default reviewers.

        This method is idempotent. Adding a user a second time has no effect.

        :param user: string: The user to add

        :return: The added DefaultReviewer object

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/default-reviewers/%7Btarget_username%7D#put
        """
        # the mention_id parameter is undocumented but if missed, leads to 400 statuses
        return self.__get_object(self.put(user, data={"mention_id": user}))

    def each(self, q=None, sort=None):
        """
        Returns the repository's default reviewers.
        These are the users that are automatically added as reviewers on every new pull request
        that is created.

        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the DefaultReviewer objects

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/default-reviewers#get
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        for default_reviewer in self._get_paged(None, params=params):
            yield self.__get_object(default_reviewer)

        return

    def get(self, user):
        """
        Returns the default reviewer in this repository.

        :param user: string: The requested username

        :return: The requested DefaultReviewer object, None if not a default reviewer

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/default-reviewers/%7Btarget_username%7D#get
        """
        default_reviewer = None
        try:
            default_reviewer = self.__get_object(super(DefaultReviewers, self).get(user))
        except HTTPError as e:
            # A 404 indicates that the specified user is not a default reviewer.
            if not e.response.status_code == 404:
                # Rethrow the exception
                raise

        return default_reviewer


class DefaultReviewer(User):
    def __init__(self, url, data, *args, **kwargs):
        super(DefaultReviewer, self).__init__(url, data, *args, **kwargs)

    def delete(self):
        """
        Delete the default reviewer.

        :return: The response on success

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/default-reviewers/%7Btarget_username%7D#delete
        """
        return super(DefaultReviewer, self).delete(None)
