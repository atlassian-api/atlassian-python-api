from unittest import TestCase
from unittest.mock import patch

from atlassian.bitbucket import Bitbucket

from .mockup import mockup_server


class TestWebhook(TestCase):
    def setUp(self):
        self.bitbucket = Bitbucket(f"{mockup_server()}/bitbucket/server", username="username", password="password")
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


class TestHookScripts(TestCase):
    def setUp(self):
        self.bitbucket = Bitbucket("https://bitbucket.example.com", username="admin", password="password")

    @patch.object(Bitbucket, "post")
    def test_create_hook_script_uses_multipart_latest_endpoint(self, mock_post):
        script = b"#!/bin/sh\necho hook\n"
        mock_post.return_value = {"id": 12}

        result = self.bitbucket.create_hook_script(script, "Audit pushes", "POST", "Audit every push")

        self.assertEqual(result, {"id": 12})
        files = mock_post.call_args.kwargs["files"]
        self.assertEqual(files["content"], ("hook-script", script, "application/octet-stream"))
        self.assertEqual(files["name"], (None, "Audit pushes"))
        self.assertEqual(files["type"], (None, "POST"))
        self.assertEqual(files["description"], (None, "Audit every push"))
        self.assertEqual(mock_post.call_args.args[0], "rest/api/latest/hook-scripts")
        self.assertEqual(mock_post.call_args.kwargs["headers"], self.bitbucket.no_check_headers)

    def test_create_hook_script_rejects_unknown_hook_type(self):
        with self.assertRaisesRegex(ValueError, "PRE.*POST"):
            self.bitbucket.create_hook_script(b"#!/bin/sh", "Invalid", "PRE_RECEIVE")


class TestRepositoryForking(TestCase):
    def setUp(self):
        self.bitbucket = Bitbucket("https://bitbucket.example.com", username="admin", password="password")

    @patch.object(Bitbucket, "get_repo", return_value={"forkable": True})
    def test_get_repo_forkable(self, mock_get_repo):
        assert self.bitbucket.get_repo_forkable("PRJ", "repo") is True
        mock_get_repo.assert_called_once_with("PRJ", "repo")

    @patch.object(Bitbucket, "update_repo", return_value={"forkable": False})
    def test_set_repo_forkable_uses_repository_put_wrapper(self, mock_update_repo):
        result = self.bitbucket.set_repo_forkable("PRJ", "repo", False)

        assert result == {"forkable": False}
        mock_update_repo.assert_called_once_with("PRJ", "repo", forkable=False)

    def test_set_repo_forkable_requires_boolean(self):
        with self.assertRaisesRegex(TypeError, "boolean"):
            self.bitbucket.set_repo_forkable("PRJ", "repo", "false")

    @patch.object(Bitbucket, "put")
    def test_configure_project_hook_script(self, mock_put):
        self.bitbucket.configure_project_hook_script("PROJ", 12, ["repo:refs_changed"])

        mock_put.assert_called_once_with(
            "rest/api/latest/projects/PROJ/hook-scripts/12", data={"triggerIds": ["repo:refs_changed"]}
        )

    @patch.object(Bitbucket, "put")
    def test_configure_repo_hook_script(self, mock_put):
        self.bitbucket.configure_repo_hook_script("PROJ", "repository", 12)

        mock_put.assert_called_once_with(
            "rest/api/latest/projects/PROJ/repos/repository/hook-scripts/12", data={"triggerIds": []}
        )

    @patch.object(Bitbucket, "get")
    def test_get_hook_script(self, mock_get):
        mock_get.return_value = {"id": 12, "name": "Audit pushes"}

        result = self.bitbucket.get_hook_script(12)

        self.assertEqual(result["id"], 12)
        mock_get.assert_called_once_with("rest/api/latest/hook-scripts/12")

    @patch.object(Bitbucket, "get")
    def test_get_hook_script_content_is_not_json(self, mock_get):
        mock_get.return_value = b"#!/bin/sh\necho hook\n"

        result = self.bitbucket.get_hook_script_content(12)

        self.assertEqual(result, b"#!/bin/sh\necho hook\n")
        mock_get.assert_called_once_with("rest/api/latest/hook-scripts/12/content", not_json_response=True)

    @patch.object(Bitbucket, "put")
    def test_update_hook_script_uses_multipart_latest_endpoint(self, mock_put):
        script = b"#!/bin/sh\necho hook v2\n"
        mock_put.return_value = {"id": 12}

        result = self.bitbucket.update_hook_script(12, script, "Audit pushes", "POST", "Audit every push")

        self.assertEqual(result, {"id": 12})
        files = mock_put.call_args.kwargs["files"]
        self.assertEqual(files["content"], ("hook-script", script, "application/octet-stream"))
        self.assertEqual(files["name"], (None, "Audit pushes"))
        self.assertEqual(files["type"], (None, "POST"))
        self.assertEqual(files["description"], (None, "Audit every push"))
        self.assertEqual(mock_put.call_args.args[0], "rest/api/latest/hook-scripts/12")
        self.assertEqual(mock_put.call_args.kwargs["headers"], self.bitbucket.no_check_headers)

    def test_update_hook_script_rejects_unknown_hook_type(self):
        with self.assertRaisesRegex(ValueError, "PRE.*POST"):
            self.bitbucket.update_hook_script(12, b"#!/bin/sh", "Invalid", "PRE_RECEIVE")

    @patch.object(Bitbucket, "delete")
    def test_delete_hook_script(self, mock_delete):
        self.bitbucket.delete_hook_script(12)

        mock_delete.assert_called_once_with("rest/api/latest/hook-scripts/12")


