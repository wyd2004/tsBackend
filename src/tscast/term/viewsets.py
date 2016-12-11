from django_filters import FilterSet

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response 
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from .models import Tier
from .models import Order
from .models import Payment
from .serializers import TierSerializer
from .serializers import OrderSerializer
from .serializers import PaymentSerializer

from member.models import Member


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
        queryset = self.model.objects.filter(is_published=True)
        queryset = queryset.order_by('seq')
        return queryset

class MemberWriteOnly(BasePermission):
    def has_permission(self, request, view):
        if type(request.user) is Member and request.method == 'POST':
            return True
        else:
            return False

    def has_object_permission(self, request, view, object):
        return False


class OrderViewSet(viewsets.ModelViewSet):
    model = Order
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (MemberWriteOnly,)
