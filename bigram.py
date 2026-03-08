import collections
from collections import defaultdict
import re


class BigramModel:
    def __init__(self):
        self.counts = defaultdict(lambda: defaultdict(int))

    def train(self, corpus_path: str) -> None:
        wordlist = []
        with open("mobydick.txt", "r") as f:
            for line in f:
                a = line.split()
                for word in a:
                    word = re.sub(r'[^a-zA-Z]', '', word)
                    word = word.lower()
                    wordlist.append(word)
        for i in range(len(wordlist) - 1):
            word1 = wordlist[i]
            word2 = wordlist[i + 1]
            self.counts[word1][word2] += 1

    def predict(self, word: str, top_k: int = 5) -> list[str]:
        results = []
        gotword = self.counts.get(word)
        if not gotword:
            return results
        for i in gotword.items():
            results.append(i)
        results.sort(key=lambda x: x[1])
        results.reverse()
        return [word for word, freq in results[:top_k]]


if __name__ == "__main__":
    bigram = BigramModel()
    bigram.train("mobydick.txt")
    running = True
    print("Enter q to quit.")
    while running:
        part = input("Enter a word: \n")
        if part == 'q':
            break
        num = input("Enter how many suggestions: \n")
        completedlist = bigram.predict(part, int(num))
        print(completedlist)
    print("Quitting...")


