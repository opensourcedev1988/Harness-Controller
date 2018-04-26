import os
from django_celery_beat.models import IntervalSchedule, CrontabSchedule, SolarSchedule
from django.http import Http404
from django.conf import settings
from action.models import AppAction, DSCAction, BigipAction
from action.serializers import AppActionSerilizer, IntervalScheduleSerializer, \
    CrontabScheduleSerializer, SolarScheduleSerializer, DSCActionSerilizer, BigipActionSerilizer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics


class IntervalScheduleList(generics.ListCreateAPIView):
    queryset = IntervalSchedule.objects.all()
    serializer_class = IntervalScheduleSerializer


class IntervalScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = IntervalSchedule.objects.all()
    serializer_class = IntervalScheduleSerializer


class CrontabScheduleList(generics.ListCreateAPIView):
    queryset = CrontabSchedule.objects.all()
    serializer_class = CrontabScheduleSerializer


class CrontabScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CrontabSchedule.objects.all()
    serializer_class = CrontabScheduleSerializer


class SolarScheduleeList(generics.ListCreateAPIView):
    queryset = SolarSchedule.objects.all()
    serializer_class = SolarScheduleSerializer


class SolarScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SolarSchedule.objects.all()
    serializer_class = SolarScheduleSerializer


class Action(APIView):
    def get(self, request, format=None):
        plugin_list = []
        for (dirpath, dirnames, filenames) in os.walk(settings.PLUGIN_DIR):
            for file in filenames:
                if file.endswith('.py') is True:
                    file_path = os.path.join(dirpath, file)
                    if "def %s(*args, **kwargs):" % settings.ACTION_FUNC in open(file_path, "r").read():
                        plugin_list.append("-".join([dirpath.replace(os.path.sep, "."),
                                                     file.split(".")[0],
                                                     settings.ACTION_FUNC]))

        return Response(plugin_list)


class AppActionGetList(APIView):

    def get(self, request, format=None):
        app_actions = AppAction.objects.all()
        serializer = AppActionSerilizer(app_actions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AppActionAddList(APIView):

    def post(self, request, action, format=None):
        serializer = AppActionSerilizer(data=request.data)
        if serializer.is_valid():
            action_obj = serializer.save()
            action_obj.set_task_str(action)
            action_obj.build_args_str()
            action_obj.build_kwargs_str()
            action_obj.create_task()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppActionDetail(APIView):
    """
    Retrieve, update or delete a AppAction instance.
    """
    def get_object(self, pk):
        try:
            return AppAction.objects.get(pk=pk)
        except AppAction.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        action = self.get_object(pk)
        serializer = AppActionSerilizer(action)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        action = self.get_object(pk)
        serializer = AppActionSerilizer(action, data=request.data, partial=True)
        if serializer.is_valid():
            action_obj = serializer.save()
            action_obj.update_task()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        action = self.get_object(pk)
        action.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DSCActionGetList(APIView):

    def get(self, request, format=None):
        dsc_actions = DSCAction.objects.all()
        serializer = DSCActionSerilizer(dsc_actions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DSCActionAddList(APIView):

    def post(self, request, action, format=None):
        serializer = DSCActionSerilizer(data=request.data)
        if serializer.is_valid():
            action_obj = serializer.save()
            action_obj.set_task_str(action)
            action_obj.build_args_str()
            action_obj.build_kwargs_str()
            action_obj.create_task()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DSCActionDetail(APIView):
    """
    Retrieve, update or delete a DSCAction instance.
    """
    def get_object(self, pk):
        try:
            return DSCAction.objects.get(pk=pk)
        except DSCAction.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        action = self.get_object(pk)
        serializer = DSCActionSerilizer(action)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        action = self.get_object(pk)
        serializer = DSCActionSerilizer(action, data=request.data, partial=True)
        if serializer.is_valid():
            action_obj = serializer.save()
            action_obj.update_task()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        action = self.get_object(pk)
        action.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BigipActionGetList(APIView):

    def get(self, request, format=None):
        bip_actions = BigipAction.objects.all()
        serializer = BigipActionSerilizer(bip_actions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BigipActionAddList(APIView):

    def post(self, request, action, format=None):
        serializer = BigipActionSerilizer(data=request.data)
        if serializer.is_valid():
            action_obj = serializer.save()
            action_obj.set_task_str(action)
            action_obj.build_args_str()
            action_obj.build_kwargs_str()
            action_obj.create_task()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BigipActionDetail(APIView):
    """
    Retrieve, update or delete a BigipAction instance.
    """
    def get_object(self, pk):
        try:
            return BigipAction.objects.get(pk=pk)
        except BigipAction.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        action = self.get_object(pk)
        serializer = BigipActionSerilizer(action)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        action = self.get_object(pk)
        serializer = BigipActionSerilizer(action, data=request.data, partial=True)
        if serializer.is_valid():
            action_obj = serializer.save()
            action_obj.update_task()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        action = self.get_object(pk)
        action.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)