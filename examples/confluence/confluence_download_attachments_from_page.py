import os

from atlassian import Confluence

host = "<cloud_instance_url/wiki>"  # e.g., "https://your-instance.atlassian.net/wiki" for cloud instances
username = "<user_email>"
password = "<API_TOKEN>"
confluence = Confluence(
    url=host,
    username=username,
    password=password,
    api_version="cloud",
)

# this is the directory where the attachments will be saved.
# In this example we use current working directory where script is executed + subdirectory 'attachment_tests'

current_dir = os.getcwd()
my_path = current_dir + "/attachment_tests"
page = 393464  # make sure the page id exists and has attachments

confluence.download_attachments_from_page(page)
# Directory  'attachment_tests' should include saved attachment.
# If directory doesn't exist or if there is permission issue function should raise an error.

if __name__ == "__main__":

    def save_file(name, content):
        if os.path.exists("attachments_folder") is False:
            os.mkdir("attachments_folder")
        file = open("attachments_folder/" + name, "wb")
        file.write(content)
        file.close()

    attachments = confluence.get_attachments_from_content(page_id="327683", start=0, limit=500)

    for attachment in attachments["results"]:
        print(attachment["title"])
        content = confluence.get_attachment_content(attachment["id"])
        save_file(attachment["title"], content)
