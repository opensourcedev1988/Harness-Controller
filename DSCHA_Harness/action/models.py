import json
import ast
from django.db import models
from django.db.models import SET_NULL
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule, SolarSchedule


class AppAction(models.Model):
    name = models.CharField(max_length=100, unique=True)
    task_str = models.CharField(max_length=200)
    periodic_task = models.OneToOneField('django_celery_beat.PeriodicTask',
                                         on_delete=models.CASCADE,
                                         null=True,
                                         blank=True)
    application = models.ForeignKey('application.Application',
                                    on_delete=models.CASCADE,
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
    args_str = models.CharField(max_length=1024, null=True, blank=True)
    kwargs_str = models.CharField(max_length=1024, null=True, blank=True)
    is_enable = models.BooleanField(default=False)

    def set_task_str(self, task_str):
        self.task_str = task_str.replace("-", ".")
        self.save()

    def build_args_str(self):
        self.args_str = str(self.application.id)
        self.save()

    def build_kwargs_str(self):
        self.kwargs_str = "{'app' : %s}" % self.application.id

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
                             enabled=self.is_enable
                         )
        self.periodic_task = periodic_task
        self.save()

    def update_task(self):

        self.periodic_task.interval = self.interval
        self.periodic_task.crontab = self.crontab
        self.periodic_task.solar = self.solar
        self.periodic_task.name = self.name
        self.periodic_task.task = self.task_str
        self.periodic_task.args = json.dumps(self.args_str.strip().split(","))
        self.periodic_task.kwargs = json.dumps(ast.literal_eval(self.kwargs_str))
        self.periodic_task.enabled = self.is_enable
        self.periodic_task.save()
        self.save()

    def __str__(self):

        return "%s" % self.name


class DSCAction(models.Model):
    name = models.CharField(max_length=100, unique=True)
    task_str = models.CharField(max_length=200)
    periodic_task = models.OneToOneField('django_celery_beat.PeriodicTask',
                                         on_delete=models.CASCADE,
                                         null=True,
                                         blank=True)
    dsc = models.ForeignKey('dsc.DSC',
                            on_delete=models.CASCADE,
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
    args_str = models.CharField(max_length=1024, null=True, blank=True)
    kwargs_str = models.CharField(max_length=1024, null=True, blank=True)
    is_enable = models.BooleanField(default=False)

    def set_task_str(self, task_str):
        self.task_str = task_str.replace("-", ".")
        self.save()

    def build_args_str(self):
        self.args_str = str(self.dsc.id)
        self.save()

    def build_kwargs_str(self):
        self.kwargs_str = "{'dsc' : %s}" % self.dsc.id

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
                             enabled=self.is_enable
                         )
        self.periodic_task = periodic_task
        self.save()

    def update_task(self):

        self.periodic_task.interval = self.interval
        self.periodic_task.crontab = self.crontab
        self.periodic_task.solar = self.solar
        self.periodic_task.name = self.name
        self.periodic_task.task = self.task_str
        self.periodic_task.args = json.dumps(self.args_str.strip().split(","))
        self.periodic_task.kwargs = json.dumps(ast.literal_eval(self.kwargs_str))
        self.periodic_task.enabled = self.is_enable
        self.periodic_task.save()
        self.save()

    def __str__(self):

        return "%s" % self.name


class BigipAction(models.Model):
    name = models.CharField(max_length=100, unique=True)
    task_str = models.CharField(max_length=200)
    periodic_task = models.OneToOneField('django_celery_beat.PeriodicTask',
                                         on_delete=models.CASCADE,
                                         null=True,
                                         blank=True)
    bigip = models.ForeignKey('dsc.BIGIP',
                              on_delete=models.CASCADE,
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
    args_str = models.CharField(max_length=1024, null=True, blank=True)
    kwargs_str = models.CharField(max_length=1024, null=True, blank=True)
    is_enable = models.BooleanField(default=False)

    def set_task_str(self, task_str):
        self.task_str = task_str.replace("-", ".")
        self.save()

    def build_args_str(self):
        self.args_str = str(self.bigip.id)
        self.save()

    def build_kwargs_str(self):
        self.kwargs_str = "{'bigip' : %s}" % self.bigip.id

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
                             enabled=self.is_enable
                         )
        self.periodic_task = periodic_task
        self.save()

    def update_task(self):

        self.periodic_task.interval = self.interval
        self.periodic_task.crontab = self.crontab
        self.periodic_task.solar = self.solar
        self.periodic_task.name = self.name
        self.periodic_task.task = self.task_str
        self.periodic_task.args = json.dumps(self.args_str.strip().split(","))
        self.periodic_task.kwargs = json.dumps(ast.literal_eval(self.kwargs_str))
        self.periodic_task.enabled = self.is_enable
        self.periodic_task.save()
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
