from django.contrib import admin
from .models import Class, User, Book

# Registering our Models

admin.site.register(Class)
admin.site.register(User)
admin.site.register(Book)


