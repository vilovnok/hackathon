from utils import cleanup

class ImageGenerator():
    def __init__ (self, translator, image_pipe, neg_prompt, device):   
        self.translator = translator  
        self.neg_prompt = neg_prompt
        self.device = device            
        self.image_model = image_pipe.to(self.device)           
        
    def generate(self, prompt):
        i = 0
        REGENERATE_STEPS=1
        while i < REGENERATE_STEPS:
            output = self.pipe(prompt, negative_prompt = self.neg_prompt)
            image = output.images[0]
            i += 1
        cleanup()
        return image