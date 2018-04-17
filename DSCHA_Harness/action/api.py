from django_celery_beat.models import IntervalSchedule, CrontabSchedule, SolarSchedule
from django.http import Http404
from action.models import FailoverAction
from action.serializers import FailoverActionSerilizer, IntervalScheduleSerializer, CrontabScheduleSerializer, SolarScheduleSerializer
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


# Create your views here.
class FailoverActionList(APIView):

    def get(self, request, format=None):
        failover_actions = FailoverAction.objects.all()
        serializer = FailoverActionSerilizer(failover_actions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FailoverActionSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FailoverActionDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return FailoverAction.objects.get(pk=pk)
        except FailoverAction.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = FailoverActionSerilizer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = FailoverActionSerilizer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)