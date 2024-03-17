import django_filters

from core.models import News


class NewsFilter(django_filters.FilterSet):
    employe = django_filters.NumberFilter(field_name="employe__id")

    class Meta:
        model = News
        fields = ['employe']