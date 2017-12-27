import json
import re
import scrapy
from locations.items import hourstudy

class McDonaldsGTSpider(scrapy.Spider):
    name = "mcdonalds_gt"
    allowed_domains = ["mcdonalds.com.gt"]

    def start_requests(self):
        url = 'https://mcdonalds.com.gt/wp-admin/admin-ajax.php'
        headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://mcdonalds.com.gt',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': '*/*',
            'Referer': 'https://mcdonalds.com.gt/ubicaciones-mc/',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
        }
        form_data = {
            'action':'obtener_marcadores'
        }

        yield scrapy.http.FormRequest(
            url=url, method='POST', formdata=form_data,
            headers=headers, callback=self.parse
        )
    
    def parse_latlon(self, data):
        match = re.search(r'(.*)(,<div)', data)
        data = match.groups()[0]
        lat = data.split(",")[0].strip()
        lon = data.split(",")[1].strip()
        return lat, lon

    def parse_address(self, data):
        match = re.search(r'(McDonald&#039;s )(.*)', data)
        return match.groups()[1]

    def parse(self, response):
        stores = response.body_as_unicode().split("|")
        index = 0
        for item in stores:
            lat, lon = self.parse_latlon(item)
            address = self.parse_address(item)
            properties = {
                'ref': index,
                'name': "Mcdonald's",
                'addr_full': address,
                'lat': lat,
                'lon': lon,
            }

            index = index + 1

            yield hourstudy(**properties)