class TestPullRequestInlineComments(TestCase):
    def setUp(self):
        self.bitbucket = Bitbucket(f"{mockup_server()}/bitbucket/server", username="username", password="password")
        self.project_key = "PRJ"
        self.repository_slug = "my-repo1-slug"
        self.pull_request_id = 1

    @patch.object(Bitbucket, "post")
    def test_add_inline_comment_range(self, mock_post):
        self.bitbucket.add_pull_request_inline_comment(
            project_key=self.project_key,
            repository_slug=self.repository_slug,
            pull_request_id=self.pull_request_id,
            text="This whole file looks great!",
            path="src/main.py",
            from_hash="abc123",
            to_hash="def456",
            diff_type="RANGE",
        )
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        body = call_args[1]["data"]
        self.assertEqual(body["text"], "This whole file looks great!")
        self.assertIn("anchor", body)
        self.assertEqual(body["anchor"]["diffType"], "RANGE")
        self.assertEqual(body["anchor"]["path"], "src/main.py")
        self.assertEqual(body["anchor"]["srcPath"], "src/main.py")
        self.assertEqual(body["anchor"]["fromHash"], "abc123")
        self.assertEqual(body["anchor"]["toHash"], "def456")

    @patch.object(Bitbucket, "post")
    def test_add_inline_comment_commit_line(self, mock_post):
        self.bitbucket.add_pull_request_inline_comment(
            project_key=self.project_key,
            repository_slug=self.repository_slug,
            pull_request_id=self.pull_request_id,
            text="This line has a bug",
            path="src/utils.py",
            from_hash="aaa111",
            to_hash="bbb222",
            line=42,
            line_type="ADDED",
            diff_type="COMMIT",
            file_type="TO",
        )
        mock_post.assert_called_once()
        body = mock_post.call_args[1]["data"]
        anchor = body["anchor"]
        self.assertEqual(anchor["diffType"], "COMMIT")
        self.assertEqual(anchor["line"], 42)
        self.assertEqual(anchor["lineType"], "ADDED")
        self.assertEqual(anchor["fileType"], "TO")

    @patch.object(Bitbucket, "post")
    def test_add_inline_comment_with_parent(self, mock_post):
        self.bitbucket.add_pull_request_inline_comment(
            project_key=self.project_key,
            repository_slug=self.repository_slug,
            pull_request_id=self.pull_request_id,
            text="I agree with this comment",
            path="README.md",
            from_hash="ccc333",
            to_hash="ddd444",
            parent_id=99,
        )
        body = mock_post.call_args[1]["data"]
        self.assertEqual(body["parent"]["id"], 99)
        self.assertIn("anchor", body)

    @patch.object(Bitbucket, "post")
    def test_add_inline_comment_custom_src_path(self, mock_post):
        self.bitbucket.add_pull_request_inline_comment(
            project_key=self.project_key,
            repository_slug=self.repository_slug,
            pull_request_id=self.pull_request_id,
            text="Renamed file comment",
            path="src/new_name.py",
            src_path="src/old_name.py",
            from_hash="eee555",
            to_hash="fff666",
        )
        body = mock_post.call_args[1]["data"]
        self.assertEqual(body["anchor"]["path"], "src/new_name.py")
        self.assertEqual(body["anchor"]["srcPath"], "src/old_name.py")


class TestPersonalRepositories(TestCase):
    def setUp(self):
        self.bitbucket = Bitbucket("https://bitbucket.example.com", username="admin", password="password")

    def test_personal_repository_urls_use_the_user_centric_route(self):
        self.assertEqual(
            self.bitbucket._url_repo("~alice", "example"),
            "rest/api/1.0/users/~alice/repos/example",
        )
        self.assertEqual(self.bitbucket._url_repos("~alice"), "rest/api/1.0/users/~alice/repos")

    @patch.object(Bitbucket, "post")
    def test_pull_request_settings_support_personal_repositories(self, mock_post):
        settings = {"requiredApprovals": 2}

        self.bitbucket.set_pull_request_settings("~alice", "example", settings)

        mock_post.assert_called_once_with(
            "rest/api/1.0/users/~alice/repos/example/settings/pull-requests", data=settings
        )
