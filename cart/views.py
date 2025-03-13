from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from comicshop.models import Product
from django.http import JsonResponse
from django.contrib import messages


import logging

logger = logging.getLogger(__name__)


# Create your views here.

def cart_summary(request):
    logger.error(f'***** AN ERROR OCCURRED AT CART SUMMARY: {request.path}')
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    cart_totals = cart.total()
    return render(request, 'cart_summary.html', {'cart_products': cart_products, 'quantities': quantities, 'cart_totals': cart_totals})

def cart_add(request):
    logger.error(f'***** AN ERROR OCCURRED AT CART ADD: {request.path}')
    # get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # get product id
        product_id = int(request.POST.get('product_id'))
        print(product_id)
        # get product quantity
        product_qty = int(request.POST.get('product_qty'))
        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)
        print(product)
        # save to session and add to cart
        cart.add(product=product, quantity=product_qty)

        # get cart quantity
        cart_quantity = cart.__len__()

        # return JSON response
        #response = JsonResponse({‘Product Brand’: product.brand, ‘Product Model’: product.model})
        response = JsonResponse({'qty': cart_quantity})
        return response


def cart_update(request):
    logger.error(f'***** AN ERROR OCCURRED AT CART UPDATE: {request.path}')
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({"qty": product_qty})
        messages.success(request, "Your cart has been updated.")
        return response


def cart_delete(request):
    logger.error(f'***** AN ERROR OCCURRED AT CART DELETE: {request.path}')
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        cart.delete(product=product_id)
        response = JsonResponse({"product_id": product_id})
        messages.success(request, "Item has been removed from your cart.")
        return response
