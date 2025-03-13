from unicodedata import category

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
import json
from cart.cart import Cart

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django.contrib.auth.models import User

from .models import Product, Category, Profile

from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, ProductForm

import logging

logger = logging.getLogger(__name__)

# Create your views here.


def home(request):
    products = Product.objects.all()
    logger.error(f'***** AN ERROR OCCURRED AT: {request.path})')
    return render(request, 'home.html', {'products': products})

def about(request):
    logger.error(f'***** AN ERROR OCCURRED AT: {request.path}')
    return render(request, 'about.html')

############################# PRODUCT VIEWS ########################################

def details(request, pk):
    logger.error(f'***** AN ERROR OCCURRED AT: {request.path}')
    product = Product.objects.get(pk=pk)
    return render(request, 'details.html', {'product': product})

def product_entry(request):
    logger.error(f'***** AN ERROR OCCURRED AT PRODUCT ENTRY: {request.path}')
    p_form = ProductForm()
    if request.method == 'POST':
        p_form = ProductForm(request.POST, request.FILES)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'You have successfully entered a product')
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during product entry. Try again')
            return redirect('product_entry')
    else:
        context = {'p_form': p_form}
        return render(request, 'product_entry.html', context)

def categories(request, foo):
    logger.error(f'***** AN ERROR OCCURRED AT: {request.path}')
    foo = foo.replace('-', '' )
    print(foo)
    try:
        category = Category.objects.get(name=foo)
        print('TESTING CATEGORY!!!!')
        print('TESTING CATEGORY!!!!')
        print('TESTING CATEGORY!!!!')
        print(category)
        products = Product.objects.filter(publisher=category)
        context = {'products': products, 'category': category}
        return render(request, 'categories.html', context)
    except:
        messages.success(request, 'That publisher does not exist')
        return redirect('home')

def search(request):
    logger.error(f'***** AN ERROR OCCURRED AT: {request.path}')
    if request.method == 'POST':
        searched = request.POST['search']
        print('TESTING SEARCH - ENTRY!!!!')
        print('TESTING SEARCH - ENTRY!!!!')
        print(searched)
        results = Product.objects.filter(artist_name__contains=searched)
        if not search:
            messages.success(request, 'No search results found')
            return redirect('search')
        else:
            print('TESTING SEARCH - RESULTS!!!!')
            print('TESTING SEARCH - RESULTS!!!!')
            print(results)
            context = {'results': results}
            return render(request, 'search.html', context)
    else:
        context = {}
        return render(request, 'search.html', context)

########################### PROFILE, LOGIN, LOGOUT, UPDATES VIEWS #######################################

def login_user(request):
    logger.error(f'***** AN ERROR OCCURRED AT LOGIN USER: {request.path}')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            ## Add cart to session
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request, 'You have successfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logger.error(f'***** AN ERROR OCCURRED AT LOGOUT USER: {request.path}')
    logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect('home')


def register_user(request):
    logger.error(f'***** AN ERROR OCCURRED AT REGISTER USER: {request.path}')
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered')
            return redirect('update_profile')
        else:
            messages.error(request, 'An error occurred during registration. Try again')
            return redirect('register')
    else:
        context = {'form': form}
        return render(request, 'register.html', context)

def update_user(request):
    logger.error(f'***** AN ERROR OCCURRED AT UPDATE USER: {request.path}')
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, 'You have successfully updated your user information')
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.error(request, 'You must be logged in to update your user information')
        return redirect('home')

def update_password(request):
    logger.error(f'***** AN ERROR OCCURRED AT UPDATE PASSWORD: {request.path}')
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'You have successfully updated your password')
                login(request, current_user)
                return redirect('update_user')
        else:
            form = ChangePasswordForm(current_user)
            context = {'form': form}
            return render(request, 'update_password.html', context)
    else:
        messages.error(request, 'You must be logged in to update your password')
        return redirect('home')

def update_profile(request):
    logger.error(f'***** AN ERROR OCCURRED AT UPDATE PROFILE: {request.path}')
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, 'Your billing and shipping information has been updated')
            return redirect('home')
        return render(request, 'update_profile.html', {'form': form, 'shipping_form': shipping_form})
    else:
        messages.error(request, 'You must be logged in to update your profile information')
        return redirect('home')

