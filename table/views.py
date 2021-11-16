from django.shortcuts import render

# Create your views here.
from reservation.custom_permissions import IsAdmin
from table.models import Table
from rest_framework.viewsets import ModelViewSet

from table.serializers import TableSerializer


class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    filter_fields = ['number', 'num_of_seats']
    permission_classes = [IsAdmin]
