from rest_framework.permissions import IsAuthenticated

from dashboard.serializers.inventory_serializer import InventorySerializer
from dashboard.serializers.product_serializer import ProductSerializer
from dashboard.views.base_views import BaseCreateAPIView
from mvp_task.api_response import SuccessApiResponse
from mvp_task.permissions import AllowSellerOnly


class InventoryCreateView(BaseCreateAPIView):
    serializer_class = InventorySerializer
    permission_classes = (IsAuthenticated, AllowSellerOnly)

    def build_success(self) -> SuccessApiResponse:
        return SuccessApiResponse(
            "Inventory created successfully",
            data=ProductSerializer(self.object.product).data
        )
