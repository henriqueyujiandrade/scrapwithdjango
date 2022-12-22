from rest_framework import serializers

from rest_framework.exceptions import APIException



import ipdb
from .models import Monitor
from .scrapping import Scrapper


class UniqueValidationError(APIException):
    status_code = 200

class ScrapValidationError(APIException):
    status_code = 404


class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = ['id','description','price','category','store','link']
        read_only_fields = ['description','price','store','link']   

    def create(self, validated_data):
        monitor_dict = []
        monitors = Scrapper.scrapping(validated_data)
        if not monitors:
            raise ScrapValidationError("scrapper didn't find any items")

        for monitor in monitors:          
            find_existing_monitor = Monitor.objects.filter(description=monitor['description'])
            if not find_existing_monitor:        
                monitor_data = Monitor.objects.create(**monitor)
                monitor_dict.append(monitor_data)
        if not monitor_dict:
             raise UniqueValidationError("there is no new data")

        return monitor_data