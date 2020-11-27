# coding=utf-8

from ..base import BitbucketCloudBase

from ..repositories import ProjectRepositories


class Projects(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(Projects, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        if "errors" in data:
            return
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

        :param name: string: The name of the project.
        :param key: string: The key of the project.
        :param description: string: The description of the project.
        :param is_private: boolean (True): True if it is a private project.
        :param avatar: string (None): The avatar of the project.

        :return: The created project object
        """
        data = {
            "name": name,
            "key": key,
            "description": description,
            "is_private": is_private,
        }
        return self.__get_object(self.post(None, data=data))

    def each(self, q=None, sort=None):
        """
        Get all projects in the workspace matching the criteria.


        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the project objects
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
        :param by: string: How to interprate project, can be 'key' or 'name'.

        :return: The requested Project object
        """
        if by == "key":
            return self.__get_object(super(Projects, self).get(project))
        elif by == "name":
            for p in self.each():
                if p.name == project:
                    return p
        else:
            ValueError("Unknown value '{}' for argument [by], expected 'key' or 'name'".format(by))

        raise Exception("Unknown project {} '{}'".format(by, project))


class Project(BitbucketCloudBase):
    def __init__(self, data, *args, **kwargs):
        super(Project, self).__init__(None, *args, data=data, expected_type="project", **kwargs)
        try:
            url = self.get_link("repositories")
        except KeyError:
            workspace = self.get_data("workspace")
            url = '{}/?q=project.key="{}"'.format(workspace["links"]["self"], workspace["slug"])
        self.__repositories = ProjectRepositories(url, **self._new_session_args)

    @property
    def repositories(self):
        return self.__repositories

    @property
    def name(self):
        return self.get_data("name")

    @name.setter
    def name(self, name):
        return self.update(name=name)

    @property
    def key(self):
        return self.get_data("key")

    @key.setter
    def key(self, key):
        return self.update(key=key)

    @property
    def description(self):
        return self.get_data("description")

    @description.setter
    def description(self, description):
        return self.update(description=description)

    @property
    def is_private(self):
        return self.get_data("is_private")

    @is_private.setter
    def is_private(self, is_private):
        return self.update(is_private=is_private)

    @property
    def created_on(self):
        return self.get_data("created_on")

    @property
    def updated_on(self):
        return self.get_data("updated_on", "never updated")

    def get_avatar(self):
        return self.get(self.get_link("avatar"), absolute=True)

    def delete(self):
        """
        Delete the project
        """
        return super(Project, self).delete(None)
