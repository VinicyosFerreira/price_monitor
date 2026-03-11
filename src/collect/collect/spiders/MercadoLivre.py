import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "MercadoLivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/notebooks"]
    max_pages = 10
    offset = 0

    def parse(self, response):
        products = response.css("div.poly-card__content")

        for product in products: 
            yield {
                "store": product.css("span.poly-component__seller::text").get(),
                "name": product.css("a.poly-component__title::text").get(),
                "oldPrice": product.css("s.andes-money-amount--previous span.andes-money-amount__fraction::text").get(),
                "currentPrice": product.css("div.poly-price__current span.andes-money-amount__fraction::text").get(),
                "rating": product.css("span.poly-component__review-compacted span.poly-phrase-label::text").get(),
            }

       
        current_url = response.url 
        self.offset += 50
        next_page = f"{current_url.split('_Desde_')[0]}_Desde_{self.offset}_NoIndex_True"
        self.max_pages -= 1

        if self.max_pages > 0:
            yield scrapy.Request(next_page, callback=self.parse)