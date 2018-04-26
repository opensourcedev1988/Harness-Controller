from celery import shared_task
from lib.bigip_tmsh import *
from lib.bigip_rest import *
from lib.bigip_lib import *
from lib.dsc_lib import *
from lib.application_lib import *
from action.handler.base import get_application, get_bigip, get_dsc
from action.handler.error import ModelNotExistException


@shared_task()
def action(*args, **kwargs):
    """
    Action function to define your periodic task action. Get your target object id from kwargs or args

    :param args: list argument of application id, bigip id, or dsc id. [<app_id>/<bigip_id>/<dsc_id>]
    :param kwargs: dictionary of app id, bigip id, or dsc id.
    {"app": <app_id>, "bigip": <bigip_id>, "dsc": <dsc_id>}
    :return:
    """
    app_obj = None
    bigip_obj = None
    dsc_obj = None
    if 'app' in kwargs:
        app_id = kwargs.get('app')
        app_obj = get_application(app_id)
    if 'bigip' in kwargs:
        bigip_id = kwargs.get('bigip')
        bigip_obj = get_application(bigip_id)
    if 'dsc' in kwargs:
        dsc_id = kwargs.get('dsc')
        dsc_obj = get_application(dsc_id)
    if not app_obj and not bigip_obj and not dsc_obj:
        raise ModelNotExistException
    active_dev = get_active_device(app_obj)
    traffic_group_failover(app_obj.trafficgroup, active_dev)


