from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect, get_object_or_404


from django.views.decorators.http import require_POST
from catalog.models import Products, Services
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.product_add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    print (cart.cart['product'].keys())
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    cart.product_remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})