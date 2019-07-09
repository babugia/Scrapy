import scrapy

from ..items import SampleItem

class EventImages(scrapy.Spider):
    name = "img_event"
    start_urls = [
        'https://www.hltv.org/stats/events?matchType=BigEvents',
    ]

    def parse(self, response):
        for camp in response.css('td.name-col a::attr(href)'):
            campURL= response.urljoin(camp.get())
            yield scrapy.Request(campURL, callback=self.get_item)   

        next_page = response.css('div.pagination-component.pagination-bottom a.pagination-next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)  

    def get_item(self, response):
        item = SampleItem()
        img_urls = []
        url = response.css('img.event-img::attr(src)').extract_first()
        img_urls.append(response.css('img.event-img::attr(src)').extract_first())
        item["image_urls"] = img_urls
        return item