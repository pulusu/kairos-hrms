from django import template
from test1.models import Cart
from django.db.models import Q

register = template.Library()


@register.simple_tag
def cart_count(user_id):
    cart_count = Cart.objects.filter(user_id=user_id)
    return cart_count.count()


@register.simple_tag
def cart_with_user(product_id, user_id):
    if user_id:
        cart = Cart.objects.filter(
            Q(product_id=product_id) & Q(user=user_id)).first()
        if cart is not None:
            return True
    else:
        return False


@register.simple_tag
def product_page_quantity(product_id, user_id):
    if user_id:
        cart = Cart.objects.filter(
            Q(product_id=product_id) & Q(user=user_id)).first()
        if cart is not None:
            return cart.quantity
    return 1
