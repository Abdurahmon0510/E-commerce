from django.urls import path
from users import views

urlpatterns = [
    path('login_page/', views.LoginPage.as_view(), name='login_page'),
    path('register_page/', views.register_page, name='register_page'),
    path('logout_page/', views.LogoutPage.as_view(), name='logout_page'),
    path('send-email/', views.SendingEmail.as_view(), name='sending_email'),
    path('activation-link/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate')
]
