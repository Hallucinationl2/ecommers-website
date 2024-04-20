from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .cart import Cart
from django.contrib import messages
from store.models import Product
from django.http import JsonResponse


class CartSummaryView(View):
    def get(self, request):
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        context = {
            "cart_products": cart_products,
            "quantities": quantities,
            "totals": totals
        }
        return render(request, 'cart/cart_summary.html', context)


class CartAddView(View):
    def post(self, request):
        cart = Cart(request)

        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))

            product = get_object_or_404(Product, id=product_id)

            cart.add(product=product, quantity=product_qty)

            cart_quantity = cart.__len__()

            response = JsonResponse({'qty': cart_quantity})
            messages.success(request, 'Product added to cart')
            return response


def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)
        messages.success(request, 'Item deleted from cart')
        return redirect('cart_summary')


class CartUpdateView(View):
    def post(self, request):
        cart = Cart(request)

        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))

            cart.update(product=product_id, quantity=product_qty)

            messages.success(request, 'Your cart has been updated!')
            return redirect('cart_summary')
