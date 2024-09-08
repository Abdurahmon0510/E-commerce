from django.contrib import admin

from app.models import Author
from app.models import Book

# Register your models here.
admin.site.register(Author)
admin.site.register(Book)