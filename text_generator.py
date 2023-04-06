import os
import sys
import re
import random
from collections import defaultdict, Counter
import spacy
from spacy.tokenizer import Tokenizer
from typing import List

# Global variables. Some can be changed to match what you want to accomplish.
# Cache for file data
CACHE = {}
# Discord's output characters limit.
MAX_SENTENCE_LENGTH = 1999
START_TOKENS_REGEX = re.compile(r'\S+').match
CORPUS_DIR = os.path.join(sys.path[0], "corpus")
# N-grams being used in the model are at least 5-grams (sequences of 5 consecutive words).
N_GRAM_SIZE = 5


def read_file(filename: str) -> str:
    """Reads the contents of a file located in the specified directory and
     returns the contents of the file as a string."""
    with open(os.path.join(CORPUS_DIR, f"{filename}.txt"), encoding="utf-8") as file:
        text = file.read()
    return text


def tokenize_corpus(text: str) -> list:
    """Tokenizes a given text (string) and returns a list of tokens."""
    # You can use spacy.load() instead for better accuracy, but it demands more time and resources.
    nlp = spacy.blank("pt")
    # This expands Spacy's max length so you can avoid errors.
    nlp.max_length = len(text) + 100
    # The modified tokenizer matches any non-whitespace characters.
    nlp.tokenizer = Tokenizer(nlp.vocab, token_match=START_TOKENS_REGEX)
    doc = nlp(text)
    tokens_list = [token.text for token in doc]
    return tokens_list


def get_ngrams(tokens_list: list) -> defaultdict:
    """Returns a dictionary with bigrams as keys and a Counter object as values.
    The Counter object contains the frequency
    of the next word after each bigram in the input list of tokens."""
    ngrams = defaultdict(Counter)
    for i in range(len(tokens_list) - 2):
        bigram = " ".join(tokens_list[i: i + 2])
        next_word = tokens_list[i + 2]
        ngrams[bigram].update((next_word,))
    return ngrams


def preprocess_ngrams(ngrams: defaultdict) -> List[str]:
    """
    Returns a list of word pairs that can start a sentence based on a dictionary of n-grams."""
    sentence_starts = []
    for pair in ngrams:
        if pair[0].isupper() and not pair.endswith((".", "!", "?")):
            sentence_starts.append(pair)
    return sentence_starts


def select_start(ngrams: defaultdict) -> list:
    """
    Selects a random pair of words from the ngrams dictionary.
    """
    candidate_sentence_starts = [
        pair.split()
        for pair in ngrams
        if pair[0].isupper()
        and not pair.endswith((".", "!", "?"))
    ]
    return random.choice(candidate_sentence_starts)


def generate_sentence(ngrams: defaultdict, n: int) -> str:
    """Generates a new sentence based on the n-gram model represented by the ngrams dictionary."""
    result = []
    sentence_starts = preprocess_ngrams(ngrams)
    while True:
        if not result:
            result = select_start(sentence_starts)
        if len(result) < 2:
            result.clear()
            continue
        prev_word1, prev_word2 = result[-2:]
        next_word_choices = list(ngrams[f"{prev_word1} {prev_word2}"].keys())
        if not next_word_choices:
            result.clear()
            continue
        next_word = random.choice(next_word_choices)
        result.append(next_word)

        if next_word[-1] in ".!?":
            if len(result) < n:
                result.clear()
                continue
            return " ".join(result)


def generate_text(filename: str) -> str:
    """Reads a text file, tokenizes it, generates an n-gram model,
    and uses it to create a new sentence."""
    if filename in CACHE:
        tokenized_text, ngrams = CACHE[filename]
    else:
        text = read_file(filename)
        tokenized_text = tokenize_corpus(text)
        ngrams = get_ngrams(tokenized_text)
        CACHE[filename] = (tokenized_text, ngrams)

    text = generate_sentence(ngrams, N_GRAM_SIZE)
    text = text[:MAX_SENTENCE_LENGTH]
    return text
