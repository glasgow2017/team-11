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

    // API calls start

    const apiUrl = 'http://ec2-52-209-24-100.eu-west-1.compute.amazonaws.com:5000/';
    const getTextUrl = 'getText';
    const getTextWithImgUrl = 'getTextWithImg';
    const getTopicUrl = 'getTopic';
    const parseMapUrl = 'parseMap';
    const setTextUrl = 'setText';

    // send a google map url to the backend and gets back the location text and distance and time to location
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

    // sends the url to the backend and gets back a list of common word and word count
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

    // sets the image recognition text on the backend, for manual description improvement
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

    // try to get text of image from backend cache using image hash only
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

    // get text of image by sending image blob, this will use the cloud vision apis
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

    // get blob of img src or return src if already a data url
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

    // API calls end

    // get base64 encoded string of blob from img src
    async function getBlobBase64FromSrc(src) {
        let blob = await getBlobFromServer(src);
        if (blob.constructor.name === 'Blob') {
            return await blobToBase64(blob);
        } else {
            return blob.replace(/data:.*base64,/, '');
        }
    }

    // convert blob to base64 string
    function blobToBase64(blob) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result.replace(/data:.*base64,/, ''));
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    }

    // build array of img elements storing the element, src, image blob and sha256 of the blob
    async function getImgElements() {
        let imgElements = [];
        for (let i = 0; i < document.images.length; i++) {
            let imgElement = document.images[i];
            if (!imgElement.src.includes('maps.googleapis.com')) {
                let blob = await getBlobBase64FromSrc(imgElement.src);
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

    // returns onclick function for image recognition improvement providing image hash in closure
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

    // process image elements, calling backend api and adding to alt text and adding improve recognition button
    // tries the image hash api call, if fails then sends the image blob
    async function getImgElementsAndConvertToText() {
        let imageElements = await getImgElements();
        if (imageElements.length > 0) {
            for (let imageElement of imageElements) {
                let text = await getTextFromServer(imageElement.sha256);
                if (!text || !text.result) {
                    text = await getTextWithImgFromServer(imageElement.blob);
                }
                if (text && text.result) {
                    if (imageElement.element.alt) {
                        imageElement.element.alt += ' Image also auto recognised as ' + text.result;
                    } else {
                        imageElement.element.alt = 'Image auto recognised as ' + text.result;
                    }
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

    // get list of document keywords and word count and display at top of page
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

    // get array of elements whether images or iframes of google maps
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

    // gets map text and adds details to page
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
