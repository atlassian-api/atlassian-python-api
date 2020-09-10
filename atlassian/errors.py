# coding=utf-8


class ApiError(Exception):
    def __init__(self, *args, **kwargs):
        self.reason = kwargs.get("reason")
        super(ApiError, self).__init__(*args)


class ApiNotFoundError(ApiError):
    pass


class ApiPermissionError(ApiError):
    pass


class ApiValueError(ApiError):
    pass


class ApiConflictError(ApiError):
    pass
