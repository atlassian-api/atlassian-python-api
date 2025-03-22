# Example server with Flask demonstrating use of OAuth 2.0. Server
# needs to be deployed. Example code is requesting access token from
# Bitbucket. User has to grant access rights. After authorization the
# token and the available workspaces are returned.

from requests_oauthlib import OAuth2Session
from atlassian.bitbucket import Cloud
from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = ""

# Bitbucket OAuth URLs
authorization_base_url = "https://bitbucket.org/site/oauth2/authorize"
token_url = "https://bitbucket.org/site/oauth2/access_token"

# 1. Create OAuth consumer
# Go to "Your profile and setting" -> "All workspaces" -> "Manage".
# Go to "Apps and features" -> "OAuth consumers".
# Click "Add consumer". Fill in Name and Callback URL. Set permissions
# as needed. Click save and copy client id and secret.
client_id = ""
client_secret = ""


# 2. Redirect to Bitbucket for authorization
# The server request to {server_url}/login is redirected to Bitbucket.
# The user is asked to grant access permissions.
@app.route("/login")
def login():
    bitbucket = OAuth2Session(client_id)
    authorization_url, state = bitbucket.authorization_url(authorization_base_url)
    session["oauth_state"] = state
    return redirect(authorization_url)


# 3. Bitbucket sends callback with token
# Bitbucket is calling the Callback URL specified in the OAuth
# consumer. This should be set to {server_url}/callback. The callback
# contains the access token.
@app.route("/callback")
def callback():
    bitbucket = OAuth2Session(client_id, state=session["oauth_state"])
    token = bitbucket.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)

    return f"Token: {token}<p />Workspaces: {', '.join(get_workspaces(token))}"


# 4. Token used for Bitbucket Python API
# Bitbucket Cloud API library is called with token information. User is
# authenticated with OAuth 2.0.
def get_workspaces(token):
    oauth2 = {"client_id": client_id, "token": token}

    bitbucket = Cloud(url="https://api.bitbucket.org/", oauth2=oauth2, cloud=True)

    return [ws.name for ws in bitbucket.workspaces.each()]
