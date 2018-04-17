import inspect
import json
import ast
from django.db import models
from django.db.models import SET_NULL
from application.tasks import tg_failover
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule, SolarSchedule


# Create your models here.
class FailoverAction(models.Model):
    name = models.CharField(max_length=100)
    task_str = models.CharField(max_length=200)
    periodic_task = models.ForeignKey('django_celery_beat.PeriodicTask',
                                      on_delete=models.CASCADE,
                                      null=True,
                                      blank=True)
    application = models.ForeignKey('application.Application',
                                    on_delete=SET_NULL,
                                    null=True,
                                    blank=True)
    interval = models.ForeignKey(IntervalSchedule,
                                 on_delete=SET_NULL,
                                 null=True,
                                 blank=True)
    crontab = models.ForeignKey(CrontabSchedule,
                                on_delete=SET_NULL,
                                null=True,
                                blank=True)
    solar = models.ForeignKey(SolarSchedule,
                              on_delete=SET_NULL,
                              null=True,
                              blank=True)
    args_str = models.CharField(max_length=1024)
    kwargs_str = models.CharField(max_length=1024)
    is_enable = models.BooleanField(default=False)

    def set_task_str(self, func):
        self.task_str = "%s.%s" % (inspect.getmodule(func).__name__, func.__name__)
        self.save()

    def build_args_str(self):
        self.args_str = self.application.name
        self.save()

    def build_kwargs_str(self):
        self.kwargs_str = "{'app' : %s}" % self.application.name

    def create_task(self):
        periodic_task = PeriodicTask.objects.create(
                             interval=self.interval,
                             crontab=self.crontab,
                             solar=self.solar,
                             name=self.name,
                             task=self.task_str,
                             args=json.dumps(self.args_str.strip().split(",")),
                             kwargs=json.dumps(ast.literal_eval(self.kwargs_str)),
                             # expires=datetime.utcnow() + timedelta(seconds=30)
                         )
        self.is_enable = True
        self.periodic_task = periodic_task
        self.save()

    def __str__(self):

        return "%s" % self.name


class EditThroughputAction(models.Model):
    pass


class BigipRebootAction(models.Model):
    pass


class AddAppServerAction(models.Model):
    pass


class AppServerRebootAction(models.Model):
    pass
