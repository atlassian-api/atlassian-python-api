# coding: utf8
import json
import os

from unittest.mock import Mock, MagicMock

from requests import Session, Response

SERVER = None
RESPONSE_ROOT = None


def init_response_mockup(server, response_root):
    global SERVER
    SERVER = server
    global RESPONSE_ROOT
    RESPONSE_ROOT = response_root


def request_mookup(*args, **kwargs):
    method = kwargs["method"]
    url = kwargs["url"]
    if not url.startswith(SERVER + "/"):
        raise ValueError("URL [{}] does not start with [{}/].".format(url, SERVER))
    parts = url[len(SERVER) + 1 :].split("?")
    url = parts[0]
    params = parts[1] if len(parts) > 1 else None

    response = Response()
    response.url = kwargs["url"]

    response_file = os.path.join(RESPONSE_ROOT, url, method)
    try:
        with open(response_file) as f:
            data = {"responses": {}, "__builtins__": {}}
            exec(f.read(), data)
            data = data["responses"][params]
            if type(data) is dict:
                if "status_code" in data:
                    response.status_code = data.pop("status_code")
                else:
                    response.status_code = 200

                # Extend the links with the server
                for item in [None, "owner", "project", "workspace"]:
                    cur_dict = data if item is None else data.get(item, {})
                    if "links" in cur_dict:
                        for link in cur_dict["links"].values():
                            try:
                                link["href"] = "{}/{}".format(SERVER, link["href"])
                            except:
                                pass
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
        response.reason = "No stub defined for param [{}]".format(params)
    except Exception as e:
        raise e

    return response


Session.request = Mock()
Session.request.side_effect = request_mookup
