import scrapy
# https://docs.scrapy.org/
# titulo = //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"]/text()
# top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()
# Next page button = //ul[@class="pager"]//li[@class="next"]/a/@href


class QuotesSpider(scrapy.Spider):
    name = "quotes"  # name of the spider scrapy lo usa para referirse a este proyecto. Es único
    """ start_urls = [
        'http://quotes.toscrape.com/page/1',
        'https://www.disco.com.ar/'
    ] """
    start_urls = [
        'http://quotes.toscrape.com/page/1'
    ]
    custom_settings = {
        'FEEDS': {
            'quotes.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 4,
                'item_export_kwargs': {
                    'export_empty_fields': True,
                },
            },
        }
    }
    
    def parse_only_quotes(self, response, **kwargs): #**kwargs quiere decir que voy a desempaquetar el diccionario que recibo
        if kwargs:
            quotes = kwargs['quotes'] #desempaqueto el diccionario y guardo el valor de quotes. quotes es una lista.

        #agrego la nueva cita a la lista de citas:
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())

        #siguiente pagina:
        next_page_button_link = response.xpath(
            '//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes':quotes})
        else:  # si no hay link de la tercer página (o la pagina que sea), entonces ya terminé.
            yield {
                'quotes':quotes
            }

    def parse(self, response):  # metodo obligatorio en la clase
        # with open('resultados.html', 'w', encoding='utf-8')  as f:
        #    f.write(response.text)
        # print('*' * 10)
        # print(response.status, response.headers)
        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall()
        top_ten_tags = response.xpath(
            '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()

        yield {
            'title': title,
            'top_ten_tags': top_ten_tags
        }
        # --> guardar la salida en un archivo json: scrapy crawl quotes -o quotes.json (hace append)

        next_page_button_link = response.xpath(
            '//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes':quotes}) #kwargs= Keyword arguments to be passed to the callback function
