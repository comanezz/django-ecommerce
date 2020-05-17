from django.shortcuts import render
from products.models import Product

# Create your views here.
def do_search(request):
    """We have the model called Product.objects.filter. And filter is a built-in function.
        And we have (name_icontains=request.GET['q]), and this will get whatever 'q' is returned from the form,
        so we'll give the form a name of 'q'.
    """
    products = Product.objects.filter(name__icontains=request.GET['q'])
    return render(request, "products.html", {"products": products})