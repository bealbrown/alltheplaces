# -*- coding: utf-8 -*-
import json
import scrapy

from locations.items import hourstudy


class SuperonefoodsSpider(scrapy.Spider):
    name = "superonefoods"
    allowed_domains = ["www.superonefoods.com"]
    start_urls = (
        'https://www.superonefoods.com/store-finder',
    )

    def parse(self, response):
        # retrieve js data variable from script tag
        items = response.xpath('//script/text()')[3].re("var stores =(.+?);\n")

        # convert data variable from unicode to string
        items = [str(x) for x in items]

        # convert type string representation of list to type list
        data = [items[0]]

        # load list into json object for parsing
        jsondata = json.loads(data[0])

        # loop through json data object and retrieve values; yield the values to hourstudy
        for item in jsondata:
            yield hourstudy(
                ref=item.get('_id'),
                lat=float(item.get('latitude')),
                lon=float(item.get('longitude')),
                addr_full=item.get('address'),
                city=item.get('city'),
                state=item.get('state'),
                postcode=item.get('zip'),
                website='https://www.superonefoods.com/store-details/'+item.get('url'),
            )
