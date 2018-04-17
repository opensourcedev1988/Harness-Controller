import requests
import logging
import configparser
from django.shortcuts import render, redirect
from global_var import *
from dsc.models import DSC, VIP
from .forms import AppForm
from .lib.app_config import *
from .models import Application, SOURCEIP, AppServer
from dsc.models import VirtualServer, TrafficGroup, BIGIP

logger = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read(harness_config_path)


def create_app(request, dsc_id):

    dsc = DSC.objects.get(id=dsc_id)
    free_vips = VIP.objects.filter(application=None)
    free_src_ips = SOURCEIP.objects.filter(application=None)

    if request.method == 'POST':
        form = AppForm(request.POST)

        if form.is_valid():
            app = Application()
            app.name = form.cleaned_data['name']
            app.description = form.cleaned_data['description']
            app.protocol = form.cleaned_data['protocol']
            app.socket_port = form.cleaned_data['socket_port']
            app.packet_per_second = form.cleaned_data['packet_per_second']
            app.vip = VIP.objects.get(ip=form.cleaned_data['vip'])
            app.src_ip = SOURCEIP.objects.get(ip=form.cleaned_data['src_ip'])
            app.dsc = dsc

            # Create client application
            app.client_app_id = create_client_app(app)

            app.save()
            # Create server objects
            server_list = list(set(filter(None, form.cleaned_data['server_pool'].strip().split(";"))))
            for server in server_list:
                server_obj = AppServer()
                server_obj.ip = server.split(":")[0]
                server_obj.port = server.split(":")[1]
                server_obj.application = app
                server_obj.save()
            app_init_config(app)
            # Create virtual server and traffic group object
            virtual = VirtualServer()
            virtual.name = "%s-virtual" % app.name
            virtual.application = app
            virtual.save()
            tg = TrafficGroup()
            tg.name = "%s-tg" % app.name
            tg.application = app
            tg.save()
            biglist = BIGIP.objects.filter(dsc=app.dsc)
            for bigip in biglist:
                tg.bigips.add(bigip)
            tg.save()

            return redirect(dsc)

    else:
        form = AppForm()

    return render(request,
                  'create_app.html',
                  {'form': form,
                   'free_vips': free_vips,
                   'free_src_ips': free_src_ips})


def delete_app(request, app_id, confirm):
    app = Application.objects.get(id=app_id)
    dsc = app.dsc

    if confirm == '1':
        app_tear_config(app)
        delete_client_app(app)
        app.delete()
        return redirect(dsc)

    return render(request,
                  'delete_app.html', {'app': app})


def start_app(request, app_id):
    app = Application.objects.get(id=app_id)
    dsc = app.dsc
    start_client_app(app)

    return redirect(dsc)


def stop_app(request, app_id):
    app = Application.objects.get(id=app_id)
    dsc = app.dsc
    stop_client_app(app)
    app.is_start = False
    app.save()
    return redirect(dsc)
