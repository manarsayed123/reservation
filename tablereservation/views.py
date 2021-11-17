from django.shortcuts import render

# Create your views here.
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from reservation.custom_permissions import IsAdmin
from reservation.utility import get_best_fit_table_slots, get_best_available_table_on_time
from table.models import Table
from tablereservation.models import Reservation
from tablereservation.serializers import ReservationSerializer, ReservationPostRequestSerializer
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend


class ListBestFitTableTimeSlots(ListAPIView):
    serializer_class = ReservationSerializer
    queryset = Table.objects.all()

    def list(self, request, *args, **kwargs):
        group_count = self.request.query_params.get("group_count", None)
        if not group_count:
            raise ValidationError("group_count field is required")

        return Response(get_best_fit_table_slots(group_count))


class TableReservation(CreateAPIView):
    serializer_class = ReservationPostRequestSerializer
    queryset = Reservation.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ReservationPostRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            best_table = get_best_available_table_on_time(self.request.data.get('start_time'),
                                                          self.request.data.get('end_time'),
                                                          self.request.data.get('group_member_count'))
            if best_table:
                obj = Reservation.objects.create(start_time=self.request.data.get('start_time'),
                                                 end_time=self.request.data.get('end_time'), table_id=best_table.id,
                                                 date=datetime.today().strftime('%Y-%m-%d'))
                return Response(ReservationSerializer(obj).data)
            return Response("on this time there are no table fit your group count")


class ListReservation(ListAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['date', 'table_id']
    filterset_fields = {'date': ['gte', 'lte', 'exact', 'gt', 'lt']}


class ListTodayReservation(ListAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.filter(date=datetime.today().strftime('%Y-%m-%d'))


class DeleteReservation(APIView):

    def delete(self, request, reservation_id):
        reservation = Reservation.objects.filter(id=reservation_id, date=datetime.today().strftime('%Y-%m-%d')).first()
        if not reservation:
            return Response("There are no reservation today with this id")
        reservation.delete()
        return Response("reservation deleted successfully")
