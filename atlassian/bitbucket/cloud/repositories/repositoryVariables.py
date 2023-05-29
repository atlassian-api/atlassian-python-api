# coding=utf-8

from ..base import BitbucketCloudBase


class RepositoryVariables(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(RepositoryVariables, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        return RepositoryVariable(
            self.url_joiner(self.url, data["uuid"]),
            data,
            **self._new_session_args,
        )

    def each(self, q=None, sort=None):
        """
        Returns the list of repository variables in this repository.

        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the RepositoryVariable objects

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pipelines_config/variables/#get
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        for pipeline_variable in self._get_paged(
            None,
            trailing=True,
            paging_workaround=True,
            params=params,
        ):
            yield self.__get_object(pipeline_variable)

        return

    def get(self, uuid):
        """
        Returns the pipeline with the uuid in this repository.

        :param uuid: string: The requested pipeline uuid

        :return: The requested RepositoryVariable objects

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pipelines_config/variables/%7Bvariable_uuid%7D#get
        """
        return self.__get_object(super(RepositoryVariables, self).get(uuid))


class RepositoryVariable(BitbucketCloudBase):
    def __init__(self, url, data, *args, **kwargs):
        super(RepositoryVariable, self).__init__(url, *args, data=data, expected_type="pipeline_variable", **kwargs)

    @property
    def uuid(self):
        """The repository variable uuid"""
        return self.get_data("uuid")

    @property
    def key(self):
        """The repository variable key"""
        return self.get_data("key")

    @property
    def scope(self):
        """The repository variable scope"""
        return self.get_data("scope")

    @property
    def secured(self):
        """The repository variable secured"""
        return self.get_data("secured")

    @property
    def system(self):
        """The repository variable system"""
        return self.get_data("system")

    @property
    def type(self):
        """The repository variable type"""
        return self.get_data("type")

    @property
    def value(self):
        """The repository variable value"""
        return self.get_data("value")
