from django.http import Http404
from .models import BIGIP, DSC, VIP, VirtualServer, TrafficGroup
from .serializers import DSCSerializer, BIGIPSerializer, VIPSerializer, VirtualServerSerializer, TrafficGroupSerializer
from .lib.bigip_config import add_bigip_to_dsc, remove_bigip_from_dsc
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics


class DSCList(APIView):

    def get(self, request, format=None):
        failover_actions = DSC.objects.all()
        serializer = DSCSerializer(failover_actions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        serializer = DSCSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DSCDetail(APIView):
    """
    Retrieve, update or delete a dsc instance.
    """
    def get_object(self, pk):
        try:
            return DSC.objects.get(pk=pk)
        except DSC.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dsc = self.get_object(pk)
        serializer = DSCSerializer(dsc)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        data = request.data
        dsc = self.get_object(pk)
        serializer = DSCSerializer(dsc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        data = request.data
        dsc = self.get_object(pk)
        serializer = DSCSerializer(dsc, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dsc = self.get_object(pk)
        # Unlink all bigips under this dsc before delete dsc
        for bigip in dsc.bigip_set.all():
            remove_bigip_from_dsc(bigip, dsc)
        dsc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class DSCAddList(APIView):
#
#     def get_dsc_object(self, pk):
#         try:
#             return DSC.objects.get(pk=pk)
#         except DSC.DoesNotExist:
#             raise Http404
#
#     def get_bigip_object(self, pk):
#         try:
#             return BIGIP.objects.get(pk=pk)
#         except BIGIP.DoesNotExist:
#             raise Http404
#
#     def post(self, request, pk, bigip_pk, format=None):
#         dsc = self.get_dsc_object(pk)
#         bigip = self.get_bigip_object(bigip_pk)
#         add_bigip_to_dsc(bigip, dsc)
#         return Response(status=status.HTTP_200_OK)
#
#
# class DSCRemoveList(APIView):
#
#     def get_dsc_object(self, pk):
#         try:
#             return DSC.objects.get(pk=pk)
#         except DSC.DoesNotExist:
#             raise Http404
#
#     def get_bigip_object(self, pk):
#         try:
#             return BIGIP.objects.get(pk=pk)
#         except BIGIP.DoesNotExist:
#             raise Http404
#
#     def post(self, request, pk, bigip_pk, format=None):
#         dsc = self.get_dsc_object(pk)
#         bigip = self.get_bigip_object(bigip_pk)
#         remove_bigip_from_dsc(bigip, dsc)
#         return Response(status=status.HTTP_200_OK)


class BIGIPList(APIView):

    def get(self, request, format=None):
        failover_actions = BIGIP.objects.all()
        serializer = BIGIPSerializer(failover_actions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        serializer = BIGIPSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BIGIPDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_dsc_object(self, pk):
        try:
            return DSC.objects.get(pk=pk)
        except DSC.DoesNotExist:
            raise Http404

    def get_bigip_object(self, pk):
        try:
            return BIGIP.objects.get(pk=pk)
        except BIGIP.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        bigip = self.get_bigip_object(pk)
        serializer = BIGIPSerializer(bigip)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        bigip = self.get_bigip_object(pk)
        serializer = BIGIPSerializer(bigip, data=request.data, partial=True)
        if serializer.is_valid():
            validate_data = serializer.validated_data
            if not bigip.dsc and validate_data.get("dsc"):
                # Add bigip to dsc
                dsc_obj = validate_data.get("dsc")
                add_bigip_to_dsc(bigip, dsc_obj)
            elif bigip.dsc and not validate_data.get("dsc"):
                # Remove bigip from dsc
                remove_bigip_from_dsc(bigip, bigip.dsc)
            if bigip.dsc and validate_data.get("dsc"):
                del serializer.validated_data["dsc"]
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        bigip = self.get_bigip_object(pk)
        # Unlink all bigips under this dsc before delete dsc
        bigip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VIPList(generics.ListCreateAPIView):
    queryset = VIP.objects.all()
    serializer_class = VIPSerializer

    def perform_create(self, serializer):
        serializer.save()


class VIPDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VIP.objects.all()
    serializer_class = VIPSerializer


class VirtualServerList(generics.ListCreateAPIView):
    queryset = VirtualServer.objects.all()
    serializer_class = VirtualServerSerializer

    def perform_create(self, serializer):
        serializer.save()


class VirtualServerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VirtualServer.objects.all()
    serializer_class = VirtualServerSerializer


class TrafficGroupList(generics.ListCreateAPIView):
    queryset = TrafficGroup.objects.all()
    serializer_class = TrafficGroupSerializer

    def perform_create(self, serializer):
        serializer.save()


class TrafficGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TrafficGroup.objects.all()
    serializer_class = TrafficGroupSerializer
