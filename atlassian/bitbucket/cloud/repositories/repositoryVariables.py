# coding=utf-8
from ..base import BitbucketCloudBase


class RepositoryVariables(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(RepositoryVariables, self).__init__(url, *args, **kwargs)

    def __get_object(self, data) -> "RepositoryVariable":
        return RepositoryVariable(
            self.url_joiner(self.url, data["uuid"]),
            data,
            **self._new_session_args
        )  # fmt: skip

    def create(self, key, value, secured):
        """
        Create a new repository variable for the given repository.

        :param key: string: The unique name of the variable.
        :param value: string: The value of the variable. If the variable is secured, this will be empty.
        :param secured: boolean: If true, this variable will be treated as secured. The value will never be exposed in the logs or the REST API.

        :return: The created RepositoryVariable object

        API docs: https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pipelines/#api-repositories-workspace-repo-slug-pipelines-config-variables-post
        """
        data = {
            "key": key,
            "value": value,
            "secured": secured,
        }
        return self.__get_object(self.post(None, data=data))

    def each(self, q=None, sort=None):
        """
        Returns the list of repository variables in this repository.

        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the RepositoryVariable objects

        API docs: https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pipelines/#api-repositories-workspace-repo-slug-pipelines-config-variables-get
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

    def get(self, uuid: str):  # type: ignore[override]
        """
        Returns the pipeline with the uuid in this repository.

        :param uuid: string: The requested pipeline uuid

        :return: The requested RepositoryVariable objects

        API docs: https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pipelines/#api-repositories-workspace-repo-slug-pipelines-config-variables-variable-uuid-get
        """
        return self.__get_object(super(RepositoryVariables, self).get(uuid))


class RepositoryVariable(BitbucketCloudBase):
    def __init__(self, url, data, *args, **kwargs):
        super(RepositoryVariable, self).__init__(url, *args, data=data, expected_type="pipeline_variable", **kwargs)

    def update(self, **kwargs):
        """
        Update the repository variable properties. Fields not present in the request body are ignored.

        :param kwargs: dict: The data to update.

        :return: The updated repository variable

        API docs: https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pipelines/#api-repositories-workspace-repo-slug-pipelines-config-variables-variable-uuid-put
        """
        return self._update_data(self.put(None, data=kwargs))

    def delete(self):
        """
        Delete the repository variable.

        :return: The response on success

        API docs: https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pipelines/#api-repositories-workspace-repo-slug-pipelines-config-variables-variable-uuid-delete
        """
        return super(RepositoryVariable, self).delete(None)

    @property
    def uuid(self):
        """The repository variable uuid"""
        return self.get_data("uuid")

    @property
    def key(self):
        """The repository variable key"""
        return self.get_data("key")

    @key.setter
    def key(self, key):
        """Setter for the repository variable is key"""
        return self.update(key=key)

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

    @value.setter
    def value(self, value):
        """Setter for the repository variable value"""
        return self.update(value=value)
