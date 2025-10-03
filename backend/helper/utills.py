import nltk
from collections import Counter
import re

try:
    nltk.data.find("tokenizers/punkt")
except:
    nltk.download("punkt", quiet=True)
try:
    nltk.data.find("taggers/averaged_perceptron_tagger")
except:
    nltk.download("averaged_perceptron_tagger", quiet=True)

def extract_top_nouns(text, n=3):
    if not text or not text.strip():
        return []
    tokens = nltk.word_tokenize(text)
    tags = nltk.pos_tag(tokens)
    nouns = [w.lower() for w, pos in tags if pos.startswith("NN") and re.match("^[A-Za-z]+$", w)]
    most_common = [word for word, _ in Counter(nouns).most_common(n)]
    return most_common


