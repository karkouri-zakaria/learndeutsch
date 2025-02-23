from streamlit import audio, button, cache_data, columns, container, data_editor, popover, rerun, session_state, sidebar, write
from Audio.generate_audio import generate_audio
import pandas as pd

cache_data()
def display_flashcard(index, flashcard):
    """Display a single flashcard with its audio."""
    with container(border=True):
        Eng, Deu = columns([1, 1])
        Eng.write(f"> {flashcard['English']}")
        Deu.write(f"> {flashcard['Deutsch']}")
        try:
            # Generate the audio file path based on the Deutsch
            audio_file = generate_audio(flashcard['Deutsch'])  # This generates and returns the file path

            # Open and play the generated audio file
            with open(audio_file, "rb") as audio_data:
                audio(audio_data, format="audio/mp3", autoplay=False)

        except Exception as e:
            write(f"Error: {str(e)}")