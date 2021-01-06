# coding=utf-8
import json
import os
import unittest
from requests import Response

from atlassian import Confluence
from atlassian.errors import ApiError


@unittest.skipIf(
    not os.path.exists("../credentials.secret"),
    "credentials.secret missing, skipping test",
)
class TestConfluenceAdvancedModeCalls(unittest.TestCase):
    secret_file = "../credentials.secret"

    """
        Keep the credentials private, the file is excluded. There is an example for credentials.secret
        See also: http://www.blacktechdiva.com/hide-api-keys/

        {
          "host" : "https://localhost:8080",
          "username" : "john_doe",
          "password" : "12345678"
        }
    """

    @classmethod
    def setUpClass(cls):
        try:
            with open(cls.secret_file) as json_file:
                credentials = json.load(json_file)
                cls.confluence = Confluence(
                    url=credentials["host"],
                    username=credentials["username"],
                    password=credentials["password"],
                )
        except Exception as err:
            raise cls.failureException("[{0}]: {1}".format(cls.secret_file, err))

        cls.space = "SAN"
        cls.created_pages = set()

    def test_confluence_advanced_mode_post(self):
        """Tests the advanced_mode option of AtlassianRestAPI post method by manually creating a page"""
        page_title = "Test_confluence_advanced_mode_post"
        data = {
            "type": "page",
            "title": page_title,
            "space": {"key": self.space},
            "body": {"editor": {"value": "<h1>Created page</h1>", "representation": "editor"}},
        }
        result = self.confluence.post(
            path="rest/api/content",
            data=data,
            advanced_mode=True,
        )
        self.assertIsInstance(result, Response)

        # For cleanup
        page_id = self.confluence.get_page_id(space=self.space, title=page_title)
        self.created_pages |= {page_id}

    def test_confluence_advanced_mode_put(self):
        """Tests the advanced_mode option of AtlassianRestAPI post method by creating a page using python API, then
        directly updating the text through PUT"""

        page_title = "Test_confluence_advanced_mode_put"
        page_id = self.confluence.create_page(
            space=self.space, title=page_title, body="h1. Test content\n", representation="wiki"
        )["id"]
        self.created_pages |= {page_id}
        data = {
            "id": page_id,
            "type": "page",
            "title": page_title,
            "version": {"number": 2, "minorEdit": False},
            "body": {"editor": {"value": "<h1>Updated page</h1>", "representation": "editor"}},
        }

        result = self.confluence.put(path="/rest/api/content/{0}".format(page_id), data=data, advanced_mode=True)
        self.assertIsInstance(result, Response)

    def test_confluence_advanced_mode_delete(self):
        """Tests the advanced_mode option of AtlassianRestAPI post method by creating a page using python API, then
        deleting the page through DELETE"""
        page_title = "Test_confluence_advanced_mode_delete"
        page_id = self.confluence.create_page(
            space=self.space, title=page_title, body="h1. Test content\n", representation="wiki"
        )["id"]
        response = self.confluence.delete(
            path="rest/api/content/{page_id}".format(page_id=page_id), params={}, advanced_mode=True
        )
        self.assertIsInstance(response, Response)

    def tearDown(self):
        """Run after every test. Destroys created pages"""
        for page_id in self.created_pages:
            try:
                self.confluence.remove_page(page_id=page_id)
            except ApiError as e:
                if e.args[0].startswith("There is no content with the given id"):
                    # Page was probably already deleted
                    pass
                else:
                    raise e


if __name__ == "__main__":
    unittest.main()
