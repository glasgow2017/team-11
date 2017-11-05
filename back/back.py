from flask import Flask, request, jsonify
import base64
import hashlib
from image_recognition.img_trans import getRecogTextFromImage
from nlp.parse_sentence import get_webpage_description
from map.map_aloud import parse_map

app = Flask(__name__)

# cache of image recognition
# key: sha256 of the base64 of the image blob, value: the recognition result
imageCache = {}

@app.route('/')
def blankDefault():
    return ''

# accepts a google maps static or embed url
# returns location text and distance and time to destination
@app.route('/parseMap', methods=['POST'])
def parseMap():
    data = request.get_json()
    if data and data['url']:
        result = parse_map(data['url'])
        if result and result['location'] and result['distance']:
            return jsonify(result)
        else:
            return jsonify(errorCode=1, errorMsg='No result'), 204
    else:
        return jsonify(errorCode=20, errorMsg='Invalid request'), 400

# accepts url of website and returns list of common words on page and word count
@app.route('/getTopic', methods=['POST'])
def getTopic():
    data = request.get_json()
    if data and data['url']:
        result = get_webpage_description(data['url'])
        if result and result['topic'] and result['word_count']:
            return jsonify(result)
        else:
            return jsonify(errorCode=1, errorMsg='No result'), 204
    else:
        return jsonify(errorCode=20, errorMsg='Invalid request'), 400

# gets image text from cache using the sha256 of the base64 of the image blob
@app.route('/getText/<imageHash>', methods=['GET'])
def getTextUsingCache(imageHash):
    if imageHash in imageCache:
        return jsonify(result=imageCache[imageHash])
    else:
        return jsonify(errorCode=10, errorMsg='Not in cache'), 404

# accepts base64 image blob and send to cloud image recognition api
# returns description of image
@app.route('/getTextWithImg', methods=['POST'])
def getTextUsingAPI():
    data = request.get_json()
    if data and data['image']:
        imageEncoded = data['image']
        imageHash = hashlib.sha256(imageEncoded).hexdigest()
        imageDecoded = base64.b64decode(imageEncoded)

        recognitionResult = getRecogTextFromImage(imageDecoded)

        if recognitionResult:
            imageCache[imageHash] = recognitionResult
            return jsonify(result=recognitionResult)
        else:
            return jsonify(errorCode=1, errorMsg='No result'), 204

    else:
        return jsonify(errorCode=20, errorMsg='Invalid request'), 400

# updates cache of image recognition with custom description
@app.route('/setText/<imageHash>', methods=['POST'])
def setTextInCache(imageHash):
    data = request.get_json()
    if data and data['description']:
        imageCache[imageHash] = data['description']
        return jsonify(status='ok')
    else:
        return jsonify(errorCode=20, errorMsg='Invalid request'), 400

if __name__ == '__main__':
    app.run()
