from .models import BIGIP
from dsc.lib.bigip_rest import *
from django import forms
from django.forms import ModelForm


class BIGIPForm(ModelForm):
    class Meta:
        model = BIGIP
        fields = ['mgmt_ip', 'login', 'password']


class DSCForm(forms.Form):
    name = forms.CharField(max_length=256)
    initial_bigip_id = forms.IntegerField()
