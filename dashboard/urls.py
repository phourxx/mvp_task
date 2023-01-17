from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from dashboard.views.auth_view import LogoutView, LoginView
from dashboard.views.deposit_view import DepositView, ResetDepositView
from dashboard.views.inventory_view import InventoryCreateView
from dashboard.views.product_view import ProductViewSet
from dashboard.views.purchase_view import PurchaseView
from dashboard.views.user_view import *


user_view = UserViewSet.as_view({
    'get': 'retrieve',
    'post': 'create',
    'put': 'update',
    'delete': 'destroy'
})

product_view = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

product_mod_view = ProductViewSet.as_view({
    'delete': 'destroy',
    'get': 'retrieve',
    'put': 'update',
})

urlpatterns = [
    path('user', user_view),
    path('products', product_view),
    path('products/<int:pk>', product_mod_view),
    path('products/inventory', InventoryCreateView.as_view()),
    path('deposit', DepositView.as_view()),
    path('buy', PurchaseView.as_view()),
    path('reset', ResetDepositView.as_view()),
    path('login', LoginView.as_view()),
    path('logout/all', LogoutView.as_view()),
]
