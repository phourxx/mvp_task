from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from dashboard.mixins.delete_mixin import DeleteMixin
from dashboard.mixins.retrieve_mixin import RetrieveMixin
from dashboard.models import Product
from dashboard.serializers.create_product_serializer import \
    CreateProductSerializer
from dashboard.serializers.product_serializer import ProductSerializer, \
    ListProductSerializer
from dashboard.serializers.update_product_serializer import \
    UpdateProductSerializer
from dashboard.views.base_views import (
    BaseCreateAPIView, BaseUpdateAPIView,
    BaseListAPIView
)
from mvp_task import errors
from mvp_task.api_response import (
    SuccessApiResponse,
    ServerErrorApiResponse,
)
from mvp_task.permissions import AllowSellerOnly
from mvp_task.utils import log_exception


class ProductViewSet(BaseCreateAPIView, BaseListAPIView, BaseUpdateAPIView,
                     RetrieveMixin, DeleteMixin, viewsets.ModelViewSet):
    serializer_classes = {
        'list': ListProductSerializer,
        'retrieve': ProductSerializer,
        'create': CreateProductSerializer,
        'update': UpdateProductSerializer,
    }
    permissions = {
        'create': (IsAuthenticated, AllowSellerOnly),
        'update': (IsAuthenticated, AllowSellerOnly),
        'destroy': (IsAuthenticated, AllowSellerOnly),
    }

    def get_error(self) -> str:
        return errors.INVALID_PRODUCT_ID_ERROR

    def get_queryset(self):
        if self.action in ('destroy', 'update'):
            return self.request.user.products.all()
        return Product.objects.all()

    def get_serializer_class(self):
        return self.serializer_classes[self.action]

    def build_success(self) -> SuccessApiResponse:
        # action -> create, update
        return SuccessApiResponse(
            f"Product {self.action}d successfully",
            data=ProductSerializer(self.object).data
        )

    def initial(self, request, *args, **kwargs):
        if self.action in self.permissions:
            self.permission_classes = self.permissions[self.action]
        return super(ProductViewSet, self).initial(request, *args, **kwargs)

    def handle_exception(self, exc):
        try:
            return super(ProductViewSet, self).handle_exception(exc)
        except Exception as ex:
            log_exception(type(self).__name__, ex)
            return ServerErrorApiResponse()
