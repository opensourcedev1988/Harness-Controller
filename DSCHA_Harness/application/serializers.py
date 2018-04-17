from rest_framework import serializers
from .models import UDPTrafficStat, SOURCEIP, AppServer, Application


class UDPTrafficStatSerializer(serializers.ModelSerializer):

    class Meta:
        model = UDPTrafficStat
        fields = ('id', 'app_id', 'byte_sent', 'packets_sent',
                  'packets_receive', 'drop_packets', 'avg_latency', 'pkt_time')


class SourceIPSerializer(serializers.ModelSerializer):

    class Meta:
        model = SOURCEIP
        fields = ('id', 'ip')


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ('id', 'name', 'description', 'protocol', 'socket_port',
                  'packet_per_second', "dsc", 'vip', 'src_ip', 'is_start',
                  'client_app_id', 'virtualserver_set', 'trafficgroup_set', 'appserver_set')
        read_only_fields = ('virtualserver_set', 'trafficgroup_set', 'appserver_set')


class AppServerSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppServer
        fields = ('id', 'ip', 'port', 'server_side_id', 'application', 'is_start')



