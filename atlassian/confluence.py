from atlassian import Atlassian


class Confluence(Atlassian):

    def create_page(self, space, title, body):
        return self.post("/rest/api/content/", {
            "type": "page",
            "title": title,
            "space": {"key": space},
            "body": {"storage": {
                "value": body,
                "representation": "storage"}}})
