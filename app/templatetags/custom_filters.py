from django import template
from ..models import Category, Question

register = template.Library()

@register.filter
def in_pool(subcategory, pool):
    categories_in_pool = Question.objects.filter(pool__pool_name=pool).values_list('subcategory', flat=True)
    return subcategory.filter(pk__in=categories_in_pool)
