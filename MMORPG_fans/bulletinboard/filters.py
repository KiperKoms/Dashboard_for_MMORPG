from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter
from .models import *


class CommentFilter(FilterSet):
    added_after = DateTimeFilter(
            field_name='comment_dateCreation',
            lookup_expr='gt',
            widget=DateTimeInput(
                format='%Y-%m-%d',
                attrs={'type':'date'},
            ),
            label=pgettext_lazy('date of creation', 'Posted after')
        )

    class Meta:
        model = Comment
        fields = {
            'comment_author__username': ['contains'],
            'comment_post__title': ['icontains'],
            'accepted': ['exact']
        }