from colorama import Fore, Back, Style
import scrapy


class StatsEvents(scrapy.Spider):
    name = "events"

    start_urls = [
        'https://www.hltv.org/stats/events?matchType=BigEvents',
    ]

    def parse(self, response):
        for camp in response.css('td.name-col a::attr(href)'):
            campURL= response.urljoin(camp.get())
            yield scrapy.Request(campURL, callback=self.parse_camp)   

        next_page = response.css('div.pagination-component.pagination-bottom a.pagination-next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)  

    def parse_camp(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def get_dates(query):
            dates = response.css(query)[0]
            date = dates.css("span::text").getall()
            fullDate = ""

            for d in date: 
                fullDate += d

            return fullDate

        yield {
            'location': extract_with_css('span.text-ellipsis::text'),
            'date': get_dates('td.eventdate'),
            'prizepool':extract_with_css('td.prizepool.text-ellipsis::text'),
            'teams':extract_with_css('td.teamsNumber::text'),
        }

    # // TODO Save event name and banner