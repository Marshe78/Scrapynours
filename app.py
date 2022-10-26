import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys

try:search_query = ''.join(arg+' ' for arg in sys.argv[1:-1])
except: search_query = 'Intelligence artificielle'

try: n = int(sys.argv[-1])
except: n=1

def metadata_collect(data):
    time.sleep(2)
    print('Collection des métédata de la page de recherche')
    articles = driver.find_elements(By.TAG_NAME, 'article')
    for article in articles: 
        data_temp = {}

        # Collecte des images des articles
        try:data_temp['img'] = article.find_element(By.TAG_NAME, 'img').get_attribute('src')
        except:data_temp['img'] = None

        # Collecte des images des titres
        try:data_temp['title'] = article.find_element(By.TAG_NAME, 'h3').text
        except:data_temp['title'] = None

        # Collecte des images des liens
        try:
            data_temp['link'] = article.find_element(By.TAG_NAME, 'a').get_attribute('href')
            id_= data_temp['link'].split('-')[-1]
        except:data_temp['link'] = None

        # Collecte des images des contents
        try:data_temp['content'] = True
        except:data_temp['content'] = None

        data[id_] = data_temp
    return data


def content_collect(data, search_query):
    for u in data:
        driver.get(data[u]['link'])
        time.sleep(2)

        # Collecte des images des dates de publication
        try:data[u]['time'] = driver.find_element(By.XPATH, 
                                                  '/html/head/meta[22]').get_attribute('content')
        except:data[u]['time'] = None

        # Collecte des images du contenue des pages   
        try:data[u]['content'] = str([p.text for p in driver.find_elements(By.CLASS_NAME,
                                                                           'sc-14kwckt-6.gPHWRV')])
        except:
            data[u]['content'] = None

        # Collecte des auteurs 
        try:
            data[u]['author'] = driver.find_element(By.CLASS_NAME,'sc-1oe11kk-0.gPfqhZ').text
        except:
            data[u]['author'] = None
            
        print(data)

        with open(f'data {search_query}.json', 'w') as f:
            f.write(str(data))

    return data

driver = webdriver.Chrome('./chromedriver')
driver.get('https://www.lesechos.fr/')
driver.set_window_size(800,2000)
driver.set_window_position(800,0)
#driver.implicitly_wait(1)


# Cookies consent
driver.find_element(By.ID, 'didomi-notice-agree-button').click()

# Bare de recherche
driver.find_element(By.CLASS_NAME,
                    'sc-14kwckt-16.sc-5udzxv-0.hIJloJ.fPxKzE.sc-ctlfsq-0.cQrgEv').click()

time.sleep(1)
# Recherche par mots clés
driver.find_element(By.TAG_NAME, 
                    'input').send_keys(search_query+Keys.ENTER)

# Url de la page de recherche
serach_url = driver.current_url

data = {}

for page in range(2,n+2):
    print(f'Data Collect from page : {page-1}')
    data = metadata_collect(data)
    driver.get(serach_url + f'&page={page}')


data = content_collect(data, search_query)

driver.close()