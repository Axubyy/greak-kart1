from django.shortcuts import render

# Create your views here.

from store.models import Product


def home(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        "products": products,
    }
    return render(request, 'category/home.html', context)
