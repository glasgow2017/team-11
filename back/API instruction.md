# API Instruction
## How to get the image:
### Build function getTextUsingCache 
1. Use function getTextUsingCache to get the image and if imageHash is in imageCache return jason and the result turns to function imageCache[imagehash], if not we should return error code and explain error that it couldn't find in cache

## How to post image
### Build function getRecogTextFromImage 
This function is used to combine two function(parse_response and send_requests_by_image) to request for URL
### Build function getTextUsingAPI 
1.First try to tell if the data are images or not. If data are image and find its URL and encode it into more simple code by hashlib to avoid long source and then import base64 and encode it again. The result imageDecoded will become very short and is easy to read. 
2. Put imageDecoded into function getRecogTextFromImage to get the recognitionResult which describe the picture and if recognitionResult is in the imagCache, it will return the recognitionResult to show description of the picture
