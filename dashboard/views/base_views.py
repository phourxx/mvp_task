from django.http import Http404

from mvp_task import errors
from mvp_task.api_response import SuccessApiResponse, \
    ServerErrorApiResponse, FailureApiResponse, ApiResponse
from mvp_task.utils import log_exception
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView


class BaseListAPIView(ListAPIView):
    def list(self, request, *args, **kwargs) -> ApiResponse:
        try:
            response = super(BaseListAPIView, self).list(
                request, *args, **kwargs)
            return SuccessApiResponse(
                "success",
                response.data
            )
        except NotFound:
            return FailureApiResponse(errors.PAGE_404_ERROR, status=404)
        except Exception as ex:
            log_exception(type(self).__name__, ex)
        return ServerErrorApiResponse()


class BaseCreateAPIView(CreateAPIView):
    def perform_create(self, serializer):
        self.object = serializer.save()

    def build_success(self) -> SuccessApiResponse:
        return SuccessApiResponse("Operation successful", None)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return self.build_success()
        except ValidationError as ex:
            return FailureApiResponse(
                "Operation could not be completed due to validation errors",
                ex.detail
            )
        except Exception as ex:
            log_exception(type(self).__name__, ex)
            return ServerErrorApiResponse()


class BaseUpdateAPIView(UpdateAPIView):
    def get_error(self) -> str:
        raise NotImplemented

    def perform_update(self, serializer):
        self.object = serializer.save()

    def build_success(self) -> SuccessApiResponse:
        return SuccessApiResponse("Operation successful", None)

    def update(self, request, *args, **kwargs):
        try:
            super(BaseUpdateAPIView, self).update(request, *args, **kwargs)
            return self.build_success()
        except ValidationError as ex:
            return FailureApiResponse(
                "Operation could not be completed due to validation errors",
                ex.detail
            )
        except Http404:
            return FailureApiResponse(
                self.get_error(),
                status=404
            )
        except Exception as ex:
            log_exception(type(self).__name__, ex)
            return ServerErrorApiResponse()
