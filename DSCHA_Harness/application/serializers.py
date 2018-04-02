from rest_framework import serializers
from .models import UDPTrafficStat


class UDPTrafficStatSerializer(serializers.ModelSerializer):

    class Meta:
        model = UDPTrafficStat
        fields = ('id', 'app_id', 'byte_sent', 'packets_sent',
                  'packets_receive', 'drop_packets', 'avg_latency', 'pkt_time')
