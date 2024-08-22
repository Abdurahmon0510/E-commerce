from django.contrib import messages
from django.contrib.auth import  login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from config import settings
from config.settings import EMAIL_DEFAULT_SENDER
from users.forms import LoginFrom, RegisterForm, SendingEmailForm
from users.authentication_form import AuthenticationForm


# def login_page(request):
#     if request.method == 'POST':
#         form = LoginFrom(request.POST)
#         if form.is_valid():
#            email = form.cleaned_data.get('email')
#            password = form.cleaned_data.get('password')
#            user =  authenticate(request,email=email,password=password)
#            if user:
#               login(request,user)
#               return redirect('customer_list')
#            else:
#                 messages.error(request,'Invalid email or password')
#
#
#     else:
#          form=LoginFrom()
#     return  render(request, 'users/login.html', {'form': form})
# class LoginPageView(View):
#     def get(self, request):
#         form = LoginFrom()
#         return render(request, 'users/login.html', {'form': form})
#     def post(self, request):
#         form = LoginFrom(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, email=email, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('customer_list')
#             else:
#                 messages.error(request, 'Invalid email or password')

class LoginPage(LoginView):
    redirect_authenticated_user = True
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('customer_list')
    def form_invalid(self, form):
        messages.error(self.request,'Invalid email or password')
        return self.render_to_response(self.get_context_data(form=form))
# def register_page(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()
#             login(request, user)
#             return redirect('customer_list')
#     else:
#         form = RegisterForm()
#
#     context = {
#         'form': form
#     }

    # return render(request, 'users/register.html', context)

# class RegistrationPageView(View):
#     def get(self, request):
#         form = RegisterForm()
#         return render(request, 'users/register.html', {'form': form})
#     def post(self, request):
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()
#             login(request, user)
#             return redirect('customer_list')

class RegisterPage(FormView):
     template_name = 'users/register.html'
     form_class = RegisterForm
     success_url = reverse_lazy('customer_list')

     def form_valid(self, form):
         user = form.save(commit=False)
         user.save()
         send_mail(
             'User successfully registered',
             'Test body',
             EMAIL_DEFAULT_SENDER,
             [user.email],
             fail_silently=False,
         )
         login(self.request, user)
         return super().form_valid(form)


class LogoutPage(LogoutView):
    next_page = reverse_lazy('customer_list')



class SendingEmail(View):
    def get(self, request, *args, **kwargs):
        form = SendingEmailForm()
        return render(request, 'users/send-email.html', {'form': form, 'sent': False})

    def post(self, request, *args, **kwargs):
        form = SendingEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipient_list = form.cleaned_data['recipient_list']

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list,
                fail_silently=False
            )
            return render(request, 'users/send-email.html', {'form': form, 'sent': True})

        return render(request, 'users/send-email.html', {'form': form, 'sent': False})
