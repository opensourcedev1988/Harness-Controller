from rest_framework import serializers
from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule, CrontabSchedule, SolarSchedule
from .models import AppAction, DSCAction, BigipAction


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


class AppActionSerilizer(serializers.ModelSerializer):

    class Meta:
        model = AppAction
        fields = ('id', 'name', 'application', 'interval',
                  'crontab', 'solar', 'is_enable', 'periodic_task',
                  'args_str', 'kwargs_str')
        read_only_fields = ('periodic_task', 'args_str', 'kwargs_str')


class DSCActionSerilizer(serializers.ModelSerializer):

    class Meta:
        model = DSCAction
        fields = ('id', 'name', 'dsc', 'interval',
                  'crontab', 'solar', 'is_enable', 'periodic_task',
                  'args_str', 'kwargs_str')
        read_only_fields = ('periodic_task', 'args_str', 'kwargs_str')


class BigipActionSerilizer(serializers.ModelSerializer):

    class Meta:
        model = BigipAction
        fields = ('id', 'name', 'bigip', 'interval',
                  'crontab', 'solar', 'is_enable', 'periodic_task',
                  'args_str', 'kwargs_str')
        read_only_fields = ('periodic_task', 'args_str', 'kwargs_str')
