from rest_framework.permissions import BasePermission


class AllowSellerOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_seller


class AllowBuyerOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_buyer


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated)
