"""Atlassian Compass REST API client."""

from ..rest_client import AtlassianRestAPI


class Compass(AtlassianRestAPI):
    """Client for the Compass gateway REST API.

    Compass Cloud exposes these endpoints below ``/gateway/api`` on an
    Atlassian site. JSON requests use ``data`` or ``json`` as accepted by the
    base REST client; multipart methods accept a file path or a ``files``
    mapping.
    """

    def __init__(self, *args, **kwargs):
        kwargs["api_root"] = "gateway/api"
        super().__init__(*args, **kwargs)

    @staticmethod
    def _multipart_file(filename, files=None):
        if files is not None:
            return files, None
        if filename is None:
            raise ValueError("filename or files is required")
        handle = open(filename, "rb")
        return {"file": handle}, handle

    def send_metric(self, data=None):
        """Send a metric value to Compass."""
        return self.post(self.url_joiner(self.api_root, "compass/v1/metrics"), data=data)

    def send_event(self, data=None):
        """Send a streamlined event to Compass."""
        return self.post(self.url_joiner(self.api_root, "compass/v1/events"), data=data)

    def get_entitlement_results(self, data=None):
        """Retrieve entitlement results for a Compass component."""
        return self.post(self.url_joiner(self.api_root, "compass/v1/entitlements"), data=data)

    def invoke_webhook(self, webhook_id, data=None):
        """Invoke an inbound Compass webhook."""
        path = self.url_joiner(self.api_root, f"compass/v1/webhooks/{webhook_id}")
        return self.post(path, data=data)

    def upload_package_dependencies_lock_file(
        self, source_id, base_source_url, component_id, filename=None, files=None
    ):
        """Upload a package dependency lock file."""
        multipart, handle = self._multipart_file(filename, files)
        try:
            path = self.url_joiner(self.api_root, "compass/v1/package_dependencies/lock_file")
            params = {
                "sourceId": source_id,
                "baseSourceUrl": base_source_url,
                "componentId": component_id,
            }
            return self.put(path, params=params, files=multipart)
        finally:
            if handle:
                handle.close()

    def delete_package_dependencies(self, component_id, source_id):
        """Delete package dependencies for a component and source."""
        path = self.url_joiner(self.api_root, f"compass/v1/package_dependencies/lock_file/{component_id}/{source_id}")
        return self.delete(path)

    def get_forge_app_attachment(self, component_id, forge_app_id, key, not_json_response=True):
        """Download a Forge app attachment belonging to a component."""
        path = self.url_joiner(
            self.api_root, f"compass/v1/component/{component_id}/app/{forge_app_id}/attachment/{key}"
        )
        return self.get(path, not_json_response=not_json_response)

    def upload_forge_app_attachment(self, component_id, forge_app_id, key, filename=None, files=None):
        """Upload a Forge app attachment."""
        multipart, handle = self._multipart_file(filename, files)
        try:
            path = self.url_joiner(
                self.api_root, f"compass/v1/component/{component_id}/app/{forge_app_id}/attachment/{key}"
            )
            return self.put(path, files=multipart)
        finally:
            if handle:
                handle.close()

    def delete_forge_app_attachment(self, component_id, forge_app_id, key):
        """Delete a Forge app attachment."""
        path = self.url_joiner(
            self.api_root, f"compass/v1/component/{component_id}/app/{forge_app_id}/attachment/{key}"
        )
        return self.delete(path)

    def upload_component_api_spec(self, component_id, filename=None, files=None):
        """Upload an OpenAPI specification for a Compass component."""
        multipart, handle = self._multipart_file(filename, files)
        try:
            path = self.url_joiner(self.api_root, f"compass/v1/component/{component_id}/api_specs")
            return self.put(path, files=multipart)
        finally:
            if handle:
                handle.close()

    def delete_component_api_spec(self, component_id):
        """Delete the API specification for a Compass component."""
        path = self.url_joiner(self.api_root, f"compass/v1/component/{component_id}/api_specs")
        return self.delete(path)


__all__ = ["Compass"]
