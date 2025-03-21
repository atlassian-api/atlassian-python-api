# coding=utf-8

from .pullRequests import PullRequest
from requests import HTTPError

from ..base import BitbucketCloudBase


class Pipelines(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(Pipelines, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        return Pipeline(
            self.url_joiner(self.url, data["uuid"]),
            data,
            **self._new_session_args
        )  # fmt: skip

    def trigger(self, branch="master", type="custom", commit=None, pattern=None, variables=None):
        """
        Trigger a new pipeline. The following options are possible (1 and 2
        trigger the pipeline that the branch is associated with in the Pipelines
        configuration):

        1. Latest revision of a branch (specify ``branch``)
        2. Specific commit on a branch (additionally specify ``commit``)
        3. Specific pipeline (additionally specify ``pattern``. ``commit`` is optional here)

        Variables have to be a list of dictionaries:

        {
           "key": "var1key",
           "value": "var1value",
           "secured": true
        },

        :return: The initiated Pipeline object

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pipelines/#post
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
                "type": type,
                "hash": commit,
            }
        if pattern is not None:
            data["target"]["selector"] = {
                "type": "custom",
                "pattern": pattern,
            }
        if variables is not None:
            data["variables"] = variables

        return self.__get_object(self.post(None, trailing=True, data=data))

    def each(self, q=None, sort=None):
        """
        Returns the list of pipelines in this repository.

        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the Pipeline objects

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pipelines/#get
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        for pipeline in self._get_paged(
            None,
            trailing=True,
            paging_workaround=True,
            params=params,
        ):
            yield self.__get_object(pipeline)

        return

    def get(self, uuid):
        """
        Returns the pipeline with the uuid in this repository.

        :param uuid: string: The requested pipeline uuid

        :return: The requested Pipeline objects

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pipelines/%7Bpipeline_uuid%7D#get
        """
        return self.__get_object(super(Pipelines, self).get(uuid))


class Pipeline(BitbucketCloudBase):
    def __init__(self, url, data, *args, **kwargs):
        super(Pipeline, self).__init__(url, *args, data=data, expected_type="pipeline", **kwargs)

    def __get_object(self, data):
        return Step(
            f"{self.url}/steps/{data['uuid']}",
            data,
            **self._new_session_args
        )  # fmt: skip

    @property
    def uuid(self):
        """The pipeline uuid"""
        return self.get_data("uuid")

    @property
    def build_number(self):
        """The pipeline build number"""
        return self.get_data("build_number")

    @property
    def build_seconds_used(self):
        """The pipeline duration in seconds"""
        return self.get_data("build_seconds_used")

    @property
    def created_on(self):
        """The pipeline creation time"""
        return self.get_time("created_on")

    @property
    def completed_on(self):
        """The pipeline completion time"""
        return self.get_time("completed_on")

    @property
    def pullrequest(self):
        """Returns a PullRequest object if the pipeline was triggered by a pull request, else None"""
        target = self.get_data("target")
        if target["type"] == "pipeline_pullrequest_target":
            return PullRequest(
                target["pullrequest"]["links"]["self"]["href"],
                target["pullrequest"],
                **self._new_session_args
            )  # fmt: skip
        else:
            return None

    def stop(self):
        """
        Stop the pipeline

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pipelines/%7Bpipeline_uuid%7D/stopPipeline#post
        """
        return self.post("stopPipeline")

    def steps(self):
        """
        Get the pipeline steps.

        :return: A generator for the pipeline steps objects

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pipelines/%7Bpipeline_uuid%7D/steps/#get
        """
        for step in self._get_paged("steps", trailing=True):
            yield self.__get_object(step)

        return

    def step(self, uuid):
        """
        Get a specific pipeline step with the uuid.

        :return: The requested pipeline step objects

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pipelines/%7Bpipeline_uuid%7D/steps/%7Bstep_uuid%7D#get
        """
        return self.__get_object(self.get(f"steps/{uuid}"))


class Step(BitbucketCloudBase):
    def __init__(self, url, data, *args, **kwargs):
        super(Step, self).__init__(url, *args, data=data, expected_type="pipeline_step", **kwargs)

    @property
    def uuid(self):
        """The step uuid"""
        return self.get_data("uuid")

    @property
    def run_number(self):
        """The run number"""
        return self.get_data("run_number")

    @property
    def started_on(self):
        """The step start time"""
        return self.get_time("started_on")

    @property
    def completed_on(self):
        """The step end time"""
        return self.get_time("completed_on")

    @property
    def duration_in_seconds(self):
        """The step duration in seconds"""
        return self.get_data("duration_in_seconds")

    @property
    def state(self):
        """The step state"""
        return self.get_data("state")

    @property
    def setup_commands(self):
        """The step setup commands"""
        return self.get_data("setup_commands")

    @property
    def script_commands(self):
        """The step script commands"""
        return self.get_data("script_commands")

    def log(self, start=None, end=None):
        """
        Returns the log content in the given range.

        :param start: int: The start of the range. First element is 0.
        :param end: int: The end of the range, must be greater than start.

        :return: The byte representation of the log or if range is given a tuple with
                 the overall size and the byte representation of the requested range.

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pipelines/%7Bpipeline_uuid%7D/steps/%7Bstep_uuid%7D/log#get
        """
        headers = {"Accept": "application/octet-stream"}
        if ((start is not None) and (end is None)) or ((start is None) and (end is not None)):
            raise ValueError("For a range [start] and [end] are needed.")
        if start is not None:
            start = int(start)
            end = int(end)
            if (start >= 0) and (start < end):
                headers["Range"] = f"bytes={start}-{end}"
            else:
                raise ValueError("Value of [start] must be o or greater and [end] must be greater than [start].")

        response = None
        try:
            response = self.get("log", headers=headers, advanced_mode=True)
            response.raise_for_status()
        except HTTPError as e:
            # A 404 indicates that no log is present.
            if not e.response.status_code == 404:
                # Rethrow the exception
                raise
            return None

        if response is None:
            if start is None:
                return None
            return None, None

        if start is None:
            return response.content
        return (
            response.headers["Content-Range"].split("/")[1],
            response.content,
        )
