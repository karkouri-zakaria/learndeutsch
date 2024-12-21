from pandas import DataFrame, concat
from streamlit import audio, button, download_button, expander, form, form_submit_button, selectbox, session_state, sidebar, success, text_input, warning, write

from Files.Handle_file_upload import show_dialog
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
                "Sort By", ["", "English", "Deutsch", "Shuffle"], key="sort_option"
            )
    
    def get_user_input(self):
        """Get user input for text area and play audio if provided."""
        self.user_input = sidebar.text_area("---", "", placeholder="Write something to read ...", key="user_input")

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
        with sidebar.expander("Add a New Flashcard", icon="📝"):
            with form(key="new_flashcard_form"):
                # Input fields for the new flashcard
                front_text = text_input("English")
                back_text = text_input("Deutsch")
                submit = form_submit_button("Add Flashcard", help="Submit the new flashcard", use_container_width=True, icon="➕")

                # Check if the form was submitted
                if submit:
                    # Validate inputs
                    if front_text and back_text:
                        # Prepend the new flashcard to the DataFrame
                        new_flashcard = DataFrame({"FrontText": [front_text], "BackText": [back_text]})
                        flashcards_df = concat([new_flashcard, flashcards_df], ignore_index=True)

                        # Save updated DataFrame to session state
                        session_state.flashcards_df = flashcards_df

                        # Display confirmation
                        success("✅ New flashcard added successfully!")
                    else:
                        warning("⚠️ Please fill in both fields!")
        
        return flashcards_df
    
    def display_download_button(self, flashcards_df):
        """Display a download button for the flashcards."""
        with sidebar.expander("Download Flashcards", expanded=False, icon="📥"):
            updated_csv = flashcards_df.to_csv(index=False)
            download_button(
                label="Download CSV",
                data=updated_csv,
                file_name="flashcards.csv",
                mime="text/csv",
                use_container_width=True,
            )