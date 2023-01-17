from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.serializers import Serializer

from dashboard.serializers.login_serializer import LoginSerializer
from dashboard.serializers.user_serializer import UserSerializer
from mvp_task.api_response import FailureApiResponse, ServerErrorApiResponse, \
    SuccessApiResponse
from mvp_task.utils import log_exception


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.user
            token = Token.objects.create(user=user)
            user_serializer = UserSerializer(user)
            data = user_serializer.data
            data['token'] = token.key
            return SuccessApiResponse(
                msg="Login successful",
                data=data
            )
        except ValidationError as ex:
            return FailureApiResponse(
                "Operation could not be completed due to validation errors",
                ex.detail
            )
        except Exception as ex:
            log_exception(type(self).__name__, ex)
            return ServerErrorApiResponse()


class LogoutView(GenericAPIView):
    serializer_class = Serializer()

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            token = Token.objects.get(user=user)
            token.delete()
            return SuccessApiResponse("Operation successful")
        except Exception as ex:
            log_exception(type(self).__name__, ex)
            return ServerErrorApiResponse()
