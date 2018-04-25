import logging

from django.db import models
from django.db.models import SET_NULL

from application.models import Application
from dsc.lib.bigip_config import add_bigip_to_dsc, remove_bigip_from_dsc
from lib.bigip_rest import rest_get

logger = logging.getLogger(__name__)


class DSC(models.Model):
    name = models.CharField(max_length=256)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('view dsc', kwargs={'dsc_id': str(self.id)})

    def __str__(self):
        return str(self.name)

    def get_primary_bigip(self):

        try:
            bigip_primary = BIGIP.objects.get(dsc=self, primary=True)
            return bigip_primary
        except BIGIP.DoesNotExist:
            return None

    def remove_bigip(self, bigip):

        remove_bigip_from_dsc(bigip, self)

    def add_bigip(self, bigip):

        add_bigip_to_dsc(bigip, self)


class BIGIP(models.Model):
    mgmt_ip = models.GenericIPAddressField()
    login = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    primary = models.BooleanField(default=False)
    device_name = models.CharField(max_length=256, default='')

    dsc = models.ForeignKey(DSC, on_delete=SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.mgmt_ip)

    def get_device_name(self):
        response = rest_get(self.mgmt_ip + "/mgmt/tm/cm/device")
        self.device_name = response.json()['items'][0]['hostname']
        self.save()


class VirtualServer(models.Model):
    name = models.CharField(max_length=256)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class TrafficGroup(models.Model):
    name = models.CharField(max_length=256)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True)
    bigips = models.ManyToManyField(BIGIP)

    def __str__(self):
        return self.name


class VIP(models.Model):
    ip = models.GenericIPAddressField()

    def __str__(self):
        return str(self.ip)


def pretty_print_post(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
