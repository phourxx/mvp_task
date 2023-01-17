from django.http import Http404

from mvp_task.api_response import (
    SuccessApiResponse,
    FailureApiResponse,
    ServerErrorApiResponse
)
from mvp_task.utils import log_exception


class DeleteMixin:
    def destroy(self, request, *args, **kwargs):
        try:
            super(DeleteMixin, self).destroy(request, *args, **kwargs)
            return SuccessApiResponse(
                msg='Operation successful'
            )
        except Http404:
            return FailureApiResponse(
                self.get_error(),
                status=404
            )
        except Exception as ex:
            log_exception(type(self).__name__, ex)
            return ServerErrorApiResponse()
