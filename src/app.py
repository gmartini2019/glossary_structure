from fastapi import FastAPI, APIRouter, HTTPException
import Trie
import pandas as pd
import pretrained
from collections import defaultdict
import uvicorn
import pickle
from transformers import pipeline, DistilBertTokenizerFast, DistilBertForMaskedLM
from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

app = FastAPI()
testInit = Trie.Trie_dict()

with open('../english_dict.pkl', 'rb') as f:
    english_dict = pickle.load(f)

vasu_dict = pd.read_csv('../vasu_df.csv')
dictionary_vasu = testInit.from_df_to_dict(vasu_dict)

testInit.insert_dict(english_dict)
testInit.insert_dict(dictionary_vasu)

@app.get('/search/{word}')
async def search(word: str):
    return testInit.search(word)

@app.get('/fuzzySearch/{word}/{cutoff}')
async def fuzzySearch(word: str, cutoff: float):
    return testInit.fuzzy_search(word, cutoff)

@app.post('/insert/{word}/{desc}')
async def insert(word: str, desc: str):
    testInit.insert(word, desc)
    return {"word": word, "description": desc}

@app.put('/update/{word}/{newDesc}')
async def update(word: str, newDesc: str):
    testInit.update(word, newDesc)
    return {"word": word, "new description": newDesc}

@app.get('/model/{word}')
def model(word: str):
    return pretrained.model(word)

def main():
    uvicorn.run(app, host='127.0.0.1', port=8000)

if __name__ == '__main__':
    main()