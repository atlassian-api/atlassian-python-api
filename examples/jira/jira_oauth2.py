# coding=utf-8
"""Example server with Flask demonstrating use of Jira OAuth 2.0.
Server needs to be deployed. Example code is requesting access token from
Jira. User has to grant access rights. After authorization the
token and Using access token, Jira cloud ID is identified and
the available projects are returned.
"""

from requests_oauthlib import OAuth2Session
from atlassian.jira import Jira
from flask import Flask, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = ""

# JIRA OAuth URLs
authorization_base_url = "https://auth.atlassian.com/authorize"
token_url = "https://auth.atlassian.com/oauth/token"
"""
 Create OAuth 2.0 Integration in Atlassian developer console
 https://developer.atlassian.com/console/myapps/
    - Click Authorization →  “Configure” under OAuth 2.0 and
    - Enter callback url  {server}/callback and save
    - Click “Permissions” and Add “Jira platform REST API” and other required permissions.
    - Click “Configure” under Jira platform REST API and Add permissions like
        "View user profiles", "View Jira issue data" and  “Create and manage issues”
    - Goto setting and copy client id and secret.
"""
client_id = ""
client_secret = ""
redirect_uri = ""  # {server_url}/callback

"""
    2. Redirect to Jira for authorization
    The server request to {server_url}/login is redirected to Jira.
    The user is asked to grant access permissions.
"""


@app.route("/login")
def login():
    scope = ["read:me", "read:jira-user", "read:jira-work"]
    audience = "api.atlassian.com"

    jira_oauth = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = jira_oauth.authorization_url(
        authorization_base_url,
        audience=audience,
    )
    session["oauth_state"] = state
    return redirect(authorization_url)


"""
    3. Jira redirects user to callback url with authorization code
    This should be set to {server_url}/callback.
    Access token is fetched using authorization code
"""


@app.route("/callback")
def callback():
    jira_oauth = OAuth2Session(client_id, state=session["oauth_state"], redirect_uri=redirect_uri)
    token_json = jira_oauth.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
    return f"Token: {token_json}<p />Projects: {', '.join(get_projects(token_json))}"


"""
    4. Access Token used for Jira Python API
    Using access token, accessible resources are fetched and
    First resource id is taken as jira cloud id,
    Jira Client library is called with  jira cloud id and token information.
"""


def get_projects(token_json):
    req = requests.get(
        "https://api.atlassian.com/oauth/token/accessible-resources",
        headers={
            "Authorization": f"Bearer {token_json['access_token']}",
            "Accept": "application/json",
        },
    )
    req.raise_for_status()
    resources = req.json()
    cloud_id = resources[0]["id"]

    oauth2_dict = {
        "client_id": client_id,
        "token": {
            "access_token": token_json["access_token"],
            "token_type": "Bearer",
        },
    }
    jira = Jira(url=f"https://api.atlassian.com/ex/jira/{cloud_id}", oauth2=oauth2_dict)
    return [project["name"] for project in jira.projects()]
