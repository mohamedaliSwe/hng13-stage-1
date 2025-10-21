"""Performs String Analysis"""
import hashlib
from string_analyzer.models.string_models import TextAnalysisModel


def is_palindrome(text: str) -> bool:
    """Checks if the text is a palindrome"""
    clean_text = text.strip().lower().replace(" ", "")
    return clean_text == clean_text[::-1]


def unique_characters(text: str) -> int:
    """Count the number unique characters in the text"""
    return len(set(text))


def word_count(text: str) -> int:
    """Counts the number of words in the text"""
    clean_text = text.strip()
    return len(clean_text.split())


def character_frequency(text: str) -> dict:
    """Count the frequency of each chracter in the text"""
    char_dict = {}
    for char in text.lower():
        char_dict[char] = char_dict.get(char, 0) + 1
    return char_dict


def sha256_hash(text: str) -> str:
    """Computes the SHA-256 hash of the text"""
    text_hash = hashlib.sha256(text.encode()).hexdigest()
    return text_hash


def analyze_string(text: str) -> dict:
    """Performs full string analysis"""
    return TextAnalysisModel(
        length=len(text),
        is_palindrome=is_palindrome(text),
        unique_characters=unique_characters(text),
        word_count=word_count(text),
        sha256_hash=sha256_hash(text),
        character_frequency_map=character_frequency(text)
    )
