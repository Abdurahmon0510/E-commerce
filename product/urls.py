from django.urls import path

from product import views
from product.views import ProductCreateView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('product-list/', views.ProductListView.as_view(), name='product_list'),
    path('product-detail/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('new_product/', ProductCreateView.as_view(), name='new_product'),
    path('edit_product/<slug:slug>/', ProductUpdateView.as_view(), name='edit_product'),
    path('delete_product/<slug:slug>/', ProductDeleteView.as_view(), name='delete_product'),
]
