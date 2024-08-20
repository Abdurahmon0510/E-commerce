from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from users.forms import LoginFrom, RegisterForm


def login_page(request):
    if request.method == 'POST':
        form = LoginFrom(request.POST)
        if form.is_valid():
           email = form.cleaned_data.get('email')
           password = form.cleaned_data.get('password')
           user =  authenticate(request,email=email,password=password)
           if user:
              login(request,user)
              return redirect('customer_list')
           else:
                messages.error(request,'Invalid email or password')


    else:
         form=LoginFrom()
    return  render(request, 'users/login.html', {'form': form})
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

def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('customer_list')
    else:
        form = RegisterForm()

    context = {
        'form': form
    }

    return render(request, 'users/register.html', context)

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


def logout_page(request):
    if request.method == 'POST':
        logout(request)
    return redirect('customer_list')
