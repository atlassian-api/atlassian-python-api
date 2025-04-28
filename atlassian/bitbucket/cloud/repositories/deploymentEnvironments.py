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
            **self._new_session_args
        )  # fmt: skip

    def each(self):
        """
        Returns the list of environments in this repository.

        :return: A list of the DeploymentEnvironment objects

        API docs:
        https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/environments/#get
        """

        # workaround for this issue
        # https://jira.atlassian.com/browse/BCLOUD-20796
        response = super(BitbucketCloudBase, self).get(None)

        deployment_environments = []

        for value in response.get("values", []):
            deployment_environments.append(self.__get_object(value))

        return deployment_environments

    def get(self, uuid):
        """
        Returns the environment with the uuid in this repository.

        :param uuid: string: The requested environment uuid

        :return: The requested DeploymentEnvironment objects

        API docs:
        https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/environments/%7Benvironment_uuid%7D#get
        """
        return self.__get_object(super(DeploymentEnvironments, self).get(uuid))


class DeploymentEnvironment(BitbucketCloudBase):
    def __init__(self, url, data, *args, **kwargs):
        super(DeploymentEnvironment, self).__init__(
            url, *args, data=data, expected_type="deployment_environment", **kwargs
        )
        deployment_environment_url = self.get_deployment_environment_variable_url(self.url)
        self.__deployment_environment_variables = DeploymentEnvironmentVariables(
            f"{deployment_environment_url}/variables", **self._new_session_args
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
        new_path = f"{path[0]}/deployments_config/environments/{path[1]}"
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
            **self._new_session_args
        )  # fmt: skip

    def create(self, key, value, secured):
        """
        Create a new deployment environment variable for the given repository.

        :param key: string: The unique name of the variable.
        :param value: string: The value of the variable. If the variable is secured, this will be empty.
        :param secured: boolean: If true, this variable will be treated as secured. The value will never be exposed in the logs or the REST API.

        :return: The created DeploymentEnvironment object

        API docs:
        https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pipelines/#api-repositories-workspace-repo-slug-deployments-config-environments-environment-uuid-variables-post
        """
        data = {"key": key, "value": value, "secured": secured}
        return self.__get_object(self.post(None, data=data))

    def each(self, pagelen=10):
        """
        Returns the list of deployment environment variables in this repository.

        :param pagelen: integer: Query string to return this number of items from api.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A list of DeploymentEnvironmentVariable objects

        API docs: https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pipelines/#api-repositories-workspace-repo-slug-deployments-config-environments-environment-uuid-variables-get
        """
        params = {"pagelen": pagelen}

        response = super(BitbucketCloudBase, self).get(None, params=params)

        pagelen = response.get("pagelen")
        size_total = response.get("size")
        pagelen_total = response.get("pagelen")
        page = 1

        deployment_environment_variables = []

        # workaround for this issue
        # https://jira.atlassian.com/browse/BCLOUD-20796
        while True:
            for value in response.get("values", []):
                deployment_environment_variables.append(self.__get_object(value))

            if pagelen_total < size_total:
                pagelen_total = pagelen_total + response["pagelen"]
                page += 1
                response = super(BitbucketCloudBase, self).get(None, params={"pagelen": pagelen, "page": page})
            else:
                break

        return deployment_environment_variables


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
        return self._update_data(self.put(f"/{self.uuid}", data=kwargs))

    def delete(self):
        """
        Delete the repository variable.
        :return: The response on success
        API docs: https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pipelines/#api-repositories-workspace-repo-slug-deployments-config-environments-environment-uuid-variables-variable-uuid-delete
        """
        return super(DeploymentEnvironmentVariable, self).delete(f"/{self.uuid}")

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
