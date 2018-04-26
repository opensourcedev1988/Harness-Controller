from rest_framework import serializers
from .models import UDPTrafficStat, SOURCEIP, AppServer, Application
from dsc.models import VirtualServer, TrafficGroup, BIGIP


class UDPTrafficStatSerializer(serializers.ModelSerializer):

    class Meta:
        model = UDPTrafficStat
        fields = ('id', 'app_id', 'byte_sent', 'packets_sent',
                  'packets_receive', 'drop_packets', 'avg_latency', 'pkt_time')


class SourceIPSerializer(serializers.ModelSerializer):

    class Meta:
        model = SOURCEIP
        fields = ('id', 'ip')


class AppServerSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppServer
        fields = ('id', 'ip', 'port', 'server_side_id', 'application', 'is_start')


class ApplicationSerializer(serializers.ModelSerializer):

    from dsc.serializers import VirtualServerSerializer, TrafficGroupSerializer
    virtualserver_set = VirtualServerSerializer(many=True)
    trafficgroup_set = TrafficGroupSerializer(many=True)
    appserver_set = AppServerSerializer(many=True)

    class Meta:
        model = Application
        fields = ('id', 'name', 'description', 'protocol', 'socket_port',
                  'packet_per_second', "dsc", 'vip', 'src_ip', 'is_start',
                  'client_app_id', 'virtualserver_set', 'trafficgroup_set', 'appserver_set')
        # read_only_fields = ('virtualserver_set', 'trafficgroup_set', 'appserver_set')

    def create(self, validated_data):
        virtualservers_data = validated_data.pop('virtualserver_set')
        trafficgroups_data = validated_data.pop('trafficgroup_set')
        appservers_data = validated_data.pop('appserver_set')
        app = Application.objects.create(**validated_data)
        for virtualserver_data in virtualservers_data:
            VirtualServer.objects.create(application=app, **virtualserver_data)
        for trafficgroup_data in trafficgroups_data:
            bigips_data = trafficgroup_data.pop('bigips')
            tg = TrafficGroup.objects.create(application=app, **trafficgroup_data)
            for bigip_data in bigips_data:
                tg.bigips.add(bigip_data)
            tg.save()
        for appserver_data in appservers_data:
            AppServer.objects.create(application=app, **appserver_data)
        return app




