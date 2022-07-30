from math import prod
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.base import TemplateView
from cart.models import Cart, CartItem

from store.models import Product
# Create your views here.


def _get_cart_id(request):  # cart_id  as used as session id
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


# def cart_view(request, quantity=0, total=0, cart_items=None):
#     try:
#         cart = Cart.objects.get(cart=_get_cart_id(request))
#         cart_items = CartItem.objects.filter(cart=cart)
#         for cart_item in cart_items:  # instance of cart_item
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity
#     except:
#         pass
#     return render(request, "cart/cart.html", {
#         "quantity": quantity,
#         "total": total,
#         "cart_items": cart_items
#     })


# class CartView(TemplateView):
#     template_name = "cart/cart.html"


class CartView(TemplateView):
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs):
        total = 0
        quantity = 0
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(cart_id=_get_cart_id(self.request))
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            quantity += cart_item.quantity
            total += (cart_item.product.price * cart_item.quantity)
        tax = int(0.02 * total)
        grand_total = total + tax
        context["quantity"] = quantity
        context["total"] = total
        context["cart_items"] = cart_items
        context["tax"] = tax
        context["grand_total"] = grand_total

        return context


def add_to_cart(request, product_id):  # private
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_get_cart_id(request))
        cart.save()

    # put product in cart to be CartItem
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            cart=cart, product=product, quantity=1)
        cart_item.save()

    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_get_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_get_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    return redirect('cart')
