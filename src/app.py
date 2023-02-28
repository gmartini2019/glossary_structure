from fastapi import FastAPI, APIRouter, HTTPException
import Trie
import uvicorn
import pickle

app = FastAPI()
testInit = Trie.Trie_dict()

with open('../english_dict.pkl', 'rb') as f:
    english_dict = pickle.load(f)

testInit.insert_dict(english_dict)

@app.get('/search/{word}')
async def search(word: str):
    return testInit.search(word)

@app.get('/fuzzySearch/{word}')
async def fuzzySearch(word: str):
    return testInit.fuzzy_search(word)

@app.post('/insert/{word}/{desc}')
async def insert(word: str, desc: str):
    testInit.insert(word, desc)
    return {"word": word, "description": desc}

@app.put('/update/{word}/{newDesc}')
async def update(word: str, newDesc: str):
    testInit.update(word, newDesc)
    return {"word": word, "new description": newDesc}


def main():
    uvicorn.run(app, host='127.0.0.1', port=8000)

if __name__ == '__main__':
    main()