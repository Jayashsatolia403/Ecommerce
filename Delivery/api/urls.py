from django.urls import path
from .views import registration_view, deliveryAdmin, activate, confirmDelivery, verifyConfirmDelivery

from rest_framework.authtoken.views import obtain_auth_token

app_name = "Delivery"

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('orders/', deliveryAdmin, name='deliveryAdmin'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('<orderID>/confirmDelivery/', confirmDelivery, name='confirmDelivery'),
    path('<delivery_uidb64>/<delivery_token>/<current_order_id>/', verifyConfirmDelivery, name='verifyConfirmDelivery')
]