import scrapy
#titulo = //h1/a/text()
#Citas = //span[@class="text" and @itemprop="text"]/text()
#top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()
#Next page button = //ul[@class="pager"]//li[@class="next"]/a/@href

class QuotesSpider(scrapy.Spider):
    name = "quotes" # name of the spider scrapy lo usa para referirse a este proyecto. Es único   
    """ start_urls = [
        'http://quotes.toscrape.com/page/1',
        'https://www.disco.com.ar/'
    ] """
    start_urls = [
        'http://quotes.toscrape.com/page/1'
    ]
    custom_settings = {
        'FEED_URI' : 'quotes.json',
        'FEED_FORMAT' : 'json'
    }

    def parse(self, response):  #metodo obligatorio en la clase
        #with open('resultados.html', 'w', encoding='utf-8')  as f:
        #    f.write(response.text)
        #print('*' * 10)
        #print(response.status, response.headers)
        title=response.xpath('//h1/a/text()').get()
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        top_ten_tags=response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()

        yield {
            'title': title,
            'quotes': quotes,
            'top_ten_tags': top_ten_tags
        }
        # --> guardar la salida en un archivo json: scrapy crawl quotes -o quotes.json (hace append)

        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse)