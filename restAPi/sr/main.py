import json
import base64
from PIL import Image
from io import BytesIO
from celery import Celery
from fastapi import FastAPI
from pipeline import Pipeline
from pydantic import BaseModel
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache.backends.redis import RedisBackend

app = FastAPI(title='RestAPI')
origins = ["http://localhost","http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin","Authorization"],
)

class Request(BaseModel):
    text: str

pipeline=Pipeline()

with open('config.json') as js_f:
    config = json.load(js_f)

celery = Celery(
    __name__, 
    broker=f"redis://{config['REDIS_HOST']}:{config['REDIS_PORT']}",
    backend=f"redis://{config['REDIS_HOST']}:{config['REDIS_PORT']}"
)    

@app.post('/generate/prompt-prepoccesing', status_code=201)
def prep(data: Request):
    text=data.text
    image_path='generated.jpg' 
    translated_sentences=translation.delay(text=text)
    translated_sentences=translated_sentences.get()
    image=generateImg.delay(translated_sentences, image_path)
    image=image.get()
    image_baytes=image_to_base64(image_path)
    return {'image_bytes':image_baytes, 'type':'jpeg'}    

def image_to_base64(path:str)->str:
    pil_image=Image.open(path)
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')
    
@celery.task
def translation(text: str):
    translated_sentences=pipeline.translation(text=text)
    return translated_sentences

@celery.task
def generateImg(text: str, path: str):
    image=pipeline.generateImg(text=text)
    image.save(path)
    return 'success'

@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(f"redis://{config['REDIS_HOST']}:{config['REDIS_PORT']}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
