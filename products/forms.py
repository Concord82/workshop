from django import forms
from mptt.forms import TreeNodeChoiceField
from .models import ProductsCategory, ServicesCategory
from django.utils.translation import ugettext_lazy as _


class ProductForm(forms.ModelForm):
    category = TreeNodeChoiceField(label=_(u'Категория'), queryset=ProductsCategory.objects.all())


class ServiceForm(forms.ModelForm):
    category = TreeNodeChoiceField(label=_(u'Категория'), queryset=ServicesCategory.objects.all())
