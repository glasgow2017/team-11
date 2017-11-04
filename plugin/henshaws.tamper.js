// ==UserScript==
// @name         JPMorgan
// @namespace    codeforgood
// @version      0.1
// @description  try to take over the world!
// @author       You
// @include      *
// @connect      *
// @grant        GM_xmlhttpRequest
// @require      https://cdnjs.cloudflare.com/ajax/libs/js-sha256/0.7.1/sha256.min.js
// ==/UserScript==

(function () {
    'use strict';

    const url = 'http://ec2-52-209-24-100.eu-west-1.compute.amazonaws.com:5000/';
    const getTextUrl = 'getText';
    const getTextWithImgUrl = 'getTextWithImg';

    function getTextFromServer(imageHash) {
        return new Promise((resolve, reject) => {
            GM_xmlhttpRequest({
                url: url + getTextUrl + '/' + imageHash,
                method: "GET",
                onload: function (response) {
                    if (response.status === 200 && response.responseText) {
                        resolve(JSON.parse(response.responseText));
                    } else if (response.status === 404) {
                        resolve();
                    } else {
                        resolve();
                    }
                }
            });
        });
    }

    function getTextWithImgFromServer(imageBase64Blob) {
        return new Promise((resolve, reject) => {
            GM_xmlhttpRequest({
                url: url + getTextWithImgUrl,
                method: "POST",
                data: JSON.stringify({image: imageBase64Blob}),
                headers: {
                    "Content-Type": "application/json"
                },
                onload: function (response) {
                    if (response.status === 200 && response.responseText) {
                        resolve(JSON.parse(response.responseText));
                    } else {
                        resolve();
                        console.error(response.status);
                    }
                }
            });
        });
    }

    function getBlobFromServer(src) {
        return new Promise((resolve, reject) => {
            if (src.startsWith('data')) {
                resolve(src);
            } else {
                GM_xmlhttpRequest({
                    url: src,
                    method: "GET",
                    responseType: 'blob',
                    onload: function (response) {
                        if (response.status === 200 && response.response) {
                            resolve(response.response);
                        } else {
                            reject(response.status);
                        }
                    }
                });
            }
        });
    }

    async function getBlobBase64FromSrc(src) {
        let blob = await getBlobFromServer(src);
        if (blob.constructor.name === 'Blob') {
            return await blobToBase64(blob);
        } else {
            return blob.replace(/data:.*base64,/, '');
        }
    }

    function blobToBase64(blob) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result.replace(/data:.*base64,/, ''));
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    }

    // {"result": "......description......"}
    async function getImgElements() {
        let imgElements = [];
        for (let i = 0; i < document.images.length; i++) {
            let imgElement = document.images[i];
            imgElements.push({
                element: imgElement,
                src: imgElement.src,
                blob: await getBlobBase64FromSrc(imgElement.src)
            });
        }
        return imgElements;
    }

    async function getImgElementsAndConvertToText() {
        let imageElements = await getImgElements();
        if (imageElements.length > 0) {
            for (let imageElement of imageElements) {
                let text = await getTextFromServer(sha256(imageElement.blob));
                if (!text || !text.result) {
                    text = await getTextWithImgFromServer(imageElement.blob);
                }
                if (text && text.result) {
                    imageElement.element.alt = text.result;
                    console.log(imageElement.src, imageElement.element.alt);
                }
            }
        }
    }

    getImgElementsAndConvertToText().catch(console.error);


})();
