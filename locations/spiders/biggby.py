# -*- coding: utf-8 -*-
import json
import scrapy
from xml.etree import ElementTree as ET
from scrapy import Selector

from locations.items import hourstudy


class BiggbySpider(scrapy.Spider):
	name = "biggby"
	allowed_domains = ["www.biggby.com"]
	start_urls = (
		'https://www.biggby.com/locations/',
	)

	def parse(self, response):
		# retrieve XML data from DIV tag
		items = response.xpath("//div[@id='loc-list']/markers").extract()
		# convert data variable from unicode to string
		items = [str(x) for x in items]
		# create element tree object
		root = ET.fromstring(items[0])

		# iterate items
		for item in root:
			yield hourstudy(
				ref=item.attrib['pid'],
				lat=float(item.attrib['lat']),
				lon=float(item.attrib['lng']),
				addr_full=item.attrib['address-two'],
				city=item.attrib['city'],
				state=item.attrib['state'],
				postcode=item.attrib['zip'],
				name=item.attrib['name'],
			)