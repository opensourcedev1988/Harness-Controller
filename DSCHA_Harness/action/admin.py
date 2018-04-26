from django.contrib import admin
from action.models import AppAction, BigipAction, DSCAction


class ActionAdmin(admin.ModelAdmin):
    pass

admin.site.register(AppAction, ActionAdmin)
admin.site.register(BigipAction, ActionAdmin)
admin.site.register(DSCAction, ActionAdmin)