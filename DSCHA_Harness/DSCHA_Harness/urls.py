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
from django.urls import path, re_path, include
from django.conf.urls import url
from dsc import views as dsc_views
from dashboard import views as dash_views
from application import views as app_views
from action import views as action_views
from dsc import api as dsc_api
from application import api as app_api
from action import api as action_api
from rest_framework.documentation import include_docs_urls

API_TITLE = 'Harness Controller API'

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

    # Rest API

    # DSC API
    url(r'^api/v1/dsc/$', dsc_api.DSCList.as_view()),
    url(r'^api/v1/dsc/(?P<pk>[0-9]+)/$', dsc_api.DSCDetail.as_view()),

    # # Two shortcut api to add/remove big, not normally used
    # url(r'^api/v1/dsc/(?P<pk>[0-9]+)/addbigip/(?P<bigip_pk>[0-9]+)/$', dsc_api.DSCAddList.as_view()),
    # url(r'^api/v1/dsc/(?P<pk>[0-9]+)/removebigip/(?P<bigip_pk>[0-9]+)/$', dsc_api.DSCRemoveList.as_view()),

    url(r'^api/v1/bigip/$', dsc_api.BIGIPList.as_view()),
    url(r'^api/v1/bigip/(?P<pk>[0-9]+)/$', dsc_api.BIGIPDetail.as_view()),
    url(r'^api/v1/vip/$', dsc_api.VIPList.as_view()),
    url(r'^api/v1/vip/(?P<pk>[0-9]+)/$', dsc_api.VIPDetail.as_view()),
    url(r'^api/v1/virtualserver/$', dsc_api.VirtualServerList.as_view()),
    url(r'^api/v1/virtualserver/(?P<pk>[0-9]+)/$', dsc_api.VirtualServerDetail.as_view()),
    url(r'^api/v1/trafficgroup/$', dsc_api.TrafficGroupList.as_view()),
    url(r'^api/v1/trafficgroup/(?P<pk>[0-9]+)/$', dsc_api.TrafficGroupDetail.as_view()),

    # Application API
    url(r'^api/v1/udptrafficstat/$', app_api.UDPTrafficStatListCreateApiView.as_view()),
    url(r'^api/v1/sourceip/$', app_api.SourceIPList.as_view()),
    url(r'^api/v1/sourceip/(?P<pk>[0-9]+)/$', app_api.SourceIPDetail.as_view()),
    url(r'^api/v1/appserver/$', app_api.AppServerList.as_view()),
    url(r'^api/v1/appserver/(?P<pk>[0-9]+)/$', app_api.AppServerDetail.as_view()),
    url(r'^api/v1/application/$', app_api.ApplicationList.as_view()),
    url(r'^api/v1/application/(?P<pk>[0-9]+)/$', app_api.ApplicationDetail.as_view()),

    # # These three api are shortcut api to start/stop/initialize application, not normally used
    # url(r'^api/v1/application/(?P<pk>[0-9]+)/start$', app_api.ApplicationStart.as_view()),
    # url(r'^api/v1/application/(?P<pk>[0-9]+)/stop$', app_api.ApplicationStop.as_view()),
    # url(r'^api/v1/application/(?P<pk>[0-9]+)/init$', app_api.ApplicationInit.as_view()),


    # Action API
    url(r'^api/v1/interval/$', action_api.IntervalScheduleList.as_view()),
    url(r'^api/v1/interval/(?P<pk>[0-9]+)/$', action_api.IntervalScheduleDetail.as_view()),
    url(r'^api/v1/crontab/$', action_api.CrontabScheduleList.as_view()),
    url(r'^api/v1/crontab/(?P<pk>[0-9]+)/$', action_api.CrontabScheduleDetail.as_view()),
    url(r'^api/v1/solar/$', action_api.SolarScheduleeList.as_view()),
    url(r'^api/v1/solar/(?P<pk>[0-9]+)/$', action_api.SolarScheduleDetail.as_view()),

    url(r'^api/v1/action/$', action_api.Action.as_view()),

    url(r'^api/v1/appaction/$', action_api.AppActionGetList.as_view()),
    url(r'^api/v1/appaction/create/(?P<action>[a-zA-Z0-9_-]+)/$', action_api.AppActionAddList.as_view()),
    url(r'^api/v1/appaction/(?P<pk>[0-9]+)/$', action_api.AppActionDetail.as_view()),

    url(r'^api/v1/dscaction/$', action_api.DSCActionGetList.as_view()),
    url(r'^api/v1/dscaction/create/(?P<action>[a-zA-Z0-9_-]+)/$', action_api.DSCActionAddList.as_view()),
    url(r'^api/v1/dscaction/(?P<pk>[0-9]+)/$', action_api.DSCActionDetail.as_view()),

    url(r'^api/v1/bigipaction/$', action_api.BigipActionGetList.as_view()),
    url(r'^api/v1/bigipaction/create/(?P<action>[a-zA-Z0-9_-]+)/$', action_api.BigipActionAddList.as_view()),
    url(r'^api/v1/bigipaction/(?P<pk>[0-9]+)/$', action_api.BigipActionDetail.as_view()),

    # REST API Doc
    url(r'^docs/', include_docs_urls(title=API_TITLE))
]