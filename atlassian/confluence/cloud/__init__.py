from .base import ConfluenceCloudBase


class Cloud(ConfluenceCloudBase):

    def __init__(self, url, *args, **kwargs):
        super(Cloud, self).__init__(url, *args, **kwargs)
