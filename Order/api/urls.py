from django.urls import path, include
from .views import orderView

urlpatterns = [
    path('<productKey>/order/', orderView, name='orderView')
]