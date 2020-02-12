from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from pytils.translit import slugify
from autoslug import AutoSlugField
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Category(MPTTModel):
    """ Абстрактный класс для общего описания категорий товаров и услуг"""
    name = models.CharField(max_length=50, db_index=True)
    url_slug = models.SlugField(max_length=200, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        abstract=True


class ProductsCategory(Category):
    """ Товары реализуемые как для выполнения работ, так
    и в качетсве самостоятельных продаж"""
    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _('Products Categories')


class ServicesCategory(Category):
    """ Услуги выполняемые мастерами"""
    class Meta:
        verbose_name = _('Service Category')
        verbose_name_plural = _('Services Categories')


class ProductsServices(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Products(ProductsServices):
    category = models.ForeignKey(ProductsCategory, related_name='Products', on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = _('Product')
        verbose_name_plural = _('Products')