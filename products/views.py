from django.shortcuts import render
from .models import Product

# Create your views here.
def all_products(request):
    """that's going to be product.objects.all, which will return all the products that are in the database."""
    products = Product.objects.all()
    return render(request, "products.html", {"products": products})
