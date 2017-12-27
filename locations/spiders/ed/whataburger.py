# -*- coding: utf-8 -*-
import scrapy
import json

from locations.items import hourstudy


class WhataburgerSpider(scrapy.Spider):
    name = "whataburger"
    allowed_domains = ["locations.whataburger.com"]
    start_urls = (
        'https://locations.whataburger.com/',
    )

    def store_hours(self, store_hours):
        day_groups = []
        this_day_group = None
        for day_info in store_hours:
            day = day_info['day'][:2].title()

            hour_intervals = []
            for interval in day_info['intervals']:
                f_time = str(interval['start']).zfill(4)
                t_time = str(interval['end']).zfill(4)
                hour_intervals.append('{}:{}-{}:{}'.format(
                    f_time[0:2],
                    f_time[2:4],
                    t_time[0:2],
                    t_time[2:4],
                ))
            hours = ','.join(hour_intervals)

            if not this_day_group:
                this_day_group = {
                    'from_day': day,
                    'to_day': day,
                    'hours': hours
                }
            elif this_day_group['hours'] != hours:
                day_groups.append(this_day_group)
                this_day_group = {
                    'from_day': day,
                    'to_day': day,
                    'hours': hours
                }
            elif this_day_group['hours'] == hours:
                this_day_group['to_day'] = day

        day_groups.append(this_day_group)

        opening_hours = ""
        if len(day_groups) == 1 and day_groups[0]['hours'] in ('00:00-23:59', '00:00-00:00'):
            opening_hours = '24/7'
        else:
            for day_group in day_groups:
                if day_group['from_day'] == day_group['to_day']:
                    opening_hours += '{from_day} {hours}; '.format(**day_group)
                elif day_group['from_day'] == 'Su' and day_group['to_day'] == 'Sa':
                    opening_hours += '{hours}; '.format(**day_group)
                else:
                    opening_hours += '{from_day}-{to_day} {hours}; '.format(**day_group)
            opening_hours = opening_hours[:-2]

        return opening_hours

    def parse(self, response):
        urls = response.xpath('//a[@class="c-directory-list-content-item-link"]/@href').extract()
        for path in urls:
            if len(path.split('/')) > 2:
                # If there's only one store, the URL will be longer than <state code>.html
                yield scrapy.Request(response.urljoin(path), callback=self.parse_store)
            else:
                yield scrapy.Request(response.urljoin(path))

    def parse_store(self, response):
        hours = json.loads(response.xpath('//div[@class="c-location-hours-details-wrapper js-location-hours"]/@data-days').extract_first())

        raw = (hours)
        formatted = self.store_hours(hours)
        yield hourstudy(raw,formatted)



