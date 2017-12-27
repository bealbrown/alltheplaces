import json
import scrapy

from locations.items import hourstudy


class PaneraBread(scrapy.Spider):

    name = 'panera'
    download_delay = 1.5
    allowed_domains = ["panerabread.com"]
    start_urls = (
        'https://locations.panerabread.com/index.html',
    )

    def store_hours(self, day_hours):
        day_groups = []
        this_day_group = {}

        for day_hour in day_hours:
            hours = ''
            day, intervals = day_hour['day'], day_hour['intervals']
            short_day = day.title()[:2]
            epochs = []
            for interval in intervals:
                hours_today = '{}-{}'.format('0' + str(interval['start'])[:-2] +
                                            ':00', str(interval['end'])[:-2] + ':00')
                epochs.append(hours_today)
            hours = ','.join(epochs)

            if not this_day_group:
                this_day_group = {
                    'from_day': short_day,
                    'to_day': short_day,
                    'hours': hours,
                }

            elif hours == this_day_group['hours']:
                this_day_group['to_day'] = short_day

            elif hours != this_day_group['hours']:
                day_groups.append(this_day_group)
                this_day_group = {
                    'from_day': short_day,
                    'to_day': short_day,
                    'hours': hours,
                }

        day_groups.append(this_day_group)

        if not day_groups:
            return None
        opening_hours = ''
        for day_group in day_groups:
            if day_group['from_day'] == day_group['to_day']:
                opening_hours += '{from_day} {hours}; '.format(**day_group)
            else:
                opening_hours += '{from_day}-{to_day} {hours}; '.format(**day_group)
        opening_hours = opening_hours [:-2]
        return opening_hours

    def parse_location(self, loc):
        props = {}
        
        opening_hours = self.store_hours(json.loads(hours))

        raw = json.loads(hours)
        formatted = opening_hours
        yield hourstudy(raw, formatted)

    def parse_city(self, city_page):
        locations = city_page.xpath('//h2[@class="c-location-grid-item-title"]').extract()
        if len(locations) > 0:
            for loc in locations:
                yield scrapy.Request(city_page.urljoin(loc), callback=self.parse_location)
        else:
            yield self.parse_location(city_page)

    def parse_state(self, state_page):
        cities = state_page.xpath('//a[@class="c-directory-list-content-item-link"]/@href').extract()
        for city in cities:
            yield scrapy.Request(state_page.urljoin(city), callback=self.parse_city)

    def parse(self, response):

        states = response.xpath('//a[@class="c-directory-list-content-item-link"]/@href').extract()
        for state in states:
            yield scrapy.Request(response.urljoin(state), callback=self.parse_state)
