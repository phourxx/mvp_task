from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from dashboard.mixins.delete_mixin import DeleteMixin
from dashboard.mixins.retrieve_mixin import RetrieveMixin
from dashboard.models import User
from dashboard.serializers.create_user_serializer import CreateUserSerializer
from dashboard.serializers.delete_user_serializer import DeleteUserSerializer
from dashboard.serializers.update_user_serializer import UpdateUserSerializer
from dashboard.serializers.user_serializer import UserSerializer
from dashboard.views.base_views import BaseCreateAPIView, BaseUpdateAPIView
from mvp_task import errors
from mvp_task.api_response import SuccessApiResponse, ServerErrorApiResponse
from mvp_task.utils import log_exception


class UserViewSet(BaseCreateAPIView, BaseUpdateAPIView, DeleteMixin,
                  RetrieveMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()

    serializer_classes = {
        'destroy': DeleteUserSerializer,
        'retrieve': UserSerializer,
        'create': CreateUserSerializer,
        'update': UpdateUserSerializer,
    }

    def get_error(self):
        return errors.INVALID_USER_ERROR

    def get_serializer_class(self):
        return self.serializer_classes[self.action]

    def build_success(self) -> SuccessApiResponse:
        # action -> create, update
        return SuccessApiResponse(
            f"User {self.action}d successfully",
            data=UserSerializer(self.object).data
        )

    def initial(self, request, *args, **kwargs):
        if self.action == 'create':
            self.permission_classes = [AllowAny, ]
        else:
            kwargs['pk'] = request.user.pk
            self.kwargs['pk'] = request.user.pk
        return super(UserViewSet, self).initial(request, *args, **kwargs)

    def handle_exception(self, exc):
        try:
            return super(UserViewSet, self).handle_exception(exc)
        except Exception as ex:
            log_exception(type(self).__name__, ex)
            return ServerErrorApiResponse()
