from django.shortcuts import render, get_object_or_404
from .models import ProductsCategory, Products
# Create your views here.


def product_list(request, category_slug=None):
    category = None
    categories = ProductsCategory.objects.filter(parent_id=None)

    print(categories)

    for category in categories:
        category_child = category.get_children()
        print (category_child)





    categories = ProductsCategory.objects.all()

    cat_test = ProductsCategory.objects.get(id=1)
    for prod in cat_test.get_children():
        print(prod.name)

    if category_slug:
        category = get_object_or_404(ProductsCategory, url_slug=category_slug)

    return render(
        request,
        'old/_base_admin.html',
        {'category': category,
         'categories': categories}
    )



