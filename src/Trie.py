import difflib
from collections import defaultdict

class TrieNode_dict:
    def __init__(self):
        self.children = defaultdict(TrieNode_dict)
        self.is_word = False
        self.description = None
        
class Trie_dict:
    def __init__(self):
        self.root = TrieNode_dict()
        self.count = 0
        
    def insert(self, word, description=None):
        current = self.root
        for char in word:
            current = current.children[char]
        if not current.is_word:
            current.is_word = True
            self.count += 1
        current.description = description
    
    def update(self, word, new_description):
        current = self.root
        for char in word:
            current = current.children[char]
        current.description = new_description
        return True
    
    def search(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                return None
            current = current.children[char]
        if current.is_word:
            return current.description
        return None

    def insert_list(self, lst):
        for word in lst:
            self.insert(word) 

    def size(self):
        return self.count
    
    def insert_dict(self, dict_obj):
        for key, definition in dict_obj.items():
            self.insert(str(key), str(definition))
    
    def fuzzy_search(self, word, cutoff):
        results = difflib.get_close_matches(word, self.words(), n=10, cutoff=cutoff)
        res = {result: (self.search(result), difflib.SequenceMatcher(None, word, result).ratio()) for result in results}
        if word in res:
            return {word: res[word][0]}
        else: return res

    def words(self):
        words = []
        def dfs(node, word):
            if node.is_word:
                words.append(word)
            for char in node.children:
                dfs(node.children[char], word + char)
        dfs(self.root, "")
        return words
    
    def from_df_to_dict(self, df):
        first_column = df.iloc[:, 0].tolist()
        second_column = df.iloc[:, 1].tolist()
        #dict_object = my_dictionary()
        dict_object = defaultdict()
        for i in range(len(first_column)):
            dict_object[first_column[i]]=  second_column[i]
        
        return dict_object