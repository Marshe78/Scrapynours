import scrapy
from scrapy import Request
from WebCrawler.items import ReviewsBoursoramaItem
import datetime
from WebCrawler.pipelines import Database

class BoursoramaSpider(scrapy.Spider):
    name = 'boursorama'
    allowed_domains = ['finance.yahoo.com']
    start_urls = [f'https://www.boursorama.com/bourse/actions/palmares/france/page-{n}?france_filter[market]=1rPCAC' for n in range(1,3)]

    Database.connectDb()
    Database.createTable()

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_boursorama)
            
    def parse_boursorama(self, response):
        liste_indices = response.css('tr.c-table__row')[1:]
        
        for indices in liste_indices:
            item = ReviewsBoursoramaItem()
            
            #indice boursier
            try: 
              item['indice'] = indices.css('.u-ellipsis.u-color-cerulean').css('a::text').extract()
            except:
              item['indice'] = 'None'
            
            #indice cours de l'action
            try: 
              item['cours'] = indices.css('.c-table__cell.c-table__cell--dotted').css('.c-instrument.c-instrument--last::text').extract()
            except:item['cours'] = 'None'
            
            #Variation de l'action
            try: 
              item['var'] = indices.css('.c-instrument.c-instrument--instant-variation::text').extract()
            except:
              item['var'] = 'None'
            
            #Valeur la plus haute
            try: 
              item['hight'] = indices.css('.c-instrument.c-instrument--high::text').extract()
            except:
              item['hight'] = 'None'
            
            #Valeur la plus basse
            try: 
              item['low'] = indices.css('.c-instrument.c-instrument--low::text').extract()
            except:
              item['low'] = 'None'

            #Valeur d'ouverture
            try: 
              item['open_'] = indices.css('.c-instrument.c-instrument--open::text').extract()
            except:
              item['open_'] = 'None'

            #Date de la collecte  tradeDate
            try: 
              item['time'] = datetime.datetime.now()
            except:
              item['time'] = 'None'

            Database.addRow(item)
            
            yield item