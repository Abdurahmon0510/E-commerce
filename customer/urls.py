
from django.urls import path

from customer.views import  views


urlpatterns = [
    path('customer-list/',views.CustomerListView.as_view(),name='customer_list'),
    path('customer-details/<slug:customer_slug>',views.CustomerDetailView.as_view(),name='customer_details'),
    path('shopping-cart/',views.ShoppingCartView.as_view(),name='shopping_cart'),
    path('new_customer/',views.CustomerCreateView.as_view(),name='new_customer'),
    path('export/', views.ExportDataView.as_view(), name='export_data'),
    path('checkout/',views.CheckoutView.as_view(),name='checkout'),
    path('profile/',views.UserProfileView.as_view(),name='profile_page'),
    path('edit/<slug:customer_slug>/', views.CustomerUpdateView.as_view(), name='edit_customer'),
    path('delete/<slug:customer_slug>/', views.CustomerDeleteView.as_view(), name='delete_customer'),



]
