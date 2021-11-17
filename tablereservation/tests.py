# Create your tests here.
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework import status

from authentication.models import User
from table.models import Table
from datetime import datetime, timedelta

from tablereservation.models import Reservation


class TestListPublishedProducts(TestCase):

    def setUp(self):
        self.client = APIClient()
        emp_user = User.objects.create(employee_num=1234, role=User.EMPLOYEE)
        emp_user.set_password('123456')
        emp_user.save()
        Table.objects.create(number=1, num_of_seats=3)
        Table.objects.create(number=2, num_of_seats=6)
        table3 = Table.objects.create(number=3, num_of_seats=12)
        Reservation.objects.create(start_time='12:00', end_time='13:00', table=table3)
        Reservation.objects.create(start_time='21:00', end_time='22:00', table=table3)

    def test_reserve_best_fit_table(self):
        """reserve the best fit table with the smallest seats that cover the group"""
        start_time = datetime.now() + timedelta(hours=2)
        start_time = start_time.strftime('%H:%M:%S')
        end_time = datetime.now() + timedelta(hours=3)
        end_time = end_time.strftime('%H:%M:%S')

        self.client.login(employee_num="1234", password='123456')
        response = self.client.post('/reserve/',
                                    data={'start_time': start_time, 'end_time': end_time, 'group_member_count': 2})
        self.assertEqual(Reservation.objects.first().table.number, 1)

    def test_reserve_table_before_restaurant_open(self):
        """start time of reservation before the restaurant open"""
        start_time = "11:00"
        end_time = "12:00"
        self.client.login(employee_num="1234", password='123456')
        response = self.client.post('/reserve/',
                                    data={'start_time': start_time, 'end_time': end_time, 'group_member_count': 2})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reserve_table_with_group_count_greater_than_max_seats(self):
        start_time = "22:00"
        end_time = "23:00"
        self.client.login(employee_num="1234", password='123456')
        response = self.client.post('/reserve/',
                                    data={'start_time': start_time, 'end_time': end_time, 'group_member_count': 15})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_table_that_fit_group_count_reserved_on_this_time(self):
        start_time = "12:00"
        end_time = "14:00"
        self.client.login(employee_num="1234", password='123456')
        response = self.client.post('/reserve/',
                                    data={'start_time': start_time, 'end_time': end_time, 'group_member_count': 12})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_table_time_slots_when_there_are_no_reservations(self):
        self.client.login(employee_num="1234", password='123456')
        response = self.client.get(reverse('time_slots'), {'group_count': 12})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_table_time_slots_when_there_are_areservation_on_the_middle_of_day(self):
        self.client.login(employee_num="1234", password='123456')
        response = self.client.get(reverse('time_slots'), {'group_count': 12})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
