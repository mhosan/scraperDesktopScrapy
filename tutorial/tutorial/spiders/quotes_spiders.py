import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes" # name of the spider    
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        with open('resultados.html', 'w', encoding='utf-8')  as f:
            f.write(response.text)