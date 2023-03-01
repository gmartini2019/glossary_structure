import requests
import app
import json

def navigate_trie():
    # ML_used = False
    # Prompt the user to enter a search term
    print('Enter the term for which you would like the definition')
    search = input()
    
    # Use the trie data structure to perform a fuzzy search on the search term
    search_result = requests.get(f'http://127.0.0.1:8000/fuzzySearch/{search}').text
    search_obj = json.loads(search_result)
    key_list = list(search_obj)
    list_length = len(search_obj)
    
    # If the search term is not found in the trie, prompt the user to define it
    if list_length == 0:
        print("Empty list, you will have the choice of ML model generated definition or custom definition")    
    # If the search term is found in the trie, present the user with a list of search results
    else:
        i = 1
        for key, val in search_obj.items():
            print(f'{i}. {key}: {val[0]}')
            i += 1
        
    # Prompt the user to select a search result from the list
    print('If the desired item is in the list, type Y, else N')
    choice = input()
    if choice == 'Y':
        print('Now type the number associated to the desired term')
        user_choice = int(input())
        
        # Ensure that the user's choice is a valid index in the list of search results
        1 <= user_choice <= list_length
        selected_item = key_list[user_choice - 1]
        print(f"You selected: {selected_item}")
        
        # Look up the definition of the selected term in the trie data structure
        word_definition = requests.get(f'http://127.0.0.1:8000/search/{selected_item}').text
        
        # If the term has no definition in the trie, prompt the user to define it
        if word_definition == None:
            print(f'No previous definition has been found, however {selected_item} is commonly referred to as:\n ')
            print(app.english_dict[selected_item])
            print('Now you can define it yourself')
            custom_definition = input()
            requests.put(f'http://127.0.0.1:8000/update/{selected_item}/{custom_definition}')
            print('Thank you, I learned a new word!')
        
        # If the term has a definition in the trie, present the definition to the user and prompt for redefinition
        else:
            print(f'The definition for {selected_item} is : {word_definition}')
            print(f'Do you like it? Type "Y" if so, if not you"ll redefine it')
            redefinition_choice = input()
            
            # If the user chooses to redefine the term, prompt for a new definition and update the trie
            if redefinition_choice != 'Y':
                print('Type it in:')
                custom_definition = input()
                requests.put(f'http://127.0.0.1:8000/update/{selected_item}/{custom_definition}')
                print('Thank you, I learned a new word!')
    else:
        print(f'Run ML model? (Type "Y" for yes and "N" for no)')
        runChoice = input()
        if runChoice == "Y":
            print(f'"{search}" is not in the list, running ML model to generate definition - generated output below:')
            
            modelDef = str(requests.get(f'http://127.0.0.1:8000/model/{search}').text)
            print(modelDef)

            print(f'If you are satisfied with the definition type "Y", else type "N": ')
            mlChoice = input()

            if mlChoice != 'N':
                requests.post(f'http://127.0.0.1:8000/insert/{search}/{modelDef}')
            else:
                print('Add your own definition: ')
                definition_nbs = input()
                requests.post(f'http://127.0.0.1:8000/insert/{search}/{definition_nbs}')
        else:
            print('Add your own definition: ')
            definition_nbs = input()
            requests.post(f'http://127.0.0.1:8000/insert/{search}/{definition_nbs}')
                
def main():
    navigate_trie()


if __name__ == "__main__":
    main()