from collections import OrderedDict

from django.db.models import Sum, Value, Count
from django.db.models.functions import Coalesce, TruncMonth, TruncYear


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))

def summary_per_year_month(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(month=TruncMonth("date"))
        .order_by('month')
        .values('month')
        .annotate(s=Sum('amount'))
        .values_list('month', 's')
    ))

def total_items(queryset):
    return OrderedDict(sorted(
        queryset
        .order_by('category')
        .values('category')
        .annotate(cat_name=Count('category__name'))
        .values_list('category__name', 'cat_name')
    ))