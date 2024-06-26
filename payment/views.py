from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')

        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = (f"{my_shipping['shipping_address1']}\n"
                            f"{my_shipping['shipping_address2']}\n"
                            f"{my_shipping['shipping_city']}\n"
                            f"{my_shipping['shipping_state']}\n"
                            f"{my_shipping['shipping_zipcode']}\n"
                            f"{my_shipping['shipping_country']}")
        amount_pay = totals
        # create order
        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_pay)
            create_order.save()

            messages.success(request, "Order placed!")
            return redirect('home')
        else:
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_pay)
            create_order.save()

            messages.success(request, "Order placed!")
            return redirect('home')

    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:
            billing_form = PaymentForm()

            return render(request, 'payment/billing_info.html', {"cart_products": cart_products,
                                                                 "quantities": quantities, "totals": totals,
                                                                 "shipping_info": request.POST,
                                                                 "billing_form": billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products,
                                                                 "quantities": quantities, "totals": totals,
                                                                 "shipping_info": request.POST,
                                                                 "billing_form": billing_form})

        shipping_form = request.POST
        return render(request, 'payment/billing_info.html', {"cart_products": cart_products,
                                                             "quantities": quantities, "totals": totals,
                                                             "shipping_form": shipping_form})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # checkout as user

        shipping_user = ShippingAddress.objects.get(id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        return render(request, 'payment/checkout.html', {"cart_products": cart_products,
                                                         "quantities": quantities, "totals": totals,
                                                         "shipping_form": shipping_form})
    else:
        # checkout as guest

        shipping_form = ShippingForm(request.POST or None)

        return render(request, 'payment/checkout.html', {"cart_products": cart_products,
                                                         "quantities": quantities, "totals": totals,
                                                         "shipping_form": shipping_form})


def payment_success(request):
    return render(request, 'payment/payment_success.html', {})
