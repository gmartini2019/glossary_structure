from transformers import pipeline, DistilBertTokenizerFast, DistilBertForMaskedLM
from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import openai

openai.api_key = "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"

def model(word):
    prompt = f"Define the column name {word} with a short description and then a longer description in at least 50 words"
    completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1000)
    return completion.choices[0].text.strip()