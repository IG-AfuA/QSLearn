from django import template
from ..models import Category, Question

register = template.Library()

@register.filter
def in_pool(subcategory, pool):
    categories_in_pool = Question.objects.filter(pool__pool_name=pool).values_list('subcategory', flat=True)
    return subcategory.filter(pk__in=categories_in_pool)

@register.filter
def category_in_pool_count(category, pool):
    return Question.objects.filter(pool__pool_name=pool, subcategory__parent__pk=category.pk).count()

@register.filter
def subcategory_in_pool_count(subcategory, pool):
    return Question.objects.filter(pool__pool_name=pool, subcategory__pk=subcategory.pk).count()
