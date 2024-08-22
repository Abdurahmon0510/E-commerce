from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ProductForm
from product.models import Product

class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        paginator = Paginator(products, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'products': page_obj}
        return render(request, 'product/product-list.html', context)

# class ProductDetailView(View):
#     def get(self, request, slug):
#         product = get_object_or_404(Product, slug=slug)
#         context = {'product': product}
#         return render(request, 'product/product-details.html', context)
class ProductDetailView(DetailView):
    template_name = 'product/product-details.html'
    model = Product
    context_object_name = 'product'


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product/edit_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_list')

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return super().get_object(queryset)

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('product_list')

class ProductCreateView(CreateView):
    model = Product
    template_name = 'product/new_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
