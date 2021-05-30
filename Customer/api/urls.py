from django.urls import path
from .views import registration_view, activate

from rest_framework.authtoken.views import obtain_auth_token

app_name = "Customer"

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('activate/<uidb64>/<token>/', activate, name='activate')
]