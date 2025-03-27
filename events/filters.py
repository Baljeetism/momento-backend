import django_filters
from .models import Eventsz

class EventFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre', lookup_expr='iexact')
    exclude = django_filters.NumberFilter(field_name='id', exclude=True)

    class Meta:
        model = Eventsz
        fields = ['genre']