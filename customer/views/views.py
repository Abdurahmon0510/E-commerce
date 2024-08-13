
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

import customer
from customer.forms import CustomerModelForm
from customer.models import Customer
from django.http import HttpResponse
import csv

def customer_list(request):
    search = request.GET.get('search')
    filter_button_clicked = request.GET.get('filter')
    if filter_button_clicked:
        customers = Customer.objects.all().order_by('-updated_at')
    else:
        customers = Customer.objects.all()
    if search:
        customers = customers.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search) | Q(address__icontains=search))
    return render(request, 'customer/customer-list.html', {'customers': customers})

def customer_details(request, customer_slug):
    customer = get_object_or_404(Customer, slug=customer_slug)
    context = {'customer': customer}
    return render(request, 'customer/customer-details.html', context)

def shopping_cart(request):
    return render(request, 'shop/shopping-cart.html')

@login_required
def new_customer(request):
    form = CustomerModelForm()

    if request.method == 'POST':
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customer_list')

    context = {'form': form}
    return render(request, 'customer/new_customer.html', context)

@login_required
def export_customers(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Full_Name', 'Email', 'Updated At'])
    for customer in Customer.objects.all():
        writer.writerow([customer.id, customer.full_name, customer.email, customer.updated_at])

    return response

@login_required
def profile_page(request):

    if request.method == 'POST':
        user = User.objects.get(username=request.POST['username'])
        context = {'user': user}
        return render(request, 'customer/profile_page.html', context)

    return render(request, 'customer/profile_page.html')

@login_required
def delete_customer(request, customer_slug):
    customer = get_object_or_404(Customer, slug=customer_slug)
    customer.delete()
    return redirect('customer_list')


@login_required
def edit_customer(request, customer_slug):
    customer = get_object_or_404(Customer, slug=customer_slug)
    form = CustomerModelForm(instance=customer)

    if request.method == 'POST':
        form = CustomerModelForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')

    return render(request, 'customer/edit_customer.html', {'customer': customer, 'form': form})

