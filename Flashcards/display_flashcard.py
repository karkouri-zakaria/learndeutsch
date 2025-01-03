from streamlit import audio, button, cache_data, columns, container, data_editor, popover, rerun, session_state, sidebar, write
from Audio.generate_audio import generate_audio
from Flashcards.get_noun_articles import get_noun_articles
import pandas as pd

cache_data()
def display_flashcard(index, flashcard):
    """Display a single flashcard with its audio."""
    with container(border=True):
        write(f"{flashcard['English']}")
        with popover("⚫🔴🟡", help="Click to open"):
            try:
                # Generate the audio file path based on the Deutsch
                audio_file = generate_audio(flashcard['Deutsch'])  # This generates and returns the file path

                # Open and play the generated audio file
                with open(audio_file, "rb") as audio_data:
                    audio(audio_data, format="audio/mp3", autoplay=False)

            except Exception as e:
                write(f"Error: {str(e)}")
            write(f"> {flashcard['Deutsch']}")

            # Use the flashcard data as-is (no renaming)
            flashcard_df = pd.DataFrame([flashcard])

            col1, col2 = columns(2)

            if col1.button("Edit", key=f"Edit_{flashcard['Deutsch']}_{index}", icon="✏️", use_container_width=True):
                data_editor(
                    flashcard_df,
                    column_config={
                        "English": "English",
                        "Deutsch": "Deutsch",
                    },
                    use_container_width=True,
                    hide_index=True,
                )

            if col2.button("Dlete", key=f"Delete_{flashcard['Deutsch']}_{index}", icon="🗑️", use_container_width=True):
                session_state.flashcards_df.drop(flashcard_df.index, inplace=True)
                rerun()