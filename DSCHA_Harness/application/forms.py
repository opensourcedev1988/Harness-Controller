from django import forms


class AppForm(forms.Form):
    name = forms.CharField(max_length=256)
    description = forms.CharField(max_length=1024)
    server_pool = forms.CharField(max_length=1024)
    protocol = forms.IntegerField()
    socket_port = forms.IntegerField()
    packet_per_second = forms.IntegerField()
    vip = forms.GenericIPAddressField()
    src_ip = forms.GenericIPAddressField()
