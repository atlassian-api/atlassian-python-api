from atlassian import Confluence

# init the Confluence object
host = "<cloud_instance_url/wiki>"
username = "<user_email>"
password = "<API_TOKEN>"
confluence = Confluence(
    url=host,
    username=username,
    password=password,
)
space_key = "TEST"
confluence.get_space_export(space_key=space_key, export_type="html")
# This method should be used to trigger the space export action.
# Provide `space_key` and `export_type` (html/pdf/xml/csv) as arguments.

# It was tested on Confluence Cloud and might not work properly with Confluence on-prem.
# (!) This is an experimental method that should be considered a workaround for the missing space export REST endpoint.
# (!) The method might break if Atlassian implements changes to their space export front-end logic.

# The while loop does not have an exit condition; it will run until the space export is completed.
# It is possible that the space export progress might get stuck. It is up to the library user to handle this scenario.

# Method returns the link to the space export file.
# It is up to the library user to handle the file download action.
