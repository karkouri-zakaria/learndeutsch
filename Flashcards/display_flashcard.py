from streamlit import audio, cache_data, container, popover, write
from Audio.generate_audio import generate_audio
from Flashcards.get_noun_articles import get_noun_articles

@cache_data
def display_flashcard(flashcard):
    """Display a single flashcard with its audio."""
    with container(border=True):
        write(f"{flashcard['FrontText']}")
        with popover("⚫🔴🟡", help="Click to open"):
            try:
                # Generate the audio file path based on the BackText
                audio_file = generate_audio(flashcard['BackText'])  # This generates and returns the file path

                # Open and play the generated audio file
                with open(audio_file, "rb") as audio_data:
                    audio(audio_data, format="audio/mp3", autoplay=False)
                    
            except Exception as e:
                write(f"Error: {str(e)}")
            write(f"> {flashcard['BackText']}")
            for word, article in get_noun_articles(flashcard['BackText']):
                write(f"{article} {word}")