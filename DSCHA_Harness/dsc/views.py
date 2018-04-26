import logging

from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from lib.bigip_rest import *
from .forms import BIGIPForm, DSCForm
from.models import BIGIP, DSC

logger = logging.getLogger(__name__)


def manage_bigip(request):

    return render(request,
                  'manage_bigip.html',
                  {'device_list': BIGIP.objects.all()})


def add_bigip(request):
    if request.method == 'POST':
        form = BIGIPForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/manage_bigip')
    else:
        form = BIGIPForm()

    return render(request,
                  'add_bigip.html',
                  {'form': form})


def delete_bigip(request, bigip_id, confirm):

    if confirm == '1':
        BIGIP.objects.get(id=bigip_id).delete()
        return HttpResponseRedirect('/manage_bigip')

    return render(request,
                  'delete_bigip.html',
                  {'bigip': BIGIP.objects.get(id=bigip_id)})


def get_bigip_sync_status(request, bigip_id):
    bigip = BIGIP.objects.get(id=bigip_id)

    r = requests.session()
    r.auth = (bigip.login, bigip.password)
    r.verify = False
    r.headers.update({'Content-Type': 'application/json'})
    response = r.get('https://' + bigip.mgmt_ip + '/mgmt/tm/cm/sync-status')
    return JsonResponse({'status': response.json()['entries']['https://localhost/mgmt/tm/cm/sync-status/0']['nestedStats']['entries']['color']['description']})


def get_bigip_failover_state(request, bigip_id):
    bigip = BIGIP.objects.get(id=bigip_id)

    r = requests.session()
    r.auth = (bigip.login, bigip.password)
    r.verify = False
    r.headers.update({'Content-Type': 'application/json'})
    response = r.get('https://' + bigip.mgmt_ip + '/mgmt/tm/cm/device')

    # We get back ALL of the BIG-IP's in the DSC. Find the one we care about
    items = response.json()['items']
    found_item = None
    for item in items:
        if item['selfDevice'] == 'true':
            found_item = item
            break

    if found_item is not None:
        return JsonResponse({'state': found_item['failoverState']})
    else:
        return JsonResponse({'state': 'unknown'})


def create_dsc(request):

    if request.method == 'POST':
        form = DSCForm(request.POST)

        if form.is_valid():

            bigip = get_object_or_404(BIGIP, id=form.cleaned_data['initial_bigip_id'])

            dsc = DSC()
            dsc.name = form.cleaned_data['name']
            dsc.save()

            dsc.add_bigip(bigip)

            return HttpResponseRedirect('/')
        else:
            print(form)
    else:
        form = DSCForm()

    bigips = BIGIP.objects.filter(dsc=None)

    return render(request,
                  'create_dsc.html',
                  {'form': form,
                   'free_bigips': bigips})


def view_dsc(request, dsc_id):
    dsc = DSC.objects.get(id=dsc_id)

    # Build a list of the BIG-IP's that aren't in a DSC
    bigips = BIGIP.objects.filter(dsc=None)

    return render(request,
                  'view_dsc.html',
                  {'dsc': dsc,
                   'free_bigips': bigips})


def delete_dsc(request, dsc_id, confirm):

    dsc = DSC.objects.get(id=dsc_id)

    if confirm == '1':

        # Remove any BIG-IP's from the Device Trust
        for bigip in BIGIP.objects.filter(dsc=dsc):
            dsc.remove_bigip(bigip=bigip)

        dsc.delete()
        return HttpResponseRedirect('/')

    return render(request,
                  'delete_dsc.html',
                  {'dsc': dsc})


def dsc_add_bigip(request):

    if request.method == 'POST':
        dsc = get_object_or_404(DSC, id=request.POST.get('dsc-id'))
        free_bigips = BIGIP.objects.filter(dsc=None)

        # See if the checkbox was checked for each free bigip
        for bigip in free_bigips:
            if request.POST.get('free-bigip-' + str(bigip.id), None) is not None:
                dsc.add_bigip(bigip=bigip)

        return redirect(dsc)
    else:
        return HttpResponseRedirect('/')


def dsc_remove_bigip(request, dsc_id, bigip_id, confirm):

    dsc = get_object_or_404(DSC, id=dsc_id)
    bigip = get_object_or_404(BIGIP, id=bigip_id)

    if confirm == '1':
        dsc.remove_bigip(bigip=bigip)

    return redirect(dsc)
