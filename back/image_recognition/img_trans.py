import requests
import json
import os

with open(os.path.join(os.path.dirname(__file__), 'API_KEYS.json'), 'r') as f:
    api_config = json.load(f)

AZURE_APIKEY = api_config.get('Azure_APIKEY')

url_format = 'https://{location}.api.cognitive.microsoft.com/vision/v1.0/analyze?visualFeatures={vf}'

config = {'location': 'westeurope',
          'visualFeatures': 'Tags,Description'}

azure_url = url_format.format(location=config.get('location'),
                              vf=config.get('visualFeatures'))

HEADER_CONFIG = {
    'url_image': {
        'Ocp-Apim-Subscription-Key': AZURE_APIKEY,
        'Content-Type': 'application/json'
    },
    'raw_image': {
        'Ocp-Apim-Subscription-Key': AZURE_APIKEY,
        'Content-Type': 'application/octet-stream'
    }
}

# requests image recognition using cloud api using image url
def send_request_by_url(img_url, headers=HEADER_CONFIG['url_image']):
    rdata = {'url': img_url}
    r = requests.post(azure_url, headers=headers, data=json.dumps(rdata))
    return r

# requests image recogition using cloud api using image binary
def send_request_by_image(img_data, headers=HEADER_CONFIG['raw_image']):
    r = requests.post(azure_url, headers=headers, data=img_data)
    return r

# parse the response and gets the description text
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
        return

# sends image binary and return image description
def getRecogTextFromImage(image):
    res = send_request_by_image(image)
    return parse_response(res)