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

    const apiUrl = 'http://ec2-52-209-24-100.eu-west-1.compute.amazonaws.com:5000/';
    const getTextUrl = 'getText';
    const getTextWithImgUrl = 'getTextWithImg';
    const getTopicUrl = 'getTopic';
    const parseMapUrl = 'parseMap';
    const setTextUrl = 'setText';

    function parseMapFromServer(url) {
        return new Promise((resolve, reject) => {
            GM_xmlhttpRequest({
                url: apiUrl + parseMapUrl,
                method: "POST",
                data: JSON.stringify({url: url}),
                headers: {
                    "Content-Type": "application/json"
                },
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

    function getTopicFromServer(url) {
        return new Promise((resolve, reject) => {
            GM_xmlhttpRequest({
                url: apiUrl + getTopicUrl,
                method: "POST",
                data: JSON.stringify({url: url}),
                headers: {
                    "Content-Type": "application/json"
                },
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

    function setTextOnServer(imageHash, description) {
        return new Promise((resolve, reject) => {
            GM_xmlhttpRequest({
                url: apiUrl + setTextUrl + '/' + imageHash,
                method: "POST",
                data: JSON.stringify({description: description}),
                headers: {
                    "Content-Type": "application/json"
                },
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

    function getTextFromServer(imageHash) {
        return new Promise((resolve, reject) => {
            GM_xmlhttpRequest({
                url: apiUrl + getTextUrl + '/' + imageHash,
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
                url: apiUrl + getTextWithImgUrl,
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

    async function getImgElements() {
        let imgElements = [];
        for (let i = 0; i < document.images.length; i++) {
            let imgElement = document.images[i];
            if (!imgElement.src.includes('maps.googleapis.com')) {
                let blob = await getBlobBase64FromSrc(imgElement.src)
                imgElements.push({
                    element: imgElement,
                    src: imgElement.src,
                    blob: blob,
                    sha256: sha256(blob)
                });
            }
        }
        return imgElements;
    }

    function onImproveWrapper(imageHash) {
        return function (e) {
            e.preventDefault();
            let betterDescription = prompt('Write a better description');
            if (betterDescription) {
                setTextOnServer(imageHash, betterDescription).then(result => {
                    if (result && result.status && result.status === 'ok') {
                        alert('Thanks for your contribution');
                    }
                }).catch(console.error)
            }
        }
    }


    async function getImgElementsAndConvertToText() {
        let imageElements = await getImgElements();
        if (imageElements.length > 0) {
            for (let imageElement of imageElements) {
                if (!imageElement.element.alt) {
                    let text = await getTextFromServer(imageElement.sha256);
                    if (!text || !text.result) {
                        text = await getTextWithImgFromServer(imageElement.blob);
                    }
                    if (text && text.result) {
                        imageElement.element.alt = text.result;
                        let imageTextDiv = document.createElement('div');
                        let improveDiv = document.createElement('button');
                        imageTextDiv.innerText = text.result;
                        improveDiv.innerText = 'Improve this recognition';
                        improveDiv.onclick = onImproveWrapper(imageElement.sha256);
                        imageElement.element.parentNode.insertBefore(imageTextDiv, imageElement.element);
                        imageElement.element.parentNode.insertBefore(improveDiv, imageElement.element);
                        console.log(imageElement.src, imageElement.element.alt);
                    }
                }
            }
        }
    }

    async function addTopicsToDocument() {
        let topics = await getTopicFromServer(document.URL);
        if (topics && topics.topic && topics.word_count) {
            let topicJoin = topics.topic.join(', ');
            let topicString = `The most used words in this document are ${topicJoin}. The word count is ${topics.word_count}.`;
            let topicDiv = document.createElement('div');
            topicDiv.innerText = topicString;
            document.body.insertBefore(topicDiv, document.body.firstChild);
            console.log(topicString);
        }
    }

    async function getMapElements() {
        let mapElements = [];
        for (let i = 0; i < document.images.length; i++) {
            let element = document.images[i];
            if (element.src.includes('maps.googleapis.com')) {
                mapElements.push({
                    element: element,
                    src: element.src
                });
            }
        }
        let iframes = document.getElementsByTagName('iframe');
        for (let i = 0; i < iframes.length; i++) {
            let element = iframes[i];
            if (element.src.includes('www.google.com/maps')) {
                mapElements.push({
                    element: element,
                    src: element.src
                });
            }
        }
        return mapElements;
    }

    async function addMapDetailsToDocument() {
        let mapElements = await getMapElements();
        for (let mapElement of mapElements) {
            let mapData = await parseMapFromServer(mapElement.src);
            if (mapData) {
                let mapTextDiv = document.createElement('div');
                mapTextDiv.innerText = mapData.location + ' ' + mapData.distance;
                mapElement.element.parentNode.insertBefore(mapTextDiv, mapElement.element);
                console.log(mapData);
            }
        }
    }

    getImgElementsAndConvertToText().catch(console.error);

    addTopicsToDocument().catch(console.error);

    addMapDetailsToDocument().catch(console.error);

})();
