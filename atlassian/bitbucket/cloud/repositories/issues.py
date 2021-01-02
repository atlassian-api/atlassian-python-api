# coding=utf-8

from ..base import BitbucketCloudBase


class Issues(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(Issues, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        return Issue(data, **self._new_session_args)

    def create(self, title, description, kind, priority):
        """
        Create a new issue in the issue tracker of the given repository.

        :param title: string: The title of the issue
        :param description: string: The description of the issue
        :param kind: string: One of: bug, enhancement, proposal, task
        :param priority: string: One of: trivial, minor, major, critical, blocker

        :return: The created Issue object

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/issues/%7Bissue_id%7D#put
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

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/issues#get
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

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/issues/%7Bissue_id%7D#get
        """
        return self.__get_object(super(Issues, self).get(id))


class Issue(BitbucketCloudBase):
    def __init__(self, data, *args, **kwargs):
        super(Issue, self).__init__(None, *args, data=data, expected_type="issue", **kwargs)

    def update(self, **kwargs):
        """
        Update the issue properties. Fields not present in the request body are ignored.

        :param kwargs: dict: The data to update.

        :return: The updated issue

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/issues/%7Bissue_id%7D#put
        """
        return self._update_data(self.put(None, data=kwargs))

    def delete(self):
        """
        Delete the issue.

        :return: The response on success

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/issues/%7Bissue_id%7D#delete
        """
        return super(Issue, self).delete(None)

    @property
    def id(self):
        """ The issue id """
        return self.get_data("id")

    @property
    def title(self):
        """ The issue title """
        return self.get_data("title")

    @title.setter
    def title(self, title):
        """ Setter for the issue title """
        return self.update(title=title)

    @property
    def state(self):
        """ The issue state """
        return self.get_data("state")

    @state.setter
    def state(self, state):
        """ Setter for the issue state """
        return self.update(state=state)

    @property
    def kind(self):
        """ The issue kind """
        return self.get_data("kind")

    @kind.setter
    def kind(self, kind):
        """ Setter for the issue kind """
        return self.update(kind=kind)

    @property
    def priority(self):
        """ The issue priority """
        return self.get_data("priority")

    @priority.setter
    def priority(self, priority):
        """ Setter for the issue property """
        return self.update(priority=priority)

    @property
    def votes(self):
        """ The issue votes """
        return self.get_data("votes")

    @property
    def content(self):
        """ The issue content """
        return self.get_data("content")

    @property
    def created_on(self):
        """ The issue creation time """
        return self.get_time("created_on")

    @property
    def edited_on(self):
        """ The issue edit time """
        return self.get_time("edited_on")

    @property
    def updated_on(self):
        """ The issue last update time """
        return self.get_time("updated_on")
