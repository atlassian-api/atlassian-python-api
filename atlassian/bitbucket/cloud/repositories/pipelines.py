# coding=utf-8

from requests import HTTPError

from ..base import BitbucketCloudBase


class Pipelines(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(Pipelines, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        if "errors" in data:
            return
        return Pipeline(self.url_joiner(self.url, data["uuid"]), data, **self._new_session_args)

    def each(self, q=None, sort=None):
        """
        Returns the list of pipelines in this repository.

        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the Pipeline objects
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        for pipeline in self._get_paged(None, trailing=True, params=params):
            yield self.__get_object(pipeline)

        return

    def get(self, uuid):
        """
        Returns the pipeline with the uuid in this repository.

        :param uuid: string: The requested pipeline uuid

        :return: The requested Pipeline objects
        """
        return self.__get_object(super(Pipelines, self).get(uuid))

    def trigger(self, branch="master", commit=None, pattern=None, variables=None):
        """
        Trigger a new pipeline. The following options are possible (1 and 2
        trigger the pipeline that the branch is associated with in the Pipelines
        configuration):

        1. Latest revision of a branch (specify ``branch``)
        2. Specific commit on a branch (additionally specify ``commit``)
        3. Specific pipeline (additionally specify ``pattern``)

        Variables has to be a list of dictionaries:

        {
           "key": "var1key",
           "value": "var1value",
           "secured": true
        },

        :return: The initiated Pipeline object
        """
        data = {
            "target": {
                "ref_type": "branch",
                "type": "pipeline_ref_target",
                "ref_name": branch,
            },
        }
        if commit is not None:
            data["target"]["commit"] = {
                "type": "commit",
                "hash": commit,
            }
        if pattern is not None:
            if commit is None:
                raise ValueError("Missing argument [commit].")
            data["target"]["selector"] = {
                "type": "custom",
                "pattern": pattern,
            }
        if variables is not None:
            data["variables"] = variables

        return self.__get_object(self.post(None, trailing=True, data=data))


class Pipeline(BitbucketCloudBase):
    def __init__(self, url, data, *args, **kwargs):
        super(Pipeline, self).__init__(url, *args, data=data, expected_type="pipeline", **kwargs)

    def __get_object(self, data):
        if "errors" in data:
            return
        return Step("{}/steps/{}".format(self.url, data["uuid"]), data, **self._new_session_args)

    @property
    def uuid(self):
        return self.get_data("uuid")

    @property
    def build_number(self):
        return self.get_data("build_number")

    @property
    def build_seconds_used(self):
        return self.get_data("build_seconds_used")

    @property
    def created_on(self):
        return self.get_data("created_on")

    @property
    def completed_on(self):
        return self.get_data("completed_on", "never completed")

    def stop(self):
        return self.post("stopPipeline")

    def steps(self):
        """
        Returns the list of pipeline steps.

        :return: A generator for the pipeline steps objects
        """
        for step in self._get_paged("steps", trailing=True):
            yield self.__get_object(step)

        return

    def step(self, uuid):
        """
        Returns the pipeline step with the uuid of this pipeline.

        :return: The requested pipeline objects
        """
        return self.__get_object(self.get("steps/{}".format(uuid)))


class Step(BitbucketCloudBase):
    def __init__(self, url, data, *args, **kwargs):
        super(Step, self).__init__(url, *args, data=data, expected_type="pipeline_step", **kwargs)

    @property
    def uuid(self):
        return self.get_data("uuid")

    @property
    def run_number(self):
        return self.get_data("run_number")

    @property
    def started_on(self):
        return self.get_data("started_on")

    @property
    def completed_on(self):
        return self.get_data("completed_on")

    @property
    def duration_in_seconds(self):
        return self.get_data("duration_in_seconds")

    @property
    def state(self):
        return self.get_data("state")

    @property
    def setup_commands(self):
        return self.get_data("setup_commands")

    @property
    def script_commands(self):
        return self.get_data("script_commands")

    def log(self, start=None, end=None):
        """
        Returns the log content in the given range.

        :param start: int: The start of the range. First elment is 0.
        :param end: int: The end of the range, must be greater than start.

        :return: The byte representation of the log or if range is given a tuple with
                 the overall size and the byte representation of the requested range.
        """
        headers = {"Accept": "application/octet-stream"}
        if ((start is not None) and (end is None)) or ((start is None) and (end is not None)):
            raise ValueError("For a range [start] and [end] are needed.")
        if start is not None:
            start = int(start)
            end = int(end)
            if (start >= 0) and (start < end):
                headers["Range"] = "bytes={}-{}".format(start, end)
            else:
                raise ValueError("Value of [start] must be o or greater and [end] must be greater than [start].")

        response = None
        try:
            response = self.get("log", headers=headers, advanced_mode=True)
        except HTTPError as e:
            # A 404 indicates that no log is present.
            if not e.response.status_code == 404:
                # Rethrow the exception
                raise

        if response is None:
            if start is None:
                return None
            return (None, None)

        if start is None:
            return response.content
        return (response.headers["Content-Range"].split("/")[1], response.content)
