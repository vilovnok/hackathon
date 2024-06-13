from config import *
from celery import Celery
from utils.pipeline import Pipeline
import time


from PIL import Image, ImageDraw
import io
import base64

celery = Celery(
    __name__, 
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}"
)       


pipeline = Pipeline()

@celery.task
def conversation(text: str):
    answer=pipeline.conversation(text=text)
    return answer

@celery.task
def translation(text: str):
    translated_sentences=pipeline.translation(text=text)
    return translated_sentences

# @celery.task
# def generateImg(text: str):
#     time.sleep(5)
#     img = Image.new('RGB', (200, 100), color=(73, 109, 137))
#     d = ImageDraw.Draw(img)
#     d.text((10, 10), text, fill=(255, 255, 0))
#     img_byte_arr = io.BytesIO()
#     img.save(img_byte_arr, format='PNG')
#     img_byte_arr = img_byte_arr.getvalue()
#     return base64.b64encode(img_byte_arr).decode('utf-8')    
    
    

@celery.task
def generateImg(text: str):
    image=pipeline.generateImg(text=text)
    return image