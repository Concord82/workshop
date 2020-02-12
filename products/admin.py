from django.contrib import admin
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import ProductsCategory, ServicesCategory, Products, Services
from .forms import ProductForm, ServiceForm
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
    fieldsets = (
        (None, {'fields': (
            'name',
            'slug',
            'category',
            'vendor_code',
            'unit',
            'price'
        )}),
        ('Other info', {'fields': (
            'available',
            'image_tag',
            'image',
            'description',
        )}),
    )

    readonly_fields = ['image_tag']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    form = ProductForm


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = (
        ('category', TreeRelatedFieldListFilter),
        'available',
        'created',
        'updated'
    )
    fieldsets = (
        (None, {'fields': (
            'name',
            'slug',
            'category',
            'price',
        )}),
        ('Other info', {'fields': (
            'available',
            'description',
        )}),
    )
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    form = ServiceForm
