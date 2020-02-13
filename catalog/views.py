from django.shortcuts import render, get_object_or_404
from .models import ProductsCategory, Products
# Create your views here.


def product_list(request, category_slug=None):
    category = None
    categories = ProductsCategory.objects.all()

    if category_slug:
        category = get_object_or_404(ProductsCategory, slug=category_slug)

    return render(
        request,
        'catalog_base.html',
        {'category': category,
         'categories': categories}
    )



