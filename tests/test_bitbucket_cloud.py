# coding: utf8
import os
import requests
import pytest
import sys

from atlassian import Bitbucket

BITBUCKET = None
try:
    from .mockup import mockup_server

    BITBUCKET = Bitbucket(
        "{}/bitbucket/cloud".format(mockup_server()), username="username", password="password", cloud=True
    )
except ImportError:
    pass


class TestBasic:
    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_get_repositories(self):
        result = [x["name"] for x in BITBUCKET.get_repositories("TestWorkspace1")]
        assert result == ["testrepository1", "testrepository2"], "Result of [get_repositories(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_get_pipelines(self):
        result = [x["uuid"] for x in BITBUCKET.get_pipelines("TestWorkspace1", "testrepository1")]
        assert result == ["{PipelineUuid}"], "Result of [get_pipelines(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_trigger_pipeline(self):
        result = BITBUCKET.trigger_pipeline("TestWorkspace1", "testrepository1")
        assert result["uuid"] == "{PipelineUuid}", "Result of [trigger_pipeline(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_get_pipeline(self):
        result = BITBUCKET.get_pipeline("TestWorkspace1", "testrepository1", "{PipelineUuid}")
        assert result["state"]["name"] == "COMPLETED", "Result of [get_pipeline(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_stop_pipeline(self):
        result = BITBUCKET.stop_pipeline("TestWorkspace1", "testrepository1", "{PipelineUuid}")
        assert result == {}, "Result of [stop_pipeline(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_get_pipeline_steps(self):
        result = [
            x["uuid"] for x in BITBUCKET.get_pipeline_steps("TestWorkspace1", "testrepository1", "{PipelineUuid}")
        ]
        assert result == ["{PipelineStep1Uuid}", "{PipelineStep2Uuid}"], "Result of [get_pipeline_steps(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_get_pipeline_step(self):
        result = BITBUCKET.get_pipeline_step(
            "TestWorkspace1", "testrepository1", "{PipelineUuid}", "{PipelineStep1Uuid}"
        )
        assert result["uuid"] == "{PipelineStep1Uuid}", "Result of [get_pipeline_step(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_get_pipeline_step_log_1(self):
        result = BITBUCKET.get_pipeline_step_log(
            "TestWorkspace1", "testrepository1", "{PipelineUuid}", "{PipelineStep1Uuid}"
        )
        assert result == None, "Result of step1 [get_pipeline_step_log(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_get_pipeline_step_log_2(self):
        result = BITBUCKET.get_pipeline_step_log(
            "TestWorkspace1", "testrepository1", "{PipelineUuid}", "{PipelineStep2Uuid}"
        )
        assert result == b"Log content", "Result of step2 [get_pipeline_step_log(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_get_issues(self):
        result = [x["title"] for x in BITBUCKET.get_issues("TestWorkspace1", "testrepository1")]
        assert result == ["First issue", "Second issue"], "Result of [get_issues(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_create_issue(self):
        result = BITBUCKET.create_issue("TestWorkspace1", "testrepository1", "Title", "Description", "bug", "minor")[
            "content"
        ]["raw"]
        assert result == "Description", "Result of [create_issue(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_get_issue(self):
        result = BITBUCKET.get_issue("TestWorkspace1", "testrepository1", 3)["kind"]
        assert result == "bug", "Result of [get_issue(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_update_issue(self):
        result = BITBUCKET.update_issue("TestWorkspace1", "testrepository1", 3, kind="enhancement")["kind"]
        assert result == "enhancement", "Result of [update_issue(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_delete_issue(self):
        result = BITBUCKET.delete_issue("TestWorkspace1", "testrepository1", 3)["title"]
        assert result == "Title deleted issue", "Result of [get_issue(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_get_branch_restrictions(self):
        result = [x["kind"] for x in BITBUCKET.get_branch_restrictions("TestWorkspace1", "testrepository1")]
        assert result == [
            "delete",
            "force",
            "delete",
            "restrict_merges",
            "push",
        ], "Result of [get_branch_restrictions(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_update_branch_restriction(self):
        result = BITBUCKET.update_branch_restriction("TestWorkspace1", "testrepository1", 17203842, branch="master")[
            "pattern"
        ]
        assert result == "master", "Result of [update_branch_restrictions(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_delete_branch_restriction(self):
        result = BITBUCKET.delete_branch_restriction("TestWorkspace1", "testrepository1", 17203842)["pattern"]
        assert result == "deleted_branch", "Result of [update_branch_restrictions(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_get_default_reviewers(self):
        result = [x["display_name"] for x in BITBUCKET.get_default_reviewers("TestWorkspace1", "testrepository1")]
        assert result == ["DefaultReviewer1"], "Result of [get_default_reviewers(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_is_default_reviewer(self):
        result = BITBUCKET.is_default_reviewer("TestWorkspace1", "testrepository1", "DefaultReviewerNo")
        assert result == False, "Result of [is_default_reviewer(...)]"
        result = BITBUCKET.is_default_reviewer("TestWorkspace1", "testrepository1", "DefaultReviewer1")
        assert result == True, "Result of [is_default_reviewer(...)]"

    @pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
    def test_delete_default_reviewer(self):
        result = BITBUCKET.delete_default_reviewer("TestWorkspace1", "testrepository1", "DefaultReviewer1")["nickname"]
        assert result == "DefaultReviewer1Nickname", "Result of [delete_default_reviewer(...)]"
