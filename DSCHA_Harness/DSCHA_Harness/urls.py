"""DSCHA_Harness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from dsc import views as dsc_views
from dashboard import views as dash_views
from application import views as app_views


urlpatterns = [

    path(r'', dash_views.index, name='index'),

    # BIG-IP management
    path(r'add_bigip', dsc_views.add_bigip, name='add bigip'),
    re_path(r'^delete_bigip/(?P<bigip_id>[0-9]+)/(?P<confirm>\d)$', dsc_views.delete_bigip, name='delete bigip'),
    path(r'manage_bigip', dsc_views.manage_bigip, name='manage bigip'),
    re_path(r'^get_bigip_sync_status/(?P<bigip_id>[0-9]+)$', dsc_views.get_bigip_sync_status, name='get bigip sync status'),
    re_path(r'^get_bigip_failover_state/(?P<bigip_id>[0-9]+)$', dsc_views.get_bigip_failover_state, name='get bigip failover state'),

    # Application management
    re_path(r'^create_app/(?P<dsc_id>[0-9]+)$', app_views.create_app, name='create app'),
    re_path(r'^delete_app/(?P<app_id>[0-9]+)/(?P<confirm>\d)$', app_views.delete_app, name='delete app'),
    re_path(r'^start_app/(?P<app_id>[0-9]+)$', app_views.start_app, name='start app'),
    re_path(r'^stop_app/(?P<app_id>[0-9]+)$', app_views.stop_app, name='stop app'),

    # DSC management
    path(r'create_dsc', dsc_views.create_dsc, name='create dsc'),
    re_path(r'dsc/(?P<dsc_id>[0-9]+)$', dsc_views.view_dsc, name='view dsc'),
    re_path(r'delete_dsc/(?P<dsc_id>[0-9]+)/(?P<confirm>\d)$', dsc_views.delete_dsc, name='delete dsc'),
    re_path(r'dsc_add_bigip', dsc_views.dsc_add_bigip, name='dsc add bigip'),
    re_path(r'dsc_remove_bigip/(?P<dsc_id>[0-9]+)/(?P<bigip_id>[0-9]+)/(?P<confirm>\d)$', dsc_views.dsc_remove_bigip, name='dsc remove bigip'),

    # Admin interface
    path('admin/', admin.site.urls),
]
