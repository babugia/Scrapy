import scrapy


class StatsEvents(scrapy.Spider):
    name = "events"

    start_urls = [
        'https://www.hltv.org/stats/events?matchType=BigEvents',
    ]

    def parse(self, response):
        for camp in response.css('td.name-col '):
            yield {
                'title': camp.css('img::attr(title)').get(),
            }

        next_page = response.css('div.pagination-component.pagination-bottom a.pagination-next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)    