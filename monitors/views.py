from rest_framework import generics
from .serializers import MonitorSerializer

from .models import Monitor

class MonitorView(generics.ListCreateAPIView):
    serializer_class = MonitorSerializer
    queryset = Monitor.objects.all()
