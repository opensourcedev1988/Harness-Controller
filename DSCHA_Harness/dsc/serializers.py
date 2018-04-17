from rest_framework import serializers
from .models import BIGIP, DSC, VirtualServer, TrafficGroup, VIP


class DSCSerializer(serializers.ModelSerializer):

    class Meta:
        model = DSC
        fields = ('id', 'name', 'bigip_set', 'application_set')
        read_only_fields = ('bigip_set', 'application_set')


class BIGIPSerializer(serializers.ModelSerializer):

    dsc = DSCSerializer()

    class Meta:
        model = BIGIP
        fields = ('id', 'mgmt_ip', 'login', 'password', 'primary', 'device_name', 'dsc')
        read_only_fields = ('primary', 'device_name', 'dsc',)


class VIPSerializer(serializers.ModelSerializer):

    class Meta:
        model = VIP
        fields = ('id', 'ip')


class VirtualServerSerializer(serializers.ModelSerializer):

    class Meta:
        model = VirtualServer
        fields = ('id', 'name', 'application')


class TrafficGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrafficGroup
        fields = ('id', 'name', 'application', 'bigips')
