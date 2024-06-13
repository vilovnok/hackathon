

class Generator():
    def __init__ (self, clf_model, chat_tokenizer, qa_tokenizer, chat_model, qa_model):
        
        self.qa_model = qa_model
        self.clf_model = clf_model
        self.chat_tokenizer = chat_tokenizer
        self.qa_tokenizer = qa_tokenizer
        self.chat_model = chat_model    

    def clf_fun(self, text: str):
        result=self.clf_model(text)
        return result[0]['label']
    
    def chat_fun(self, text: str):
        tokenized_sentence = self.chat_tokenizer(text, return_tensors='pt', truncation=True)
        res = self.chat_model.generate(**tokenized_sentence, num_beams=2, max_length=100)            
        return self.chat_tokenizer.decode(res[0], skip_special_tokens=True)
    
    def qa_fun(self, text):
        question = "Что нужно нарисовать?"
        tokenized_sentence = self.qa_tokenizer(text, question, return_tensors='pt')
        res = self.qa_model.generate(**tokenized_sentence)
        decoded_res = self.qa_tokenizer.decode(res[0], skip_special_tokens=True)
        return decoded_res    
