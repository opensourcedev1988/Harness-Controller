from dsc.lib.bigip_rest import *


def add_bigip_to_dsc(bigip, dsc):
    from dsc.models import BIGIP
    bigip.dsc = dsc
    bigip.save()

    try:
        bigip_primary = BIGIP.objects.get(dsc=dsc, primary=True)
    except BIGIP.DoesNotExist:
        # This is the first BIG-IP in the DSC - nothing else to do.
        bigip.primary = True
        bigip.save()
        bigip.get_device_name()

        # Create Device Group
        url_endpoint = "/mgmt/tm/cm/device-group"
        post_args = {"name": "%s-dg" % dsc.name,
                     "auto-sync": "enabled",
                     "type": "sync-failover"}

        rest_post(bigip.mgmt_ip + url_endpoint, post_args,
                  login=bigip.login,
                  password=bigip.password)
        # Add device to device group (patch)
        url_endpoint = "/mgmt/tm/cm/device-group/%s-dg" % dsc.name
        device_group_list = [bigip.device_name]
        dsc.device_name_list = str(bigip.device_name)
        dsc.save()
        print(device_group_list)
        post_args = {"devices": device_group_list}
        rest_patch(url_endpoint=bigip.mgmt_ip + url_endpoint,
                   post_args=post_args,
                   login=bigip.login,
                   password=bigip.password)
        return

    bigip.get_device_name()
    post_args = {
        'command': 'run',
        'name': 'Root',
        'deviceName': bigip.device_name,
        'device': bigip.mgmt_ip,
        'username': bigip.login,
        'password': bigip.password,
        'caDevice': True
    }

    rest_post(url_endpoint=bigip_primary.mgmt_ip + '/mgmt/tm/cm/add-to-trust',
              post_args=post_args,
              login=bigip_primary.login,
              password=bigip_primary.password)
    # Add device to device group (patch)
    url_endpoint = "/mgmt/tm/cm/device-group/%s-dg" % dsc.name
    device_group_list = dsc.device_name_list.split(",")
    device_group_list.append(bigip.device_name)
    dsc.device_name_list = ",".join(list(set(device_group_list)))
    dsc.save()
    print(device_group_list)
    post_args = {"devices": device_group_list}
    rest_patch(url_endpoint=bigip_primary.mgmt_ip + url_endpoint,
               post_args=post_args,
               login=bigip_primary.login,
               password=bigip_primary.password)
    # Apply config sync
    url_endpoint = '/mgmt/tm/cm/config-sync'
    post_args = {'command': 'run',
                 'options': [{'to-group': '%s-dg' % dsc.name}]}
    rest_post(bigip_primary.mgmt_ip + url_endpoint,
              post_args,
              login=bigip_primary.login,
              password=bigip_primary.password)


def remove_bigip_from_dsc(bigip, dsc):
    from dsc.models import BIGIP
    dsc_bigip_count = BIGIP.objects.filter(dsc=dsc).count()

    # If this is the primary BIG-IP, find another one to be primary
    if bigip.primary:
        bigip.primary = False

        new_primary_list = BIGIP.objects.filter(dsc=dsc).exclude(id=bigip.id)
        if new_primary_list.count():
            new_primary = new_primary_list.first()
            new_primary.primary = True
            new_primary.save()

    bigip.dsc = None
    bigip.save()

    # Remove this BIGIP from the DSC
    if dsc_bigip_count > 1:
        bigip_primary = BIGIP.objects.get(dsc=dsc, primary=True)

        # Remove device from device group (delete)
        url_endpoint = "/mgmt/tm/cm/device-group/%s-dg/devices/%s" % (dsc.name, bigip.device_name)
        device_group_list = dsc.device_name_list.split(",")
        device_group_list.remove(bigip.device_name)
        dsc.device_name_list = ",".join(device_group_list)
        dsc.save()
        rest_delete(bigip_primary.mgmt_ip + url_endpoint,
                    login=bigip_primary.login,
                    password=bigip_primary.password)
        post_args = {
            'command': 'run',
            'deviceName': bigip.device_name,
            'caDevice': True,
        }

        rest_post(url_endpoint=bigip_primary.mgmt_ip + '/mgmt/tm/cm/remove-from-trust',
                  post_args=post_args,
                  login=bigip_primary.login,
                  password=bigip_primary.password)
        # Delete device group after removing from DSC
        url_endpoint = "/mgmt/tm/cm/device-group/%s-dg" % dsc.name
        rest_delete(bigip.mgmt_ip + url_endpoint)

    elif dsc_bigip_count == 1:
        # bigip_primary = BIGIP.objects.get(dsc=self, primary=True)
        # Delete device group after removing from DSC
        # Remove device from device group (delete)
        url_endpoint = "/mgmt/tm/cm/device-group/%s-dg/devices/%s" % (dsc.name, bigip.device_name)
        dsc.device_name_list = ""
        dsc.save()
        rest_delete(bigip.mgmt_ip + url_endpoint,
                    login=bigip.login,
                    password=bigip.password)
        url_endpoint = "/mgmt/tm/cm/device-group/%s-dg" % dsc.name
        rest_delete(bigip.mgmt_ip + url_endpoint)
        dsc.device_name_list = ""
        dsc.save()