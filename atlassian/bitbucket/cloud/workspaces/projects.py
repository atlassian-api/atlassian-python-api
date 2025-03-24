# coding=utf-8

from requests import HTTPError
from ..base import BitbucketCloudBase

from ..repositories import ProjectRepositories


class Projects(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(Projects, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        return Project(data, **self._new_session_args)

    def create(self, name, key, description, is_private=True, avatar=None):
        """
        Creates a new project with the given values

        Note that the avatar has to be embedded as either a data-url or a URL to an external image as shown in
        the examples below:

            w.projects.create( "Mars Project", "MARS", "Software for colonizing mars.",
                avatar="data:image/gif;base64,R0lGODlhEAAQAMQAAORHHOVSKudfOulrSOp3WOyDZu6QdvCchPGolfO0o/...",
                is_private=False
            )

            w.projects.create( "Mars Project", "MARS", "Software for colonizing mars.",
                avatar="http://i.imgur.com/72tRx4w.gif",
                is_private=False
            )

        :param name: string:                       The name of the project.
        :param key: string:                        The key of the project.
        :param description: string:                The description of the project.
        :param is_private: bool (default is True): True if it is a private project.
        :param avatar: string (default is None):   The avatar of the project.

        :return: The created project object

        API docs:
            https://developer.atlassian.com/bitbucket/api/2/reference/resource/workspaces/%7Bworkspace%7D/projects#post
        """
        data = {
            "name": name,
            "key": key,
            "description": description,
            "is_private": is_private,
        }
        if avatar:
            data["avatar"] = avatar
        return self.__get_object(self.post(None, data=data))

    def each(self, q=None, sort=None):
        """
        Get all projects in the workspace matching the criteria.
        :param q: string (default is None):    Query string to narrow down the response.
                                               See for details:
                                               https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering
        :param sort: string (default is None): Name of a response property to sort results.
                                               See for details:
                                               https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering
        :return: A generator for the project objects

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/workspaces/%7Bworkspace%7D/projects#get
        """
        params = {}
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        for project in self._get_paged(None, params=params):
            yield self.__get_object(project)

        return

    def get(self, project, by="key"):
        """
        Returns the requested project

        :param project: string: The requested project.
        :param by: string (default is "key"): How to interpret project, can be 'key' or 'name'.

        :return: The requested Project object

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/workspaces/%7Bworkspace%7D/projects/%7Bproject_key%7D#get
        """
        if by == "key":
            return self.__get_object(super(Projects, self).get(project))
        elif by == "name":
            for p in self.each():
                if p.name == project:
                    return p
        else:
            ValueError(f"Unknown value '{by}' for argument [by], expected 'key' or 'name'")

        raise Exception(f"Unknown project {by} '{project}'")

    def exists(self, project, by="key"):
        """
        Check if project exist.

        :param project: string: The requested project.
        :param by: string (default is "key"): How to interpret project, can be 'key' or 'name'.

        :return: True if the project exists

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/workspaces/%7Bworkspace%7D/projects/%7Bproject_key%7D#get
        """
        exists = False
        try:
            self.get(project, by)
            exists = True
        except HTTPError as e:
            if e.response.status_code in (401, 404):
                pass
        except Exception as e:
            if not str(e) == f"Unknown project {by} '{project}'":
                raise e
        return exists


class Project(BitbucketCloudBase):
    def __init__(self, data, *args, **kwargs):
        super(Project, self).__init__(None, *args, data=data, expected_type="project", **kwargs)
        try:
            url = self.get_link("repositories")
        except KeyError:
            workspace = self.get_data("workspace")
            url = f'{workspace["links"]["self"]}/?q=project.key="{workspace["slug"]}"'
        self.__repositories = ProjectRepositories(url, **self._new_session_args)

    def update(self, **kwargs):
        """
        Update the project properties. Fields not present in the request body are ignored.

        :param kwargs: dict: The data to update.

        :return: The updated project

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/workspaces/%7Bworkspace%7D/projects/%7Bproject_key%7D#put
        """
        return self._update_data(self.put(None, data=kwargs))

    def delete(self):
        """
        Delete the project.

        :return: The response on success

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/workspaces/%7Bworkspace%7D/projects/%7Bproject_key%7D#delete
        """
        data = super(Project, self).delete(None)
        if data is None or "errors" in data:
            return
        return data

    @property
    def name(self):
        """The project name"""
        return self.get_data("name")

    @name.setter
    def name(self, name):
        """Setter for the project name"""
        return self.update(name=name)

    @property
    def key(self):
        """The project key"""
        return self.get_data("key")

    @key.setter
    def key(self, key):
        """Setter for the project key"""
        return self.update(key=key)

    @property
    def description(self):
        """The project description"""
        return self.get_data("description")

    @description.setter
    def description(self, description):
        """Setter for the project description"""
        return self.update(description=description)

    @property
    def is_private(self):
        """The project private flag"""
        return self.get_data("is_private")

    @is_private.setter
    def is_private(self, is_private):
        """Setter for the project private flag"""
        return self.update(is_private=is_private)

    @property
    def created_on(self):
        """The project creation time"""
        return self.get_data("created_on")

    @property
    def updated_on(self):
        """The project last update time"""
        return self.get_data("updated_on", "never updated")

    def get_avatar(self):
        """The project avatar"""
        return self.get(self.get_link("avatar"), absolute=True)

    @property
    def repositories(self):
        """The project repositories"""
        return self.__repositories
