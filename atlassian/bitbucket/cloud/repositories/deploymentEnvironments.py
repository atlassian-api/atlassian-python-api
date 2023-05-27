# coding=utf-8

from ..base import BitbucketCloudBase


class DeploymentEnvironments(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(DeploymentEnvironments, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        return DeploymentEnvironment(
            self.url_joiner(self.url, data["uuid"]),
            data,
            **self._new_session_args,
        )

    def each(self, q=None, sort=None):
        """
        Returns the list of environments in this repository.

        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the DeploymentEnvironment objects

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/environments/#get
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        for deployment_environment in self._get_paged(
            None,
            params=params,
        ):
            yield self.__get_object(deployment_environment)

        return

    def get(self, uuid):
        """
        Returns the environment with the uuid in this repository.

        :param uuid: string: The requested environment uuid

        :return: The requested DeploymentEnvironment objects

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/environments/%7Benvironment_uuid%7D#get
        """
        return self.__get_object(super(DeploymentEnvironments, self).get(uuid))


class DeploymentEnvironment(BitbucketCloudBase):
    def __init__(self, url, data, *args, **kwargs):
        super(DeploymentEnvironment, self).__init__(
            url, *args, data=data, expected_type="deployment_environment", **kwargs
        )

    @property
    def uuid(self):
        """The deployment environment uuid"""
        return self.get_data("uuid")

    @property
    def category(self):
        """The deployment environment category"""
        return self.get_data("category")

    @property
    def deployment_gate_enabled(self):
        """The deployment environment deployment gate enabled"""
        return self.get_data("deployment_gate_enabled")

    @property
    def environment_lock_enabled(self):
        """The deployment environment environment lock enabled"""
        return self.get_data("environment_lock_enabled")

    @property
    def environment_type(self):
        """The deployment environment environment type"""
        return self.get_data("environment_type")

    @property
    def hidden(self):
        """The deployment environment hidden"""
        return self.get_data("hidden")

    @property
    def lock(self):
        """The deployment environment lock"""
        return self.get_data("lock")

    @property
    def name(self):
        """The deployment environment name"""
        return self.get_data("name")

    @property
    def rank(self):
        """The deployment environment rank"""
        return self.get_data("rank")

    @property
    def restrictions(self):
        """The deployment environment restrictions"""
        return self.get_data("restrictions")

    @property
    def slug(self):
        """The deployment environment slug"""
        return self.get_data("slug")

    @property
    def type(self):
        """The deployment environment type"""
        return self.get_data("type")
