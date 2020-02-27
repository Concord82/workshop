from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Category(MPTTModel):
    """ Абстрактный класс для общего описания категорий товаров и услуг"""
    name = models.CharField(_('name'), max_length=50, db_index=True)
    url_slug = models.SlugField(_('slug'), max_length=200, unique=True)
    image = models.ImageField(_('Image'), upload_to='categories/%Y/%m-%d', default='../static/images/noimage.png')
    description = models.TextField(_('description'), blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')



    def __str__(self):
        return self.name

    class Meta:
        abstract=True


class ProductsCategory(Category):
    """ Товары реализуемые как для выполнения работ, так
    и в качетсве самостоятельных продаж"""

    def get_absolute_url(self):
        return reverse('catalog:product_list_by_category', args=[self.url_slug])

    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _('Products Categories')


class ServicesCategory(Category):
    """ Услуги выполняемые мастерами"""
    def get_absolute_url(self):
        return reverse('catalog:service_list_by_category', args=[self.url_slug])


    class Meta:
        verbose_name = _('Service Category')
        verbose_name_plural = _('Services Categories')


class ProductsServices(models.Model):
    """ товары реализуемые организацией """
    name = models.CharField(_('name'), max_length=200, db_index=True)
    slug = models.SlugField(_('slug'), max_length=200, db_index=True)
    description = models.TextField(_('description'), blank=True)
    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
    available = models.BooleanField(_('Available'), default=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    def get_absoluete_url(self):
        return reverse('catalog:product_detail', args=[self.id, self.slug])

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Products(ProductsServices):
    UNIT_CHOISE = (
        (1, _('thing')),
        (2, _('meter')),
        (3, _('packaging')),
    )
    category = models.ForeignKey(ProductsCategory, verbose_name=_('Product Category'), related_name='Product_Category',
                                 on_delete=models.CASCADE)
    image = models.ImageField(_('Image'), upload_to='products/%Y/%m-%d', default='../static/images/avatar/unnamed.jpg')
    vendor_code = models.CharField(_('Vendor Code'), max_length=32, blank=True)
    unit = models.IntegerField(_('Unit'), choices=UNIT_CHOISE)

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % (self.image))

    image_tag.short_description = _('Image product')
    image_tag.allow_tags = True

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class Services(ProductsServices):
    category = models.ForeignKey(ServicesCategory, verbose_name=_('Service Category'), related_name='Service_Category',
                                 on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
