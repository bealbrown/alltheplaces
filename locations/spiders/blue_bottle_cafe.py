# -*- coding: utf-8 -*-
import scrapy
import json
from locations.items import hourstudy


class BlueBottleCafeSpider(scrapy.Spider):

    name = "bluebottlecafe"
    allowed_domains = ["www.bluebottlecoffee.com"]
    start_urls = (
        'https://bluebottlecoffee.com/api/cafe_search/fetch.json?coordinates=false&query=true&search_value=all',
    )

    def parse(self, response):
        results = json.loads(response.body_as_unicode())
        for region_name in results["cafes"]:
            for store_data in results["cafes"][region_name]:

                address_string = store_data['address'].replace('\n', ' ').replace('\r', '').replace('<br>', ', ')

                properties = {
                    'name': store_data['name'],
                    'addr_full': address_string,
                    'city': address_string.split(", ")[1],
                    'website': store_data['url'],
                    'ref': store_data['id'],
                    'lon': store_data['longitude'],
                    'lat': store_data['latitude'],
                }

                yield hourstudy(**properties)
