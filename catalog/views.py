from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import ProductsCategory, Products, ServicesCategory, Services
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

    return render(request, 'product_list.html',
                  {'breathCrumb': breathCrumb,
                   'serviceCategory': serviceCategory,
                   'serviceCategoryChildren': serviceCategoryChildren,
                   'serviceCategoryes': serviceCategoryes,
                   'services': services})


