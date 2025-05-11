# coding=utf-8
import logging
import random
import time
from http.cookiejar import CookieJar
from json import dumps
from typing import (
    List,
    MutableMapping,
    Optional,
    Tuple,
    Union,
    overload,
)
from urllib.parse import urlencode

import requests
import urllib3
from requests.adapters import HTTPAdapter
from typing_extensions import Literal

from atlassian.typehints import T_resp_json

try:
    from oauthlib.oauth1.rfc5849 import SIGNATURE_RSA_SHA512 as SIGNATURE_RSA
except ImportError:
    from oauthlib.oauth1 import SIGNATURE_RSA

from requests import HTTPError, Response, Session
from requests_oauthlib import OAuth1, OAuth2
from typing_extensions import Self
from urllib3.util import Retry

from atlassian.request_utils import get_default_logger

T_resp = Union[Response, T_resp_json]
T_resp_get = Union[Response, T_resp_json, str, bytes]


log = get_default_logger(__name__)


class AtlassianRestAPI(object):
    default_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    experimental_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-ExperimentalApi": "opt-in",
    }
    # https://developer.atlassian.com/server/confluence/enable-xsrf-protection-for-your-app/#scripting
    form_token_headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Atlassian-Token": "no-check",
    }
    # https://developer.atlassian.com/server/confluence/enable-xsrf-protection-for-your-app/#scripting
    no_check_headers = {"X-Atlassian-Token": "no-check"}
    # https://developer.atlassian.com/server/confluence/enable-xsrf-protection-for-your-app/#scripting
    safe_mode_headers = {
        "X-Atlassian-Token": "no-check",
        "Content-Type": "application/vnd.atl.plugins.safe.mode.flag+json",
    }
    # https://developer.atlassian.com/server/confluence/enable-xsrf-protection-for-your-app/#scripting
    experimental_headers_general = {
        "X-Atlassian-Token": "no-check",
        "X-ExperimentalApi": "opt-in",
    }
    response = None

    def __init__(
        self,
        url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: int = 75,
        api_root: str = "rest/api",
        api_version: Union[str, int] = "latest",
        verify_ssl: bool = True,
        session: Optional[requests.Session] = None,
        oauth: Optional[dict] = None,
        oauth2: Optional[dict] = None,
        cookies: Optional[CookieJar] = None,
        advanced_mode: Optional[bool] = None,
        kerberos: object = None,
        cloud: bool = False,
        proxies: Optional[MutableMapping[str, str]] = None,
        token: Optional[str] = None,
        cert: Union[str, Tuple[str, str], None] = None,
        backoff_and_retry: bool = False,
        retry_status_codes: List[int] = [413, 429, 503],
        max_backoff_seconds: int = 1800,
        max_backoff_retries: int = 1000,
        backoff_factor=1.0,
        backoff_jitter=1.0,
        retry_with_header=True,
        header=None,
    ):
        """
        init function for the AtlassianRestAPI object.

        :param url: The url to be used in the request.
        :param username: Username. Defaults to None.
        :param password: Password. Defaults to None.
        :param timeout: Request timeout. Defaults to 75.
        :param api_root: Root for the api requests. Defaults to "rest/api".
        :param api_version: Version of the API to use. Defaults to "latest".
        :param verify_ssl: Turn on / off SSL verification. Defaults to True.
        :param session: Pass an existing Python requests session object. Defaults to None.
        :param oauth: oauth. Defaults to None.
        :param oauth2: oauth2. Defaults to None.
        :param cookies: Cookies to send with the request. Defaults to None.
        :param advanced_mode: Return results in advanced mode. Defaults to None.
        :param kerberos: Kerberos. Defaults to None.
        :param cloud: Specify if using Atlassian Cloud. Defaults to False.
        :param proxies: Specify proxies to use. Defaults to None.
        :param token: Atlassian / Jira auth token. Defaults to None.
        :param cert: Client-side certificate to use. Defaults to None.
        :param backoff_and_retry: Enable exponential backoff and retry.
                This will retry the request if there is a predefined failure. Primarily
                designed for Atlassian Cloud where API limits are commonly hit if doing
                operations on many issues, and the limits require a cooling off period.
                The wait period before the next request increases exponentially with each
                failed retry. Defaults to False.
        :param retry_status_codes: Errors to match, passed as a list of HTTP
                response codes. Defaults to [413, 429, 503].
        :param max_backoff_seconds: Max backoff seconds. When backing off, requests won't
                wait any longer than this. Defaults to 1800.
        :param max_backoff_retries: Maximum number of retries to try before
                continuing. Defaults to 1000.
        :param backoff_factor: Factor by which to multiply the backoff time (for exponential backoff).
                Defaults to 1.0.
        :param backoff_jitter: Random variation to add to the backoff time to avoid synchronized retries.
                Defaults to 1.0.
        :param retry_with_header: Enable retry logic based on the `Retry-After` header.
                If set to True, the request will automatically retry if the response
                contains a `Retry-After` header with a delay and has a status code of 429.
                The retry delay will be extracted
                from the `Retry-After` header and the request will be paused for the specified
                duration before retrying. Defaults to True.
                If the `Retry-After` header is not present, retries will not occur.
                However, if the `Retry-After` header is missing and `backoff_and_retry` is enabled,
                the retry logic will still be triggered based on the status code 429,
                provided that 429 is included in the `retry_status_codes` list.
        """
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
        self.cert = cert
        self.backoff_and_retry = backoff_and_retry
        self.max_backoff_retries = max_backoff_retries
        self.retry_status_codes = retry_status_codes
        self.max_backoff_seconds = max_backoff_seconds
        self.use_urllib3_retry = int(urllib3.__version__.split(".")[0]) >= 2
        self.backoff_factor = backoff_factor
        self.backoff_jitter = backoff_jitter
        self.retry_with_header = retry_with_header
        if session is None:
            self._session = requests.Session()
        else:
            self._session = session

        if self.proxies is not None:
            self._session.proxies = self.proxies

        if self.backoff_and_retry and self.use_urllib3_retry:
            # Note: we only retry on status and not on any of the
            # other supported reasons
            retries = Retry(
                total=None,
                status=self.max_backoff_retries,
                allowed_methods=None,
                status_forcelist=self.retry_status_codes,
                backoff_factor=self.backoff_factor,
                backoff_jitter=self.backoff_jitter,
                backoff_max=self.max_backoff_seconds,
                respect_retry_after_header=self.retry_with_header,
            )
            self._session.mount(self.url, HTTPAdapter(max_retries=retries))
        if username and password:
            self._create_basic_session(username, password)
        elif token is not None:
            self._create_token_session(token)
        elif oauth is not None:
            self._create_oauth_session(oauth)
        elif oauth2 is not None:
            self._create_oauth2_session(oauth2)
        elif kerberos is not None:
            self._create_kerberos_session(kerberos)
        elif cookies is not None:
            self._session.cookies.update(cookies)
        elif header is not None:
            self._create_header_session(header)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object):
        self.close()

    def _create_basic_session(self, username: str, password: str) -> None:
        self._session.auth = (username, password)

    def _create_token_session(self, token: str) -> None:
        self._update_header("Authorization", f"Bearer {token.strip()}")

    def _create_header_session(self, header: dict) -> None:
        self._session.headers.update(header)

    def _create_kerberos_session(self, _):
        from requests_kerberos import OPTIONAL, HTTPKerberosAuth

        self._session.auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)

    def _create_oauth_session(self, oauth_dict: dict) -> None:
        oauth = OAuth1(
            oauth_dict["consumer_key"],
            rsa_key=oauth_dict["key_cert"],
            signature_method=oauth_dict.get("signature_method", SIGNATURE_RSA),
            resource_owner_key=oauth_dict["access_token"],
            resource_owner_secret=oauth_dict["access_token_secret"],
        )
        self._session.auth = oauth

    def _create_oauth2_session(self, oauth_dict: dict) -> None:
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

    def _update_header(self, key: str, value: str):
        """
        Update header for exist session
        :param key:
        :param value:
        :return:
        """
        self._session.headers.update({key: value})

    @staticmethod
    def _response_handler(response: Response) -> T_resp_json:
        try:
            return response.json()
        except ValueError:
            log.debug("Received response with no content")
            return None
        except Exception as e:
            log.error(e)
            return None

    def _calculate_backoff_value(self, retry_count):
        """
        Calculate the backoff delay for a given retry attempt.

        This method computes an exponential backoff delay based on the retry count and
        a configurable backoff factor. It optionally adds a random jitter to introduce
        variability in the delay, which can help prevent synchronized retries in
        distributed systems. The calculated backoff delay is clamped between 0 and a
        maximum allowable delay (`self.max_backoff_seconds`) to avoid excessively long
        wait times.

        :param retry_count: int, REQUIRED: The current retry attempt number (1-based).
            Determines the exponential backoff delay.
        :return: float: The calculated backoff delay in seconds, adjusted for jitter
            and clamped to the maximum allowable value.
        """
        backoff_value = self.backoff_factor * (2 ** (retry_count - 1))
        if self.backoff_jitter != 0.0:
            backoff_value += random.uniform(0, self.backoff_jitter)  # nosec B311
        return float(max(0, min(self.max_backoff_seconds, backoff_value)))

    def _retry_handler(self):
        """
        Creates and returns a retry handler function for managing HTTP request retries.

        The returned handler function determines whether a request should be retried
        based on the response and retry settings.

        :return: Callable[[Response], bool]: A function that takes an HTTP response object as input and
        returns `True` if the request should be retried, or `False` otherwise.
        """
        retries = 0

        def _handle(response):
            nonlocal retries

            if self.retry_with_header and "Retry-After" in response.headers and response.status_code == 429:
                time.sleep(int(response.headers["Retry-After"]))
                return True

            if not self.backoff_and_retry or self.use_urllib3_retry:
                return False

            if retries < self.max_backoff_retries and response.status_code in self.retry_status_codes:
                retries += 1
                backoff_value = self._calculate_backoff_value(retries)
                time.sleep(backoff_value)
                return True

            return False

        return _handle

    def log_curl_debug(
        self,
        method: str,
        url: str,
        data: Union[dict, str, None] = None,
        headers: Optional[dict] = None,
        level: int = logging.DEBUG,
    ) -> None:
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
            headers=" -H ".join([f"'{key}: {value}'" for key, value in list(headers.items())]),
            data="" if not data else f"--data '{dumps(data)}'",
            url=url,
        )
        log.log(level=level, msg=message)

    def resource_url(
        self, resource: str, api_root: Optional[str] = None, api_version: Union[str, int, None] = None
    ) -> str:
        if api_root is None:
            api_root = self.api_root
        if api_version is None:
            api_version = self.api_version
        return "/".join(str(s).strip("/") for s in [api_root, api_version, resource] if s is not None)

    @staticmethod
    def url_joiner(url: Optional[str], path: str, trailing: Optional[bool] = None) -> str:
        url_link = "/".join(str(s).strip("/") for s in [url, path] if s is not None)
        if trailing:
            url_link += "/"
        return url_link

    def close(self) -> None:
        return self._session.close()

    def request(
        self,
        method: str = "GET",
        path: str = "/",
        data: Union[dict, str, None] = None,
        json: Union[dict, str, None] = None,
        flags: Optional[list] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        files: Optional[dict] = None,
        trailing: Optional[bool] = None,
        absolute: bool = False,
        advanced_mode: bool = False,
    ) -> Response:
        """

        :param method:
        :param path:
        :param data:
        :param json:
        :param flags:
        :param params:
        :param headers:
        :param files:
        :param trailing: bool - OPTIONAL: Add trailing slash to url
        :param absolute: bool, OPTIONAL: Do not prefix url, url is absolute
        :param advanced_mode: bool, OPTIONAL: Return the raw response
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
            url += urlencode((params or {}), safe=",")
        if flags:
            url += ("&" if params or params_already_in_url else "") + "&".join(flags or [])
        json_dump = None
        if files is None:
            data = None if not data else dumps(data)
            json_dump = None if not json else dumps(json)

        headers = headers or self.default_headers

        retry_handler = self._retry_handler()
        while True:
            self.log_curl_debug(
                method=method,
                url=url,
                headers=headers,
                data=data or json_dump,
            )
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
                cert=self.cert,
            )
            continue_retries = retry_handler(response)
            if continue_retries:
                continue
            break

        response.encoding = "utf-8"

        log.debug("HTTP: %s %s -> %s %s", method, path, response.status_code, response.reason)
        log.debug("HTTP: Response text -> %s", response.text)

        if self.advanced_mode or advanced_mode:
            return response

        self.raise_for_status(response)
        return response

    # both True
    @overload
    def get(
        self,
        path: str,
        data: Union[dict, str, None] = ...,
        flags: Optional[list] = ...,
        params: Optional[dict] = ...,
        headers: Optional[dict] = ...,
        *,
        not_json_response: Literal[True],
        trailing: Optional[bool] = ...,
        absolute: bool = ...,
        advanced_mode: Literal[True],
    ) -> bytes:
        ...  # fmt: skip

    # not_json_response True
    @overload
    def get(
        self,
        path: str,
        data: Union[dict, str, None] = ...,
        flags: Optional[list] = ...,
        params: Optional[dict] = ...,
        headers: Optional[dict] = ...,
        *,
        not_json_response: Literal[True],
        trailing: Optional[bool] = ...,
        absolute: bool = ...,
        advanced_mode: bool = ...,
    ) -> bytes:
        ...  # fmt: skip

    # advanced mode True
    @overload
    def get(
        self,
        path: str,
        data: Union[dict, str, None] = ...,
        flags: Optional[list] = ...,
        params: Optional[dict] = ...,
        headers: Optional[dict] = ...,
        not_json_response: Optional[Literal[False]] = ...,
        trailing: Optional[bool] = ...,
        absolute: bool = ...,
        *,
        advanced_mode: Literal[True],
    ) -> Response:
        ...  # fmt: skip

    # both False
    @overload
    def get(
        self,
        path: str,
        data: Union[dict, str, None] = ...,
        flags: Optional[list] = ...,
        params: Optional[dict] = ...,
        headers: Optional[dict] = ...,
        not_json_response: Optional[Literal[False]] = ...,
        trailing: Optional[bool] = ...,
        absolute: bool = ...,
        advanced_mode: Literal[False] = ...,
    ) -> T_resp_json:
        ...  # fmt: skip

    # basic overall case
    @overload
    def get(
        self,
        path: str,
        data: Union[dict, str, None] = ...,
        flags: Optional[list] = ...,
        params: Optional[dict] = ...,
        headers: Optional[dict] = ...,
        not_json_response: Optional[bool] = ...,
        trailing: Optional[bool] = ...,
        absolute: bool = ...,
        advanced_mode: bool = ...,
    ) -> T_resp_get:
        ...  # fmt: skip

    def get(
        self,
        path: str,
        data: Union[dict, str, None] = None,
        flags: Optional[list] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        not_json_response: Optional[bool] = None,
        trailing: Optional[bool] = None,
        absolute: bool = False,
        advanced_mode: bool = False,
    ) -> T_resp_get:
        """
        Get request based on the python-requests module. You can override headers, and also, get not json response
        :param path:
        :param data:
        :param flags:
        :param params:
        :param headers:
        :param not_json_response: OPTIONAL: For get content from raw request's packet
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
            advanced_mode=advanced_mode,
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

    def _get_response_content(
        self,
        *args,
        fields,
        **kwargs,
    ):
        """
        :param fields: list of tuples in the form (field_name, default value (optional)).
            Used for chaining dictionary value accession.
            E.g. [("field1", "default1"), ("field2", "default2"), ("field3", )]
        """
        response = self.get(*args, **kwargs)
        if "advanced_mode" in kwargs:
            advanced_mode = kwargs["advanced_mode"]
        else:
            advanced_mode = self.advanced_mode

        if not advanced_mode:  # dict
            for field in fields:
                response = response.get(*field)
        else:  # requests.Response
            first_field = fields[0]
            response = response.json().get(*first_field)
            for field in fields[1:]:
                response = response.get(*field)

        return response

    # advanced false
    @overload
    def post(
        self,
        path: str,
        data: Union[dict, str],
        *,
        json: Union[dict, str, None] = ...,
        headers: Optional[dict] = ...,
        files: Optional[dict] = ...,
        params: Optional[dict] = ...,
        trailing: Optional[bool] = ...,
        absolute: bool = ...,
        advanced_mode: Literal[False] = ...,
    ) -> T_resp_json:
        ...  # fmt: skip

    @overload
    def post(
        self,
        path: str,
        data: Union[dict, str, None] = ...,
        json: Union[dict, str, None] = ...,
        headers: Optional[dict] = ...,
        files: Optional[dict] = ...,
        params: Optional[dict] = ...,
        trailing: Optional[bool] = ...,
        absolute: bool = ...,
        *,
        advanced_mode: Literal[False] = ...,
    ) -> T_resp_json:
        ...  # fmt: skip

    @overload
    def post(
        self,
        path: str,
        data: Union[dict, str, None] = ...,
        json: Union[dict, str, None] = ...,
        headers: Optional[dict] = ...,
        files: Optional[dict] = ...,
        params: Optional[dict] = ...,
        trailing: Optional[bool] = ...,
        absolute: bool = ...,
        advanced_mode: Literal[False] = ...,
    ) -> T_resp_json:
        ...  # fmt: skip

    # advanced True
    @overload
    def post(
        self,
        path: str,
        data: Union[dict, str, None] = ...,
        json: Union[dict, str, None] = ...,
        headers: Optional[dict] = ...,
        files: Optional[dict] = ...,
        params: Optional[dict] = ...,
        trailing: Optional[bool] = ...,
        absolute: bool = ...,
        *,
        advanced_mode: Literal[True],
    ) -> Response:
        ...  # fmt: skip

    # basic overall case
    @overload
    def post(
        self,
        path: str,
        data: Union[dict, str, None] = ...,
        json: Union[dict, str, None] = ...,
        headers: Optional[dict] = ...,
        files: Optional[dict] = ...,
        params: Optional[dict] = ...,
        trailing: Optional[bool] = ...,
        absolute: bool = ...,
        advanced_mode: bool = ...,
    ) -> Union[Response, dict, None]:
        ...  # fmt: skip

    def post(
        self,
        path: str,
        data: Union[dict, str, None] = None,
        json: Union[dict, str, None] = None,
        headers: Optional[dict] = None,
        files: Optional[dict] = None,
        params: Optional[dict] = None,
        trailing: Optional[bool] = None,
        absolute: bool = False,
        advanced_mode: bool = False,
    ) -> Union[Response, dict, None]:
        """
        :param path:
        :param data:
        :param json:
        :param headers:
        :param files:
        :param params:
        :param trailing:
        :param absolute:
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
            advanced_mode=advanced_mode,
        )
        if self.advanced_mode or advanced_mode:
            return response
        return self._response_handler(response)

    # advanced False
    @overload
    def put(
        self,
        path: str,
        data: Union[dict, str, None] = ...,
        headers: Optional[dict] = ...,
        files: Optional[dict] = ...,
        trailing: Optional[bool] = ...,
        params: Optional[dict] = ...,
        absolute: bool = ...,
        *,
        advanced_mode: Literal[False],
    ) -> T_resp_json:
        ...  # fmt: skip

    @overload
    def put(
        self,
        path: str,
        data: Union[dict, str, None] = ...,
        headers: Optional[dict] = ...,
        files: Optional[dict] = ...,
        trailing: Optional[bool] = ...,
        params: Optional[dict] = ...,
        absolute: bool = ...,
        advanced_mode: Literal[False] = ...,
    ) -> T_resp_json:
        ...  # fmt: skip

    # advanced True
    @overload
    def put(
        self,
        path: str,
        data: Union[dict, str, None] = ...,
        headers: Optional[dict] = ...,
        files: Optional[dict] = ...,
        trailing: Optional[bool] = ...,
        params: Optional[dict] = ...,
        absolute: bool = ...,
        *,
        advanced_mode: Literal[True],
    ) -> Response:
        ...  # fmt: skip

    # basic overall case
    @overload
    def put(
        self,
        path: str,
        data: Union[dict, str, None] = ...,
        headers: Optional[dict] = ...,
        files: Optional[dict] = ...,
        trailing: Optional[bool] = ...,
        params: Optional[dict] = ...,
        absolute: bool = ...,
        advanced_mode: bool = ...,
    ) -> Union[Response, dict, None]:
        ...  # fmt: skip

    def put(
        self,
        path: str,
        data: Union[dict, str, None] = None,
        headers: Optional[dict] = None,
        files: Optional[dict] = None,
        trailing: Optional[bool] = None,
        params: Optional[dict] = None,
        absolute: bool = False,
        advanced_mode: bool = False,
    ) -> Union[Response, dict, None]:
        """
        :param path: Path of request
        :param data:
        :param headers: adjusted headers, usually it's default
        :param files:
        :param trailing:
        :param params:
        :param absolute:
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
            advanced_mode=advanced_mode,
        )
        if self.advanced_mode or advanced_mode:
            return response
        return self._response_handler(response)

    """
        Partial modification of resource by PATCH Method
        LINK: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PATCH
    """

    def patch(
        self,
        path: str,
        data: Union[dict, str, None] = None,
        headers: Optional[dict] = None,
        files: Optional[dict] = None,
        trailing: Optional[bool] = None,
        params: Optional[dict] = None,
        absolute: bool = False,
        advanced_mode: bool = False,
    ) -> T_resp:
        """
        :param path: Path of request
        :param data:
        :param headers: adjusted headers, usually it's default
        :param files:
        :param trailing:
        :param params:
        :param absolute:
        :param advanced_mode: bool, OPTIONAL: Return the raw response
        :return: if advanced_mode is not set - returns dictionary. If it is set - returns raw response.
        """
        response = self.request(
            "PATCH",
            path=path,
            data=data,
            headers=headers,
            files=files,
            params=params,
            trailing=trailing,
            absolute=absolute,
            advanced_mode=advanced_mode,
        )
        if self.advanced_mode or advanced_mode:
            return response
        return self._response_handler(response)

    # advanced False
    @overload
    def delete(
        self,
        path: str,
        data: Union[dict, str, None] = ...,
        headers: Optional[dict] = ...,
        params: Optional[dict] = ...,
        trailing: Optional[bool] = ...,
        absolute: bool = ...,
        *,
        advanced_mode: Literal[False],
    ) -> T_resp_json:
        ...  # fmt: skip

    @overload
    def delete(
        self,
        path: str,
        data: Union[dict, str, None] = ...,
        headers: Optional[dict] = ...,
        params: Optional[dict] = ...,
        trailing: Optional[bool] = ...,
        absolute: bool = ...,
        advanced_mode: Literal[False] = ...,
    ) -> T_resp_json:
        ...  # fmt: skip

    # advanced True
    @overload
    def delete(
        self,
        path: str,
        data: Union[dict, str, None] = ...,
        headers: Optional[dict] = ...,
        params: Optional[dict] = ...,
        trailing: Optional[bool] = ...,
        absolute: bool = ...,
        *,
        advanced_mode: Literal[True],
    ) -> Response:
        ...  # fmt: skip

    # basic overall case
    @overload
    def delete(
        self,
        path: str,
        data: Union[dict, str, None] = ...,
        headers: Optional[dict] = ...,
        params: Optional[dict] = ...,
        trailing: Optional[bool] = ...,
        absolute: bool = ...,
        advanced_mode: bool = ...,
    ) -> T_resp:
        ...  # fmt: skip

    def delete(
        self,
        path: str,
        data: Union[dict, str, None] = None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        trailing: Optional[bool] = None,
        absolute: bool = False,
        advanced_mode: bool = False,
    ) -> T_resp:
        """
        Deletes resources at given paths.
        :param path:
        :param data:
        :param headers:
        :param params:
        :param trailing:
        :param absolute:
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
            advanced_mode=advanced_mode,
        )
        if self.advanced_mode or advanced_mode:
            return response
        return self._response_handler(response)

    def raise_for_status(self, response: Response) -> None:
        """
        Checks the response for errors and throws an exception if return code >= 400
        Since different tools (Atlassian, Jira, ...) have different formats of returned json,
        this method is intended to be overwritten by a tool specific implementation.
        :param response:
        :return:
        """
        if response.status_code == 401 and response.headers.get("Content-Type") != "application/json;charset=UTF-8":
            raise HTTPError("Unauthorized (401)", response=response)

        if 400 <= response.status_code < 600:
            try:
                j = response.json()
                if self.url == "https://api.atlassian.com":
                    error_msg = "\n".join([f"{k}: {v}" for k, v in list(j.items())])
                else:
                    error_msg_list = j.get("errorMessages", list())
                    errors = j.get("errors", dict())
                    if isinstance(errors, dict) and "message" not in errors:
                        error_msg_list.extend(list(errors.values()))
                    elif isinstance(errors, dict) and "message" in errors:
                        error_msg_list.append(errors.get("message", ""))
                    elif isinstance(errors, list):
                        error_msg_list.extend([v.get("message", "") if isinstance(v, dict) else v for v in errors])
                    error_msg = "\n".join(error_msg_list)
            except Exception as e:
                log.error(e)
                response.raise_for_status()
            else:
                raise HTTPError(error_msg, response=response)
        else:
            response.raise_for_status()

    @property
    def session(self) -> Session:
        """Providing access to the restricted field"""
        return self._session
