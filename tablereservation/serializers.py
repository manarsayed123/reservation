from django.conf import settings
from rest_framework import serializers

from .models import Reservation


class ReservationPostRequestSerializer(serializers.Serializer):
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    group_member_count = serializers.IntegerField()

    def validate_start_time(self, start_time):
        if start_time < settings.RESTAURANT_OPEN_AT or start_time > settings.RESTAURANT_CLOSE_AT:
            raise serializers.ValidationError(
                f'restaurant only available from {settings.RESTAURANT_OPEN_AT} to {settings.RESTAURANT_CLOSE_AT}')

    def validate_end_time(self, end_time):
        if end_time < settings.RESTAURANT_OPEN_AT or end_time > settings.RESTAURANT_CLOSE_AT:
            raise serializers.ValidationError(
                f'restaurant only available from {settings.RESTAURANT_OPEN_AT} to {settings.RESTAURANT_CLOSE_AT}')

    def validate_group_member_count(self, group_member_count):
        if group_member_count > settings.MAX_TABLE_SEATS_COUNT:
            raise serializers.ValidationError(f'max group that we can serve is {settings.MAX_TABLE_SEATS_COUNT}')


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
