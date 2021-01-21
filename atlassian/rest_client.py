# coding=utf-8
import logging
from json import dumps

import requests
from oauthlib.oauth1 import SIGNATURE_RSA
from requests_oauthlib import OAuth1, OAuth2
from six.moves.urllib.parse import urlencode

from atlassian.request_utils import get_default_logger

log = get_default_logger(__name__)


class AtlassianRestAPI(object):
    default_headers = {"Content-Type": "application/json", "Accept": "application/json"}
    experimental_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-ExperimentalApi": "opt-in",
    }
    form_token_headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Atlassian-Token": "no-check",
    }
    no_check_headers = {"X-Atlassian-Token": "no-check"}
    safe_mode_headers = {
        "X-Atlassian-Token": "nocheck",
        "Content-Type": "application/vnd.atl.plugins.safe.mode.flag+json",
    }
    experimental_headers_general = {
        "X-Atlassian-Token": "no-check",
        "X-ExperimentalApi": "opt-in",
    }
    response = None

    def __init__(
        self,
        url,
        username=None,
        password=None,
        timeout=75,
        api_root="rest/api",
        api_version="latest",
        verify_ssl=True,
        session=None,
        oauth=None,
        oauth2=None,
        cookies=None,
        advanced_mode=None,
        kerberos=None,
        cloud=False,
        proxies=None,
    ):
        self.url = url
        self.username = username
        self.password = password
        self.timeout = int(timeout)
        self.verify_ssl = verify_ssl
        self.api_root = api_root
        self.api_version = api_version
        self.cookies = cookies
        self.advanced_mode = advanced_mode
        self.cloud = cloud
        self.proxies = proxies
        if session is None:
            self._session = requests.Session()
        else:
            self._session = session
        if username and password:
            self._create_basic_session(username, password)
        elif oauth is not None:
            self._create_oauth_session(oauth)
        elif oauth2 is not None:
            self._create_oauth2_session(oauth2)
        elif kerberos is not None:
            self._create_kerberos_session(kerberos)
        elif cookies is not None:
            self._session.cookies.update(cookies)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def _create_basic_session(self, username, password):
        self._session.auth = (username, password)

    def _create_kerberos_session(self, _):
        from requests_kerberos import HTTPKerberosAuth, OPTIONAL

        self._session.auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)

    def _create_oauth_session(self, oauth_dict):
        oauth = OAuth1(
            oauth_dict["consumer_key"],
            rsa_key=oauth_dict["key_cert"],
            signature_method=SIGNATURE_RSA,
            resource_owner_key=oauth_dict["access_token"],
            resource_owner_secret=oauth_dict["access_token_secret"],
        )
        self._session.auth = oauth

    def _create_oauth2_session(self, oauth_dict):
        """
        Use OAuth 2.0 Authentication
        :param oauth_dict: Dictionary containing access information. Must at
            least contain "client_id" and "token". "token" is a dictionary and
            must at least contain "access_token" and "token_type".
        :return:
        """
        if "client" not in oauth_dict:
            oauth_dict["client"] = None
        oauth = OAuth2(oauth_dict["client_id"], oauth_dict["client"], oauth_dict["token"])
        self._session.auth = oauth

    def _update_header(self, key, value):
        """
        Update header for exist session
        :param key:
        :param value:
        :return:
        """
        self._session.headers.update({key: value})

    @staticmethod
    def _response_handler(response):
        try:
            return response.json()
        except ValueError:
            log.debug("Received response with no content")
            return None
        except Exception as e:
            log.error(e)
            return None

    def log_curl_debug(self, method, url, data=None, headers=None, level=logging.DEBUG):
        """

        :param method:
        :param url:
        :param data:
        :param headers:
        :param level:
        :return:
        """
        headers = headers or self.default_headers
        message = "curl --silent -X {method} -H {headers} {data} '{url}'".format(
            method=method,
            headers=" -H ".join(["'{0}: {1}'".format(key, value) for key, value in headers.items()]),
            data="" if not data else "--data '{0}'".format(dumps(data)),
            url=url,
        )
        log.log(level=level, msg=message)

    def resource_url(self, resource, api_root=None, api_version=None):
        if api_root is None:
            api_root = self.api_root
        if api_version is None:
            api_version = self.api_version
        return "/".join(s.strip("/") for s in [api_root, api_version, resource] if s is not None)

    @staticmethod
    def url_joiner(url, path, trailing=None):
        url_link = "/".join(str(s).strip("/") for s in [url, path] if s is not None)
        if trailing:
            url_link += "/"
        return url_link

    def close(self):
        return self._session.close()

    def request(
        self,
        method="GET",
        path="/",
        data=None,
        json=None,
        flags=None,
        params=None,
        headers=None,
        files=None,
        trailing=None,
        absolute=False,
    ):
        """

        :param method:
        :param path:
        :param data:
        :param json:
        :param flags:
        :param params:
        :param headers:
        :param files:
        :param trailing: bool
        :param absolute: bool, OPTIONAL: Do not prefix url, url is absolute
        :return:
        """
        url = self.url_joiner(None if absolute else self.url, path, trailing)
        params_already_in_url = True if "?" in url else False
        if params or flags:
            if params_already_in_url:
                url += "&"
            else:
                url += "?"
        if params:
            url += urlencode(params or {})
        if flags:
            url += ("&" if params or params_already_in_url else "") + "&".join(flags or [])
        json_dump = None
        if files is None:
            data = None if not data else dumps(data)
            json_dump = None if not json else dumps(json)
        self.log_curl_debug(method=method, url=url, headers=headers, data=data if data else json_dump)
        headers = headers or self.default_headers
        response = self._session.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            json=json,
            timeout=self.timeout,
            verify=self.verify_ssl,
            files=files,
            proxies=self.proxies,
        )
        response.encoding = "utf-8"

        log.debug("HTTP: {} {} -> {} {}".format(method, path, response.status_code, response.reason))
        log.debug("HTTP: Response text -> {}".format(response.text))
        if self.advanced_mode:
            return response

        response.raise_for_status()
        return response

    def get(
        self,
        path,
        data=None,
        flags=None,
        params=None,
        headers=None,
        not_json_response=None,
        trailing=None,
        absolute=False,
        advanced_mode=False,
    ):
        """
        Get request based on the python-requests module. You can override headers, and also, get not json response
        :param path:
        :param data:
        :param flags:
        :param params:
        :param headers:
        :param not_json_response: OPTIONAL: For get content from raw requests packet
        :param trailing: OPTIONAL: for wrap slash symbol in the end of string
        :param absolute: bool, OPTIONAL: Do not prefix url, url is absolute
        :param advanced_mode: bool, OPTIONAL: Return the raw response
        :return:
        """
        response = self.request(
            "GET",
            path=path,
            flags=flags,
            params=params,
            data=data,
            headers=headers,
            trailing=trailing,
            absolute=absolute,
        )
        if self.advanced_mode or advanced_mode:
            return response
        if not_json_response:
            return response.content
        else:
            if not response.text:
                return None
            try:
                return response.json()
            except Exception as e:
                log.error(e)
                return response.text

    def post(
        self,
        path,
        data=None,
        json=None,
        headers=None,
        files=None,
        params=None,
        trailing=None,
        absolute=False,
        advanced_mode=False,
    ):
        """
        :param advanced_mode: bool, OPTIONAL: Return the raw response
        :return: if advanced_mode is not set - returns dictionary. If it is set - returns raw response.
        """
        response = self.request(
            "POST",
            path=path,
            data=data,
            json=json,
            headers=headers,
            files=files,
            params=params,
            trailing=trailing,
            absolute=absolute,
        )
        if self.advanced_mode or advanced_mode:
            return response
        return self._response_handler(response)

    def put(
        self,
        path,
        data=None,
        headers=None,
        files=None,
        trailing=None,
        params=None,
        absolute=False,
        advanced_mode=False,
    ):
        """
        :param advanced_mode: bool, OPTIONAL: Return the raw response
        :return: if advanced_mode is not set - returns dictionary. If it is set - returns raw response.
        """
        response = self.request(
            "PUT",
            path=path,
            data=data,
            headers=headers,
            files=files,
            params=params,
            trailing=trailing,
            absolute=absolute,
        )
        if self.advanced_mode or advanced_mode:
            return response
        return self._response_handler(response)

    def delete(
        self,
        path,
        data=None,
        headers=None,
        params=None,
        trailing=None,
        absolute=False,
        advanced_mode=False,
    ):
        """
        Deletes resources at given paths.
        :param advanced_mode: bool, OPTIONAL: Return the raw response
        :rtype: dict
        :return: Empty dictionary to have consistent interface.
        Some of Atlassian REST resources don't return any content.
        If advanced_mode is set - returns raw response.
        """
        response = self.request(
            "DELETE",
            path=path,
            data=data,
            headers=headers,
            params=params,
            trailing=trailing,
            absolute=absolute,
        )
        if self.advanced_mode or advanced_mode:
            return response
        return self._response_handler(response)
