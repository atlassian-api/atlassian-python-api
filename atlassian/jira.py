from atlassian import Atlassian


class Jira(Atlassian):

    def reindex_status(self):
        return self.get("/rest/api/2/reindex")

    def reindex(self):
        return self.post("/rest/api/2/reindex")

    def jql(self, jql):
        return self.get("/rest/api/2/search?jql={0}&maxResults=999999".format(jql))

    def projects(self):
        return self.get("/rest/api/2/project")

    def user(self, username):
        return self.get("/rest/api/2/user?username=%s" % username)

    def project(self, key):
        return self.get("/rest/api/2/project/{0}".format(key))

    def project_leaders(self):
        for project in self.projects().json():
            key = project["key"]
            project_data = self.project(key).json()
            lead = self.user(project_data["lead"]["key"]).json()
            yield {
                "project_key": key,
                "project_name": project["name"],
                "lead_name": lead["displayName"],
                "lead_key": lead["key"],
                "lead_email": lead["emailAddress"]}
