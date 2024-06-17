import gc
import torch
from huggingface_hub import login

def cleanup():
    torch.cuda.empty_cache()
    gc.collect()

def auth_hf(token: str):
    login(token=token)
    print("Successfully auth with Huggin Face")