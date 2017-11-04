// ==UserScript==
// @name         JPMorgan
// @namespace    codeforgood
// @version      0.1
// @description  try to take over the world!
// @author       You
// @include      *
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function () {
    'use strict';

    const url = 'http://ec2-52-209-24-100.eu-west-1.compute.amazonaws.com:5000/';
    const getTextUrl = 'getText';
    const getTextWithImg = 'getTextWithImg';

    function getBlobFromServer(src) {
        return new Promise((resolve, reject) => {
            GM_xmlhttpRequest({
                url: src,
                method: "GET",
                onload: function (response) {
                    if (response.status === 200 && response.responseText) {
                        resolve(response.responseText);
                    } else {
                        reject(response.status);
                    }
                }
            });
        });
    }

    async function getBlobBase64FromSrc(src) {
        let blob = await getBlobFromServer(src);
        return await blobToBase64(blob);
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
        let imgElements = {};
        for (let i = 0; i < document.images.length; i++) {
            let imgElement = document.images[i];
            imgElements[i] = {
                element: imgElement,
                src: imgElement.src,
                blob: await getBlobBase64FromSrc(imgElement.src)
            }
        }
        return imgElements;
    }

    getImgElements().then(console.log);

    
})();
