import random
from utility import *
words = {}

def ParseWords():
    with open('static/word_list.txt') as f:
        lines = [line.strip() for line in f if line.strip()]

    for i in range(0, len(lines) - 1, 2):
        category = lines[i]
        category_words = [word.strip() for word in lines[i + 1].split(',')]
        words[category] = category_words

def RandomizeWord():
    category = random.choice(list(words.keys()))
    word = random.choice(words[category])
    return [category, word]


ParseWords()
print(RandomizeWord())
#def DefineRoles(database, word):