import re
import sys


class TrieNode:
    def __init__(self) -> None:
        self.children = {}
        self.isEnd = False
        self.freq = 0

class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()  #update children of node
            node = node.children[char]
        node.isEnd = True
        node.freq += 1


    def complete(self, prefix: str, num:int) -> list[str]:
        prefix = prefix.lower()
        results = []
        node = self.root
        for char in prefix:
            if char not in node.children:
                return[] #return empty if a character in prefix is not in the trie
            else:
                node = node.children[char]
        self.collect(node, prefix, results)
        results.sort(key=lambda x: x[1])
        results.reverse()
        return [word for word, freq in results[:num]]
    def collect(self, node: TrieNode, prefix: str, results: list[(str,int)]) -> None:
        if node.isEnd:
                results.append((prefix,node.freq))
        for child in node.children: #for char in children,
            self.collect(node.children[child], prefix+child, results)#recurse with the child node, and the prefix with that string inclding the child char

    def save(self, path: str) -> None:
        import pickle
        words = []
        self.collect(self.root, "", words)
        with open(path, "wb") as f:
            pickle.dump(words, f)

    def load(self, path: str) -> None:
        import pickle
        with open(path, "rb") as f:
            words = pickle.load(f)
        for word, freq in words:
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.isEnd = True
            node.freq = freq

if __name__ == "__main__":
    trie = Trie()
    with open("mobydick.txt", "r") as f:
        for line in f:
            a = line.split()
            for word in a:
                word = re.sub(r'[^a-zA-Z]', '', word)
                word = word.lower()
                trie.insert(word)
    running = True
    print("Enter q to quit.")
    while running:
        part = input("Enter a partial word: \n")
        if part == 'q':
            break
        num = input("Enter how many suggestions: \n")
        completedlist = trie.complete(part, int(num))
        print(completedlist)

    print("Quitting...")
    quit()


