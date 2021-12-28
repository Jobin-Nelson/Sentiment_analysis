import scrapy

asin = 'B08L5VJWCV'
# iphone - B08L5VJWCV, alexa - B07PFFMP9P

class Reviews_spider(scrapy.Spider):
    name = 'reviews'
    start_urls = [f'https://www.amazon.in/product-reviews/{asin}']

    def parse(self, response):
        for review in response.css('[data-hook="review"]'):
            item = {
                'name': review.css('.a-profile-name ::text').get(),
                'stars': review.css('[data-hook="review-star-rating"] ::text').get()[0],
                'title': review.css('[data-hook="review-title"] span ::text').get(),
                'review': review.xpath('normalize-space(.//*[@data-hook="review-body"])').get()
            }
            yield item
        
        next_page = response.xpath('//a[text()="Next page"]/@href').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page))