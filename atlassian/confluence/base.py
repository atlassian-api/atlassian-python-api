# coding=utf-8

import copy
import re
from urllib.parse import parse_qsl, urljoin, urlparse
import logging
from requests import HTTPError
from ..rest_client import AtlassianRestAPI
from ..errors import ApiValueError

log = logging.getLogger(__name__)


class ConfluenceBase(AtlassianRestAPI):
    """
    Base class for Confluence API operations.
    """

    @staticmethod
    def _is_cloud_url(url):
        """Compatibility proxy for the version-aware Confluence base class."""
        from ..confluence_base import ConfluenceBase as VersionedConfluenceBase

        return VersionedConfluenceBase._is_cloud_url(url)

    def __init__(self, url, *args, **kwargs):
        """
        Init the rest api wrapper

        :param url: string:    The base url used for the rest api.
        :param *args: list:    The fixed arguments for the AtlassianRestApi.
        :param **kwargs: dict: The keyword arguments for the AtlassianRestApi.

        :return: nothing
        """
        self._update_data(kwargs.pop("data", {}))
        if url is None:
            url = self.get_link("self")
            if isinstance(url, list):  # Server has a list of links
                url = url[0]
        super().__init__(url, *args, **kwargs)

    def _sub_url(self, url):
        """
        Get the full url from a relative one.

        :param url: string: The sub url
        :return: The absolute url
        """
        return self.url_joiner(self.url, url)

    def get_page_id_by_url(self, page_url):
        """Resolve a Confluence page URL to its page ID.

        ``viewpage.action?pageId=...`` URLs are resolved without a request.
        Display and short ``/x/...`` URLs are requested through the configured
        authenticated session, which follows the Confluence redirect and reads
        the page ID from the resulting URL or HTML metadata.
        """
        parsed_url = urlparse(page_url)
        page_id_match = re.search(r"(?:[?&]pageId=)([^&#]+)", page_url, re.IGNORECASE)
        if page_id_match:
            return page_id_match.group(1)

        client_host = urlparse(self.url).hostname
        if not parsed_url.scheme or not parsed_url.hostname:
            raise ApiValueError("page_url must be an absolute Confluence page URL")
        if client_host and parsed_url.hostname != client_host:
            raise ApiValueError("page_url must belong to the configured Confluence instance")

        response = self.get(page_url, absolute=True, advanced_mode=True)
        resolved_url = response.url
        page_id_match = re.search(r"(?:[?&]pageId=)([^&#]+)", resolved_url, re.IGNORECASE)
        if page_id_match:
            return page_id_match.group(1)

        content = response.content.decode("utf-8", errors="ignore")
        page_id_match = re.search(
            r'<meta[^>]+name=["\']ajs-page-id["\'][^>]+content=["\']([^"\']+)["\']',
            content,
            re.IGNORECASE,
        )
        if page_id_match:
            return page_id_match.group(1)

        raise ApiValueError("Could not determine a page ID from page_url")

    @property
    def _new_session_args(self):
        """
        Get the kwargs for new objects (session, root, version,...).

        :return: A dict with the kwargs for new objects
        """
        return {
            "session": self._session,
            "cloud": self.cloud,
            "api_root": self.api_root,
            "api_version": self.api_version,
        }

    def _update_data(self, data):
        """
        Internal function to update the data.

        :param data: dict: The new data.
        :return: The updated object
        """
        self.__data = data
        return self

    @property
    def data(self):
        """
        Get the internal cached data. For data integrity a deep copy is returned.

        :return: A copy of the data cache
        """
        return copy.copy(self.__data)

    def get_data(self, id, default=None):
        """
        Get a data element from the internal data cache. For data integrity a deep copy is returned.
        If data isn't present, the default value is returned.

        :param id: string:                     The data element to return
        :param default: any (default is None): The value to return if id is not present

        :return: The requested data element
        """
        return copy.copy(self.__data[id]) if id in self.__data else default

    def get_link(self, link):
        """
        Get a link from the data.

        :param link: string: The link identifier
        :return: The requested link or None if it isn't present
        """
        links = self.get_data("links")
        if links is None or link not in links:
            return None
        return links[link]["href"]

    def _get_paged(
        self,
        url,
        params=None,
        data=None,
        flags=None,
        trailing=None,
        absolute=False,
    ):
        """
        Used to get the paged data

        :param url: string:                        The url to retrieve
        :param params: dict (default is None):     The parameter's
        :param data: dict (default is None):       The data
        :param flags: string[] (default is None):  The flags
        :param trailing: bool (default is None):   If True, a trailing slash is added to the url
        :param absolute: bool (default is False):  If True, the url is used absolute and not relative to the root

        :return: A generator object for the data elements
        """
        if params is None:
            params = {}

        while True:
            current_url = url
            response = self.get(
                url,
                trailing=trailing,
                params=params,
                data=data,
                flags=flags,
                absolute=absolute,
            )
            if "results" not in response:
                return

            yield from response.get("results", [])

            next_link = response.get("_links", {}).get("next")
            if next_link is None:
                break
            if isinstance(next_link, str):
                url = next_link
            else:
                url = next_link.get("href")
            if url is None:
                break

            # Cloud V2 cursor links contain a relative endpoint and a cursor
            # query.  Reusing the already-resolved endpoint preserves both
            # ``/wiki`` and API-gateway tenant prefixes.
            parsed_next = urlparse(url)
            if getattr(self, "api_version", None) == 2 and parsed_next.query and not parsed_next.scheme:
                url = current_url
                params = dict(parse_qsl(parsed_next.query, keep_blank_values=True))
                trailing = False
                continue

            if not urlparse(url).scheme:
                # Confluence returns both ``/rest/api/...`` and
                # ``rest/api/...`` forms for next links.  Neither is an
                # absolute URL, despite the latter lacking a leading slash.
                parsed = urlparse(self.url)
                site_url = f"{parsed.scheme}://{parsed.netloc}"
                if url.startswith("/") or url.startswith(("rest/", "wiki/")):
                    url = f"{site_url}/{url.lstrip('/')}"
                else:
                    url = urljoin(f"{self.url.rstrip('/')}/", url)

            # From now on we have absolute URLs with parameters
            absolute = True
            # Params are now provided by the url
            params = {}
            # Trailing should not be added as it is already part of the url
            trailing = False

        return

    def raise_for_status(self, response):
        """
        Checks the response for errors and throws an exception if return code >= 400

        Implementation for Confluence Server according to
            https://developer.atlassian.com/server/confluence/rest/v1002/intro/#about
        Implementation for Confluence Cloud according to
            https://developer.atlassian.com/cloud/confluence/rest/v2/intro/#about
        :param response:
        :return:
        """
        if 400 <= response.status_code < 600:
            try:
                j = response.json()
            except (TypeError, ValueError):
                j = None

            messages = []
            if isinstance(j, dict):
                for key in ("message", "detail", "reason"):
                    value = j.get(key)
                    if value:
                        messages.append(str(value))
                errors = j.get("errors")
                if isinstance(errors, dict):
                    messages.extend(str(value) for value in errors.values() if value)
                elif isinstance(errors, list):
                    messages.extend(
                        str(item.get("message", item)) if isinstance(item, dict) else str(item)
                        for item in errors
                        if item
                    )
                error_messages = j.get("errorMessages")
                if isinstance(error_messages, list):
                    messages.extend(str(value) for value in error_messages if value)

            if not messages:
                # Some Confluence proxy and HTML-validation failures are not
                # JSON. Include only a bounded, whitespace-normalized server
                # response; never include the submitted page body.
                response_text = " ".join((getattr(response, "text", "") or "").split())
                if response_text:
                    messages.append(response_text[:1000])
                else:
                    messages.append(f"HTTP {response.status_code}: {response.reason}")

            raise HTTPError("\n".join(dict.fromkeys(messages)), response=response)
        else:
            response.raise_for_status()
