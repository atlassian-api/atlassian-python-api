"""Confluence Cloud v2 administrative and workspace operations."""


class AdminManagementOperations:
    """Wrappers for v2 administrative resources not covered by legacy helpers."""

    @staticmethod
    def _query(**values):
        return {key: value for key, value in values.items() if value is not None}

    def _v2(self, path):
        return self.url_joiner("api/v2", path)

    def get_admin_key(self):
        return self.get(self._v2("admin-key"))

    def enable_admin_key(self):
        return self.post(self._v2("admin-key"))

    def disable_admin_key(self):
        return self.delete(self._v2("admin-key"))

    def get_space_permissions(self, cursor=None, limit=None):
        return self.get(self._v2("space-permissions"), params=self._query(cursor=cursor, limit=limit))

    def get_space_permission_combinations(self, cursor=None, limit=None):
        return self.get(
            self._v2("space-permissions/transition/combinations"),
            params=self._query(cursor=cursor, limit=limit),
        )

    def generate_space_permission_combinations(self, data=None):
        return self.post(self._v2("space-permissions/transition/combinations"), data=data)

    def assign_space_permission_roles(self, data=None):
        return self.post(self._v2("space-permissions/transition/role-assignments"), data=data)

    def remove_space_permission_access(self, data=None):
        return self.post(self._v2("space-permissions/transition/access-removals"), data=data)

    def get_space_permission_transition_task(self, task_id):
        return self.get(self._v2(f"space-permissions/transition/tasks/{task_id}"))

    def get_space_roles(
        self,
        space_id=None,
        role_type=None,
        principal_id=None,
        principal_type=None,
        cursor=None,
        limit=None,
    ):
        return self.get(
            self._v2("space-roles"),
            params=self._query(
                **{
                    "space-id": space_id,
                    "role-type": role_type,
                    "principal-id": principal_id,
                    "principal-type": principal_type,
                    "cursor": cursor,
                    "limit": limit,
                }
            ),
        )

    def create_space_role(self, data=None):
        return self.post(self._v2("space-roles"), data=data)

    def get_space_role(self, role_id):
        return self.get(self._v2(f"space-roles/{role_id}"))

    def update_space_role(self, role_id, data=None):
        return self.put(self._v2(f"space-roles/{role_id}"), data=data)

    def delete_space_role(self, role_id):
        return self.delete(self._v2(f"space-roles/{role_id}"))

    def get_space_role_mode(self):
        return self.get(self._v2("space-role-mode"))

    def bulk_get_users(self, data=None):
        return self.post(self._v2("users-bulk"), data=data)

    def check_user_access_by_email(self, data=None):
        return self.post(self._v2("user/access/check-access-by-email"), data=data)

    def invite_user_by_email(self, data=None):
        return self.post(self._v2("user/access/invite-by-email"), data=data)

    def get_data_policy_metadata(self):
        return self.get(self._v2("data-policies/metadata"))

    def get_data_policy_spaces(self, **filters):
        return self.get(self._v2("data-policies/spaces"), params=self._query(**filters))

    def get_global_footer_comments(self, **params):
        return self.get(self._v2("footer-comments"), params=self._query(**params))

    def create_global_footer_comment(self, data=None):
        return self.post(self._v2("footer-comments"), data=data)

    def get_global_inline_comments(self, **params):
        return self.get(self._v2("inline-comments"), params=self._query(**params))

    def create_global_inline_comment(self, data=None):
        return self.post(self._v2("inline-comments"), data=data)

    def get_comment_children_v2(self, comment_id, comment_type="footer-comments", **params):
        return self.get(self._v2(f"{comment_type}/{comment_id}/children"), params=self._query(**params))

    def get_comment_likes_count_v2(self, comment_id, comment_type="footer-comments"):
        return self.get(self._v2(f"{comment_type}/{comment_id}/likes/count"))

    def get_comment_likes_users_v2(self, comment_id, comment_type="footer-comments", **params):
        return self.get(self._v2(f"{comment_type}/{comment_id}/likes/users"), params=self._query(**params))

    def get_comment_operations_v2(self, comment_id, comment_type="footer-comments"):
        return self.get(self._v2(f"{comment_type}/{comment_id}/operations"))

    def get_comment_versions_v2(self, comment_id, comment_type="footer-comments", **params):
        return self.get(self._v2(f"{comment_type}/{comment_id}/versions"), params=self._query(**params))

    def get_comment_version_v2(self, comment_id, version_number, comment_type="footer-comments"):
        return self.get(self._v2(f"{comment_type}/{comment_id}/versions/{version_number}"))
