
# coding: utf-8

# In[355]:

import json
import requests
import os
import urlparse

'''
call solve_map()              to get response: I found a Map of LOCATION: 62-66 Union St, Glasgow G1 3QS, UK
call parse_distance(distance) This place is 0.7 mi from You! ... And ....It will take you 8 mins to Get There!

# loc1_text, loc1 = solve_map(url1)
# loc2_text, loc2 = solve_map(url2)
# distance = find_distance(loc1)
# parse_distance(distance) 

Test using these... we are using a fake user location! it is here!!!
'''

# 'https://maps.googleapis.com/maps/api/geocode/json?address={addr}&key={APIKEY}'
# 'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{long}&key={APIKEY}'

# url1 = "https://maps.googleapis.com/maps/api/staticmap?scale=2&amp;center=55.859419%2C-4.256227&amp;language=None&amp;zoom=15&amp;markers=scale%3A2%7Cicon%3Ahttps%3A%2F%2Fyelp-images.s3.amazonaws.com%2Fassets%2Fmap-markers%2Fannotation_64x86.png%7C55.859419%2C-4.256227&amp;client=gme-yelp&amp;sensor=false&amp;size=286x135&amp;signature=eUaECXWgmexENnSeHT3XlwmhODc="
# url2 = "https://www.google.com/maps/embed/v1/place?q=Harrods,Brompton%20Rd,%20UK"

# with open(os.path.join(os.path.dirname(__file__), 'API_KEYS.json'), 'r') as f:
FAKE_LOCATION_PLACE_NAME = 'JP Morgan Glasgow Office'
FAKE_LOCATION_LATLNG = (55.8612967, -4.2638861)
with open('API_KEYS.json', 'r') as f:
    api_config = json.load(f)
    
API_KEY = api_config.get('GOOGLE_APIKEY1')


# In[356]:

def get_place_name_from_latlng(lat, lon, apikey=API_KEY):
    url_template = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={APIKEY}'
    search_url = url_template.format(lat=lat,lon=lon,APIKEY=apikey)
#     print search_url
    response = requests.get(search_url)
    return response

def get_latlng_from_placename(pn, apikey=API_KEY):
    url_template ='https://maps.googleapis.com/maps/api/geocode/json?address={addr}&key={APIKEY}'
    search_url = url_template.format(addr=pn, APIKEY=apikey)
    response = requests.get(search_url)
    return response


# In[357]:

def parse_geoencoding(res):
    try:
        res = res.json()
        results = res.get('results')
        result = results[0]
        addr_comp = result.get("formatted_address")
        place_id = result.get("place_id")
        types = result.get("types")
        location = result.get('geometry').get('location')
        lat_long = (location.get('lat'), location.get('lng'))
        return addr_comp, place_id, types, lat_long
    except:
        return '', '', []


# In[358]:

# https://maps.googleapis.com/maps/api/staticmap?scale=2&center=51.504058%2C-0.192783
def parse_embeded_url(input_url):
    if 'googleapis' in input_url:
        return 0, google_map_search_staticmap(input_url)
    elif 'google.com' in input_url:
        return 1, google_map_search_embed(input_url)
    else:
        return 2, None
    

def google_map_search_staticmap(input_url):
    try:
        parsed = urlparse.urlparse(input_url)
        return urlparse.parse_qs(parsed.query)['center'][0]
    except:
        return None


def google_map_search_embed(input_url):
    try:
        parsed = urlparse.urlparse(input_url)
        return urlparse.parse_qs(parsed.query)['q'][0]
    except:
        return None


# In[359]:

def solve_map(input_url):
    flag, location = parse_embeded_url(input_url)
    if flag == 1 and location:
        print "I found a Map of LOCATION: " + location
    elif flag == 0 and location:
        lat, lng = location.split(',')
        res = get_place_name_from_latlng(lat, lng)
        loc = parse_geoencoding(res)[0]
        print "I found a Map of LOCATION: " + loc
    try:
        flag, location = parse_embeded_url(input_url)
        res = ""

        if flag == 1 and location:
            res = "I found a Map of LOCATION: " + location
        elif flag == 0 and location:
            lat, lng = location.split(',')
            res = get_place_name_from_latlng(lat, lng)
            loc = parse_geoencoding(res)[0]
            res = "I found a Map of LOCATION: " + loc
        return res, location
    except:
        return None, None


# In[360]:

def find_distance(loc2, loc1=FAKE_LOCATION_PLACE_NAME, apikey=API_KEY):
    # https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=Washington,DC&destinations=New+York+City,NY&key=YOUR_API_KEY
    url_template = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={ORI}&destinations={DEST}&key={APIKEY}"
    search_url = url_template.format(ORI=loc1, DEST=loc2, APIKEY=apikey)
    response = requests.get(search_url)
    return response


# In[361]:

def parse_distance(res):
    res = res.json()
    try:
        element = res.get('rows')[0].get('elements')[0]
        distance = element.get('distance').get('text')
        duration = element.get('duration').get('text')
        res = 'This place is ' + distance + ' from You! ... And ....'
        res += 'It will take you ' + duration + ' to Get There!'
        return res
    except:
        res = 'Sorry we cannot find a route for you!'
        return res

