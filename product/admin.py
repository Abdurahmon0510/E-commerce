from django.contrib import admin

from product.models import Category, Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'price', 'category', 'description', 'image','favourite']
    list_display = ['name', 'price', 'category', 'description', 'image']

    exclude = ('slug',)

admin.site.register(Category)




