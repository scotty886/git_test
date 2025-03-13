from django.shortcuts import render

from cart.cart import Cart
from comicshop.models import Category
from django.contrib.auth.models import User
from comicshop.models import Product, Profile

from .forms import ShippingForm
from .models import Order, OrderItem
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

import datetime

from .forms import PaymentForm, ShippingForm
from .models import ShippingAddress

import logging

logger = logging.getLogger(__name__)


# Create your views here.


def payment_process(request):
    return render(request, 'payments/payment_process.html')


def checkout(request):
    logger.error(f'***** AN ERROR OCCURRED AT: {request.path}')
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        context = {
            'cart_products': cart_products,
            'quantities': quantities,
            'totals': totals,
            'shipping_form': shipping_form
        }
        return render(request, 'payments/checkout.html', context)
    else:
        shipping_form = ShippingForm(request.POST or None)
        context = {
            'cart_products': cart_products,
            'quantities': quantities,
            'totals': totals,
            'shipping_form': shipping_form
        }
        return render(request, 'payments/checkout.html', context)



def billing_info(request):
    logger.error(f'***** AN ERROR OCCURRED AT: {request.path}')
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.total()
        billing_form = PaymentForm()
        bill = PaymentForm()

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:

            context = {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_address": request.POST,
                "billing_address": billing_form,
                "bill": bill,
            }
            return render(request, "payments/billing_info.html", context)
        else:
            billing_form = PaymentForm()
            context = {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_address": request.POST,
                "billing_address": billing_form
            }
            return render(request, "payments/billing_info.html", context)
    else:
        messages.warning(request, "You must fill out the form.")
        return redirect("home")


def process_order(request):
    if request.POST:
        # Get the Cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.total()

        # Get billing information
        # payment_form = PaymentForm(request.POST or None)

        # Get shipping session data
        my_shipping = request.session.get("my_shipping")

        # Gather order information
        full_name = my_shipping["shipping_full_name"]
        email = my_shipping["shipping_email"]

        # create shipping address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}, {my_shipping['shipping_state']}, {my_shipping['shipping_postal_code']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        # Create an Order
        if request.user.is_authenticated:
            # Logged in
            user = request.user
            # Create order
            create_order = Order(
                user=user,
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid,
            )
            create_order.save()

            # Add order items
            # Get the order ID
            order_id = create_order.pk

            # Get product info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Get product price
                price = product.price
                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(
                            order_id=order_id,
                            product_id=product_id,
                            user=user,
                            quantity=value,
                            price=price,
                        )
                        create_order_item.save()
            # Delete cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

            # Delete Cart from Database (old cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in db
            current_user.update(old_cart="")

            messages.success(request, "Order successfully placed!")
            return redirect("home")
        else:
            # Not logged in
            # Create order
            create_order = Order(
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid,
            )
            create_order.save()
            # Add order items
            # Get the order ID
            order_id = create_order.pk

            # Get product info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Get product price
                price = product.price
                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(
                            order_id=order_id,
                            product_id=product_id,
                            quantity=value,
                            price=price,
                        )
                        create_order_item.save()
            # Delete cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

            messages.success(
                request,
                "Order successfully placed! You should consider creating an account for faster checkouts.",
            )
            return redirect("home")
    else:
        messages.warning(request, "Access Denied!")
        return redirect("home")

def dashboard_shipped(request):
    if request.user.is_authenticated and request.user.is_superuser:
       orders = Order.objects.filter(shipped=True)

       # Update Shipping Status
       if request.POST:   #<—————————— ADD THIS AND BELOW!
           # status = Order.objects.filter(shipped=True)
           num = request.POST['num']
           order = Order.objects.filter(id=num)
           order.update(shipped=False)
           messages.success(request, "Shipping status updated!")
           return redirect("home")
       context = {"orders": orders}

       return render(request, "payments/dashboard_shipped.html", context) #<—————————— UPDATE THIS!
    else:
        messages.success(request, "Access denied")
        return redirect("home")

def dashboard_outstanding(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST: #<—————————— ADD THIS AND BELOW!
            # status = request.POST[‘shipping_status’]
            num = request.POST['num']
            # Get the order
            order = Order.objects.filter(id=num)
            # Grab current date and time
            now = datetime.datetime.now()
            # Update order
            order.update(shipped=True, date_shipped=now)
            # Message and redirect
            messages.success(request, "Shipping status updated!")
            return redirect("home")
        context = {"orders": orders}
        return render(request, "payments/dashboard_outstanding.html", context) #<—————————— UPDATE THIS!
    else:
        messages.success(request, "Access denied")
        return redirect("home")

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)

        # add functionality to shipped button
        if request.POST:  # <—————————ADD THIS: START
            status = request.POST["shipping_status"]
            # Check if true or false
            if status == "true":
                # get the order
                order = Order.objects.filter(id=pk)
                # Update the status and date shipped
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the status
                order.update(shipped=False)
            messages.success(request, "Order status updated!")
            return redirect("home")  # <—————————ADD THIS: END


        context = {'order': order, 'items': items}
        return render(request, 'payments/orders.html', context)
    else:
        messages.warning(request, "Access denied.")
        return redirect("home")





