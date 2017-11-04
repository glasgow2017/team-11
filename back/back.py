from flask import Flask, request, jsonify
import base64
import hashlib

app = Flask(__name__)

imageCache = {}

@app.route('/')
def blankDefault():
    return ''

@app.route('/getText/<imgId>', methods=['GET'])
def getTextUsingCache(imgId):
    if imgId in imageCache:
        return jsonify(result=imageCache[imgId])
    else:
        return jsonify(errorCode=1, errorMsg='Not in cache'), 404

@app.route('/getTextWithImg', methods=['POST'])
def getTextUsingAPI():
    data = request.get_json()
    if data and data.image:
        imageEncoded = data.image
        imageHash = hashlib.sha256(imageEncoded).hexdigest()
        imageDecoded = base64.b64decode(imageEncoded)

        recognitionResult = getTextFromImage(imageDecoded)

        imageCache[imageHash] = recognitionResult
        return jsonify(result=recognitionResult)
    else:
        return jsonify(errorCode=2, errorMsg='Invalid request'), 400

def getTextFromImage(image):
    return 'dummyData'

if __name__ == '__main__':
    app.run()
