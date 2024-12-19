from pandas import DataFrame, concat
from streamlit import audio, button, selectbox, sidebar, success, text_input, warning, write

from Flashcards.detect_spelling_errors import detect_spelling_errors
from Flashcards.get_noun_articles import get_noun_articles
from Audio.generate_audio import generate_audio


class AppSidebar:
    def __init__(self):
        """Initialize the Sidebar class."""
        self.search_query = None
        self.sort_option = None
        self.user_input = None
        self.front_text = None
        self.back_text = None

    def display_search_and_sort(self):
        """Display search and sort options with an expander."""
        with sidebar.expander("Search and Sort Options", expanded=False, icon="🔍"):
            self.search_query = text_input("Search Flashcards", key="search_query")
            self.sort_option = selectbox(
                "Sort By", ["", "Front Text", "Back Text", "Shuffle"], key="sort_option"
            )
    
    def get_user_input(self):
        """Get user input for text area and play audio if provided."""
        self.user_input = sidebar.text_area("", "", placeholder="Write something to read ...", key="user_input")

        if self.user_input:
            with sidebar.expander("Reading", expanded=True, icon="🗣️"):
                audio_path = generate_audio(self.user_input)
                with open(audio_path, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                    audio(audio_bytes, format="audio/mp3", autoplay=True)

                write("> Articles and misspelled:")

                for word, article in get_noun_articles(self.user_input):
                    write(f"{article} {word}")

                for word, suggestions in detect_spelling_errors(self.user_input):
                    if suggestions:
                        write(f"**{word}** -> {', '.join(suggestions)}")

    def add_flashcard(self, flashcards_df):
        """Handle the addition of new flashcards."""
        with sidebar.expander("Add New Flashcard", expanded=False, icon="➕"):
            self.front_text = text_input("Enter Front Text", key="front_text")
            self.back_text = text_input("Enter Back Text", key="back_text")

            if button("Add Flashcard", key="add_flashcard"):
                if self.front_text and self.back_text:
                    new_row = DataFrame({
                        "FrontText": [self.front_text],
                        "BackText": [self.back_text]
                    })

                    # Add to DataFrame
                    if flashcards_df is None:
                        flashcards_df = new_row
                    else:
                        flashcards_df = concat([new_row, flashcards_df], ignore_index=True)

                    success(f"Flashcard added: {self.front_text} -> {self.back_text}", icon="✅")
                else:
                    warning("Please fill both fields.", icon="⚠️")

        return flashcards_df

    def display_download_button(self, flashcards_df):
        """Display a download button for the flashcards."""
        with sidebar.expander("Download Flashcards", expanded=False, icon="📥"):
            updated_csv = flashcards_df.to_csv(index=False)
            sidebar.download_button(
                label="Download CSV",
                data=updated_csv,
                file_name="flashcards.csv",
                mime="text/csv",
            )
