from django.conf import settings
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from table.models import Table
from table.serializers import TableSerializer
from tablereservation.models import Reservation


def get_best_available_table_on_time(start_time, end_time, group_count):
    # if end_time < settings.RESTAURANT_OPEN_AT or end_time > settings.RESTAURANT_CLOSE_AT:
    #     raise ValidationError(
    #         f'restaurant only available from {settings.RESTAURANT_OPEN_AT} to {settings.RESTAURANT_CLOSE_AT}')
    # if customer_count > settings.MAX_TABLE_SEATS_COUNT:
    #     raise ValidationError(f'max group that we can serve is {settings.MAX_TABLE_SEATS_COUNT}')
    tables_fit_customer_count = Table.objects.filter(num_of_seats__gte=group_count).order_by('num_of_seats')
    un_available_tables = Reservation.objects.filter(table__in=tables_fit_customer_count,
                                                     start_time__gte=start_time,
                                                     end_time__lte=end_time).values_list('table',flat=True).distinct()
    best_available_table = tables_fit_customer_count.filter(~Q(id__in=un_available_tables))
    if best_available_table:
        return best_available_table.first()
    return None


def get_best_fit_table_slots(group_count):
    from datetime import datetime
    time_now = datetime.now().strftime('%H:%M:%S')
    fit_tables = Table.objects.filter(num_of_seats__gte=group_count).order_by('num_of_seats')
    if not fit_tables:
        return Response("there are no tables fit your group")

    for table in fit_tables:
        time_slots = []
        table_reservations = Reservation.objects.filter(table__id=table.id, end_time__gt=time_now)
        if table_reservations.count() == 0:
            time_slots.append({"from": time_now, "to": settings.RESTAURANT_CLOSE_AT})
            return {"table": TableSerializer(table).data, "time_slots": time_slots}

        for index, reservation in enumerate(table_reservations):
            if index + 1 < table_reservations.count():
                if reservation.end_time < table_reservations[index + 1].start_time:
                    time_slots.append(
                        {"from": reservation.end_time, "to": table_reservations[index + 1].start_time})

            elif reservation.end_time < settings.RESTAURANT_CLOSE_AT:
                time_slots.append(
                    {"from": reservation.end_time, "to": settings.RESTAURANT_CLOSE_AT})
        if len(time_slots) > 0:
            return {"table": TableSerializer(table).data, "time_slots": time_slots}
        else:
            return Response("there are no tables fit your group")
