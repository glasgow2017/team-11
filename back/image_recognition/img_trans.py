
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
print azure_url


# In[67]:

HEADER_CONFIG = {
    'Ocp-Apim-Subscription-Key': AZURE_APIKEY,
    'Content-Type' : 'application/json'
}


# In[68]:

def send_request(server_url, img_url, headers=HEADER_CONFIG):
    rdata = {'url': img_url}
    r = requests.post(azure_url, headers=headers, data=json.dumps(rdata))
    try:
        return r.json()
    except:
        return {'Error': 'wrong image searching request'}
#         return {'error': '404'}


# In[69]:

r = send_request(azure_url, furl, headers=HEADER_CONFIG)


# In[70]:

r


# In[ ]:



