"""
Build the dictionary of global variables that will be available to all templates.
"""
from dsc.models import BIGIP, DSC


def get_globals(request):
    return {'dsc_list': DSC.objects.all(),
            'bigip_list': BIGIP.objects.all()}
