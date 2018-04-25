from lib.bigip_tmsh import *
from lib.bigip_rest import *


def get_active_device(app_obj):
    """
    Fetch the device object which is hosting the specified traffic group
    :param dsc: The DSC object
    :param tg: Traffic group name
    :return: A Device object, or None if no BIG-IP's are active for the TG
    """
    for bigip in app_obj.dsc.bigips:
        cmd = 'tmsh show cm traffic-group ' + app_obj.trafficgroup
        output = runcmd_ssh(address=bigip.mgmt_ip, cmd=cmd).stdout.split('\n')
        for dev_index in output:
            if bigip.device_name in dev_index:
                if ('next-active' not in dev_index and 'active' in dev_index) or \
                        'degraded' in dev_index:
                    return bigip
    return None


def traffic_group_failover(tg_name, bigip):

    url_endpoint = "/mgmt/tm/sys/failover"
    args = {
                'command': 'run',
                'trafficGroup': tg_name,
                'standby': True
            }
    rest_post(bigip.mgmt_ip + url_endpoint, args,
              login=bigip.login,
              password=bigip.password)