# Your imports go here
import os, json, io, requests, re
from PIL import Image

import logging

logger = logging.getLogger(__name__)

'''
    Given a directory with receipt file and OCR output, this function should extract the amount

    Parameters:
    dirpath (str): directory path containing receipt and ocr output

    Returns:
    float: returns the extracted amount

'''
def get_data_from_Image(path):      # it takes time to process this around a minute
                # used ocr.space to get the text out of the image
    url_api = 'https://api.ocr.space/parse/image'
    api_key = '105fcebecc88957'

    img = Image.open(os.path.join(path, os.listdir(path)[-1]))
    buf = io.BytesIO()
    img.save(buf, 'jpeg')

    buf.seek(0)
    image_bytes = buf.read()
    buf.close()

    result = requests.post(url_api,
                           files = {os.path.join(path, os.listdir(path)[-1]) : image_bytes},
                           data = {"apikey" : api_key,
                                   'language' : 'eng'})

    result = result.content.decode()
    result = json.loads(result)

    parsed_results = result.get("ParsedResults")[0]
    text_detected = parsed_results.get("ParsedText")

    matchs = re.findall(r'\d+[.]\d\d', text_detected)

    if (len(matchs) > 0):
        return float(max(matchs))
    return 0.0

def get_data_from_Json(path):

    path = os.path.join(path, 'ocr.json')

    with open(path) as f:
        ocr = json.load(f)

    ocr = ocr['Blocks']

    temp = []
    for i in range(1, 50):
        matchs = re.findall(r'\d+[.]\d+', ocr[i]['Text'])
        temp.extend(matchs)

    return float(max(temp))
    


def extract_amount(dirpath: str) -> float:

    logger.info('extract_amount called for dir %s', dirpath)
    # your logic goes here

    # comment and uncomment the two lines below to for required process
##    result = get_data_from_Image(dirpath)
    result = get_data_from_Json(dirpath)
    
    return result



