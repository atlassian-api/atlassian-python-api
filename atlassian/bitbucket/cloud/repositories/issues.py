# coding=utf-8

from ..base import BitbucketCloudBase


class Issues(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(Issues, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        if "errors" in data:
            return
        return Issue(data, **self._new_session_args)

    def create(self, title, description, kind, priority):
        """
        Create a new issue in the issue tracker of the given repository.

        :param title: string: The title of the issue
        :param description: string: The description of the issue
        :param kind: string: One of: bug, enhancement, proposal, task
        :param priority: string: One of: trivial, minor, major, critical, blocker

        :return: The created Issue object
        """
        data = {
            "title": title,
            "kind": kind,
            "priority": priority,
            "content": {"raw": description},
        }
        return self.__get_object(self.post(None, data=data))

    def each(self, q=None, sort=None):
        """
        Returns the list of issues in this repository.

        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the Issue objects
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        for issue in self._get_paged(None, params=params):
            yield self.__get_object(issue)

        return

    def get(self, id):
        """
        Returns the issue with the ID in this repository.

        :param id: string: The requested issue ID

        :return: The requested Issue objects
        """
        return self.__get_object(super(Issues, self).get(id))


class Issue(BitbucketCloudBase):
    def __init__(self, data, *args, **kwargs):
        super(Issue, self).__init__(None, *args, data=data, expected_type="issue", **kwargs)

    @property
    def id(self):
        return self.get_data("id")

    @property
    def title(self):
        return self.get_data("title")

    @title.setter
    def title(self, title):
        return self.update(title=title)

    @property
    def state(self):
        return self.get_data("state")

    @state.setter
    def state(self, state):
        return self.update(state=state)

    @property
    def kind(self):
        return self.get_data("kind")

    @kind.setter
    def kind(self, kind):
        return self.update(kind=kind)

    @property
    def priority(self):
        return self.get_data("priority")

    @priority.setter
    def priority(self, priority):
        return self.update(priority=priority)

    @property
    def votes(self):
        return self.get_data("votes")

    @property
    def content(self):
        return self.get_data("content")

    @property
    def created_on(self):
        return self.get_data("created_on")

    @property
    def edited_on(self):
        return self.get_data("edited_on", "never edited")

    @property
    def updated_on(self):
        return self.get_data("updated_on", "never updated")

    def delete(self):
        """
        Deletes the issue
        """
        data = super(Issue, self).delete(None)
        if "errors" in data:
            return
        return Issue(data, **self._new_session_args)
