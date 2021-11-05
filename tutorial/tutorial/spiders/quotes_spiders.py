import scrapy
#titulo = //h1/a/text()
#Citas = //span[@class="text" and @itemprop="text"]/text()
#top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()

class QuotesSpider(scrapy.Spider):
    name = "quotes" # name of the spider scrapy lo usa para referirse a este proyecto. Es único   
    """ start_urls = [
        'http://quotes.toscrape.com/page/1',
        'https://www.disco.com.ar/'
    ] """
    start_urls = [
        'http://quotes.toscrape.com/page/1'
    ]

    def parse(self, response):  #metodo obligatorio en la clase
        #with open('resultados.html', 'w', encoding='utf-8')  as f:
        #    f.write(response.text)
        print('*' * 10)
        #print(response.status, response.headers)
        title=response.xpath('//h1/a/text()').get()
        print(f'Titulo: {title}')
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        print('Citas: ')
        for quote in quotes:
            print(f'- {quote}')
        top_ten_tags=response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()
        print('top ten tags:')
        for tag in top_ten_tags:    
            print(f'- {tag}')
