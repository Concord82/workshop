from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import ProductsCategory, Products, ServicesCategory, Services

from cart.forms import CartAddProductForm, CartAddServiceForm
# Create your views here.

@login_required
def product_list(request, products_slug=None):
    productCategory = None
    productCategoryChildren = None
    breathCrumb = None

    ProductCategories = ProductsCategory.objects.all()
    products = Products.objects.all()
    if products_slug:
        productCategory = get_object_or_404(ProductsCategory, url_slug=products_slug)

        productCategoryChildren = productCategory.get_children

        products = products.filter(category=productCategory)

        breathCrumb = productCategory.get_ancestors(ascending=False)

    return render(request, 'product_list.html', {'type': 2,
                                          'breathCrumb': breathCrumb,
                                          'Category': productCategory,
                                          'CategoryChildrens': productCategoryChildren,
                                          'Categoryes': ProductCategories,
                                          'items': products})

@login_required
def product_detail(request, id, slug):
    product = get_object_or_404(Products, id=id, slug=slug, available=True)

    breathCrumb = product.category.get_ancestors(ascending=False)

    ProductCategories = ProductsCategory.objects.all()

    cart_product_form = CartAddProductForm()

    return render(request, 'detail.html', {'type': 1,
                                           'product': product,
                                           'Categoryes': ProductCategories,
                                           'breathCrumb': breathCrumb,
                                           'cart_product_form': cart_product_form
                                           })


@login_required
def service_list(request, services_slug=None):
    # категория услуг
    serviceCategory = None
    serviceCategoryChildren = None
    breathCrumb = None
    # список всех категорий услуг
    serviceCategoryes = ServicesCategory.objects.all()
    # список услуг
    services = Services.objects.all()
    # если при вызове задана категория услуг
    if services_slug:
        # задаем выбранную категорию
        serviceCategory = get_object_or_404(ServicesCategory, url_slug=services_slug)

        serviceCategoryChildren = serviceCategory.get_children
        # получаем услуги которые входят в эту категорию
        services = services.filter(category=serviceCategory)

        breathCrumb = serviceCategory.get_ancestors(ascending=False)

    return render(request, 'product_list.html', {'type': 1,
                                                 'breathCrumb': breathCrumb,
                                                 'Category': serviceCategory,
                                                 'CategoryChildrens': serviceCategoryChildren,
                                                 'Categoryes': serviceCategoryes,
                                                 'items': services})


@login_required
def service_detail(request, id, slug):
    service = get_object_or_404(Services, id=id, slug=slug, available=True)

    breath_crumb = service.category.get_ancestors(ascending=False)
    product_categories = ServicesCategory.objects.all()

    cart_service_form = CartAddServiceForm()

    return render(request, 'detail.html', {'type': 1,
                                           'product': service,
                                           'Categoryes': product_categories,
                                           'breathCrumb': breath_crumb,
                                           'cart_product_form': cart_service_form
                                           })
