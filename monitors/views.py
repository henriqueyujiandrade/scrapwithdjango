from rest_framework import generics
from rest_framework.views import APIView, Request, Response, status
from django.shortcuts import get_object_or_404

from .serializers import (
    MonitorSerializer,
    MonitorGetSerializer,
    MonitorDetailSerializer,
    MonitorPatchSerializer,
)
from rest_framework import generics

from .models import Monitor
from .scrapping import Scrapper

import ipdb


class MonitorScrappingView(APIView):
    def post(self, request: Request) -> Response:
        serializer = MonitorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Scrap Success"}, status.HTTP_201_CREATED)

    def patch(self, request: Request) -> Response:
        monitors = Scrapper.scrapping()
        for monitor in monitors:
            monitor_data = Monitor.objects.filter(description=monitor["description"])
            if monitor_data:
                serializer = MonitorPatchSerializer(
                    monitor_data[0],
                    data={"current_price": monitor["current_price"]},
                    partial=True,
                )
                serializer.is_valid(raise_exception=True)

                serializer.save()

        return Response({"message": "Update Success"})


class MonitorView(generics.ListAPIView):
    serializer_class = MonitorGetSerializer
    queryset = Monitor.objects.all()


class MonitorDetailView(generics.RetrieveAPIView):
    serializer_class = MonitorDetailSerializer
    queryset = Monitor.objects.all()
    lookup_url_kwarg = "pk"
