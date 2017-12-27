# -*- coding: utf-8 -*-
import scrapy
import json
import re

from locations.items import hourstudy

class TacocabanaSpider(scrapy.Spider):
    name = "tacocabana"
    allowed_domains = ["www.tacocabana.com"]
    start_urls = (
        "http://www.tacocabana.com/wp-admin/admin-ajax.php?action=get_ajax_processor&processor=get-locations&queryType=&postID=816",
    )
        
    def parse(self, response):
        data = json.loads(re.sub(r"\s<.*?>.*<.*?>\s", "", response.body_as_unicode()))

        for store in data:
            # properties = {
            #     "phone"         : store["phone_number"],
            #     "ref"           : str(store["locator_store_number"]),
            #     "name"          : store["post_title"],
            #     "opening_hours" : store["hours"],
            #     "website"       : store["permalink"],
            #     "lat"           : store["x_coordinate"],
            #     "lon"           : store["y_coordinate"],
            #     "street"        : store["street_address_1"] + store["street_address_2"],
            #     "city"          : store["city"],
            #     "state"         : store["state"],
            #     "postcode"      : store["zip_code"]
            # }
            
            # yield hourstudy(**properties)
            raw = store["hours"]
            formatted = store["hours"]
            yield hourstudy(raw,formatted)
        
        else:
            self.logger.info("No results")
