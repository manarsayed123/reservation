from django.urls import path, include
from rest_framework.routers import DefaultRouter

from table.views import TableViewSet
from tablereservation.views import ListBestFitTableTimeSlots, TableReservation, ListReservation, DeleteReservation, \
    ListTodayReservation

urlpatterns = [
    path('slots/', ListBestFitTableTimeSlots.as_view(), name='time_slots'),
    path('reserve/', TableReservation.as_view(), name='reserve_table'),
    path('get-reservations/', ListReservation.as_view(), name='list_reservations'),
    path('get-today-reservations/', ListTodayReservation.as_view(), name='list_today_reservations'),
    path('delete-reservations/<int:reservation_id>/', DeleteReservation.as_view(), name='delete_reservation'),

]