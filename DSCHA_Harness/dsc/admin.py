from django.contrib import admin
from dsc.models import BIGIP, DSC, VIP, VirtualServer, TrafficGroup


class BIGIPAdmin(admin.ModelAdmin):
    pass


class DSCAdmin(admin.ModelAdmin):
    pass


class VIPAdmin(admin.ModelAdmin):
    pass

admin.site.register(VIP, VIPAdmin)
admin.site.register(DSC, DSCAdmin)
admin.site.register(BIGIP, BIGIPAdmin)
admin.site.register(VirtualServer, BIGIPAdmin)
admin.site.register(TrafficGroup, BIGIPAdmin)
