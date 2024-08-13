from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from customer.forms import LoginFrom, RegisterForm
from customer.models import Customer


def login_page(request):
    if request.method == 'POST':
        form = LoginFrom(request.POST)
        if form.is_valid():
           username = form.cleaned_data.get('username')
           password = form.cleaned_data.get('password')
           user =  authenticate(request,username=username,password=password)
           if user:
              login(request,user)
              return redirect('customer_list')
           else:
                messages.error(request,'Invalid username or password')

    else:
         form=LoginFrom()
    return  render(request,'auth/login.html',{'form': form })
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

    return render(request, 'auth/register.html', context)

def logout_page(request):
    if request.method == 'POST':
        logout(request)
    return redirect('customer_list')
