# coding: utf8
import json
import os

from unittest.mock import Mock

from requests import Session, Response

SERVER = "https://my.test.server.com"
RESPONSE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "responses")


def mockup_server():
    return SERVER


def request_mockup(*args, **kwargs):
    method = kwargs["method"]
    url = kwargs["url"]
    if not url.startswith(SERVER + "/"):
        raise ValueError("URL [{}] does not start with [{}/].".format(url, SERVER))
    parts = url[len(SERVER) + 1 :].split("?")
    url = parts[0]
    response_key = parts[1] if len(parts) > 1 else None
    if kwargs["data"] is not None:
        response_key = str(kwargs["data"])

    response = Response()
    response.url = kwargs["url"]

    response_file = os.path.join(RESPONSE_ROOT, url, method)
    try:
        with open(response_file, encoding="utf-8") as f:
            data = {"responses": {}, "__builtins__": {}, "true": True, "false": False, "null": None}
            exec(f.read(), data)
            data = data["responses"][response_key]
            if type(data) is dict:
                if "status_code" in data:
                    response.status_code = data.pop("status_code")
                else:
                    response.status_code = 200

                # Extend the links with the server
                for item in [None, "owner", "project", "workspace"]:
                    # Use values of paged response
                    for elem in data["values"] if "values" in data else [data]:
                        cur_dict = elem if item is None else elem.get(item, {})
                        if "links" in cur_dict:
                            for link in cur_dict["links"].values():
                                for ld in link if type(link) is list else [link]:
                                    ld["href"] = "{}/{}".format(SERVER, ld["href"])
                if "next" in data:
                    data["next"] = "{}/{}".format(SERVER, data["next"])

                response.encoding = "utf-8"
                response._content = bytes(json.dumps(data), response.encoding)
            else:
                response.status_code = 200
                response._content = data
    except FileNotFoundError:
        response.encoding = "utf-8"
        response._content = b"{}"
        response.status_code = 404  # Not found
        response.reason = "No stub defined [{}]".format(response_file)
    except KeyError:
        response.encoding = "utf-8"
        response._content = b"{}"
        response.status_code = 404  # Not found
        response.reason = "No stub defined for key [{}] in [{}]".format(response_key, response_file)

    return response


Session.request = Mock()
Session.request.side_effect = request_mockup
