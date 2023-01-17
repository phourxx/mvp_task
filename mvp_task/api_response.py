from rest_framework.response import Response
from typing import Optional


class ApiResponse(Response):
    def __init__(self, succeeded: bool, msg: str, data: Optional = None,
                 status: int = 200):
        resp = {
            "succeeded": succeeded,
            "message": msg,
            "data": data
        }
        super().__init__(data=resp, status=status)


class SuccessApiResponse(ApiResponse):
    def __init__(self, msg: str, data: Optional = None):
        super(SuccessApiResponse, self).__init__(True, msg, data)


class FailureApiResponse(ApiResponse):
    def __init__(self, msg: str, data: Optional = None,
                 status: Optional = 400):
        super(FailureApiResponse, self).__init__(False, msg, data,
                                                 status=status)


class ServerErrorApiResponse(ApiResponse):
    def __init__(self):
        super(ServerErrorApiResponse, self).__init__(False, "Server error",
                                                     status=500)
