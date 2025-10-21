"""Contains Natural Language filtering"""


def filter_nlp(query: str) -> dict:
    query = query.lower().strip()
    filters = {}

    if "palindromic" in query or "palindrome" in query:
        filters["is_palindrome"] = True

    if "single word" in query or "one word" in query or "a word" in query:
        filters["word_count"] = 1

    if "first vowel" in query:
        filters["contains_character"] = "a"

    if "containing the letter" in query or "contain the letter" in query:
        try:
            letter = query.split("letter")[1].strip().split()[0]
            filters["contains_character"] = letter[0]
        except IndexError:
            raise ValueError("Unable to extract letter")

    if "longer than" in query:
        try:
            num = int(query.split("longer than")[1].split()[0])
            filters["min_length"] = num + 1
        except (IndexError, ValueError):
            raise ValueError("Unable to extract numeric length")

    if "min_length" in filters and "max_length" in filters and filters["min_length"] > filters["max_length"]:
        raise RuntimeError("Query parsed but resulted in conflicting filters")

    if not filters:
        raise ValueError("Unable to parse natural language query")

    return filters
