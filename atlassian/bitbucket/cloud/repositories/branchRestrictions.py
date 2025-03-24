# coding=utf-8

from ..base import BitbucketCloudBase


class BranchRestrictions(BitbucketCloudBase):
    def __init__(self, url, *args, **kwargs):
        super(BranchRestrictions, self).__init__(url, *args, **kwargs)

    def __get_object(self, data):
        return BranchRestriction(data, **self._new_session_args)

    def create(
        self,
        kind,
        branch_match_kind="glob",
        branch_pattern="*",
        branch_type=None,
        users=None,
        groups=None,
        value=None,
    ):
        """
        Add a new branch restriction.

        :param value:
        :param kind: string: One of require_tasks_to_be_completed, force, restrict_merges,
                             enforce_merge_checks, require_approvals_to_merge, delete,
                             require_all_dependencies_merged, push, require_passing_builds_to_merge,
                             reset_pullrequest_approvals_on_change, require_default_reviewer_approvals_to_merge
        :param branch_match_kind: string: branching_model or glob, if branching_model use
                                          param branch_type otherwise branch_pattern.
        :param branch_pattern: string: A glob specifying the branch this restriction should
                                       apply to (supports * as wildcard).
        :param branch_type: string: The branch type specifies the branches this restriction
                                    should apply to. One of: feature, bugfix, release, hotfix, development, production.
        :param users: List: List of user objects that are excluded from the restriction.
                            Minimal: {"username": "<username>"}
        :param groups: List: List of group objects that are excluded from the restriction.
                             Minimal: {"owner": {"username": "<teamname>"}, "slug": "<groupslug>"}

        :return: The created BranchRestriction object

        API docs:
        https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/branch-restrictions#post
        """
        if branch_match_kind == "branching_model":
            branch_pattern = ""

        data = {
            "kind": kind,
            "branch_match_kind": branch_match_kind,
            "pattern": branch_pattern,
        }

        if branch_match_kind == "branching_model":
            data["branch_type"] = branch_type

        if users is not None:
            data["users"] = users

        if groups is not None:
            data["groups"] = groups

        if value is not None:
            data["value"] = value

        return self.__get_object(self.post(None, data=data))

    def each(self, kind=None, pattern=None, q=None, sort=None):
        """
        Returns the list of branch restrictions in this repository.

        :param kind: string: Branch restrictions of this type
        :param pattern: string: Branch restrictions applied to branches of this pattern
        :param q: string: Query string to narrow down the response.
                          See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.
        :param sort: string: Name of a response property to sort results.
                             See https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering for details.

        :return: A generator for the BranchRestriction objects

        API docs: https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/branch-restrictions#get
        """
        params = {}
        if kind is not None:
            params["kind"] = kind
        if pattern is not None:
            params["pattern"] = pattern
        if sort is not None:
            params["sort"] = sort
        if q is not None:
            params["q"] = q
        for branch_restriction in self._get_paged(None, params=params):
            yield self.__get_object(branch_restriction)

        return

    def get(self, id):
        """
        Returns the branch restriction with the ID in this repository.

        :param id: string: The requested issue ID

        :return: The requested BranchRestriction objects

        API docs:
        https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/branch-restrictions/%7Bid%7D#get
        """
        return self.__get_object(super(BranchRestrictions, self).get(id))


class BranchRestriction(BitbucketCloudBase):
    def __init__(self, data, *args, **kwargs):
        super(BranchRestriction, self).__init__(None, *args, data=data, expected_type="branchrestriction", **kwargs)

    def update(self, **kwargs):
        """
        Update the branch restriction properties. Fields not present in the request body are ignored.

        :param kwargs: dict: The data to update.

        :return: The updated branch restriction

        API docs:
        https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/branch-restrictions/%7Bid%7D#put
        """
        return self._update_data(self.put(None, data=kwargs))

    def delete(self):
        """
        Delete the branch restriction.

        :return: The response on success

        API docs:
        https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/branch-restrictions/%7Bid%7D#delete
        """
        return super(BranchRestriction, self).delete(None)

    @property
    def id(self):
        """The branch restriction id"""
        return str(self.get_data("id"))

    @property
    def kind(self):
        """The branch restriction kind"""
        return self.get_data("kind")

    @property
    def branch_match_kind(self):
        """The branch restriction match kind"""
        return self.get_data("branch_match_kind")

    @property
    def branch_type(self):
        """The branch restriction type"""
        return self.get_data("branch_type")

    @property
    def pattern(self):
        """The branch restriction pattern"""
        return self.get_data("pattern")

    @property
    def users(self):
        """The branch restriction users"""
        return self.get_data("users")

    @property
    def groups(self):
        """The branch restriction groups"""
        return self.get_data("groups")

    @property
    def value(self):
        """The branch restriction value"""
        return self.get_data("value")
