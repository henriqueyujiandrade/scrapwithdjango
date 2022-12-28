from rest_framework import serializers
from rest_framework.exceptions import APIException

import ipdb
from .models import Monitor
from prices.models import Price

from prices.serializers import PriceSerializer

from .scrapping import Scrapper



class UniqueValidationError(APIException):
    status_code = 200

class ScrapValidationError(APIException):
    status_code = 404


class MonitorGetSerializer(serializers.ModelSerializer):
     prices = PriceSerializer(read_only=True, many=True)
     class Meta:
        model = Monitor
        fields = ['id','description','current_price','category','store','link','created_at', 'updated_at','prices']
        read_only_fields = ['description','current_price','store','link', 'created_at', 'updated_at']   


class MonitorDetailSerializer(serializers.ModelSerializer):
     prices = PriceSerializer(read_only=True, many=True)
     class Meta:
        model = Monitor
        fields = ['id','description','current_price','category','store','link','created_at', 'updated_at','prices']
        read_only_fields = ['description','current_price','store','link', 'created_at', 'updated_at'] 


class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = ['id','description','current_price','category','store','link']
        read_only_fields = ['description','current_price','category','store','price','link']   

    def create(self, validated_data):
        monitor_dict = []
        monitors = Scrapper.scrapping()
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


class MonitorPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = ['id','description','current_price','category','store','link']
        read_only_fields = ['description','store','link','category']  


    def update(self, instance: Monitor, validated_data: dict):
        for key, value in validated_data.items():
            setattr(instance, key, value)
            Price.objects.create(price=value, monitor=instance)

        instance.save()

        return instance
