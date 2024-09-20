import scrapy


class MlSpider(scrapy.Spider):
    name = "ml"

    start_urls = [f"https://www.mercadolivre.com.br/ofertas?page={i}" for i in range(1, 21)]

    def parse(self, response, **kwargs):
        for i in response.xpath('//div[contains(@class, "andes-card")]'):
            title = i.xpath('.//a[@class="poly-component__title"]/text()').get()
            price = i.xpath('.//span[@class="andes-money-amount__fraction"]/text()').get()
            link = i.xpath('.//a[@class="poly-component__title"]/@href').get()
            
            if link:
                link = response.urljoin(link)

            yield {
                'title': title,
                'price': price,
                'link': link
            }

            next_page = response.xpath('//a[contains(@title,"Siguiente")]/@href').get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                yield scrapy.Request(next_page_url, callback=self.parse)
