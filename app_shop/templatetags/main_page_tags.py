from django.db.models import QuerySet
from django import template

register = template.Library()


@register.filter
def in_category(queryset: QuerySet, category: str) -> QuerySet:
    """Returns queryset of some items filtered by category"""

    return queryset.filter(category=category)
