from atlassian import Atlassian


class Confluence(Atlassian):

    def create_page(self, space, parent_id, title, body):
        return self.post("/rest/api/content/", {
            "type": "page",
            "title": title,
            "ancestors": [{"type": "page", "id": parent_id}],
            "space": {"key": space},
            "body": {"storage": {
                "value": body,
                "representation": "storage"}}})
