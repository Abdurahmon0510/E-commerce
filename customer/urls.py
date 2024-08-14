from config import settings
from django.conf.urls.static import static
from django.urls import path

from customer.views import auth, views
from customer.views.views import customer_list, customer_details, shopping_cart, new_customer, export_customers

urlpatterns = [
    path('customer-list/',customer_list,name='customer_list'),
    path('customer-details/<slug:customer_slug>',customer_details,name='customer_details'),
    path('shopping-cart/',shopping_cart,name='shopping_cart'),
    path('new_customer/',new_customer,name='new_customer'),
    path('export/', export_customers, name='export_customers'),
    path('checkout/',views.checkout,name='checkout'),
# login,register
    path('login_page/', auth.login_page, name='login_page'),
    path('register_page/', auth.register_page, name='register_page'),
    path('logout_page/',auth.logout_page, name='logout_page'),
    path('profile/',views.profile_page,name='profile_page'),
    path('edit/<slug:customer_slug>/', views.edit_customer, name='edit_customer'),
    path('delete/<slug:customer_slug>/', views.delete_customer, name='delete_customer'),

]
