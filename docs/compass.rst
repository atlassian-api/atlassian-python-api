Compass
=======

The ``Compass`` client wraps the Compass Cloud gateway API at
``/gateway/api``.

.. code-block:: python

    from atlassian import Compass

    compass = Compass(
        "https://example.atlassian.net",
        username="email@example.com",
        password="api-token",
    )
    compass.send_event({"event": "deployment", "componentId": "123"})
    compass.send_metric({"metric": "build.duration", "value": 42})

Multipart endpoints accept either a local file path or a Requests-compatible
``files`` mapping:

.. code-block:: python

    compass.upload_component_api_spec("123", filename="openapi.yaml")
    compass.upload_package_dependencies_lock_file(
        source_id="github",
        base_source_url="https://github.com/example/repo",
        component_id="123",
        filename="package-lock.json",
    )

Attachments can be downloaded, uploaded, or deleted with
``get_forge_app_attachment``, ``upload_forge_app_attachment``, and
``delete_forge_app_attachment``. Webhooks and entitlement requests are
available through ``invoke_webhook`` and ``get_entitlement_results``.
