from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction

from products.models import Product
from .models import Cart, CartItem
from orders.models import Order, OrderItem


def get_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = get_cart(request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")


@login_required
def cart_view(request):
    cart = get_cart(request.user)

    cart_items = CartItem.objects.filter(cart=cart)

    total = sum(item.total_price for item in cart_items)

    context = {
        "cart_items": cart_items,
        "total": total,
    }

    return render(request, "cart/cart.html", context)


@login_required
@transaction.atomic
def checkout(request):

    cart = get_cart(request.user)

    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect("cart")

    total = sum(item.total_price for item in cart_items)

    if request.method == "POST":

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
        )

        for item in cart_items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        cart_items.delete()

        return redirect("order_history")

    context = {
        "cart_items": cart_items,
        "total": total,
    }

    return render(request, "cart/checkout.html", context)


@login_required
def increase_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    cart_item.quantity += 1
    cart_item.save()

    return redirect("cart")


@login_required
def decrease_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart")


@login_required
def remove_item(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    cart_item.delete()

    return redirect("cart")