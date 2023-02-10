import difflib
import numpy as np
import sys
from sklearn.neighbors import NearestNeighbors
from collections import defaultdict
from collections import deque

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_word = False
        self.description = None

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word, description):
        current = self.root
        for char in word:
            current = current.children[char]
        current.is_word = True
        current.description = description
    
    def search(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                return None
            current = current.children[char]
        if current.is_word:
            return current.description
        return None
    
    def fuzzy_search(self, word, cutoff=0.4):
        results = difflib.get_close_matches(word, self.words(), n=10, cutoff=cutoff)
        return {result: (self.search(result), difflib.SequenceMatcher(None, word, result).ratio()) for result in results}

    def fuzzy_search_knn(self, word, k=5, cutoff=0.1):
        words = np.array(self.words())
        words_len = np.array([len(w) for w in words])
        word_len = len(word)
        distances = np.abs(words_len - word_len)
        knn = NearestNeighbors(n_neighbors=k, metric='manhattan')
        knn.fit(distances.reshape(-1, 1))
        _, indices = knn.kneighbors(np.array([word_len]).reshape(-1, 1))
        results = [words[index] for index in indices[0]]
        ratio = [difflib.SequenceMatcher(None, word, result).ratio() for result in results]
        return {result: (self.search(result), ratio[i]) for i, result in enumerate(results) if ratio[i] >= cutoff}
        
    def words(self):
        words = []
        def backtrack(node, word):
            if node.is_word:
                words.append("".join(word))
            for char in node.children:
                word.append(char)
                backtrack(node.children[char], word)
                word.pop()
        backtrack(self.root, [])
        return words
    

def main():
    argList = sys.argv[1:]
    trie = Trie()
    dictionary = {"first name": "The first name of a person", "language": "which language the person speaks", 
                  "date of birth": "when the person was born", "model": "model of the car", "vehicle type": "type of vehicle  the person owns", "company": "enterprise where the employee works", 
                  "street": "The street where somebody lives", "last name": "The last name of a person"}
    
    for word, desc in dictionary.items():
        trie.insert(word, desc)

    for word in argList:
        print(trie.fuzzy_search(word))

if __name__ == '__main__':
    main()

    