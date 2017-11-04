from flask import Flask, request, jsonify
import base64
import hashlib
from image_recognition.img_trans import getRecogTextFromImage

app = Flask(__name__)

imageCache = {}

@app.route('/')
def blankDefault():
    return ''

@app.route('/getText/<imageHash>', methods=['GET'])
def getTextUsingCache(imageHash):
    if imageHash in imageCache:
        return jsonify(result=imageCache[imageHash])
    else:
        return jsonify(errorCode=10, errorMsg='Not in cache'), 404

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

if __name__ == '__main__':
    app.run()
