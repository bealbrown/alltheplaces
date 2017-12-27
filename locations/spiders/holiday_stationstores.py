# -*- coding: utf-8 -*-
import scrapy
import re

from locations.items import hourstudy


class HolidayStationstoreSpider(scrapy.Spider):
    name = "holiday_stationstores"
    allowed_domains = ["m.holidaystationstores.com"]
    start_urls = (
        'http://m.holidaystationstores.com/locations/stores/',
    )

    def parse(self, response):
        location_hrefs = response.xpath('//div[@id="stores"]/ul/li/a/@href')

        for path in location_hrefs:
            yield scrapy.Request(
                response.urljoin(path.extract()),
                callback=self.parse_location
            )

    def opening_hours(self, response):
        hour_part_elems = response.xpath('//table[@style="margin-left:0px;font-size:90%;padding:0px;"]/tr/td/text()').extract()
        day_groups = []
        this_day_group = None

        if hour_part_elems:
            def slice(source, step):
                return [source[i:i+step] for i in range(0, len(source), step)]

            for day, hours in slice(hour_part_elems, 2):
                day = day[:2]
                match = re.search(r'^(\d{1,2}):(\d{2})\w*(a|p)m - (\d{1,2}):(\d{2})\w*(a|p)m?$', hours)
                (f_hr, f_min, f_ampm, t_hr, t_min, t_ampm) = match.groups()

                f_hr = int(f_hr)
                if f_ampm == 'p':
                    f_hr += 12
                elif f_ampm == 'a' and f_hr == 12:
                    f_hr = 0
                t_hr = int(t_hr)
                if t_ampm == 'p':
                    t_hr += 12
                elif t_ampm == 'a' and t_hr == 12:
                    t_hr = 0

                hours = '{:02d}:{}-{:02d}:{}'.format(
                    f_hr,
                    f_min,
                    t_hr,
                    t_min,
                )

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

        hour_part_elems = response.xpath('//span[@style="font-size:90%"]/text()').extract()
        if hour_part_elems:
            day_groups.append({'from_day': 'Mo', 'to_day': 'Su', 'hours': '00:00-23:59'})

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

    def parse_location(self, response):
        addr_parts = response.xpath('//div[@style="float:left;padding-right:10px;padding-left:10px;"][1]/text()').extract()
        store_name = response.xpath('//h2[@style="padding-right:10px;padding-left:10px;margin-bottom:10px;"]/text()').extract_first()

        properties = {
            'name': store_name,
            'addr_full': addr_parts[1].strip(),
            'phone': response.xpath('//div[@style="margin-top:3px;margin-bottom:4px;"]/a/text()').extract_first(),
            'ref': store_name,
            'lon': float(response.xpath('//div[@id="SingleStoreMap"]/@data-longitude').extract_first()),
            'lat': float(response.xpath('//div[@id="SingleStoreMap"]/@data-latitude').extract_first()),
            'opening_hours': self.opening_hours(response),
        }

        yield hourstudy(**properties)
