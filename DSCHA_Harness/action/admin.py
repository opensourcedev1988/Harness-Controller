from django.contrib import admin
from action.models import FailoverAction


class ActionAdmin(admin.ModelAdmin):
    pass

admin.site.register(FailoverAction, ActionAdmin)