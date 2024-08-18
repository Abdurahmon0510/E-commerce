
from django.urls import path

from product import views


urlpatterns = [
# login,register
    path('product-list/', views.product_list, name='login_page'),
    ]