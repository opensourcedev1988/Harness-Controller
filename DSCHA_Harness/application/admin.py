from django.contrib import admin
from application.models import Application, SOURCEIP, AppServer, UDPTrafficStat


class ApplicationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Application, ApplicationAdmin)
admin.site.register(SOURCEIP, ApplicationAdmin)
admin.site.register(AppServer, ApplicationAdmin)
admin.site.register(UDPTrafficStat, ApplicationAdmin)