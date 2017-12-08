import json
import re
import scrapy
import logging
from locations.items import GeojsonPointItem

def process_hours(hours):
    if 'Hours' not in hours:
        return None

    opening_hours = ''
    days = hours['Hours']
    for day in days:
        shortname = day['ShortName'] 
        if '-' in shortname:
            startday, endday = shortname.split('-')
            if startday == "M": startday = "Mo"
            if endday == "M": endday = "Mo"
            shortname = '-'.join([startday, endday])
        timeperiod = day['TimePeriod']
        starttime = timeperiod['BeginTime'][:-3]
        endtime = timeperiod['ThruTime'][:-3]
        time_together = '-'.join([starttime, endtime])
        opening_hours += "{shortname} {time_together};".format(
            shortname=shortname,
            time_together=time_together
        )
    return opening_hours[:-1]

class TargetSpider(scrapy.Spider):
    ''' The Target api allows us a maximum search radius of 625 miles, so we have
        to use multiple api requests with zip codes from different states to 
        search the whole country.
    
        NOTE: There is a "key" variable used in the url for the requests.
        It seems that this does not vary between natural requests (those sent
        from a browser), but it might be something that expires and renders requests
        invalid. So, if this spider stops working, that's probably why.
    '''         
    zips = ['97062', '90021', '73301', '82633', '29401', '60007', '04019', '87101', '59601', '39056', '14201', '55111', '94203', '64030', '33601']
    name = "target"
    allowed_domains = ["target.com"]
    start_urls = tuple([
        'https://api.target.com/v2/store?nearby={zipcode}&range=625&limit=999999&locale=en-US&key=eb2551e4accc14f38cc42d32fbc2b2ea&callback=jQuery21409262105278815946_1512699093216&_=1512699093219'.format(zipcode=z) for z in zips
    ])

    def parse(self, response):
        data = json.loads(response.body_as_unicode()[41:-1])
        stores = data['Locations']['Location'] 
        for store in stores:
            loc_info = store['Address']
            properties = {
                'ref': store['ID'],
                'name': store['Name'],
                'addr_full': loc_info['AddressLine1'],
                'city': loc_info['City'],
                'state': loc_info['Subdivision'],
                'country': loc_info['CountryName'],
                'postcode': loc_info['PostalCode'],
                'lat': loc_info['Latitude'],
                'lon': loc_info['Longitude'],
            }

            phones = store['TelephoneNumber']
            if type(phones) == "list":
                for i in phones:
                    if i['FunctionalTypeDescription'] == 'Main':
                        properties['phone'] = i['PhoneNumber']
            elif type(phones) == 'dict':
                if phones['FunctionalTypeDescription'] == 'Main':
                    properties['phone'] = phones['PhoneNumber']

            if 'OperatingHours' in store:
                processed_hours = process_hours(store['OperatingHours'])                
                if processed_hours:
                    properties['opening_hours'] = processed_hours
                                                             
            yield GeojsonPointItem(**properties)             
