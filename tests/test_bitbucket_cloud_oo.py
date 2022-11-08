# coding: utf8
from atlassian.bitbucket.cloud.repositories import WorkspaceRepositories
import pytest
import sys
from datetime import datetime

from atlassian import Bitbucket
from atlassian.bitbucket import Cloud
from atlassian.bitbucket.cloud.common.users import User
from atlassian.bitbucket.cloud.repositories.pullRequests import Comment, Participant, PullRequest, Build, Task

BITBUCKET = None
try:
    from .mockup import mockup_server

    BITBUCKET = Bitbucket(
        "{}/bitbucket/cloud".format(mockup_server()), username="username", password="password", cloud=True
    )
    CLOUD = Cloud("{}/bitbucket/cloud".format(mockup_server()), username="username", password="password")
except ImportError:
    pass


def _datetimetostr(dtime):
    # convert datetime object to str because datetime.timezone is not available in py27
    # doesn't work on py27: datetime(2020, 12, 27, 14, 9, 14, 660262, tzinfo=timezone.utc)
    return dtime.strftime("%Y-%m-%d %H:%M:%S.%f")


@pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
class TestBasic:
    def test_exists_workspace(self):
        assert CLOUD.workspaces.exists("TestWorkspace1"), "Exists workspace"

    def test_not_exists_workspace(self):
        assert not CLOUD.workspaces.exists("TestWorkspace1xxx"), "Not exists workspace"

    def test_not_exists_project(self):
        assert not CLOUD.workspaces.get("TestWorkspace1").projects.exists("pr1"), "Not exists repository"

    def test_exists_repository(self):
        assert CLOUD.workspaces.get("TestWorkspace1").repositories.exists("testrepository1"), "Exists repository"

    def test_not_exists_repository(self):
        assert not CLOUD.workspaces.get("TestWorkspace1").repositories.exists(
            "testrepository1xxx"
        ), "Not exists repository"

    def test_create_repositories(self):
        result = CLOUD.workspaces.get("TestWorkspace1").repositories.create("TestRepositoryCreated")
        assert result.description == "Test newly created repository", "Result of repositories [create(...)]"
        result = CLOUD.workspaces.get("TestWorkspace1").repositories.create(
            "TestRepositoryCreated", "TEST1", fork_policy=WorkspaceRepositories.ALLOW_FORKS
        )
        assert result.fork_policy == "allow_forks", "Result of repositories [create(...)] with project and fork policy"

    def test_get_repositories(self):
        result = [x["name"] for x in BITBUCKET.get_repositories("TestWorkspace1")]
        assert result == ["testrepository1", "testrepository2"], "Result of [get_repositories(...)]"

    def test_get_pipelines(self):
        result = [x["uuid"] for x in BITBUCKET.get_pipelines("TestWorkspace1", "testrepository1")]
        assert result == ["{PipelineUuid}"], "Result of [get_pipelines(...)]"

    def test_trigger_pipeline(self):
        result = BITBUCKET.trigger_pipeline("TestWorkspace1", "testrepository1")
        assert result["uuid"] == "{PipelineUuid}", "Result of [trigger_pipeline(...)]"

    def test_get_pipeline(self):
        result = BITBUCKET.get_pipeline("TestWorkspace1", "testrepository1", "{PipelineUuid}")
        assert result["state"]["name"] == "COMPLETED", "Result of [get_pipeline(...)]"
        result = (
            CLOUD.workspaces.get("TestWorkspace1").repositories.get("testrepository1").pipelines.get("{PipelineUuid}")
        )
        assert result.get_data("state")["name"] == "COMPLETED", "Pipeline state"
        assert result.completed_on is None, "Pipeline completed time"

    def test_stop_pipeline(self):
        result = BITBUCKET.stop_pipeline("TestWorkspace1", "testrepository1", "{PipelineUuid}")
        assert result == {}, "Result of [stop_pipeline(...)]"

    def test_get_pipeline_steps(self):
        result = [
            x["uuid"] for x in BITBUCKET.get_pipeline_steps("TestWorkspace1", "testrepository1", "{PipelineUuid}")
        ]
        assert result == ["{PipelineStep1Uuid}", "{PipelineStep2Uuid}"], "Result of [get_pipeline_steps(...)]"

    def test_get_pipeline_step(self):
        result = BITBUCKET.get_pipeline_step(
            "TestWorkspace1", "testrepository1", "{PipelineUuid}", "{PipelineStep1Uuid}"
        )
        assert result["uuid"] == "{PipelineStep1Uuid}", "Result of [get_pipeline_step(...)]"

    def test_get_pipeline_step_log_1(self):
        """Test Not Found"""
        result = BITBUCKET.get_pipeline_step_log(
            "TestWorkspace1", "testrepository1", "{PipelineUuid}", "{PipelineStep1Uuid}"
        )
        assert result is None, "Result of step1 [get_pipeline_step_log(...)]"

    def test_get_pipeline_step_log_2(self):
        result = BITBUCKET.get_pipeline_step_log(
            "TestWorkspace1", "testrepository1", "{PipelineUuid}", "{PipelineStep2Uuid}"
        )
        assert result == b"Log content", "Result of step2 [get_pipeline_step_log(...)]"

    def test_get_issues(self):
        result = [x["title"] for x in BITBUCKET.get_issues("TestWorkspace1", "testrepository1")]
        assert result == ["First issue", "Second issue"], "Result of [get_issues(...)]"

    def test_create_issue(self):
        result = BITBUCKET.create_issue("TestWorkspace1", "testrepository1", "Title", "Description", "bug", "minor")[
            "content"
        ]["raw"]
        assert result == "Description", "Result of [create_issue(...)]"

    def test_get_issue(self):
        result = BITBUCKET.get_issue("TestWorkspace1", "testrepository1", 3)["kind"]
        assert result == "bug", "Result of [get_issue(...)]"

    def test_update_issue(self):
        result = BITBUCKET.update_issue("TestWorkspace1", "testrepository1", 3, kind="enhancement")["kind"]
        assert result == "enhancement", "Result of [update_issue(...)]"

    def test_delete_issue(self):
        result = BITBUCKET.delete_issue("TestWorkspace1", "testrepository1", 3)["title"]
        assert result == "Title deleted issue", "Result of [get_issue(...)]"

    def test_get_branch_restrictions(self):
        result = [x["kind"] for x in BITBUCKET.get_branch_restrictions("TestWorkspace1", "testrepository1")]
        assert result == [
            "delete",
            "force",
            "delete",
            "restrict_merges",
            "push",
        ], "Result of [get_branch_restrictions(...)]"

    def test_update_branch_restriction(self):
        result = BITBUCKET.update_branch_restriction("TestWorkspace1", "testrepository1", 17203842, branch="master")[
            "pattern"
        ]
        assert result == "master", "Result of [update_branch_restrictions(...)]"

    def test_delete_branch_restriction(self):
        result = BITBUCKET.delete_branch_restriction("TestWorkspace1", "testrepository1", 17203842)["pattern"]
        assert result == "deleted_branch", "Result of [update_branch_restrictions(...)]"

    def test_get_default_reviewers(self):
        result = [x["display_name"] for x in BITBUCKET.get_default_reviewers("TestWorkspace1", "testrepository1")]
        assert result == ["DefaultReviewer1"], "Result of [get_default_reviewers(...)]"

    def test_is_default_reviewer(self):
        result = BITBUCKET.is_default_reviewer("TestWorkspace1", "testrepository1", "DefaultReviewerNo")
        assert result is False, "Result of [is_default_reviewer(...)]"
        result = BITBUCKET.is_default_reviewer("TestWorkspace1", "testrepository1", "DefaultReviewer1Uuid")
        assert result is True, "Result of [is_default_reviewer(...)]"

    def test_delete_default_reviewer(self):
        result = BITBUCKET.delete_default_reviewer("TestWorkspace1", "testrepository1", "DefaultReviewer1Uuid")[
            "account_id"
        ]
        assert result == "DefaultReviewer1AccountId", "Result of [delete_default_reviewer(...)]"


@pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
class TestPullRequests:
    @pytest.fixture(scope="module")
    def tc1(self):
        return CLOUD.workspaces.get("TestWorkspace1").repositories.get("testrepository1").pullrequests.get(1)

    @pytest.fixture(scope="module")
    def tc2(self):
        return CLOUD.workspaces.get("TestWorkspace1").repositories.get("testrepository1").pullrequests

    def test_id(self, tc1):
        assert tc1.id == 1

    def test_title(self, tc1):
        assert tc1.title == "PRTitle"

    def test_description(self, tc1):
        assert tc1.description == "PRDescription"

    def test_is_declined(self, tc1):
        assert not tc1.is_declined

    def test_is_merged(self, tc1):
        assert not tc1.is_merged

    def test_is_open(self, tc1):
        assert tc1.is_open

    def test_is_superseded(self, tc1):
        assert not tc1.is_superseded

    def test_created_on(self, tc1):
        assert _datetimetostr(tc1.created_on) == _datetimetostr(datetime(2020, 3, 19, 12, 0, 3, 494356))

    def test_updated_on(self, tc1):
        assert _datetimetostr(tc1.updated_on) == _datetimetostr(datetime(2020, 12, 27, 14, 9, 14, 660262))

    def test_close_source_branch(self, tc1):
        assert tc1.close_source_branch

    def test_source_branch(self, tc1):
        assert tc1.source_branch == "feature/test-branch"

    def test_destination_branch(self, tc1):
        assert tc1.destination_branch == "master"

    def test_comment_count(self, tc1):
        assert tc1.comment_count == 5

    def test_task_count(self, tc1):
        assert tc1.task_count == 0

    def test_declined_reason(self, tc1):
        assert not tc1.declined_reason

    def test_author(self, tc1):
        assert isinstance(tc1.author, User)
        assert tc1.author.display_name == "User03DisplayName"
        assert tc1.author.uuid == "{User03UUID}"
        assert tc1.author.account_id == "User03AccountID"
        assert tc1.author.nickname == "User03Nickname"
        assert tc1.author.avatar == "users/%7BUser03UUID%7D.png"

    def test_participants(self, tc1):
        participants = list(tc1.participants())
        assert len(participants) == 5

        p1 = participants[1]
        assert isinstance(p1, Participant)
        assert isinstance(p1.user, User)
        print(p1)
        assert p1.user.display_name == "User03DisplayName"
        assert p1.user.uuid == "{User03UUID}"
        assert p1.user.account_id == "User03AccountID"
        assert p1.user.nickname == "User03Nickname"
        assert p1.user.avatar == "users/%7BUser03UUID%7D.png"

        assert _datetimetostr(p1.participated_on) == _datetimetostr(datetime(2020, 7, 9, 7, 0, 54, 416331))
        assert p1.is_participant
        assert not p1.is_reviewer
        assert not p1.has_approved
        assert not p1.has_changes_requested

        p2 = participants[2]
        assert p2.has_approved
        assert p2.is_reviewer
        assert not p2.is_participant
        assert not p2.has_changes_requested

        p3 = participants[3]
        assert not p3.has_approved
        assert p3.is_reviewer
        assert not p3.is_participant
        assert p3.has_changes_requested

    def test_reviewers(self, tc1):
        reviewers = list(tc1.reviewers())
        assert len(reviewers) == 3
        assert isinstance(reviewers[0], User)

    def test_comment(self, tc1):
        msg = "hello world"
        com = tc1.comment(msg)
        assert com["type"] == "pullrequest_comment"
        assert com["content"]["raw"] == msg
        assert com["pullrequest"]["id"] == 1
        assert not com["deleted"]

    def test_comments(self, tc1):
        comments = list(tc1.comments())
        assert len(comments) == 2
        c1, c2 = comments
        assert isinstance(c1, Comment)
        assert isinstance(c2, Comment)
        assert c1.raw == "Test comment 1"
        assert isinstance(c1.user, User)
        assert c1.user.display_name == "User04DisplayName"
        assert c2.html == "<p>Test comment 2</p>"

    def test_add_task(self, tc1):
        msg = "ToDo 1"
        task = tc1.add_task(msg)
        assert isinstance(task, Task)
        assert task.id == 123456
        assert task.description == msg
        assert not task.is_resolved

        with pytest.raises(ValueError):
            tc1.add_task(None)

    def test_update_task(self, tc1):
        task = [t for t in tc1.tasks() if t.id == 123456][0]
        task = task.update("ToDo 10")
        assert task.description == "ToDo 10"

        with pytest.raises(ValueError):
            task.update(None)

    def test_delete_task(self, tc1):
        task = [t for t in tc1.tasks() if t.id == 123456][0]
        assert task.delete() is None

    def test_tasks(self, tc1):
        tasks = list(tc1.tasks())
        assert len(tasks) == 2
        t1, t2 = tasks
        assert isinstance(t1, Task)
        assert isinstance(t2, Task)
        assert t2.id == 123456
        assert t1.id == 234567
        assert not t2.is_resolved
        assert t1.is_resolved
        assert isinstance(t2.creator, User)
        assert isinstance(t1.resolved_by, User)
        assert t2.description == "ToDo 1"
        assert _datetimetostr(t1.resolved_on) == _datetimetostr(datetime(2021, 10, 19, 20, 28, 47, 493275))
        assert _datetimetostr(t2.created_on) == _datetimetostr(datetime(2021, 10, 19, 20, 20, 49, 288763))

    def test_approve(self, tc1):
        ap = tc1.approve()
        assert ap["approved"]
        assert ap["state"] == "approved"

    def test_unapprove(self, tc1):
        assert tc1.unapprove() is None

    def test_request_changes(self, tc1):
        rc = tc1.request_changes()
        assert rc["approved"] is False
        assert rc["state"] == Participant.CHANGES_REQUESTED

    def test_unrequest_changes(self, tc1):
        assert tc1.unrequest_changes() is None

    def test_decline(self, tc1):
        decline = tc1.decline()
        assert decline["type"] == "pullrequest"
        assert decline["state"] == PullRequest.STATE_DECLINED
        assert decline["merge_commit"] is None
        assert decline["closed_by"]["uuid"] == "{User04UUID}"

    def test_merge(self, tc1):
        merge = tc1.merge()
        assert merge["type"] == "pullrequest"
        assert merge["state"] == PullRequest.STATE_MERGED
        assert merge["closed_by"]["uuid"] == "{User04UUID}"
        assert merge["merge_commit"]["hash"] == "36bb9607a8c9e0c6222342486e3393ae154b46c0"

    def test_each(self, tc2):
        prs = list(tc2.each())
        assert len(prs) == 2
        assert isinstance(prs[0], PullRequest)
        assert prs[0].id == 1
        assert prs[1].id == 25
        assert len(list(prs[1].participants())) == 5

    def test_create(self, tc2):
        reviewers = ["{User04UUID}", "{User02UUID}", "{User01UUID}"]
        pr = tc2.create(
            title="PRTitle",
            source_branch="feature/test-branch",
            destination_branch="master",
            description="PRDescription",
            close_source_branch=True,
            reviewers=reviewers,
        )
        assert pr.id == 1
        assert len(list(pr.reviewers())) == 3

    def test_builds(self, tc1):
        builds = list(tc1.builds())
        assert len(builds) == 1

        build = builds[0]
        assert isinstance(build, Build)
        assert build.successful
        assert build.name == "Build #5"
        assert build.description == "This commit looks good."
        assert build.key == "12345"
        assert _datetimetostr(build.created_on) == _datetimetostr(datetime(2021, 1, 22, 14, 47, 16, 366063))
        assert build.commit == "1fbd047cd99a"
        assert build.refname == "feature/abranch"
        assert build.website == "http://urltothebui.ld/5"
