from atlassian import Atlassian


class Jira(Atlassian):

    def reindex_status(self):
        return self.get("/rest/api/2/reindex")

    def reindex(self):
        return self.post("/rest/api/2/reindex")

    def jql(self, jql):
        return self.get("/rest/api/2/search?jql={0}&maxResults=999999".format(jql))
