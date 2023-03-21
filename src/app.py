from fastapi import FastAPI, APIRouter, HTTPException
from py2neo import Graph, Node, Relationship, NodeMatch, NodeMatcher
import pandas as pd
import pretrained
import db_methods
from collections import defaultdict

app = FastAPI()

graph = Graph('bolt://localhost:7687', auth=('neo4j', 'password')) ## can change the url and credentials if using another instance of the database

@app.get('/search/{word}')
async def search(word: str):
    return db_methods.search_node_in_graph(graph, word)

@app.get('/fuzzySearch/{word}/{n}')
async def fuzzySearch(word: str, n: int):
    return db_methods.fuzzy_search_native(graph, word, n)

@app.post('/insert/{word}/{desc}')
async def insert(word: str, desc: str):
    db_methods.insert_node(graph, word, desc)
    return {"word": word, "description": desc}

@app.put('/update/{word}/{newDesc}')
async def update(word: str, newDesc: str):
    db_methods.update_description(graph, word, newDesc)
    return {"word": word, "new description": newDesc}

@app.get('/model/{word}')
def model(word: str):
    return pretrained.model(word)