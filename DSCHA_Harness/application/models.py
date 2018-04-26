import logging

from django.db import models
from django.db.models import SET_NULL
from lib.bigip_rest import *

logger = logging.getLogger(__name__)


class SOURCEIP(models.Model):
    ip = models.GenericIPAddressField(unique=True)

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

    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(null=True, blank=True)
    protocol = models.IntegerField(choices=PROTOCOL_CHOICES)    # Is this TCP or UDP?
    socket_port = models.IntegerField()                         # TCP or UDP port for BIG-IP VIP and server nodes
    packet_per_second = models.BigIntegerField()
    dsc = models.ForeignKey('dsc.DSC', on_delete=models.CASCADE)
    vip = models.ForeignKey('dsc.VIP', on_delete=SET_NULL, null=True)
    src_ip = models.ForeignKey('application.SOURCEIP', on_delete=SET_NULL, null=True)
    is_start = models.BooleanField(default=False)
    client_app_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class AppServer(models.Model):
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    server_side_id = models.IntegerField(null=True, blank=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True)
    is_start = models.BooleanField(default=False)

    def __str__(self):
        return "%s:%s" % (self.ip, self.port)


class UDPTrafficStat(models.Model):

    app_id = models.IntegerField()
    byte_sent = models.BigIntegerField()
    packets_sent = models.BigIntegerField()
    packets_receive = models.BigIntegerField()
    drop_packets = models.BigIntegerField()
    avg_latency = models.FloatField()
    pkt_time = models.DateTimeField()

    def __str__(self):

        return "%s: %s" % (self.app_id, self.pkt_time)

