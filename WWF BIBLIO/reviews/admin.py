from django.contrib import admin

# Register your models here.
from .models import Book, Langue, Type

admin.site.register(Book)
admin.site.register(Langue)
admin.site.register(Type)

