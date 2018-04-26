from .serializers import SourceIPSerializer, AppServerSerializer, ApplicationSerializer
from .lib.app_config import *
from .models import Application, SOURCEIP, AppServer, UDPTrafficStat
from .serializers import UDPTrafficStatSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

logger = logging.getLogger(__name__)


class UDPTrafficStatListCreateApiView(APIView):

    def get(self, request, format=None):
        udpstats = UDPTrafficStat.objects.all()
        serializer = UDPTrafficStatSerializer(udpstats, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        post_data = request.data
        serializer_data_list = []
        for seri_data in post_data['data_list']:
            serializer = UDPTrafficStatSerializer(data=seri_data)
            if serializer.is_valid():
                serializer.save()
                serializer_data_list.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer_data_list, status=status.HTTP_201_CREATED)


class SourceIPList(generics.ListCreateAPIView):
    queryset = SOURCEIP.objects.all()
    serializer_class = SourceIPSerializer

    def perform_create(self, serializer):
        serializer.save()


class SourceIPDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SOURCEIP.objects.all()
    serializer_class = SourceIPSerializer


class AppServerList(APIView):

    def get_app_object(self, pk):
        try:
            return Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        app_servers = AppServer.objects.all()
        serializer = AppServerSerializer(app_servers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        # server side celery id information cannot be modified through REST
        if 'server_side_id' in data:
            del data['server_side_id']
        serializer = AppServerSerializer(data=data)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            # Start application server if is_start is set to True
            if serializer_data.get('is_start') is True and serializer_data.get('application') is not None:
                app_obj = serializer_data.get('application')
                server_side_id = start_server(app_obj, serializer_data.get('ip'), serializer_data.get('port'))
                serializer.validated_data['server_side_id'] = server_side_id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppServerDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return AppServer.objects.get(pk=pk)
        except AppServer.DoesNotExist:
            raise Http404

    def get_app_object(self, pk):
        try:
            return Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        app_server = self.get_object(pk)
        serializer = AppServerSerializer(app_server)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        data = request.data
        # server side celery id information cannot be modified through REST
        if 'server_side_id' in data:
            del data['server_side_id']
        app_server = self.get_object(pk)
        serializer = AppServerSerializer(app_server, data=request.data, partial=True)
        if serializer.is_valid():
            if serializer.validated_data.get('application'):
                app_obj = serializer.validated_data.get('application')
            else:
                app_obj = app_server.application
            if app_server.is_start != serializer.validated_data.get('is_start') and app_obj is not None:
                if serializer.validated_data['is_start'] is True:
                    srv_ip = serializer.validated_data.get('ip') or app_server.ip
                    srv_port = serializer.validated_data.get('port') or app_server.port
                    server_side_id = start_server(app_obj, srv_ip, srv_port)
                    serializer.validated_data['server_side_id'] = server_side_id
                else:
                    stop_server(app_obj, app_server.server_side_id)
                    serializer.validated_data['server_side_id'] = None
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        app_server = self.get_object(pk)
        if app_server.is_start is True:
            # Stop app server before deleting the object
            app_obj = self.get_app_object(app_server.application)
            stop_server(app_obj, app_server.server_side_id)
        app_server.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApplicationList(APIView):

    def get(self, request, format=None):
        application = Application.objects.all()
        serializer = ApplicationSerializer(application, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            app_obj = serializer.save()
            # Check application init
            client_app_id = create_client_app(app_obj)
            app_init_config(app_obj)
            app_obj.client_app_id = client_app_id
            if app_obj.is_start is True:
                start_client_app(app_obj)
            app_obj.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        app = self.get_object(pk)
        serializer = ApplicationSerializer(app)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        app_obj = self.get_object(pk)
        data = {}
        # Here we only process start/stop application
        if app_obj.is_start is False and request.data.get("is_start") is True:
            start_client_app(app_obj)
            data['is_start'] = True
        elif app_obj.is_start is True and request.data.get("is_start") is False:
            stop_client_app(app_obj)
            data['is_start'] = False
        serializer = ApplicationSerializer(app_obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        app = self.get_object(pk)
        if app.is_start is True:
            # Stop app server before deleting the object
            stop_client_app(app)
        app_tear_config(app)
        delete_client_app(app)
        app.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApplicationStart(APIView):

    def get_object(self, pk):
        try:
            return Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        app = self.get_object(pk)
        if app.is_start is True:
            return Response({'detail': "Client app already started"}, status=status.HTTP_400_BAD_REQUEST)
        start_client_app(app)
        serializer = ApplicationSerializer(app, data={'is_start': True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationStop(APIView):

    def get_object(self, pk):
        try:
            return Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        app = self.get_object(pk)
        if app.is_start is False:
            return Response({'detail': "Client app already stopped"}, status=status.HTTP_400_BAD_REQUEST)
        stop_client_app(app)
        serializer = ApplicationSerializer(app, data={'is_start': False}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationInit(APIView):

    def get_object(self, pk):
        try:
            return Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        app = self.get_object(pk)
        client_app_id = create_client_app(app)
        app_init_config(app)
        serializer = ApplicationSerializer(app, data={'client_app_id': client_app_id}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)