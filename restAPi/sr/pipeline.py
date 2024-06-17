import json
import torch
from hackathon.restAPi.sr.image_generator import ImageGenerator
from deep_translator import GoogleTranslator
from prompt_generator import PromptGenerator
from diffusers import (StableDiffusionPipeline, DPMSolverMultistepScheduler)
from transformers import (AutoModelForCausalLM, AutoTokenizer)


class Pipeline():
    def __init__ (self):
        with open('config.json') as js_f:
            self.config = json.load(js_f)
        self.load_prompts()    
        
        self.translator = GoogleTranslator(source='auto', target='en') 

        self.enr_tokenizer = AutoTokenizer.from_pretrained(self.config['PROMPT_ENRICHMENT_MODEL'])
        self.enr_model = AutoModelForCausalLM.from_pretrained(self.config['PROMPT_ENRICHMENT_MODEL'])

        self.llm_tokenizer = AutoTokenizer.from_pretrained(self.config["LLM_MODEL"], use_fast=True)
        self.llm = AutoModelForCausalLM.from_pretrained(self.config["LLM_MODEL"], torch_dtype=torch.float16,low_cpu_mem_usage=True)
                                                
        self.image_pipe = StableDiffusionPipeline.from_pretrained(self.config["IMAGE_GENERATION_MODEL"], torch_dtype=torch.float16)
        self.image_pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.image_pipe.scheduler.config)

        self.image_generator = ImageGenerator(
                     translator=self.translator,
                     image_pipe=self.image_pipe, 
                     neg_prompt=self.neg_prompt,
                     device = 'cuda')
        
        self.prompt_generator = PromptGenerator(model=self.llm, 
                     tokenizer=self.llm_tokenizer, 
                     translator = self.translator, 
                     template=self.llm_prompt_template, 
                     system_prompt=self.system_prompt,
                     enrichment_model=self.enr_model,
                     enrichment_tokenizer=self.enr_tokenizer,
                     device = 'cuda')
    
    def load_prompts(self):
        with open('prompts/system_prompt.txt') as f:
            self.system_prompt = f.read()
        with open('prompts/llm_prompt_template.txt') as f:
            self.llm_prompt_template = f.read()
        with open('prompts/negative_prompt_1.txt') as f:
            self.neg_prompt = f.read()
    
    def generateImg(self, text):
        prompt = self.prompt_generator.generate(text=text)
        image = self.image_generator.generate(prompt=prompt)
        return image