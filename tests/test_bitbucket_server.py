from unittest import TestCase

from atlassian.bitbucket import Bitbucket

from .mockup import mockup_server


class TestWebhook(TestCase):
    def setUp(self):
        self.bitbucket = Bitbucket(
            "{}/bitbucket/server".format(mockup_server()), username="username", password="password"
        )
        self.project_key = "PRJ"
        self.repository_slug = "my-repo1-slug"
        self.webhook_id = 3
        self.fake_webhooks = [
            {
                "project_key": self.project_key,
                "repository_slug": self.repository_slug,
                "name": "fake_name_1",
                "events": ["repo:refs_changed", "pr:merged", "pr:opened"],
                "url": "https://example1.com",
                "active": True,
                "secret": "fake_secret_1",
            },
            {
                "project_key": self.project_key,
                "repository_slug": self.repository_slug,
                "name": "fake_name_2",
                "events": ["repo:refs_changed", "pr:merged", "pr:opened"],
                "url": "https://example2.com",
                "active": False,
                "secret": None,
            },
        ]

    def test_get_webhooks(self):
        webhooks = self.bitbucket.get_webhooks(
            self.project_key,
            self.repository_slug,
        )
        for webhook, fake_webhook in zip(webhooks, self.fake_webhooks):
            self.assertEqual(webhook["name"], fake_webhook["name"])
            self.assertEqual(webhook["events"], fake_webhook["events"])

            if fake_webhook["secret"] is None:
                self.assertEqual(webhook["configuration"], {})
            else:
                self.assertEqual(webhook["configuration"]["secret"], fake_webhook["secret"])

            self.assertEqual(webhook["url"], fake_webhook["url"])
            self.assertEqual(webhook["active"], fake_webhook["active"])

    def test_create_webhook(self):
        webhook = self.bitbucket.create_webhook(
            self.fake_webhooks[0]["project_key"],
            self.fake_webhooks[0]["repository_slug"],
            self.fake_webhooks[0]["name"],
            self.fake_webhooks[0]["events"],
            self.fake_webhooks[0]["url"],
            self.fake_webhooks[0]["active"],
            self.fake_webhooks[0]["secret"],
        )
        self.assertEqual(webhook["name"], self.fake_webhooks[0]["name"])
        self.assertEqual(webhook["events"], self.fake_webhooks[0]["events"])
        self.assertEqual(webhook["configuration"]["secret"], self.fake_webhooks[0]["secret"])
        self.assertEqual(webhook["url"], self.fake_webhooks[0]["url"])
        self.assertEqual(webhook["active"], self.fake_webhooks[0]["active"])

    def test_get_webhook(self):
        webhook = self.bitbucket.get_webhook(
            self.fake_webhooks[0]["project_key"], self.fake_webhooks[0]["repository_slug"], self.webhook_id
        )
        self.assertEqual(webhook["name"], self.fake_webhooks[0]["name"])
        self.assertEqual(webhook["events"], self.fake_webhooks[0]["events"])
        self.assertEqual(webhook["configuration"]["secret"], self.fake_webhooks[0]["secret"])
        self.assertEqual(webhook["url"], self.fake_webhooks[0]["url"])
        self.assertEqual(webhook["active"], self.fake_webhooks[0]["active"])

    def test_update_webhook(self):
        params = {"events": ["repo:refs_changed"], "url": "https://example1-updated.com"}
        webhook = self.bitbucket.update_webhook(
            self.fake_webhooks[0]["project_key"], self.fake_webhooks[0]["repository_slug"], self.webhook_id, **params
        )
        self.assertEqual(webhook["name"], self.fake_webhooks[0]["name"])
        self.assertEqual(webhook["events"], params["events"])
        self.assertEqual(webhook["configuration"]["secret"], self.fake_webhooks[0]["secret"])
        self.assertEqual(webhook["url"], params["url"])
        self.assertEqual(webhook["active"], self.fake_webhooks[0]["active"])

    def test_delete_webhook(self):
        webhook = self.bitbucket.delete_webhook(
            self.fake_webhooks[0]["project_key"], self.fake_webhooks[0]["repository_slug"], self.webhook_id
        )
        self.assertIsNone(webhook, "Delete response is not None")
