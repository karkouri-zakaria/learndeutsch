from streamlit import cache_data
from spellchecker import SpellChecker

@cache_data
def detect_spelling_errors(user_input):
    try:
        spell = SpellChecker(language="de")
    except OSError:
        raise OSError("Please restart the setup failed.", icon="🚫")
    words = user_input.split()
    misspelled_words = []

    for word in words:
        # Remove any punctuation
        cleaned_word = "".join(e for e in word if e.isalnum())
        if cleaned_word:  # Ignore empty strings
            # Check for misspellings
            if cleaned_word.lower() not in spell:
                suggestions = spell.candidates(cleaned_word)
                misspelled_words.append((word, suggestions))

    return misspelled_words