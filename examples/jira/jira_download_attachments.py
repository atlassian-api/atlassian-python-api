from atlassian import Jira
import os

""" Download the attachments from tickets """

JIRA_URL = "localhost:8080"
JIRA_LOGIN = "admin"
JIRA_TOKEN = "dsadd2c3s"


def get_tickets(jql):
    pass


if __name__ == "__main__":
    jira = Jira(url=JIRA_URL, username=JIRA_LOGIN, token=JIRA_TOKEN)
    jql = "project = DOC"
    tickets = jira.jql(jql=jql, fields=["key,attachment"], limit=1000).get("issues")

    for ticket in tickets:
        mail_folder = "tickets"
        if not os.path.exists(mail_folder):
            os.makedirs(mail_folder)
        key = ticket.get("key")
        attachments = ticket.get("fields").get("attachment")

        for attachment in attachments:
            dest_folder = mail_folder + "/" + key
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            filename = attachment.get("filename")
            author = attachment.get("author").get("emailAddress")
            attachment_id = attachment.get("id")
            content_url = attachment.get("content")
            session = jira._session
            response = session.get(url=content_url)

            if response.status_code != 200:
                continue
            with open(dest_folder + "/" + filename, "wb") as f:
                print("Saving for {key} the file {filename}".format(key=key, filename=filename))
                f.write(response.content)
