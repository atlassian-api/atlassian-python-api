# coding=utf-8

from ..base import BitbucketCloudBase

from urllib.parse import urlunsplit, urlsplit


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
        deployment_environment_url = self.get_deployment_environment_variable_url(self.url)
        self.__deployment_environment_variables = DeploymentEnvironmentVariables(
            "{}/variables".format(deployment_environment_url), **self._new_session_args
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

    @property
    def deployment_environment_variables(self):
        """The deployment environment variables"""
        return self.__deployment_environment_variables

    def get_deployment_environment_variable_url(self, url):
        parsed_url = urlsplit(url)
        path = parsed_url.path.split("/environments/")
        new_path = "{}/deployments_config/environments/{}".format(path[0], path[1])
        list_parsed_url = list(parsed_url[:])
        list_parsed_url[2] = new_path
        return urlunsplit(tuple(list_parsed_url))


class DeploymentEnvironmentVariables(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(DeploymentEnvironmentVariables, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        return DeploymentEnvironmentVariable(
            self.url,
            data,
            **self._new_session_args,
        )

    def create(self, key, value, secured):
        """
        Create a new deployment environment variable for the given repository.

        :param key: string: The unique name of the variable.
        :param value: string: The value of the variable. If the variable is secured, this will be empty.
        :param secured: boolean: If true, this variable will be treated as secured. The value will never be exposed in the logs or the REST API.

        :return: The created DeploymentEnvironment object

        API docs: https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pipelines/#api-repositories-workspace-repo-slug-deployments-config-environments-environment-uuid-variables-post
        """
        data = {"key": key, "value": value, "secured": secured}
        return self.__get_object(self.post(None, data=data))

    def each(self, q=None, sort=None):
        """
        Returns the list of deployment environment variables in this repository.

        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the DeploymentEnvironmentVariable objects

        API docs: https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pipelines/#api-repositories-workspace-repo-slug-deployments-config-environments-environment-uuid-variables-get
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        for deployment_environment_variable in self._get_paged(
            None,
            params=params,
        ):
            yield self.__get_object(deployment_environment_variable)

        return


class DeploymentEnvironmentVariable(BitbucketCloudBase):
    def __init__(self, url, data, *args, **kwargs):
        # This is needed when creating a new environment variable
        # since the API doesn't return a 'type'.
        if data.get("type") is None:
            data["type"] = "pipeline_variable"

        super(DeploymentEnvironmentVariable, self).__init__(
            url, *args, data=data, expected_type="pipeline_variable", **kwargs
        )

    def update(self, **kwargs):
        """
        Update the repository variable properties. Fields not present in the request body are ignored.

        :param kwargs: dict: The data to update.

        :return: The updated repository variable

        API docs: https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pipelines/#api-repositories-workspace-repo-slug-deployments-config-environments-environment-uuid-variables-variable-uuid-put
        """
        return self._update_data(self.put("/{}".format(self.uuid), data=kwargs))

    def delete(self):
        """
        Delete the repository variable.

        :return: The response on success

        API docs: https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pipelines/#api-repositories-workspace-repo-slug-deployments-config-environments-environment-uuid-variables-variable-uuid-delete
        """
        return super(DeploymentEnvironmentVariable, self).delete("/{}".format(self.uuid))

    @property
    def uuid(self):
        """The deployment environment variable uuid"""
        return self.get_data("uuid")

    @property
    def key(self):
        """The deployment environment variable key"""
        return self.get_data("key")

    @key.setter
    def key(self, key):
        """Setter for the deployment environment variable key"""
        return self.update(key=key)

    @property
    def secured(self):
        """The deployment environment variable is secured"""
        return self.get_data("secured")

    @property
    def type(self):
        """The deployment environment variable type"""
        return self.get_data("type")

    @property
    def value(self):
        """The deployment environment variable value"""
        return self.get_data("value")

    @value.setter
    def value(self, value):
        """Setter for the deployment environment variable value"""
        return self.update(value=value)
