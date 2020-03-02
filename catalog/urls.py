from django.urls import path
from . import views


app_name = 'catalog'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/<slug:products_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    path('services/<slug:services_slug>/', views.service_list, name='service_list_by_category'),

    path('services', views.service_list, name='services'),

]