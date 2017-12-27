# -*- coding: utf-8 -*-
import scrapy
import re
from locations.items import hourstudy


class TjmaxxSpider(scrapy.Spider):
    name = "tjmaxx"
    allowed_domains = ["tjx.com", "tjmaxx.com"]
    start_urls = (
        'https://tjmaxx.tjx.com/store/stores/allStores.jsp',
    )

    def parse(self, response):
        links = response.xpath('//li[@class="storelist-item vcard address"]/a[@href]/@href')
        for link in links:
            yield scrapy.Request(
                response.urljoin(link.extract()),
                callback=self.parse_links
            )

    def parse_links(self, response):
        hours = response.xpath('//form[@id="directions-form"]/input[@name="hours"]/@value').extract_first()
        website = response.xpath('//head/link[@rel="canonical"]/@href').extract_first()
        link_id = website.split("/")[-2]

        # properties = {
        #     "addr_full": response.xpath('//form[@id="directions-form"]/input[@name="address"]/@value').extract_first(),
        #     "city": response.xpath('//form[@id="directions-form"]/input[@name="city"]/@value').extract_first(),
        #     "state": response.xpath('//form[@id="directions-form"]/input[@name="state"]/@value').extract_first(),
        #     "postcode": response.xpath('//form[@id="directions-form"]/input[@name="zip"]/@value').extract_first(),
        #     "phone": response.xpath('//form[@id="directions-form"]/input[@name="phone"]/@value').extract_first(),
        #     "website": website,
        #     "ref": link_id,
        #     "opening_hours": self.process_hours(hours[0]),
        #     "lat": float(response.xpath('//form[@id="directions-form"]/input[@name="lat"]/@value').extract_first()),
        #     "lon": float(response.xpath('//form[@id="directions-form"]/input[@name="long"]/@value').extract_first()),
        # }

        # yield hourstudy(**properties)
        raw = hours[0]
        formatted = self.process_hours(hours[0])
        yield hourstudy(raw,formatted)


    def process_hours(self, hours):
        """ This should capture these time formats as on tjmaxx
                # Mon-Wed: 9:30a-9:30p,
                # Thanksgiving Day: CLOSED,  <- this gets appended without modification
                # Fri-Sat: 7a-10p,
                # Sun: 9a-10p
        :param hours:
        :return:  string - in this format Mo-Th 11:00-12:00; Fr-Sa 11:00-01:00;
        """
        working_hour = []

        for t in hours.split(","):
            match = re.search(r"^((\w{2})\w(?:-(\w{2})\w)?\:\s(\d+)(\:\d+)?(\w)-(\d+)(\:\d+)?(\w))$",
                              t.strip(),
                              re.IGNORECASE)
            if match:
                m = list(match.groups())
                if len(m) == 9:
                    # replace second entry for day of week for formats like Sun: 9a-12p
                    if m[2] is None:
                        m[2] = ""
                    else:
                        m[2] = "-" + m[2]

                    # concatenate to our format
                    if m[4] is None:
                        if m[7] is None:
                            # time is like Mon-Wed: 9a-9p
                            hr_1 = int(m[3]) + self.am_pm(m[3], m[5])
                            hr_2 = int(m[6]) + self.am_pm(m[6], m[8])
                            working_hour.append(m[1] + m[2] + " " + f'{hr_1:02}' + ":00-" + f'{hr_2:02}' + ":00")
                        else:
                            # time is like Mon-Wed: 9a-9:30p
                            hr_1 = int(m[3]) + self.am_pm(m[3], m[5])
                            hr_2 = int(m[6]) + self.am_pm(m[6], m[8])
                            working_hour.append(m[1] + m[2] + " " + f'{hr_1:02}' + ":00-" + f'{hr_2:02}' + m[7])
                    else:
                        if m[7] is None:
                            # time is like Mon-Wed: 9:30a-9p
                            hr_1 = int(m[3]) + self.am_pm(m[3], m[5])
                            hr_2 = int(m[6]) + self.am_pm(m[6], m[8])
                            working_hour.append(m[1] + m[2] + " " + f'{hr_1:02}' + m[4] + "-" + f'{hr_2:02}' + ":00")
                        else:
                            # time is like Mon-Wed: 9:30a-9:30p
                            hr_1 = int(m[3]) + self.am_pm(m[3], m[5])
                            hr_2 = int(m[6]) + self.am_pm(m[6], m[8])
                            working_hour.append(m[1] + m[2] + " " + f'{hr_1:02}' + m[4] + "-" + f'{hr_2:02}' + m[7])
            # else:
            #     working_hour.append(t)

        if working_hour:
            return "; ".join(working_hour)
        else:
            # if something fails, return original date
            return hours

    def am_pm(self, hr, a_p):
        """
            A convenience method to fix noon and midnight issues
        :param hr: the hour has to be passed it to accurately decide 12noon and midnight
        :param a_p: this is either a or p i.e am pm
        :return: the hours that must be added

        """
        diff = 0
        if a_p == 'a':
            if int(hr) < 12:
                diff = 0
            else:
                diff = -12
        else:
            if int(hr) < 12:
                diff = 12
        return diff
