import json
from utils.model_fun import Generator
from transformers import (pipeline,AutoTokenizer, T5ForConditionalGeneration )
from deep_translator import GoogleTranslator


class Pipeline():
    def __init__ (self):
        with open('utils/config.json') as js_f:
            self.config = json.load(js_f)
        
        self.clf_model=pipeline(model=self.config['clf_model'])   
        self.chat_tokenizer = AutoTokenizer.from_pretrained(self.config['chat_model']) 
        self.qa_tokenizer = AutoTokenizer.from_pretrained(self.config['qa_model']) 
        self.qa_model = T5ForConditionalGeneration.from_pretrained(self.config['qa_model'])
        self.chat_model = T5ForConditionalGeneration.from_pretrained(self.config['chat_model'])
        self.translator = GoogleTranslator(source='auto', target='en') 
        
        self.generator = Generator(clf_model=self.clf_model,
                     chat_model=self.chat_model,
                     chat_tokenizer=self.chat_tokenizer,
                     qa_tokenizer=self.qa_tokenizer,
                     qa_model=self.qa_model,
                     translator=self.translator)

    def classification(self, text):
        result=self.generator.clf_fun(text)              
        return result
    
    def conversation(self, text):
        result=self.generator.chat_fun(text)              
        return result
    
    def question_answer(self, text):
        result=self.generator.qa_fun(text)              
        return result

    def translation(self, text):
        result=self.generator.translate_fun(text)              
        return result