
from django.urls import path

from users import views


urlpatterns = [
# login,register
    path('login_page/', views.login_page, name='login_page'),
    path('register_page/', views.register_page, name='register_page'),
    path('logout_page/',views.logout_page, name='logout_page'),
    ]