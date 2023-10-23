import os
import re
import random
from collections import defaultdict, Counter
from typing import List, Tuple
import spacy
from cache_manager import CacheManager

# Global constants.
MAX_SENTENCE_LENGTH = 1999
START_TOKENS_REGEX = re.compile(r"\S+").match
CORPUS_DIR = os.path.join(os.path.dirname(__file__), "corpus")
N_GRAM_SIZE = 3
FINAL_PUNCT = ".!?"

# Initialize Spacy tokenizer and CacheManager.
nlp = spacy.blank("pt")
tokenizer = spacy.tokenizer.Tokenizer(
    nlp.vocab, token_match=START_TOKENS_REGEX
)
nlp.tokenizer = tokenizer
nlp.max_length = 10000000
cache_manager = (
    CacheManager()
)  # Set the desired max cache size, default value is 10


def read_file(filename: str) -> str:
    """Reads and returns content of a file."""
    with open(
        os.path.join(CORPUS_DIR, f"{filename}.txt"), encoding="utf-8"
    ) as file:
        return file.read()


def tokenize_corpus(text: str) -> List:
    """Tokenizes the given text using Spacy and returns a list of tokens."""
    return [token.text for token in nlp(text)]


def get_ngrams(tokens_list: list, n=N_GRAM_SIZE) -> defaultdict:
    """Generates and returns n-grams from a list of tokens."""
    ngrams = defaultdict(Counter)
    for i in range(len(tokens_list) - n + 1):
        ngram = tuple(tokens_list[i : i + n - 1])
        next_word = tokens_list[i + n - 1]
        ngrams[ngram].update([next_word])
    return ngrams


def is_valid_start(ngram: tuple) -> bool:
    """
    Checks if a given n-gram can be used as a valid starting sequence.
    """
    return ngram[0][0].isupper() and ngram[-1][-1] not in FINAL_PUNCT


def select_start(ngrams: defaultdict) -> Tuple:
    """
    Selects a random valid starting n-gram from the n-grams list.
    """
    starts = [ngram for ngram in ngrams if is_valid_start(ngram)]
    return random.choice(starts) if starts else ()


def generate_sentence(
    ngrams: defaultdict, n=N_GRAM_SIZE, max_words=100
) -> str:
    """
    Generates a random sentence using the n-grams.
    """
    result = list(select_start(ngrams))
    if not result:
        return ""

    # Ensure the generation continues until a punctuation mark AND within word limit
    while len(result) < n or (
        result[-1][-1] not in FINAL_PUNCT and len(result) < max_words
    ):
        next_ngram = tuple(result[-(n - 1) :])
        next_word_choices = list(ngrams[next_ngram].keys())
        weights = list(
            ngrams[next_ngram].values()
        )  # Get the frequencies as weights

        if not next_word_choices or len(result) >= max_words:
            break
        # Choose the next word based on its frequency
        result.append(random.choices(next_word_choices, weights=weights)[0])

    # If the text exceeded the word limit without finding punctuation, trim to the last punctuation
    if len(result) >= max_words:
        for i in reversed(range(max_words)):
            if result[i][-1] in FINAL_PUNCT:
                result = result[: i + 1]
                break

    return " ".join(result)


def generate_text(filename: str) -> str:
    data = cache_manager.get(filename)
    if data:
        tokenized_text, ngrams = data
    else:
        text = read_file(filename)
        tokenized_text = tokenize_corpus(text)
        ngrams = get_ngrams(tokenized_text)
        cache_manager.set(filename, (tokenized_text, ngrams))
    text = generate_sentence(ngrams)
    return text[:MAX_SENTENCE_LENGTH]
