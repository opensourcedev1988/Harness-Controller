from celery import task, shared_task, uuid
from application.models import Application
from dsc.models import TrafficGroup
from DSCHA_Harness import celery_app
from dsc.lib.bigip_config import get_active_device, traffic_group_failover


@shared_task
def tg_failover(*args, **kwargs):
    if 'app' in kwargs:
        app_name = kwargs.get('app')
    elif len(args) > 0:
        app_name = args[0]
    else:
        return
    app_object = Application.objects.get(name=app_name)
    tg_name = "%s-tg" % app_object.dsc.name
    tg_object = TrafficGroup.objects.get(name=tg_name)
    active_dev = get_active_device(tg_object)
    traffic_group_failover(tg_name, active_dev)