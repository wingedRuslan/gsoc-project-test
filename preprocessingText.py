from bs4 import BeautifulSoup
import re


def cleaning_data(text):
    # Removing HTML Markup (get text without tags or markup)
    cleaned_text = BeautifulSoup(text, features="lxml")
    cleaned_text = cleaned_text.get_text()

    # Remove multiple consecutive whitespaces
    _RE_COMBINE_WHITESPACE = re.compile(r"\s+")
    cleaned_text = _RE_COMBINE_WHITESPACE.sub(" ", cleaned_text).strip()

    # Removal of characters which are not numbers and alphabets
    cleaned_text = re.sub("[\W_]+", " ", cleaned_text)

    return cleaned_text
