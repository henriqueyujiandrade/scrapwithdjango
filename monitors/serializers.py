from rest_framework import serializers
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

import ipdb
from .models import Monitor

class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = ['id','description','price','category']
        read_only_fields = ['description','price','category']

    def create(self, validated_data):
        navigate = webdriver.Chrome()
        navigate.get('https://www.terabyteshop.com.br/')
        input_place = navigate.find_element(By.ID, "isearch")
        input_place.send_keys('monitor 144hz')
        input_place.submit()

        sleep(5)

        page_content = navigate.page_source
        site = BeautifulSoup(page_content, 'html.parser')
        monitors_data = site.find_all('div', attrs={'class':'commerce_columns_item_inner'})

        for monitor_data in monitors_data:
            description = monitor_data.find('h2')
            price = monitor_data.find('div', attrs={'class':'prod-new-price'})
            if price:
                current_price = price.find('span').text
                new_data = {'description': description.text , 'price': current_price, 'category':'monitor'}
                monitor = Monitor.objects.create(**new_data)    
            
            
        return monitor