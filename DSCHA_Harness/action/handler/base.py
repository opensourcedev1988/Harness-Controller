from application.models import Application
from dsc.models import BIGIP, DSC, TrafficGroup
from dsc.models import DSC


class Bigip(object):

    def __init__(self, id, dsc=None, app=None):
        self.id = id
        self.dsc = dsc
        self.app = app
        self.mgmt_ip = None
        self.login = None
        self.password = None
        self.primary = False
        self.device_name = None
        self.get_info()

    def get_info(self):
        bigip_model = BIGIP.objects.get(id=self.id)
        self.mgmt_ip = bigip_model.mgmt_ip
        self.login = bigip_model.login
        self.password = bigip_model.password
        self.primary = bigip_model.primary
        self.device_name = bigip_model.device_name
        if bigip_model.dsc and self.dsc is None:
            self.dsc = Dsc(bigip_model.dsc.id, bigip=self)

    def __str__(self):

        return "\n" \
               "id          : %s\n" \
               "mgmt ip     : %s\n" \
               "login       : %s\n" \
               "password    : %s\n" \
               "primary     : %s\n" \
               "device name : %s\n" % (self.id, self.mgmt_ip, self.login,
                                       self.password, self.primary,
                                       self.device_name)


class Dsc(object):

    def __init__(self, id, bigip=None, app=None):
        self.id = id
        self.bigip = bigip
        self.app = app
        self.name = None
        self.bigips = []
        self.apps = []
        self.get_info()

    def get_info(self):
        dsc_model = DSC.objects.get(id=self.id)
        self.name = dsc_model.name
        for app in dsc_model.application_set.all():
            if self.app and self.app.id == app.id:
                self.apps.append(self.app)
            else:
                self.apps.append(App(app.id, dsc=self))
        for bigip in dsc_model.bigip_set.all():
            if self.bigip and self.bigip.id == bigip.id:
                self.bigips.append(self.bigip)
            else:
                self.bigips.append(Bigip(bigip.id, dsc=self))

    def __str__(self):

        return "\n" \
               "id          : %s\n" \
               "name        : %s\n" % (self.id, self.name)


class App(object):

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

    def __init__(self, id, bigip=None, dsc=None):
        self.id = id
        self.bigip = bigip
        self.dsc = dsc
        self.name = None
        self.description = None
        self.protocol = None
        self.vip_port = None
        self.packet_per_second = None
        self.vip = None
        self.source_ip = None
        self.is_start = None
        self.client_app_id = None
        self.virtualserver = None
        self.trafficgroup = None
        self.application_servers = []
        self.get_info()

    def get_info(self):
        app_model = Application.objects.get(id=self.id)
        self.name = app_model.name
        self.description = app_model.description
        self.protocol = self.PROTOCOL_MAP[app_model.protocol]
        self.vip_port = app_model.socket_port
        self.packet_per_second = app_model.packet_per_second
        if app_model.dsc and self.dsc is None:
            self.dsc = Dsc(app_model.dsc.id, app=self)
        if app_model.vip:
            self.vip = app_model.vip.ip
        if app_model.src_ip:
            self.source_ip = app_model.src_ip.ip
        self.is_start = app_model.is_start
        self.client_app_id = app_model.client_app_id
        if app_model.virtualserver_set.all():
            self.virtualserver = app_model.virtualserver_set.all().first().name
        if app_model.trafficgroup_set.all():
            self.trafficgroup = app_model.trafficgroup_set.all().first().name
        for appserver in app_model.appserver_set.all():
            self.application_servers.append("%s:%s" % (appserver.ip, appserver.port))

    def __str__(self):

        return "\n" \
               "id                : %s\n" \
               "name              : %s\n" \
               "description       : %s\n" \
               "protocol          : %s\n" \
               "vip               : %s\n" \
               "vip port          : %s\n" \
               "packet per second : %s\n" \
               "source ip         : %s\n" \
               "virtual server    : %s\n" \
               "traffic group     : %s \n" % (self.id, self.name, self.description,
                                              self.protocol, self.vip, self.vip_port,
                                              self.packet_per_second, self.source_ip,
                                              self.virtualserver, self.trafficgroup)


def get_application(id):

    return App(int(id))


def get_bigip(id):

    return Bigip(int(id))


def get_dsc(id):

    return Dsc(int(id))