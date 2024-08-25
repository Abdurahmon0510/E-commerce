

from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from customer.models import Customer,User


# Register your models here.
# admin.site.register(Customer)
@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ( 'full_name','joined')
    search_fields = ('first_name','last_name', 'phone', 'email')
    exclude = ('slug',)

@admin.register(User)
class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ( 'email', 'password')
    search_fields = ( 'email', 'password')
    exclude = ('slug',)



