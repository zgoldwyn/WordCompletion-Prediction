# Word Completion & Prediction
## What it does
This program is an autocomplete and prediction model. It suggests words that are predicted to follow a word typed, and suggests the most likely completion of the word if currently typing a word. Attached is a demo in which the model has been trained on the book Moby Dick. In order to autofill a suggestion, Tab is used. In order to exit the program, Esc is used. 
## How it works
### Trie (word completion)
The project uses a Tree data structure made up of character nodes, having finished paths which represent a valid english word. It uses data from the Reddit Comments Dataset from Kaggle (1 million comments across 40 subreddits). 
### N-Gram model with backoff (next word prediction)
For next word prediction, the project uses a dictionary of tuples, each having possible next words, and their occurence rate to predict the next word. It's an N-gram model with stupid backoff, with what I've found to be the best N value of 3. The model checks the previous n words, then incrementally decreases n until a next word is found. 
## Installation
Requires Python 3.12+
```bash
pip install -r requirements.txt
```
Place your data files in the project root:
- `reddit_comments.csv` — Reddit Comments Dataset from Kaggle
- `chat.db` — optional, copy from ~/Library/Messages/chat.db
- `mobydick.txt` — optional, download from Project Gutenberg
## How to run
Run this program with python in the terminal. AutocompleteNGram.py is the model using NGram, and AutocompleteBigram is the older model, only using the single previous word to determine the most likely next word.  
## Data sources
I used a data source from Kaggle, but the program can also use an imessage "chat.db" file, and a text file which has words separated by any whitespace. For example, the book "Moby Dick" (included in the repository) can also be used to train the model. I did not include the Chat.db file for privacy reasons. 
## Design Decisions
I decided to use a Trie over a list because it has O(k) time complexity for search given k is the already typed string. This differs from using a list of possible words and iterating through because time complexity would be O(n) for any case, even if there are only a few valid word options. 
\nI decided to use statistical backoff because I am able to know exactly why the next word was chosen. Using a neural net would have other dependencies to worry about, and I wanted this project to be trained on data I provided.  


https://github.com/user-attachments/assets/754db0dd-4206-4d91-96ab-674d995ba6ed

