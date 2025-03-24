from atlassian import Confluence
import os

host = "<cloud_instance_url/wiki>"
username = "<user_email>"
password = "<API_TOKEN>"
confluence = Confluence(
    url=host,
    username=username,
    password=password,
)

# this is the directory where the attachments will be saved.
# In this example we use current working directory where script is executed + subdirectory 'attachment_tests'

current_dir = os.getcwd()
my_path = current_dir + "/attachment_tests"
page = 393464  # make sure the page id exists and has attachments

confluence.download_attachments_from_page(page)
# Directory  'attachment_tests' should include saved attachment.
# If directory doesn't exist or if there is permission issue function should raise an error.
