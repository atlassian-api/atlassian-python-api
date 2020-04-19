# coding=utf-8


class ApiError(Exception):
    pass


class ApiNotFoundError(ApiError):
    pass


class ApiPermissionError(ApiError):
    pass


class ApiValueError(ApiError):
    pass


class ApiConflictError(ApiError):
    pass
