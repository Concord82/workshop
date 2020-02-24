from django import template
from account.models import Offices

register = template.Library()


@register.inclusion_tag('offices_select_tpl.html')
def offices_select(office_id=0):
    offices_list = Offices.objects.all()
    return {'offices_list': offices_list, 'office_id': office_id}


@register.filter
def to_str(value):
    """converts int to string"""
    return str(value)


@register.filter
def to_int(value):
    return int(value)
