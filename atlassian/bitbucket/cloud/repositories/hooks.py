# coding=utf-8

from ..base import BitbucketCloudBase


class Hooks(BitbucketCloudBase):
    """Bitbucket Cloud webhooks."""

    def __init__(self, url, *args, **kwargs):
        super(Hooks, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        return Hook(data, **self._new_session_args)

    def create(
        self,
        url,
        description,
        events,
        active=True,
    ):
        """
        Creates a new webhook for the current repository

        param: url: string: Url that will receive event requests
        param: description: string: Details about the webhook
        param: events: [string] List of event types that requests will generate for
        param: active: boolean: Enables/Disables the webhook

        :return: Hook Object
        """

        data = {"url": url, "description": description, "active": active, "events": events}

        return self.__get_object(self.post(None, data))

    def each(self):
        """
        Return the list of webhooks in this repository.

        :return: A generator for the Webhook objects
        """
        for hook in self._get_paged(None):
            yield self.__get_object(hook)

    def get(self, id):
        """
        Return the hook with the requested hook uuid in this repository.

        :param id: string: The id of the webhook

        :return: The requested hook object
        """
        return self.__get_object(
            super(Hooks, self).get(
                self.url_joiner(self.get_link("hooks"), id),
                absolute=True,
            )
        )


class Hook(BitbucketCloudBase):
    """
    Bitbucket Cloud hook endpoint.
    """

    def __init__(self, data, *args, **kwargs):
        super(Hook, self).__init__(None, *args, data=data, expected_type="webhook_subscription", **kwargs)

    def uuid(self):
        """hook uuid."""
        return self.get_data("uuid")

    def webhook_url(self):
        """webhook url."""
        return self.get_data("url")

    def description(self):
        """webhook description."""
        return self.get_data("description")

    def active(self):
        """is webhook active?"""
        return self.get_data("active")

    def events(self):
        """events that the webhook is triggered by"""
        return self.get_data("events")

    def update(self, **kwargs):
        """
        Update a webhook

        Valid keywords:
        param: url: string: Url that will receive event requests
        param: description: string: Details about the webhook
        param: events: [string] List of event types that requests will generate for
        param: active: boolean: Enables/Disables the webhook
        """

        payload = {
            "url": self.webhook_url(),
            "description": self.description(),
            "events": self.events(),
            "active": self.active(),
        }

        for key in payload.keys() and kwargs.keys():
            payload[key] = kwargs[key]

        return self._update_data(self.put(None, data=payload))

    def delete(self):
        """
        Delete the webhook.
        """
        return super(Hook, self).delete(None)
