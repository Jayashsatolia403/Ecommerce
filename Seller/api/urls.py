from django.urls import path
from .views import registration_view, addProductView, sellerAdmin

from rest_framework.authtoken.views import obtain_auth_token

app_name = "Seller"

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('addproduct/', addProductView, name='addproduct'),
    path('sellerAdmin/', sellerAdmin, name='sellerAdmin')
]