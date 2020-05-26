from django.shortcuts import get_object_or_404
from .models import Item, Cart
from django.db.models import Q


def cart_contents(request):
    cart = request.session.get('cart', {})
    print(cart)
    if request.user.is_authenticated:
        for id, quantity in cart.items():
            product_id = int(id)
            cart = Cart.objects.filter(user=request.user)
            carts = cart.filter(product_id=product_id).first()
            print(carts)
            if carts:
                print("enter1")
                carts.quantity = quantity
            elif carts is None:
                print("enter2")
                carts = Cart(user=request.user, product_id=product_id)
                carts.save()
                carts.quantity = quantity
        return {'cart': cart}

    else:
        cart_items = []
        total = 0
        product_count = 0
        for id, quantity in cart.items():
            product = get_object_or_404(Item, pk=id)
            total += int(quantity) * product.discount_price
            product_count += 1
            cart_items.append({'quantity': quantity, 'product': product})
        return {'cart_items': cart_items, 'total_cost': total, 'product_count': product_count}
