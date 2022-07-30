from itertools import product
from unicodedata import category
from webbrowser import get
import django
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from category.models import Category

from store.models import Product

# Create your views here.


class StoreListView(ListView):
    template_name = "store/store.html"
    model = Product
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super(StoreListView, self).get_context_data(**kwargs)
        if self.kwargs.get("category_slug") != None:
            categories = get_object_or_404(
                Category, slug=self.kwargs["category_slug"])
            products = Product.objects.filter(
                category=categories, is_available=True)
            product_count = products.count()
            context["products"] = products
            context["product_count"] = product_count
            # cat_products = Category.objects.get(slug=category_slug).products.all()
        else:
            products = Product.objects.all()
            product_count = products.count()

        context["products"] = products
        context["product_count"] = product_count

        return context


def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True)
        product_count = products.count()
        context = {
            "products": products,
            "product_count": product_count,
        }

    else:
        products = Product.objects.all()
        product_count = products.count()
        context = {
            "products": products,
            "product_count": product_count,
        }

    return render(request, 'store/store.html', context)


class ProductDetailView(DetailView):
    template_name = 'store/product_detail.html'
    model = Product
    context_object_name = "product"

    def get_object(self):
        product = Product.objects.get(
            category__slug=self.kwargs["category_slug"], slug=self.kwargs["product_slug"])

        return product

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     product = Product.objects.get(
    #         category__slug=self.kwargs["category_slug"], slug=self.kwargs["product_slug"])
    #     context["product"] = product

    #     return context
