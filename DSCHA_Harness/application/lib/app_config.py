import requests
import logging
import configparser
from global_var import *

logger = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read(harness_config_path)


def start_server(app, srv_obj):
    from application.models import Application
    client_ip = config.get("harness", "server_agent")

    if app.protocol == Application.PROTOCOL_UDP:
        url = "http://%s:8000/api/v1/UDPServers/" % client_ip
        post_args = {"ip": srv_obj.ip, "port": srv_obj.port, "is_start": True}
        r = requests.post(url,
                          json=post_args)
        logger.debug(r.text)
        if r.status_code == 201:
            srv_obj.server_side_id = r.json()["id"]
            srv_obj.save()

    elif app.protocol == Application.PROTOCOL_TCP:
        # TODO Create TCP traffic
        pass


def stop_server(app, srv_obj):

    from application.models import Application
    client_ip = config.get("harness", "server_agent")

    if app.protocol == Application.PROTOCOL_UDP:
        server_side_id = srv_obj.server_side_id
        url = "http://%s:8000/api/v1/UDPServers/%s/" % (client_ip, server_side_id)
        r = requests.delete(url)

    elif app.protocol == Application.PROTOCOL_TCP:
        # TODO Create TCP traffic
        pass
