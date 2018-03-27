import logging
from django.conf import settings
from django.db import models
from application.lib.app_config import start_server, stop_server
from django.db.models import SET_NULL
from dsc.lib.bigip_rest import *

logger = logging.getLogger(__name__)


class SOURCEIP(models.Model):
    ip = models.GenericIPAddressField()

    def __str__(self):
        return str(self.ip)


class Application(models.Model):

    PROTOCOL_TCP = 1
    PROTOCOL_UDP = 2

    PROTOCOL_CHOICES = (
        (PROTOCOL_TCP, "TCP"),
        (PROTOCOL_UDP, "UDP"),
    )

    PROTOCOL_MAP = {
        PROTOCOL_TCP: "tcp",
        PROTOCOL_UDP: "udp",
    }

    name = models.CharField(max_length=256)
    description = models.TextField()
    protocol = models.IntegerField(choices=PROTOCOL_CHOICES)    # Is this TCP or UDP?
    socket_port = models.IntegerField()                         # TCP or UDP port for BIG-IP VIP and server nodes
    packet_per_second = models.BigIntegerField()
    dsc = models.ForeignKey('dsc.DSC', on_delete=SET_NULL, null=True, blank=True)
    vip = models.ForeignKey('dsc.VIP', on_delete=SET_NULL, null=True, blank=True)
    src_ip = models.ForeignKey('application.SOURCEIP', on_delete=SET_NULL, null=True, blank=True)
    virtual_server = models.CharField(max_length=256, default='')           # Name of the virtual server for this app on BIG-IP
    is_start = models.BooleanField(default=False)
    client_app_id = models.IntegerField(null=True, blank=True)

    def init_config(self):

        server_obj_list = AppServer.objects.filter(application=self)
        server_list = ["%s:%s" % (server_obj.ip, server_obj.port)for server_obj in server_obj_list]
        bigip_primary = self.dsc.get_primary_bigip()

        # Create traffic group
        url_endpoint = "/mgmt/tm/cm/traffic-group"
        post_args = {"name": "%s-tg" % self.name}
        rest_post(bigip_primary.mgmt_ip + url_endpoint, post_args,
                  login=bigip_primary.login,
                  password=bigip_primary.password)

        # Create server pool
        url_endpoint = "/mgmt/tm/ltm/pool"
        post_args = {"name": "%s-pool" % self.name,
                     "members": server_list,
                     "monitor": self.PROTOCOL_MAP[self.protocol]}
        rest_post(bigip_primary.mgmt_ip + url_endpoint, post_args,
                  login=bigip_primary.login,
                  password=bigip_primary.password)

        # Create virtual server
        url_endpoint = "/mgmt/tm/ltm/virtual"
        post_args = {"name": "%s-virtual" % self.name,
                     "pool": "%s-pool" % self.name,
                     "destination": "%s:%s" % (self.vip, self.socket_port),
                     "ipProtocol": self.PROTOCOL_MAP[self.protocol],
                     "sourceAddressTranslation": {"type": "automap"}}
        rest_post(bigip_primary.mgmt_ip + url_endpoint, post_args,
                  login=bigip_primary.login,
                  password=bigip_primary.password)

        # Assign traffic group to virtual address
        url_endpoint = "/mgmt/tm/ltm/virtual-address/%s" % self.vip
        post_args = {"trafficGroup": "%s-tg" % self.name}
        rest_patch(bigip_primary.mgmt_ip + url_endpoint, post_args,
                   login=bigip_primary.login,
                   password=bigip_primary.password)

        for server_obj in server_obj_list:
            start_server(self, server_obj)

    def tear_config(self):

        bigip_primary = self.dsc.get_primary_bigip()

        # Delete virtual server
        url_endpoint = "/mgmt/tm/ltm/virtual/%s-virtual" % self.name
        rest_delete(bigip_primary.mgmt_ip + url_endpoint,
                    login=bigip_primary.login,
                    password=bigip_primary.password)

        # Delete server pool
        url_endpoint = "/mgmt/tm/ltm/pool/%s-pool" % self.name
        rest_delete(bigip_primary.mgmt_ip + url_endpoint,
                    login=bigip_primary.login,
                    password=bigip_primary.password)

        # Delete traffic group
        url_endpoint = "/mgmt/tm/cm/traffic-group/%s-tg" % self.name
        rest_delete(bigip_primary.mgmt_ip + url_endpoint,
                    login=bigip_primary.login,
                    password=bigip_primary.password)

        server_obj_list = AppServer.objects.filter(application=self)
        for server_obj in server_obj_list:
            stop_server(self, server_obj)

    def __str__(self):
        return self.name


class AppServer(models.Model):
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    server_side_id = models.IntegerField(null=True, blank=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "%s:%s" % (self.ip, self.port)


class UDPTrafficStat(models.Model):

    class Meta:
        db_table = settings.DATABASES['default']['NAME']
        managed = False

    app_id = models.IntegerField()
    byte_sent = models.BigIntegerField()
    packets_sent = models.BigIntegerField()
    packets_receive = models.BigIntegerField()
    drop_packets = models.BigIntegerField()
    avg_latency = models.FloatField()
    pkt_time = models.DateTimeField()

