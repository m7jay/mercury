from django import template
from main.utils.amount import format_amount


register = template.Library()

register.filter("format_amount", format_amount)
