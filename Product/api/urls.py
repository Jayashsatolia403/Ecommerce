from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view()), 
    path('products/<pk>', views.product_detail_view, name='product_detail_view'),
    path('category/', views.CategoryListView.as_view())
]