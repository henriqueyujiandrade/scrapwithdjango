from rest_framework import serializers
from rest_framework.exceptions import APIException
from datetime import datetime

import ipdb
from .models import Monitor
from prices.models import Price

from prices.serializers import PriceSerializer

from .scrapping import Scrapper
from .email import Email



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
            prices = Price.objects.filter(monitor=instance)
            if prices:
                last_update = prices[len(prices) -1].created_at.timestamp()
                now_time = datetime.today().timestamp()
                last_value = prices[len(prices) -1].price
                if now_time-last_update>=43000 or last_value != value:
                    Price.objects.create(price=value, monitor=instance)          
            
            if not prices:
                Price.objects.create(price=value, monitor=instance)

            check_value = float(value.replace(",","."))
            if check_value<=1000:
                Email.send_email(instance.description,value,instance.link)

        instance.save()

        return instance
