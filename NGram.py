from collections import defaultdict
import re
#this algorithm begins with a nth order n gram search, and goes down to trigram and then bigram to find the most likely next word given a dataset
class NGram:
    def __init__(self, max_n:int):
        self.max_n = max_n
        self.counts = defaultdict(lambda: defaultdict(int))

    def train(self, corpus_path: str) -> None:
        wordlist = []
        with open(corpus_path, "r") as f:
            for line in f:
                a = line.split()
                for word in a:
                    word = re.sub(r'[^a-zA-Z]', '', word)
                    word = word.lower()
                    wordlist.append(word)
        for i in range(len(wordlist)):
            for n in range(1, self.max_n + 1):
                if i + n < len(wordlist):
                    context = tuple(wordlist[i:i+n])
                    next_word = wordlist[i+n]
                    self.counts[context][next_word] += 1

    def train_from_messages(self, messages: list):
        wordlist = []
        for row in messages:
            text = row[0]
            for word in text.split():
                word = re.sub(r'[^a-zA-Z]', '', word).lower()
                if word:
                    wordlist.append(word)
        for i in range(len(wordlist)):
            for n in range(1, self.max_n + 1):
                if i + n < len(wordlist):
                    context = tuple(wordlist[i:i+n])
                    next_word = wordlist[i+n]
                    self.counts[context][next_word] += 1

    def train_from_csv(self, messages: str):
        wordlist = []
        for row in messages:
            for word in row.split():
                word = re.sub(r'[^a-zA-Z]', '', word).lower()
                if word:
                    wordlist.append(word)
        for i in range(len(wordlist)):
            for n in range(1, self.max_n + 1):
                if i + n < len(wordlist):
                    context = tuple(wordlist[i:i+n])
                    next_word = wordlist[i+n]
                    self.counts[context][next_word] += 1


    def predict(self, context: list[str], top_k: int = 5) -> list[str]:
        for n in range(self.max_n, 0, -1):  # for counting down from max_n down to 1
            key = tuple(context[-n:])       # last n words as tuple
            gotword = self.counts.get(key)
            if gotword:                      # found a match at this n, otherwise move on and try a lower n value
                results = list(gotword.items())
                results.sort(key=lambda x: x[1])
                results.reverse()
                return [word for word, freq in results[:top_k]]
        return []  # nothing found at any length

    def save(self, path: str) -> None:
        import pickle
        with open(path, "wb") as f:
            pickle.dump(dict(self.counts), f)

    def load(self, path: str) -> None:
        import pickle
        from collections import defaultdict
        with open(path, "rb") as f:
            data = pickle.load(f)
        self.counts = defaultdict(lambda: defaultdict(int), data)


