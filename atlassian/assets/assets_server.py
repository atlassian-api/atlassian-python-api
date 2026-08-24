"""Jira Service Management Assets Server/Data Center client."""

from .assets_cloud import AssetsCloud


class AssetsServer(AssetsCloud):
    """Assets REST client for Jira Server/Data Center installations.

    Assets Data Center 10.x exposes the REST resources below
    ``/rest/assets/1.0``.  The implementation shares the resource methods
    with :class:`~atlassian.assets.assets_cloud.AssetsCloud`; only workspace
    discovery and the Cloud gateway are skipped.
    """

    def __init__(self, *args, **kwargs):
        # Explicitly force the server path even if a caller reuses a config
        # dictionary that contains ``cloud=True``.
        kwargs["cloud"] = False
        super().__init__(*args, **kwargs)


# Data Center is the current product name; retain this descriptive alias for
# callers that used the previous class name.
AssetsDataCenter = AssetsServer
