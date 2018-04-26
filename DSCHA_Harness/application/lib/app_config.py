import configparser
import logging

from django.conf import settings
from lib.bigip_rest import *

logger = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read(settings.HARNESS_CONFIG_PATH)


class BadRequest(Exception):
    pass


def start_server(app, srv_ip, srv_port):
    from application.models import Application
    client_ip = config.get("harness", "server_agent")

    if app.protocol == Application.PROTOCOL_UDP:
        url = "http://%s:8000/api/v1/UDPServers/" % client_ip
        post_args = {"ip": srv_ip, "port": srv_port, "is_start": True}
        r = requests.post(url,
                          json=post_args)
        logger.debug(r.text)
        if r.status_code == 201:
            return r.json()["id"]
        else:
            raise BadRequest("UDP server didn't start successfully")

    elif app.protocol == Application.PROTOCOL_TCP:
        # TODO Create TCP traffic
        pass


def stop_server(app, server_side_id):

    from application.models import Application
    client_ip = config.get("harness", "server_agent")

    if app.protocol == Application.PROTOCOL_UDP:
        server_side_id = server_side_id
        url = "http://%s:8000/api/v1/UDPServers/%s/" % (client_ip, server_side_id)
        r = requests.delete(url)
        logger.debug(r.text)
        if r.status_code != 200:
            logger.warning(r.text)
            logger.warning("UDP server %s didn't stop successfully" % url)

    elif app.protocol == Application.PROTOCOL_TCP:
        # TODO Stop TCP traffic
        pass


def app_init_config(app):
    server_obj_list = app.appserver_set.all()
    server_list = ["%s:%s" % (server_obj.ip, server_obj.port)for server_obj in server_obj_list]
    bigip_primary = app.dsc.get_primary_bigip()

    # Create traffic group
    url_endpoint = "/mgmt/tm/cm/traffic-group"
    tg_obj = app.trafficgroup_set.first()
    post_args = {"name": "%s" % tg_obj.name}
    rest_post(bigip_primary.mgmt_ip + url_endpoint, post_args,
              login=bigip_primary.login,
              password=bigip_primary.password)

    # Create server pool
    url_endpoint = "/mgmt/tm/ltm/pool"
    post_args = {"name": "%s-pool" % app.name,
                 "members": server_list,
                 "monitor": app.PROTOCOL_MAP[app.protocol]}
    rest_post(bigip_primary.mgmt_ip + url_endpoint, post_args,
              login=bigip_primary.login,
              password=bigip_primary.password)

    # Create virtual server
    url_endpoint = "/mgmt/tm/ltm/virtual"
    virtual_obj = app.virtualserver_set.first()
    post_args = {"name": "%s" % virtual_obj.name,
                 "pool": "%s-pool" % app.name,
                 "destination": "%s:%s" % (app.vip, app.socket_port),
                 "ipProtocol": app.PROTOCOL_MAP[app.protocol],
                 "sourceAddressTranslation": {"type": "automap"}}
    rest_post(bigip_primary.mgmt_ip + url_endpoint, post_args,
              login=bigip_primary.login,
              password=bigip_primary.password)

    # Assign traffic group to virtual address
    url_endpoint = "/mgmt/tm/ltm/virtual-address/%s" % app.vip
    post_args = {"trafficGroup": "%s" % tg_obj.name}
    rest_patch(bigip_primary.mgmt_ip + url_endpoint, post_args,
               login=bigip_primary.login,
               password=bigip_primary.password)

    for server_obj in server_obj_list:
        srv_side_id = start_server(app, server_obj.ip, server_obj.port)
        server_obj.server_side_id = srv_side_id
        server_obj.is_start = True
        server_obj.save()


def app_tear_config(app):

    bigip_primary = app.dsc.get_primary_bigip()

    # Delete virtual server
    virtual_obj = app.virtualserver_set.first()
    url_endpoint = "/mgmt/tm/ltm/virtual/%s" % virtual_obj.name
    rest_delete(bigip_primary.mgmt_ip + url_endpoint,
                login=bigip_primary.login,
                password=bigip_primary.password)

    # Delete server pool
    url_endpoint = "/mgmt/tm/ltm/pool/%s-pool" % app.name
    rest_delete(bigip_primary.mgmt_ip + url_endpoint,
                login=bigip_primary.login,
                password=bigip_primary.password)

    # Delete traffic group
    tg_obj = app.trafficgroup_set.first()
    url_endpoint = "/mgmt/tm/cm/traffic-group/%s" % tg_obj.name
    rest_delete(bigip_primary.mgmt_ip + url_endpoint,
                login=bigip_primary.login,
                password=bigip_primary.password)

    server_obj_list = app.appserver_set.all()
    for server_obj in server_obj_list:
        stop_server(app, server_obj.server_side_id)
        server_obj.is_start = False
        server_obj.save()


def create_client_app(app):

    # Create client application
    from application.models import Application
    client_ip = config.get("harness", "client_agent")
    if app.protocol == Application.PROTOCOL_UDP:
        url = "http://%s:8000/api/v1/UDPTraffics/" % client_ip
        post_args = {"dst_ip": app.vip.ip, "dst_port": app.socket_port, "packet_per_second": app.packet_per_second}
        r = requests.post(url,
                          json=post_args)
        logger.debug(r.json())
        if r.status_code == 201:
            return r.json()["id"]
        else:
            raise BadRequest("Cannot create client UDPTraffic object")

    elif app.protocol == Application.PROTOCOL_TCP:
        # TODO Create TCP traffic
        pass


def delete_client_app(app):

    from application.models import Application
    client_ip = config.get("harness", "client_agent")
    if app.protocol == Application.PROTOCOL_UDP:
        url = "http://%s:8000/api/v1/UDPTraffics/%s/" % (client_ip,
                                                         app.client_app_id)
        r = requests.delete(url)
        logger.debug(r.text)
    elif app.protocol == Application.PROTOCOL_TCP:
        # TODO Delete TCP Traffic
        pass
    else:
        pass


def start_client_app(app):

    from application.models import Application
    client_ip = config.get("harness", "client_agent")
    if app.protocol == Application.PROTOCOL_UDP:
        url = "http://%s:8000/api/v1/UDPTraffics/%s/" % (client_ip,
                                                         app.client_app_id)
        post_args = {"is_start": True}
        r = requests.patch(url,
                           json=post_args)
        logger.debug(r.text)
        if r.status_code != 200:
            raise BadRequest("Client agent application didn't start successfully")
    elif app.protocol == Application.PROTOCOL_TCP:
        # TODO TCP traffic
        pass


def stop_client_app(app):
    from application.models import Application
    client_ip = config.get("harness", "client_agent")
    if app.protocol == Application.PROTOCOL_UDP:
        url = "http://%s:8000/api/v1/UDPTraffics/%s/" % (client_ip,
                                                         app.client_app_id)
        post_args = {"is_start": False}
        r = requests.patch(url,
                           json=post_args)
        logger.debug(r.text)
        if r.status_code != 200:
            raise BadRequest("Client app didn't stop or already stopped.")
    elif app.protocol == Application.PROTOCOL_TCP:
        # TODO TCP traffic
        pass