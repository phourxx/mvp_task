from django.http import Http404

from mvp_task.api_response import (
    SuccessApiResponse,
    FailureApiResponse,
    ServerErrorApiResponse
)
from mvp_task.utils import log_exception


class RetrieveMixin:
    def retrieve(self, request, *args, **kwargs):
        try:
            response = super(RetrieveMixin, self).retrieve(
                request, *args, **kwargs
            )
            return SuccessApiResponse(
                msg="Item retrieved successfully",
                data=response.data
            )
        except Http404:
            return FailureApiResponse(
                self.get_error(),
                status=404
            )
        except Exception as ex:
            log_exception(type(self).__name__, ex)
            return ServerErrorApiResponse()
