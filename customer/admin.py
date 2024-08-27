from audioop import reverse

from django.contrib import admin
from django.utils.safestring import mark_safe

from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats

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
    def get_export_formats(self):
        formats = (
            base_formats.CSV,
            base_formats.XLS,
            base_formats.JSON,
            base_formats.HTML
        )
        return [f for f in formats if f().can_import]




