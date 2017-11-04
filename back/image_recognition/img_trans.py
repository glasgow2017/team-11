
# coding: utf-8

# In[63]:

import requests
import json


# In[64]:

fn = 'test_img.jpg'
furl = 'http://colliersmagazine.com/sites/default/files/running%20dude.jpg'


# In[65]:

with open('API_KEYS.json', 'r') as f:
    api_config = json.load(f)
    
AZURE_APIKEY = api_config.get('Azure_APIKEY')


# In[66]:

# https://westus.dev.cognitive.microsoft.com/docs/services/56f91f2d778daf23d8ec6739/operations/56f91f2e778daf14a499e1fa
url_format = 'https://{location}.api.cognitive.microsoft.com/vision/v1.0/analyze?visualFeatures={vf}'
config = {'location': 'westeurope', 
          'visualFeatures': 'Tags,Description'}
azure_url = url_format.format(location=config.get('location'),
                              vf=config.get('visualFeatures'))


# In[77]:

HEADER_CONFIG = {
    'url_image': {
        'Ocp-Apim-Subscription-Key': AZURE_APIKEY,
        'Content-Type' : 'application/json'
    },
    'raw_image' : {
        'Ocp-Apim-Subscription-Key': AZURE_APIKEY,
        'Content-Type' : 'application/octet-stream'
    }
}


# In[84]:

def send_request_by_url(server_url, img_url, headers=HEADER_CONFIG['url_image']):
    rdata = {'url': img_url}
    r = requests.post(azure_url, headers=headers, data=json.dumps(rdata))
    return r
    
    
def send_request_by_image(server_url, img_data, headers=HEADER_CONFIG['raw_image']):
    rdata = {'url': img_url}
    r = requests.post(azure_url, headers=headers, data=json.dumps(rdata))
    return r


# In[85]:

def parse_response(res):
    try:
        response = res.json()
        tags = response.get('tags')
        description = response.get('description', [])
        captions = description.get('captions', [])
        tags = {x.get('name'): x.get('confidence') for x in tags}
        if len(captions) > 0:
            return captions[0]['text']
    except:
        return {'Error': 'wrong image searching request'}


# In[87]:

r = send_request_by_url(azure_url, furl)
parse_response(r)

