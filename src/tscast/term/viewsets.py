from django_filters import FilterSet
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response 
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from .models import Tier
from .serializers import TierSerializer


class Readonly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, object):
        return request.method in SAFE_METHODS


class TierViewSet(viewsets.ModelViewSet):
    model = Tier
    serializer_class = TierSerializer
    permission_classes = (Readonly,)

    def get_queryset(self):
        return self.model.objects.filter(is_published=True)
