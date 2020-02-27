from django.urls import path
from . import views


app_name = 'catalog'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),

    path('services/<slug:services_slug>/', views.service_list, name='service_list_by_category'),

    path('services', views.service_list, name='services'),

]