import json
import re
import scrapy
from locations.items import hourstudy
DAYS = {
    'monday': 'Mo',
    'tuesday': 'Tu',
    'wednesday': 'We',
    'friday': 'Fr',
    'thursday': 'Th',
    'saturday': 'Sa',
    'sunday': 'Su',
}
class CarphoneWarehouseSpider(scrapy.Spider):
    name = "carphonewarehouse"
    allowed_domains = ["www.carphonewarehouse.com"]
    def store_hours(self, store_hours):
        clean_time=''
        for key1 , value1 in DAYS.items():
           if key1 in store_hours:
               clean_time = clean_time + value1+" "+store_hours[key1]+" ;"
        return clean_time
    def start_requests(self):
        url = 'https://www.carphonewarehouse.com/services/storedata?filter=&count=1000000&lat=54.2526491&lng=-2.0411242'
        yield scrapy.Request(
                url=url,  callback=self.parse
            )

    def parse(self, response):
        data = json.loads(response.body_as_unicode())
        for key , value in data.items():
            if 'AddressLine' in value:
             addr_full = value['AddressLine'].split(',')
             address = ", ".join(addr_full[:len(addr_full)-1])
             city = addr_full[len(addr_full)-1]
            else:
                address=""
                city=""
            if 'postcode' in value:
                postcode = value['postcode']
            else:
                postcode = ""
            properties = {
                'ref': key ,
                'name': value['branch_name'],
                'addr_full': address,
                'city': city,
                'country':'United Kingdom',
                'postcode':postcode,
                'lat': value['Latitude'],
                'lon':  value['Longitude'],
                'phone':value['telephone'],
            }

            opening_hours = self.store_hours(value)
            if opening_hours:
                properties['opening_hours'] = opening_hours

            yield hourstudy(**properties)


