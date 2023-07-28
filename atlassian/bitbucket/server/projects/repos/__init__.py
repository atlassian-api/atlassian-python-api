# coding=utf-8

from requests import HTTPError
from ...base import BitbucketServerBase
from ...common.permissions import Groups, Users


class Repositories(BitbucketServerBase):
    def __init__(self, url, *args, **kwargs):
        super(Repositories, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        return Repository(data, **self._new_session_args)

    def create(self, name):
        """
        Creates a new repository with the given name.

        See https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp174

        :param name: string: The name of the project.

        :return: The created project object
        """
        return self.__get_object(self.post(None, data={"name": name}))

    def each(self):
        """
        Get all repositories.

        See https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp175

        :return: A generator for the Repository objects
        """
        for repository in self._get_paged(None):
            yield self.__get_object(repository)

    def get(self, repository, by="slug"):
        """
        Returns the requested repository.

        :param repository: string: The requested repository.
        :param by: string (default is "slug"): How to interpret project, can be 'slug' or 'name'.

        :return: The requested Repository object
        """
        if by == "slug":
            return self.__get_object(super(Repositories, self).get(repository))
        elif by == "name":
            for r in self.each():
                print(r.name)
                if r.name == repository:
                    return r
        else:
            ValueError("Unknown value '{}' for argument [by], expected 'slug' or 'name'".format(by))

        raise Exception("Unknown repository {} '{}'".format(by, repository))

    def exists(self, repository, by="slug"):
        """
        Check if repository exist.

        :param repository: string: The requested repository.
        :param by: string (default is "slug"): How to interpret repository, can be 'slug' or 'name'.

        :return: True if the repository exists
        """
        exists = False
        try:
            self.get(repository, by)
            exists = True
        except HTTPError as e:
            if e.response.status_code in (401, 404):
                pass
        except Exception as e:
            if not str(e) == "Unknown project {} '{}'".format(by, repository):
                raise e
        return exists


class Repository(BitbucketServerBase):
    def __init__(self, data, *args, **kwargs):
        super(Repository, self).__init__(None, *args, data=data, **kwargs)
        self.__groups = Groups(
            self._sub_url("permissions/groups"),
            "REPO",
            **self._new_session_args
        )  # fmt: skip
        self.__users = Users(
            self._sub_url("permissions/users"),
            "REPO",
            **self._new_session_args
        )  # fmt: skip

    def __get_object(self, data):
        return Repository(data, **self._new_session_args)

    def update(self, **kwargs):
        """
        Update the repository properties. Fields not present in the request body are ignored.

        :param kwargs: dict: The data to update.

        :return: The updated repository

        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp180
        """
        return self._update_data(self.put(None, data=kwargs))

    def delete(self):
        """
        Delete the repostory.

        :return: The response on success

        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp177
        """
        return super(Repository, self).delete(None)

    @property
    def id(self):
        """The repository identifier"""
        return self.get_data("id")

    @property
    def name(self):
        """The repository name"""
        return self.get_data("name")

    @name.setter
    def name(self, name):
        """Setter for the repository name"""
        return self.update(name=name)

    @property
    def slug(self):
        """The repository slug"""
        return self.get_data("slug")

    @property
    def description(self):
        """The repository description"""
        return self.get_data("description")

    @description.setter
    def description(self, description):
        """Setter for the repository description"""
        return self.update(description=description)

    @property
    def public(self):
        """The repository public flag"""
        return self.get_data("public")

    @public.setter
    def public(self, public):
        """Setter for the repository public flag"""
        return self.update(public=public)

    @property
    def forkable(self):
        """The repository forkable flag"""
        return self.get_data("forkable")

    @forkable.setter
    def forkable(self, forkable):
        """Setter for the repository forkable flag"""
        return self.update(forkable=forkable)

    def contributing(self, at=None, markup=None):
        """
        Get the contributing guidelines.

        :param at: string: Optional, the commit to get the contributing guideline from.
        :param markup: boolean: Optional, If set to true, the rendered content is returned as HTML.

        :return: The text content of the contributing guidlines.

        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp183
        """
        params = {}
        if at is not None:
            params["at"] = at
        if markup is True:
            params["markup"] = markup

        return self.get("contributing", params=params)

    def license(self, at=None, markup=None):
        """
        Get the license file.

        :param at: string: Optional, the commit to get the license file from.
        :param markup: boolean: Optional, If set to true, the rendered content is returned as HTML.

        :return: The text content of the license file.

        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp191
        """
        params = {}
        if at is not None:
            params["at"] = at
        if markup is True:
            params["markup"] = markup

        return self.get("license", params=params)

    def readme(self, at=None, markup=None):
        """
        Get the readme file.

        :param at: string: Optional, the commit to get the readme file from.
        :param markup: boolean: Optional, If set to true, the rendered content is returned as HTML.

        :return: The text content of the readme file.

        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp194
        """
        params = {}
        if at is not None:
            params["at"] = at
        if markup is True:
            params["markup"] = markup

        return self.get("readme", params=params)

    @property
    def default_branch(self):
        """
        Get the default branch.

        :return: The default branch (displayId without refs/heads/).

        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp185
        """
        return self.get("default-branch")["displayId"]

    @default_branch.setter
    def default_branch(self, branch):
        """
        Set the default branch.

        :param id: string: The default branch to set (without refs/heads/).

        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp186
        """
        self.put("default-branch", data={"id": "refs/heads/{}".format(branch)})

    def forks(self):
        """
        Get all forks.

        :return: A generator object for the forks.

        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp188
        """
        for fork in self._get_paged("forks"):
            yield fork

    def related(self):
        """
        Get all related repositories.

        :return: A generator for the related repository objects

        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp195
        """
        for repository in self._get_paged("related"):
            yield self.__get_object(repository)

    @property
    def groups(self):
        """
        Property to access the project groups:
        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp279
        """
        return self.__groups

    @property
    def users(self):
        """
        Property to access the project groups
        API docs: https://docs.atlassian.com/bitbucket-server/rest/7.8.0/bitbucket-rest.html#idp285
        """
        return self.__users

    def download_archive(
        self,
        dest_fd,
        at=None,
        filename=None,
        format=None,
        path=None,
        prefix=None,
        chunk_size=128,
    ):
        """
        Downloads a repository archive.
        Note that the data is written to the specified file-like object,
        rather than simply being returned.
        For further information visit:
           https://docs.atlassian.com/bitbucket-server/rest/7.13.0/bitbucket-rest.html#idp199
        :param dest_fd: a file-like object to which the archive will be written
        :param at: string: Optional, the commit to download an archive of; if not supplied, an archive of the default branch is downloaded
        :param filename: string: Optional, a filename to include the "Content-Disposition" header
        :param format: string: Optional, the format to stream the archive in; must be one of: zip, tar, tar.gz or tgz.
                        If not specified, then the archive will be in zip format.
        :param path: string: Optional, path to include in the streamed archive
        :param prefix: string: Optional, a prefix to apply to all entries in the streamed archive;
                        if the supplied prefix does not end with a trailing /, one will be added automatically
        :param chunk_size: int: Optional, download chunk size. Defeault is 128
        """
        params = {}
        if at is not None:
            params["at"] = at
        if filename is not None:
            params["filename"] = filename
        if format is not None:
            params["format"] = format
        if path is not None:
            params["path"] = path
        if prefix is not None:
            params["prefix"] = prefix
        headers = {"Accept": "*/*"}
        response = self.get("archive", params=params, headers=headers, advanced_mode=True)
        for chunk in response.iter_content(chunk_size=chunk_size):
            dest_fd.write(chunk)
