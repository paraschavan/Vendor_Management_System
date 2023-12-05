import django_filters
from main.models import PurchaseOrder


class PurchaseOrderFilter(django_filters.FilterSet):
    class Meta:
        model = PurchaseOrder
        fields = ['vendor', ]
