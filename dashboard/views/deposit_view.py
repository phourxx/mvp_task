from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer

from dashboard.models import DepositHistory
from dashboard.serializers.add_deposit_serializer import AddDepositSerializer
from dashboard.views.base_views import BaseCreateAPIView
from mvp_task.api_response import SuccessApiResponse, ServerErrorApiResponse
from mvp_task.permissions import AllowBuyerOnly
from mvp_task.utils import log_exception


class DepositView(BaseCreateAPIView):
    serializer_class = AddDepositSerializer
    permission_classes = (IsAuthenticated, AllowBuyerOnly)

    def build_success(self) -> SuccessApiResponse:
        return SuccessApiResponse(
            "Deposit successful",
            data=AddDepositSerializer(self.object).data
        )


class ResetDepositView(GenericAPIView):
    serializer_class = Serializer()
    permission_classes = (IsAuthenticated, AllowBuyerOnly)

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            DepositHistory.objects.create(
                user=user,
                amount=f"-{user.deposit}",
                deposit_before=user.deposit,
                deposit_after=0
            )
            user.deposit = 0
            user.save()
            return SuccessApiResponse('Deposit reset successful')
        except Exception as ex:
            log_exception(type(self).__name__, ex)
            return ServerErrorApiResponse()
