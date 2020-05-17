from django.contrib import admin
from .models import Product

# Register your models here.
"""we need to put this into admin.py to allow us to be able to add products through the admin panel.
    So we register(Product) here.
"""
admin.site.register(Product)