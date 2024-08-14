from django.contrib import admin

from customer.models import Customer

# Register your models here.
# admin.site.register(Customer)
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ( 'full_name','joined')
    search_fields = ('first_name','last_name', 'phone', 'email')
    exclude = ('slug',)

