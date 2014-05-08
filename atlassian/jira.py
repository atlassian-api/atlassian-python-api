from atlassian import Atlassian


class Jira(Atlassian):

    def reindex(self):
        return self.get("/rest/api/2/reindex")