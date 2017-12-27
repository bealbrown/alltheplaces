# -*- coding: utf-8 -*-
import scrapy
import json
import re

from locations.items import hourstudy


class TractorSupplySpider(scrapy.Spider):
    name = "tractorsupply"
    allowed_domains = ["tractorsupply.com"]
    download_delay = 1.5
    start_urls = (
        'https://www.tractorsupply.com/sitemap_stores.xml',
    )

    def store_hours(self, store_hours):
        day_groups = []
        this_day_group = None
        for day in store_hours:
            day = day.replace('  :-', ' 12:00 -')
            match = re.search(r'(\S*)\s+(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})', day)
            (dow, f_hr, f_min, t_hr, t_min) = match.groups()
            day_short = dow[:2]

            f_hr = int(f_hr)
            t_hr = int(t_hr)

            hours = '{:02d}:{}-{:02d}:{}'.format(
                f_hr,
                f_min,
                t_hr,
                t_min,
            )

            if not this_day_group:
                this_day_group = {
                    'from_day': day_short,
                    'to_day': day_short,
                    'hours': hours
                }
            elif this_day_group['hours'] != hours:
                day_groups.append(this_day_group)
                this_day_group = {
                    'from_day': day_short,
                    'to_day': day_short,
                    'hours': hours
                }
            elif this_day_group['hours'] == hours:
                this_day_group['to_day'] = day_short

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

    def address(self, address):
        if not address:
            return None

        addr_tags = {
            "addr_full": address['streetAddress'],
            "city": address['addressLocality'],
            "state": address['addressRegion'],
            "postcode": address['postalCode'],
        }

        return addr_tags

    def parse(self, response):
        response.selector.remove_namespaces()
        city_urls = response.xpath('//url/loc/text()').extract()
        for path in city_urls:
            yield scrapy.Request(
                path.strip(),
                callback=self.parse_store,
            )

    def parse_store(self, response):
        json_data = response.xpath('//*/script[@type="application/ld+json"]/text()').extract_first()
        json_data = json_data[: -3]
        data = json.loads(json_data)

        # properties = {
        #     'phone': data['telephone'].strip(),
        #     'website': response.xpath('//head/link[@rel="canonical"]/@href').extract_first(),
        #     'ref': data['url'],
        #     'opening_hours': self.store_hours(data['openingHours']),
        #     'lon': float(data['geo']['longitude']),
        #     'lat': float(data['geo']['latitude']),
        # }

        # address = self.address(data['address'])
        # if address:
        #     properties.update(address)


        raw = data['openingHours']
        formatted = self.store_hours(data['openingHours']),
        yield hourstudy(raw,formatted)
