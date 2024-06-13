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


@celery.task
def generateImg(text: str):
    time.sleep(5)
    
    img = Image.new('RGB', (200, 100), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    d.text((10, 10), text, fill=(255, 255, 0))


    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    return base64.b64encode(img_byte_arr).decode('utf-8')    
    
    

# # @celery.task
# # def question_answering(prompt: str):
# #     question = "Что нужно нарисовать?"
# #     tokenized_sentence = qa_tokenizer(prompt, question, return_tensors='pt')
# #     res = qa_model.generate(**tokenized_sentence)
# #     decoded_res = qa_tokenizer.decode(res[0], skip_special_tokens=True)
#     return decoded_res