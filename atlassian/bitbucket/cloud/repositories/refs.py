# coding=utf-8

from ..base import BitbucketCloudBase
from ..common.users import User


class Refs(BitbucketCloudBase):
    """
    Bitbucket Cloud Refs.

    Generic base object for any type of ref list.
    """

    def __init__(self, url, *args, **kwargs):
        """See BitbucketCloudBase."""
        super(Refs, self).__init__(url, *args, **kwargs)

    def create(
        self,
        name,
        commit,
    ):
        """
        Creates a ref with the given target commit
        :param name: string: name
        :param commit: string: commit hash

        :return: Ref
        """

        data = {"name": name, "target": {"hash": commit}}

        return self._get_object(self.post(None, data))

    def each(self, q=None, sort=None, pagelen=None):
        """
        Returns the list of refs in this repository.

        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param pagelen: int: Name of a response property to change page size.
                             See https://developer.atlassian.com/cloud/bitbucket/rest/intro/#pagination for details.

        :return: A generator for the Ref objects
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        if pagelen is not None:
            params["pagelen"] = pagelen
        for ref in self._get_paged(None, trailing=True, params=params):
            yield self._get_object(super(Refs, self).get(ref.get("name")))

        return

    def get(self, name):
        """
        Returns the Ref with the requested name in the repository.

        :param name: string: The requested name

        :return: The requested Ref object
        """
        return self._get_object(super(Refs, self).get(name))


class Branches(Refs):
    """
    BitBucket Cloud branches endpoint.

    See https://developer.atlassian.com/cloud/bitbucket/rest/api-group-refs/#api-repositories-workspace-repo-slug-refs-branches-get
    """

    def _get_object(self, data):
        return Branch(data, **self._new_session_args)


class Tags(Refs):
    """
    BitBucket Cloud tags endpoint.

    See https://developer.atlassian.com/cloud/bitbucket/rest/api-group-refs/#api-repositories-workspace-repo-slug-refs-tags-get
    """

    def _get_object(self, data):
        return Tag(data, **self._new_session_args)


class Ref(BitbucketCloudBase):
    """
    Base object for individual refs.
    """

    @property
    def name(self):
        """Ref name."""
        return self.get_data("name")

    @property
    def hash(self):
        """Commit hash."""
        return self.get_data("target")["hash"]


class Branch(Ref):
    """
    Bitbucket Cloud branch endpoint.

    See https://developer.atlassian.com/cloud/bitbucket/rest/api-group-refs/#api-repositories-workspace-repo-slug-refs-branches-name-get
    """

    def __init__(self, data, *args, **kwargs):
        """See BitbucketCloudBase."""
        super(Branch, self).__init__(None, *args, data=data, expected_type="branch", **kwargs)

    @property
    def author(self):
        """User object of the author."""
        return User(None, self.get_data("author"))


class Tag(Ref):
    """
    Bitbucket Cloud tags endpoint.

    See https://developer.atlassian.com/cloud/bitbucket/rest/api-group-refs/#api-repositories-workspace-repo-slug-refs-tags-name-get
    """

    def __init__(self, data, *args, **kwargs):
        """See BitbucketCloudBase."""
        super(Tag, self).__init__(None, *args, data=data, expected_type="tag", **kwargs)

    @property
    def author(self):
        """User object of the author."""
        return User(None, self.get_data("tagger"))
