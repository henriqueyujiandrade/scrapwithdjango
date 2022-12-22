from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import ipdb

class Scrapper:
    def scrapping(data):
        monitor_terabyte_144hz = Scrapper.get_terabyte_data(data,'monitor+144hz')
        monitor_terabyte_165hz = Scrapper.get_terabyte_data(data,'monitor+165hz')
        monitor_terabyte_180hz = Scrapper.get_terabyte_data(data,'monitor+180hz')
        
        monitorpichau144hz = Scrapper.get_pichau_data(data,'monitor+144hz','144hz')
        monitorpichau165hz = Scrapper.get_pichau_data(data,'monitor+165hz','165hz')
        monitorpichau180hz = Scrapper.get_pichau_data(data,'monitor+180hz','180hz')

        monitorkabum144hz = Scrapper.get_kabum_data(data, 'monitor-144hz', '144hz')
        monitorkabum144hz1 = Scrapper.get_kabum_data(data, 'monitor-144-hz', '144 hz')
        monitorkabum165hz = Scrapper.get_kabum_data(data, 'monitor-165hz', '165hz')
        monitorkabum165hz1 = Scrapper.get_kabum_data(data, 'monitor-165-hz', '165 hz')        
        
        all_monitors = monitorpichau144hz + monitorpichau165hz + monitorpichau180hz + monitor_terabyte_144hz + monitor_terabyte_165hz + monitor_terabyte_180hz + monitorkabum144hz + monitorkabum165hz + monitorkabum144hz1 + monitorkabum165hz1
        return all_monitors


    def get_terabyte_data(data, input):
        monitors = []
        options = Options()
        options.add_argument('window-size=1050,800')
        navigate = webdriver.Chrome(options=options)
        navigate.get(f'https://www.terabyteshop.com.br/busca?str={input}')
        sleep(2)
        page_content = navigate.page_source
        site = BeautifulSoup(page_content, 'html.parser')

        not_found = site.find('h1', attrs={'class':'busca-zerada'})
        if not_found:
            return monitors

        monitors_data = site.find_all('div', attrs={'class':'commerce_columns_item_inner'})

        for monitor_data in monitors_data:
            link = monitor_data.find('a')['href']
            description = monitor_data.find('h2')
            price = monitor_data.find('div', attrs={'class':'prod-new-price'})
            if price:
                current_price = price.find('span').text
                new_data = {
                    'description': description.text ,
                    'price': current_price.translate({ord(i): None for i in 'R$. '}),
                    'category': data['category'],
                    'store': 'terabyte',
                    'link': link
                }
                monitors.append(new_data)

        return monitors


    def get_pichau_data(data, input, hz):
        monitors = []
        options = Options()
        options.add_argument('window-size=1200,800')
        navigate = webdriver.Chrome(options=options)
        navigate.get(f'https://www.pichau.com.br/search?q={input}')
        sleep(2)
        page_content = navigate.page_source
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
            second_divs = first_divs[0].find_all('div')
            third_divs = second_divs[0].find_all('div')
            price = third_divs
            
            if 'Monitor' in description.text and hz in description.text.lower():                                
                if price:
                    if 'de' in price[1].text:
                        current_price = price[2].text
                    else:
                        current_price = price[1].text                            
                    new_data = {
                        'description': description.text,
                        'price': current_price.translate({ord(i): None for i in 'R$. '}),
                        'category': data['category'],
                        'store': 'pichau',
                        'link': link
                    }
                    monitors.append(new_data)
        
        return monitors


    def get_kabum_data(data, input, hz):
        monitors = []
        options = Options()
        options.add_argument('window-size=1200,800')
        navigate = webdriver.Chrome(options=options)
        navigate.get(f'https://www.kabum.com.br/busca/{input}?page_number=1&page_size=40&facet_filters=&sort=most_searched')
        sleep(2)
        page_content = navigate.page_source
        site = BeautifulSoup(page_content, 'html.parser')

        not_found = site.find('p')
        if not_found.text == 'Nenhum produto encontrado.':
            return monitors        

        monitors_data = site.find_all('a', attrs={'class': 'cUkkYl'})
               
        for monitor_data in monitors_data:
            link = f'https://www.kabum.com.br{monitor_data["href"]}'
            description = monitor_data.find('span', attrs={'class': 'nameCard'})
            price = monitor_data.find('span', attrs={'class': 'priceCard'})
            
            if 'Monitor' in description.text and hz in description.text.lower():                                
                if price and not '---' in price.text:
                    current_price = price.text
                    final_price = current_price.replace("&nbsp", "")                          
                    new_data = {
                        'description': description.text,
                        'price': final_price.translate({ord(i): None for i in 'R$. '}),
                        'category': data['category'],
                        'store': 'kabum',
                        'link': link
                    }
                    monitors.append(new_data)
        
        return monitors
