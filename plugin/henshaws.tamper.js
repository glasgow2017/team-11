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

    const url = 'server url';

    async function getBlobBase64FromSrc(src) {
        let response = await fetch(src);
        let blob = await response.blob();
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

    async function getImgElements() {
        let imgElements= {};
        for (let i = 0; i < document.images.length; i++) {
            let imgElement = document.images[i];
            imgElements[i] = {element: imgElement, src: imgElement.src, blob: await getBlobBase64FromSrc(imgElement.src)}
        }
        return imgElements;
    }

    getImgElements().then(console.log);




})();