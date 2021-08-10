# coding: utf8
import io
import pytest
import sys
import zipfile

from atlassian.bitbucket.server import Server

BITBUCKET = None
try:
    from .mockup import mockup_server

    BITBUCKET = Server(
        "{}/bitbucket/server".format(mockup_server()), username="username", password="password", cloud=True
    )
except ImportError:
    pass


@pytest.mark.skipif(sys.version_info < (3, 4), reason="requires python3.4")
class TestBasic:
    def test_global_permissions(self):
        result = list(BITBUCKET.groups.each())
        assert [x.name for x in result] == ["group_a", "group_b", "group_c", "group_d"], "Each global group"
        assert [x.permission for x in result] == [
            "SYS_ADMIN",
            "ADMIN",
            "PROJECT_CREATE",
            "LICENSED_USER",
        ], "The group permission"
        assert [x.is_sys_admin for x in result] == [True, False, False, False], "Is sys admin group"
        assert [x.is_admin for x in result] == [False, True, False, False], "Is admin group"
        assert [x.is_project_create for x in result] == [False, False, True, False], "Is project create group"
        assert [x.is_licensed_user for x in result] == [False, False, False, True], "Is licenced group"

        result = list(BITBUCKET.groups.each_none())
        assert [x.name for x in result] == ["group_a_1", "group_b_1"], "Each none global group"

        group = BITBUCKET.groups.get("group_a")
        assert group.name == "group_a", "Get a group"
        assert group.delete() == {}, "Delete a group"

        result = list(BITBUCKET.users.each())
        assert [x.permission for x in result] == [
            "SYS_ADMIN",
            "ADMIN",
            "PROJECT_CREATE",
            "LICENSED_USER",
        ], "The user permission"
        assert [x.name for x in result] == ["jcitizen1", "jcitizen2", "jcitizen3", "jcitizen4"], "Each global user"
        assert [x.email for x in result] == [
            "jane1@example.com",
            "jane2@example.com",
            "jane3@example.com",
            "jane4@example.com",
        ], "Each global user email"
        assert [x.displayname for x in result] == [
            "Jane Citizen 1",
            "Jane Citizen 2",
            "Jane Citizen 3",
            "Jane Citizen 4",
        ], "Each global user display name"
        assert [x.active for x in result] == [True, True, False, False], "Each global user active flag"
        assert [x.slug for x in result] == [
            "jcitizen1_slug",
            "jcitizen2_slug",
            "jcitizen3_slug",
            "jcitizen4_slug",
        ], "Each global user slug"
        assert [x.id for x in result] == [101, 102, 103, 104], "Each global user id"
        assert [x.is_sys_admin for x in result] == [True, False, False, False], "Is sys admin user"
        assert [x.is_admin for x in result] == [False, True, False, False], "Is admin user"
        assert [x.is_project_create for x in result] == [False, False, True, False], "Is project create user"
        assert [x.is_licensed_user for x in result] == [False, False, False, True], "Is licensed user"

        result = list(BITBUCKET.users.each_none())
        assert [x.name for x in result] == ["jcitizen1_1"], "Each none global user"

        user = BITBUCKET.users.get("jcitizen1")
        assert user.name == "jcitizen1", "Get a user"
        assert user.delete() == {}, "Delete a user"

    def test_projects(self):
        assert not BITBUCKET.projects.exists("PRJxxx"), "Not exists project by key"
        assert BITBUCKET.projects.exists("PRJ"), "Exists project by key"
        result = list(BITBUCKET.projects.each())
        assert [x.key for x in result] == ["PRJ", "PRJ1"], "Each project keys"
        assert [x.description for x in result] == [
            "The description for my cool project.",
            "The description for my cool project 1.",
        ], "Each project description"

        assert not BITBUCKET.projects.exists("PRJxxx"), "Not exists project by key"
        assert BITBUCKET.projects.exists("PRJ"), "Exists project by key"
        project = BITBUCKET.projects.get("PRJ")
        assert project.name == "My Cool Project", "Get project by key"
        assert not BITBUCKET.projects.exists("My Cool Project xxx", by="name"), "Not exists project by name"
        assert BITBUCKET.projects.exists("My Cool Project", by="name"), "Exists project by name"
        project = BITBUCKET.projects.get("My Cool Project", by="name")
        assert project.key == "PRJ", "Get project by name"

        assert project.id == 1, "The project id"
        assert project.type == "NORMAL", "The project type"
        assert project.name == "My Cool Project", "The project name"
        project.name = "New name"
        assert project.name == "New name", "Update the project name"

        assert project.description == "The description for my cool project.", "The project description"
        project.description = "New description."
        assert project.description == "New description.", "Update the project description"

        assert project.public is True, "The project public flag"
        project.public = False
        assert project.public is False, "Update the project public flag"

        assert project.key == "PRJ", "The project key"
        project.key = "NEWKEY"
        assert project.key == "NEWKEY", "Update the project key"

    def test_project_permissions(self):
        project = BITBUCKET.projects.get("PRJ")

        result = list(project.groups.each())
        assert [x.permission for x in result] == ["ADMIN", "WRITE", "READ"], "Each permission of project group"
        assert [x.name for x in result] == ["group_a", "group_b", "group_c"], "Each project group name"
        assert [x.is_admin for x in result] == [True, False, False], "Is admin group"
        assert [x.is_write for x in result] == [False, True, False], "Is write group"
        assert [x.is_read for x in result] == [False, False, True], "Is read group"
        assert [x.can_write for x in result] == [True, True, False], "Can group write"

        result = list(project.groups.each_none())
        assert [x.name for x in result] == ["group_a_1", "group_b_1"], "Each none project group"

        group = project.groups.get("group_a")
        assert group.name == "group_a", "Get a group"
        assert group.delete() == {}, "Delete a group"

        result = list(project.users.each())
        assert [x.permission for x in result] == ["ADMIN", "WRITE", "READ"], "Each permission of project user"
        assert [x.name for x in result] == ["jcitizen1", "jcitizen2", "jcitizen3"], "Each project user name"
        assert [x.email for x in result] == [
            "jane1@example.com",
            "jane2@example.com",
            "jane3@example.com",
        ], "Each project user email"
        assert [x.displayname for x in result] == [
            "Jane Citizen 1",
            "Jane Citizen 2",
            "Jane Citizen 3",
        ], "Each project user display name"
        assert [x.active for x in result] == [True, True, False], "Each project user active flag"
        assert [x.slug for x in result] == [
            "jcitizen1_slug",
            "jcitizen2_slug",
            "jcitizen3_slug",
        ], "Each project user slug"
        assert [x.id for x in result] == [101, 102, 103], "Each project user id"
        assert [x.is_admin for x in result] == [True, False, False], "Is admin user"
        assert [x.is_write for x in result] == [False, True, False], "Is write user"
        assert [x.is_read for x in result] == [False, False, True], "Is read user"
        assert [x.can_write for x in result] == [True, True, False], "Can user write"

        result = list(project.users.each_none())
        assert [x.name for x in result] == ["jcitizen1_1"], "Each none project user"

        user = project.users.get("jcitizen1")
        assert user.name == "jcitizen1", "Get a user"
        assert user.delete() == {}, "Delete a user"

    def test_repositories(self):
        project = BITBUCKET.projects.get("PRJ")
        result = list(project.repos.each())
        assert [x.name for x in result] == ["My repo 1", "My repo 2", "My repo 3"], "Each repo name"
        assert [x.description for x in result] == [
            "My repo 1 description",
            "My repo 2 description",
            "My repo 3 description",
        ], "Each repo description"

        print(list(project.repos.each()))

        assert project.repos.exists("my-repo1-slug"), "Repo exists by slug"

        repo = project.repos.get("my-repo1-slug")
        assert repo.name == "My repo 1", "The repo name by slug"
        assert repo.id == 1, "The repo id"

        repo = project.repos.get("My repo 1", by="name")
        assert repo.name == "My repo 1", "The repo name"
        repo.name = "New name"
        assert repo.name == "New name", "Update the repo name"

        assert repo.slug == "my-repo1-slug", "The repo slug"

        assert repo.description == "My repo 1 description", "The repo description"
        repo.description = "New description."
        assert repo.description == "New description.", "Update the repo description"

        assert repo.public is True, "The repo public flag"
        repo.public = False
        assert repo.public is False, "Update the repo public flag"

        assert repo.forkable is True, "The repo forkable flag"
        repo.forkable = False
        assert repo.forkable is False, "Update the repo forkable flag"

        assert repo.contributing() == "Test contributing.md", "The contributing.md"
        assert repo.contributing(at="CommitId") == "Test contributing.md at CommitId", "The contributing.md at CommitId"
        assert (
            repo.contributing(at="CommitId", markup=True) == "<p>Test rendered contributing.md at CommitId</p>"
        ), "The rendered contributing.md at CommitId"

        assert repo.license() == "Test license.md", "The license.md"
        assert repo.license(at="CommitId") == "Test license.md at CommitId", "The license.md at CommitId"
        assert (
            repo.license(at="CommitId", markup=True) == "<p>Test rendered license.md at CommitId</p>"
        ), "The rendered license.md at CommitId"

        assert repo.readme() == "Test readme.md", "The readme.md"
        assert repo.readme(at="CommitId") == "Test readme.md at CommitId", "The readme.md at CommitId"
        assert (
            repo.readme(at="CommitId", markup=True) == "<p>Test rendered readme.md at CommitId</p>"
        ), "The rendered readme.md at CommitId"

        assert repo.default_branch == "main", "The default branch"
        repo.default_branch = "maint/relx"

        assert [x["hierarchyId"] for x in repo.forks()] == ["e3c939f9ef4a7fae272e"], "The forks"

        assert [x.id for x in repo.related()] == [2], "The related repositories"

    def test_repository_permissions(self):
        repo = BITBUCKET.projects.get("PRJ").repos.get("my-repo1-slug")

        result = list(repo.groups.each())
        assert [x.permission for x in result] == ["ADMIN", "WRITE", "READ"], "Each permission of repo group"
        assert [x.name for x in result] == ["group_a", "group_b", "group_c"], "Each repo group name"
        assert [x.is_admin for x in result] == [True, False, False], "Is admin group"
        assert [x.is_write for x in result] == [False, True, False], "Is write group"
        assert [x.is_read for x in result] == [False, False, True], "Is read group"
        assert [x.can_write for x in result] == [True, True, False], "Can group write"

        result = list(repo.groups.each_none())
        assert [x.name for x in result] == ["group_a_1", "group_b_1"], "Each none repo group"

        group = repo.groups.get("group_a")
        assert group.name == "group_a", "Get a group"
        assert group.delete() == {}, "Delete a group"

        result = list(repo.users.each())
        assert [x.permission for x in result] == ["ADMIN", "WRITE", "READ"], "Each permission of repo user"
        assert [x.name for x in result] == ["jcitizen1", "jcitizen2", "jcitizen3"], "Each repo user name"
        assert [x.email for x in result] == [
            "jane1@example.com",
            "jane2@example.com",
            "jane3@example.com",
        ], "Each repo user email"
        assert [x.displayname for x in result] == [
            "Jane Citizen 1",
            "Jane Citizen 2",
            "Jane Citizen 3",
        ], "Each repo user display name"
        assert [x.active for x in result] == [True, True, False], "Each repo user active flag"
        assert [x.slug for x in result] == ["jcitizen1_slug", "jcitizen2_slug", "jcitizen3_slug"], "Each repo user slug"
        assert [x.id for x in result] == [101, 102, 103], "Each repo user id"
        assert [x.is_admin for x in result] == [True, False, False], "Is admin user"
        assert [x.is_write for x in result] == [False, True, False], "Is write user"
        assert [x.is_read for x in result] == [False, False, True], "Is read user"
        assert [x.can_write for x in result] == [True, True, False], "Can user write"

        result = list(repo.users.each_none())
        assert [x.name for x in result] == ["jcitizen1_1"], "Each none repo user"

        user = repo.users.get("jcitizen1")
        assert user.name == "jcitizen1", "Get a user"
        assert user.delete() == {}, "Delete a user"

    def test_download_repo_archive(self):
        repo = BITBUCKET.projects.get("PRJ").repos.get("my-repo1-slug")
        with io.BytesIO() as buf:
            repo.download_archive(buf)
            with zipfile.ZipFile(buf) as archive:
                assert archive.namelist() == ["readme.md"]
                with archive.open("readme.md") as file_in_archive:
                    assert file_in_archive.read() == b"Test readme.md"

        with io.BytesIO() as buf:
            repo.download_archive(buf, at="CommitId")
            with zipfile.ZipFile(buf) as archive:
                assert archive.namelist() == ["readme.md"]
                with archive.open("readme.md") as file_in_archive:
                    assert file_in_archive.read() == b"Test readme.md at CommitId"
