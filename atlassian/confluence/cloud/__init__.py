
from .base import ConfluenceCloudBase


class Cloud(ConfluenceCloudBase):

    def __init__(self, url, *args, **kwargs):
        kwargs["cloud"] = True
        super(Cloud, self).__init__(url, *args, **kwargs)