from rest_framework import serializers
from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule, CrontabSchedule, SolarSchedule
from .models import FailoverAction


class IntervalScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = IntervalSchedule
        fields = ('id', 'every', 'period')


class CrontabScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = CrontabSchedule
        fields = ('id', 'minute', 'hour', "day_of_week", "day_of_month", "month_of_year")


class SolarScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = SolarSchedule
        fields = ('id', 'event', 'latitude', 'longitude')


class FailoverActionSerilizer(serializers.ModelSerializer):

    class Meta:
        model = FailoverAction
        fields = ('id', 'name', 'application', 'interval', 'crontab', 'solar', 'is_enable')