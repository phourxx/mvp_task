from rest_framework.permissions import IsAuthenticated

from dashboard.serializers.product_serializer import ListProductSerializer
from dashboard.serializers.purchase_serializer import PurchaseSerializer
from dashboard.views.base_views import BaseCreateAPIView
from mvp_task.api_response import SuccessApiResponse
from mvp_task.permissions import AllowBuyerOnly


class PurchaseView(BaseCreateAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = (IsAuthenticated, AllowBuyerOnly)

    def build_success(self) -> SuccessApiResponse:
        purchase = self.object
        user = self.request.user
        return SuccessApiResponse(
            "Purchase successful",
            data={
                "total": purchase.total_cost,
                "product": ListProductSerializer(purchase.product).data,
                "change": user.deposit_breakdown
            }
        )
