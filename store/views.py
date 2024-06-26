from django.shortcuts import render, redirect
from django.views import View

from cart.cart import Cart
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, ChangeUserPasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.contrib.auth.models import User
from django.db.models import Q
import json

from store.models import Category, Product, Profile


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        if not searched:
            messages.success(request, 'That product does not exist')
            return render(request, 'store/search.html', {})
        else:
            return render(request, 'store/search.html', {'searched': searched})
    else:
        return render(request, 'store/search.html', {})


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(id=request.user.id)

        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()

            messages.success(request, 'Your info has been updated!')
            return redirect('home')
        return render(request, "accounts/update_info.html", {'form': form, 'shipping_form': shipping_form})

    else:
        messages.success(request, "You must be logged in to access this page")
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangeUserPasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been updated!')

                # auto login after pass change
                # login(request, current_user)
                # return redirect('...')

                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangeUserPasswordForm(current_user)
            return render(request, 'accounts/update_password.html', {'form': form})

    else:
        messages.success(request, 'You must be logged in to update your password')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, 'user has been updated!')
            return redirect('home')
        return render(request, "accounts/update_user.html", {'user_form': user_form})

    else:
        messages.success(request, "you must be logged in to access this page")
        return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'store/category_summary.html', {"categories": categories})


def category(request, slug):
    slug = slug.replace('-', ' ')

    try:
        category = Category.objects.get(name=slug)
        products = Product.objects.filter(category=category)
        return render(request, 'store/category.html', {'products': products, 'category': category})
    except:
        messages.success(request, "Category you search for does not exist.")
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'store/product.html', {'product': product})


def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


def about(request):
    return render(request, 'store/about.html', {})


class LoginUserView(View):
    def get(self, request):
        return render(request, 'accounts/login.html', {})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # shopping cart for specific user
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, f'Welcome {username}')
            return redirect('home')
        else:
            messages.error(request, 'Wrong username or password')
            return redirect('login')


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out")
        return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f"Welcome {username}, fill out your billing to create your account successfully.")
            return redirect('update_info')
        else:
            messages.success(request, f"there was problem to register you. Try again")
            return redirect('register')
    else:
        return render(request, 'accounts/register.html', {'form': form})

# def login_user(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             messages.success(request, f'Welcome {username}')
#             return redirect('home')
#         else:
#             messages.success(request, 'Wrong username or password')
#             return redirect('login')
#
#     else:
#         return render(request, 'login.html', {})


# def logout_user(request):
#     logout(request)
#     messages.success(request, "you have been logout")
#     return redirect('home')
