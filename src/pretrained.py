from transformers import pipeline, DistilBertTokenizerFast, DistilBertForMaskedLM
from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def model(word):
    question = f'What could "{word}" mean?'
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
    input_ids = tokenizer.encode(question + tokenizer.eos_token, return_tensors='pt')
    chat_response = model.generate(input_ids=input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    chat_response = tokenizer.decode(chat_response[0], skip_special_tokens=True)
    chat_response = chat_response.replace(question, "")
    return chat_response