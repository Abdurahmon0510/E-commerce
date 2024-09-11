from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from config import settings
from config.settings import EMAIL_DEFAULT_SENDER

from users.forms import RegisterForm, SendingEmailForm
from users.authentication_form import AuthenticationForm
from users.tokens import AccountTokenGenerator

# Login class-based view
class LoginPage(LoginView):
    redirect_authenticated_user = True
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('customer_list')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password')
        return self.render_to_response(self.get_context_data(form=form))

def register_page(request):
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                current_site = get_current_site(request)
                message = render_to_string('users/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': AccountTokenGenerator.make_token(user),
                })
                email = EmailMessage(
                    'Activate your account',
                    message,
                    EMAIL_DEFAULT_SENDER,
                    [user.email],

                )
                email.content_subtype = 'html'
                email.send()

                return HttpResponse('<h1>Please confirm your email address to complete the registration</h1>')
                # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                # return redirect('customers')
        else:
            form = RegisterForm()
        context = {'form': form}
        return render(request, 'users/register.html', context)


# Register class-based view
class RegisterPage(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = '/customer/customer-list/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        current_site = get_current_site(self.request)
        subject = 'Activate your account'
        message = render_to_string('users/acc_active_email.html', {
            'user': user,
            'protocol': 'http',
            'domain': 'example.com',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': AccountTokenGenerator.make_token(user),
        })
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return super().form_valid(form)

# Logout class-based view
class LogoutPage(LogoutView):
    next_page = reverse_lazy('customer_list')

# Sending email class-based view
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
                EMAIL_DEFAULT_SENDER,
                recipient_list,
                fail_silently=False
            )
            return render(request, 'users/send-email.html', {'form': form, 'sent': True})

        return render(request, 'users/send-email.html', {'form': form, 'sent': False})


# def active(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = get_user_model().objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
#         user = None
#
#     if user is not None and AccountTokenGenerator.check_token(user, token):
#         user.is_active = True
#         user.save()
#
#         return redirect('login_page')
#     else:
#
#         return render(request,'users/register.html')
#
class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and AccountTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login_page')
        else:
            return render(request, 'users/register.html')

