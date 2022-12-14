from .models import Cart, CartItem
from .views import _get_cart_id


def counter(request):
    cart_count = 0
    if "admin" in request.path:
        return {}
    else:
        cart = Cart.objects.filter(cart_id=_get_cart_id(request))
        # cart_items = CartItem.objects.all().filter(cart=cart[:1])
        cart_items = CartItem.objects.filter(
            cart__cart_id=_get_cart_id(request))
        for cart_item in cart_items:
            cart_count += cart_item.quantity
        return dict(cart_count=cart_count)
