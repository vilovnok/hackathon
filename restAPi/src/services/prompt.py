from utils.worker import conversation, generateImg, translation
from utils.pipeline import Pipeline
from schemas.prompt import Prompt_to



class PromptService:

    async def preproccesing(self, data:Prompt_to):          
            text=data.text        
            pipeline=Pipeline()
            prompt=pipeline.classification(text=text)
            print(text)

            if prompt == "draw":
                answer=pipeline.question_answer(text=text)                
                # img=generateImg.delay(answer)
                translated_sentences=translation.delay(text=answer)
                res=translated_sentences.get()
                return res
            else:
                answer=conversation.delay(text=text)    
                res=answer.get()                         
                return res
            
