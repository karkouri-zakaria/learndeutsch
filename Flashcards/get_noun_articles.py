from spacy import load
from streamlit import cache_data, error

@cache_data
def get_noun_articles(sentence):
    try:
        nlp = load("./de_core_news_md/de_core_news_md-3.8.0")
        articles = {"Fem": "die", "Masc": "der", "Neut": "das"}

    except OSError:
        error("Please restart the setup failed.", icon="🚫")
    result = []
    for token in nlp(sentence):
        if token.pos_ == "NOUN":
            # Get the first gender if available, otherwise assign None
            article = (
                articles.get(token.morph.get("Gender")[0])
                if token.morph.get("Gender")
                else None
            )
            if article:
                result.append((token.text, article))

    return result   