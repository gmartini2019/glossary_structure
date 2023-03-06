# Business Glossary

## Dependencies

The following will be primarily targeted for MacOS, with the assumption that Anaconda is already installed on the machine.

First, create a virtual environment with conda (replace "myenv" with desired name) and activate it:
```zsh
conda create -n myenv python=3.10.9
conda activate myenv
```

Next, install the following packages with pip or conda:
```zsh
transformers -> pip install transformers
pandas -> pip install pandas
fastapi -> pip install fastapi
uvicorn -> pip install uvicorn
torch -> pip3 install torch torchvision
```

## API Usage

The main components that the API uses are in `src` folder, in addition to the `english_dict.pkl` and `vasu_df.csv` files (which are loaded into the trie data structure). Everything else is either experiments with Jupyter Notebooks or unneeded data files.

To run, first activate the env created above 
```python
conda activate myenv
```
and navigate to the `src` folder and run:
```python
python app.py
```

This will start the server with uvicorn on http://127.0.0.1:8000 -> you can then navigate to http://127.0.0.1:8000/docs to try the API methods.

Alternatively, you could run `navigation.py` and test a potential user interaction flow with the use of the API. Simply run the following in another terminal tab or window:
```python
python navigation.py
```

Now going into more details about each file in the `src` folder:

### Trie.py

This file contains the definitions of the TrieNode and Trie classes, which are used to build the Trie data structure. The `app.py` file primarily calls the functions of the `Trie` class. The key function in this file is `fuzzy_search`, as it can be tuned to show the number of results to show for a user: 

```python
difflib.get_close_matches(word, self.words(), n=10, cutoff=cutoff)
```

The *n* parameter in `get_close_matches` is the top *n* closest matches and can be set by the business. If you'd like the user to be able to set this parameter, then we can modify the function definition to take in *n* and also modify the api GET method in `app.py` to take in the same parameter.

### app.py

This file is where we define the FastAPI application, create an instance of the `Trie` class, load the data from `english_dict.pkl` and `vasu_df.csv` into that instance, and create the REST methods to query the Trie as well as invoke the pretrained model.

### pretrained.py

This file is where we define the pretrained DialoGPT-medium model. We are using huggingface's transformers library to load the model. Two key lines in the file are below:

```python
question = f'What could "{word}" mean?'
```
The above line is the prompt that we are sending to the model and it is something that can be tweaked as per specific use case.

```python
chat_response = model.generate(input_ids=input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
```
This second line is important because it allows you to define the max length of the model response with the `max_length` parameter.

### navigation.py

This file is merely an example use case of the API to test the functionality of the methods and demo a potential flow of user interaction. Use this file to look at the in usage of calling the API endpoints.
