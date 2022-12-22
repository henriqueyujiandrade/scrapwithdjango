from rest_framework import generics
from rest_framework.views import APIView, Request, Response, status

from .serializers import MonitorSerializer

from .models import Monitor

import ipdb

class MonitorScrappingView(APIView):
      def post(self, request: Request) -> Response:
        serializer = MonitorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({'message':'scrap success'}, status.HTTP_201_CREATED)
    
        
        
