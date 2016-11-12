from __future__ import unicode_literals

from django.db.models import Manager
from django.db.models.query import QuerySet
from django.utils import timezone


class BaseManager(Manager):
    def get_query_set(self):
        queryset = super(BaseManager, self).get_query_set()
        if 'is_deleted' in dir(self.model):
            queryset = queryset.filter(is_deleted=False)
        return queryset

