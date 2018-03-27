import requests
import logging
import configparser
from django.shortcuts import render, redirect
from global_var import *
from dsc.models import DSC, VIP
from .forms import AppForm
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
            app.virtual_server = app.name + "-virtual"
            client_ip = config.get("harness", "client_agent")

            # Create client application
            if app.protocol == Application.PROTOCOL_UDP:
                url = "http://%s:8000/api/v1/UDPTraffics/" % client_ip
                post_args = {"dst_ip": app.vip.ip, "dst_port": app.socket_port, "packet_per_second": app.packet_per_second}
                r = requests.post(url,
                                  json=post_args)
                logger.debug(r.json())
                if r.status_code == 201:
                    app.client_app_id = r.json()["id"]

            elif app.protocol == Application.PROTOCOL_TCP:
                # TODO Create TCP traffic
                pass

            app.save()
            # Create server objects
            server_list = list(set(filter(None, form.cleaned_data['server_pool'].strip().split(";"))))
            for server in server_list:
                server_obj = AppServer()
                server_obj.ip = server.split(":")[0]
                server_obj.port = server.split(":")[1]
                server_obj.application = app
                server_obj.save()
            app.init_config()
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
        app.tear_config()
        client_ip = config.get("harness", "client_agent")
        if app.protocol == Application.PROTOCOL_UDP:
            url = "http://%s:8000/api/v1/UDPTraffics/%s/" % (client_ip,
                                                             app.client_app_id)
            r = requests.delete(url)
            logger.debug(r.text)
        elif app.protocol == Application.PROTOCOL_TCP:
            # TODO Delete TCP Traffic
            pass
        else:
            pass
        app.delete()
        return redirect(dsc)

    return render(request,
                  'delete_app.html', {'app': app})


def start_app(request, app_id):
    app = Application.objects.get(id=app_id)
    dsc = app.dsc
    client_ip = config.get("harness", "client_agent")
    if app.protocol == Application.PROTOCOL_UDP:
        url = "http://%s:8000/api/v1/UDPTraffics/%s/" % (client_ip,
                                                         app.client_app_id)
        post_args = {"is_start": True}
        r = requests.patch(url,
                           json=post_args)
        logger.debug(r.text)
        if r.status_code == 200:
            app.is_start = True
            app.save()
    elif app.protocol == Application.PROTOCOL_TCP:
        # TODO TCP traffic
        pass

    return redirect(dsc)


def stop_app(request, app_id):
    app = Application.objects.get(id=app_id)
    dsc = app.dsc

    client_ip = config.get("harness", "client_agent")
    if app.protocol == Application.PROTOCOL_UDP:
        url = "http://%s:8000/api/v1/UDPTraffics/%s/" % (client_ip,
                                                         app.client_app_id)
        post_args = {"is_start": False}
        r = requests.patch(url,
                           json=post_args)
        logger.debug(r.text)
        if r.status_code == 200:
            app.is_start = False
            app.save()
    elif app.protocol == Application.PROTOCOL_TCP:
        # TODO TCP traffic
        pass

    return redirect(dsc)
