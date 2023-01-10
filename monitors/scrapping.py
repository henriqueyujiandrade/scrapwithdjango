from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import undetected_chromedriver as uc

from bs4 import BeautifulSoup

import ipdb

class Scrapper:
    def scrapping():
        # monitor_terabyte = Scrapper.get_terabyte_data()        
        
        # monitorpichau_1 = Scrapper.get_pichau_data('1')
        # monitorpichau_2 = Scrapper.get_pichau_data('2')        
        # monitor_pichau = monitorpichau_1 + monitorpichau_2

        monitorkabum_1 = Scrapper.get_kabum_data('1')
        monitorkabum_2 = Scrapper.get_kabum_data('2')
        monitor_kabum = monitorkabum_1 + monitorkabum_2   
        
        # all_monitors = monitor_terabyte + monitor_pichau + monitor_kabum
        return monitor_kabum

    def get_terabyte_data():
        monitors = []
        options = uc.ChromeOptions()
        options.headless=True
        options.add_argument('--headless')
        driver = uc.Chrome(options=options)
        driver.get(f'https://www.terabyteshop.com.br/monitores')
        page_content = driver.page_source
        site = BeautifulSoup(page_content, 'html.parser')

        not_found = site.find('h1', attrs={'class':'busca-zerada'})
        if not_found:
            return monitors

        monitors_data = site.find_all('div', attrs={'class':'commerce_columns_item_inner'})

        for monitor_data in monitors_data:
            link = monitor_data.find('a')['href']
            description = monitor_data.find('h2')
            price = monitor_data.find('div', attrs={'class':'prod-new-price'})
            
            array_text = description.text.lower().split(',')
            array_hz = []
            hz = 0
            for text in array_text:
                if 'hz' in text:
                    array_hz.append(text)      
            if array_hz:
                digits = ''.join([n for n in array_hz[0] if n.isdigit()])
                hz = int(digits)  
            if price and hz>=144:
                current_price = price.find('span').text
                new_data = {
                    'description': description.text ,
                    'current_price': current_price.translate({ord(i): None for i in 'R$. '}),
                    'category': 'monitor',
                    'store': 'terabyte',
                    'link': link
                }
                monitors.append(new_data)
        
        return monitors


    def get_pichau_data(input):
        monitors = []
        options = uc.ChromeOptions()
        options.headless=True
        options.add_argument('--headless')
        driver = uc.Chrome(options=options)
        driver.get(f'https://www.pichau.com.br/monitores/monitores-geral?page={input}')
        page_content = driver.page_source
        site = BeautifulSoup(page_content, 'html.parser')

        not_found = site.find('p')
        if not_found.text == 'Nenhum produto encontrado.':
            return monitors        

        monitors_data = site.find_all('a', attrs={'data-cy': 'list-product'})        
        for monitor_data in monitors_data:
            link = f'https://www.pichau.com.br{monitor_data["href"]}'
            description = monitor_data.find('h2')
            card_content = monitor_data.find('div', attrs='MuiCardContent-root')
            first_divs = card_content.find_all('div')
            if first_divs:
                second_divs = first_divs[0].find_all('div')
                third_divs = second_divs[0].find_all('div')
                price = third_divs
                
                array_text = description.text.lower().split(',')
                array_hz = []
                hz = 0
                for text in array_text:
                    if 'hz' in text:
                        array_hz.append(text)
                        
                if array_hz and len(array_hz[0])<=7:
                    digits = ''.join([n for n in array_hz[0] if n.isdigit()])
                    hz = int(digits)                    

                if array_hz and len(array_hz[0])>7:
                    second_array_text = array_hz[0].split(' ')
                    second_array_hz = []
                    for second_text in second_array_text:
                        if 'hz' in second_text:
                            second_array_hz.append(second_text)
                    if len(second_array_hz[0])<7:         
                        digits = ''.join([n for n in second_array_hz[0] if n.isdigit()])
                        hz = int(digits)

                if price and hz>=144:
                        if 'de' in price[1].text:
                            current_price = price[2].text
                        else:
                            current_price = price[1].text                            
                        new_data = {
                            'description': description.text,
                            'current_price': current_price.translate({ord(i): None for i in 'R$. '}),
                            'category': 'monitor',
                            'store': 'pichau',
                            'link': link
                        }
                        monitors.append(new_data)
        
        return monitors


    def get_kabum_data(input):
        monitors = []
        options = uc.ChromeOptions()
        options.headless=True
        options.add_argument('--headless')
        driver = uc.Chrome(options=options)
        driver.get(f'https://www.kabum.com.br/computadores/monitores/monitor-gamer?page_number={input}&page_size=100&facet_filters=&sort=price')
        page_content = driver.page_source
        site = BeautifulSoup(page_content, 'html.parser')

        not_found = site.find('p')
        if not_found.text == 'Nenhum produto encontrado.':
            return monitors        

        monitors_data = site.find_all('a', attrs={'class': 'cUkkYl'})
               
        for monitor_data in monitors_data:
            link = f'https://www.kabum.com.br{monitor_data["href"]}'
            description = monitor_data.find('span', attrs={'class': 'nameCard'})
            price = monitor_data.find('span', attrs={'class': 'priceCard'})

            array_text = description.text.lower().split(',')
            array_hz = []
            hz = 0
            for text in array_text:
                if 'hz' in text:
                    array_hz.append(text)
                    
            if array_hz and len(array_hz[0])<=7:
                digits = ''.join([n for n in array_hz[0] if n.isdigit()])
                hz = int(digits)

            if array_hz and len(array_hz[0])>7:
                second_array_text = array_hz[0].split(' ')
                second_array_hz = []
                for second_text in second_array_text:
                    if 'hz' in second_text:
                        second_array_hz.append(second_text)
                if len(second_array_hz[0])<7 and len(second_array_hz[0])>2:
                    print(second_array_hz)         
                    digits = ''.join([n for n in second_array_hz[0] if n.isdigit()])
                    print(digits)
                    hz = int(digits)               

                                            
            if price and not '---' in price.text and hz>=144:
                    current_price = price.text
                    final_price = current_price.replace("&nbsp", "")                          
                    new_data = {
                        'description': description.text,
                        'current_price': final_price.translate({ord(i): None for i in 'R$. '}),
                        'category': 'monitor',
                        'store': 'kabum',
                        'link': link
                    }
                    monitors.append(new_data)

        return monitors
