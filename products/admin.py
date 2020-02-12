from django.contrib import admin
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import ProductsCategory, ServicesCategory, Products
from .forms import ProductForm
# Register your models here.


@admin.register(ProductsCategory)
class ProductsCategorAdmin(DjangoMpttAdmin):
    prepopulated_fields = {'url_slug': ('name',)}


@admin.register(ServicesCategory)
class ServicesCategorAdmin(DjangoMpttAdmin):
    prepopulated_fields = {'url_slug': ('name',)}

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    mptt_level_indent = 50
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = (
        ('category', TreeRelatedFieldListFilter),
        'available',
        'created',
        'updated'
    )
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    form = ProductForm