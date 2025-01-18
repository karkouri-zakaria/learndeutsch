from io import BytesIO
from pathlib import Path
from webbrowser import open as openURL
from pandas import DataFrame, ExcelWriter, concat
from Audio.generate_audio import generate_audio
from streamlit import audio, download_button, form, form_submit_button, selectbox, session_state, sidebar, success, text_area, text_input, warning, write

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
        """Get user input for either text area or Verbformen search based on the toggle."""
        # Toggle to switch between user input and verb search
        with sidebar:
            write("---")        
            # Display the respective input field based on toggle value
            verbformen_input = text_area("---", "", 
                placeholder="📖Wörterbuch...", 
                key="verbformen_input",
                height=68, 
                on_change=lambda: openURL(f"https://www.verbformen.com/?w={session_state.verbformen_input.strip()}") 
                if session_state.verbformen_input.strip() else None
            )
            self.user_input = text_area(
                label="🔉 Read ...",
                placeholder="Enter text for reading",
                key="user_input"
            )
            if self.user_input.strip():
                try:
                    audio_path = Path(f"cached_audios/{self.user_input.strip()}.mp3")
                    if not audio_path.exists():
                        audio_path = generate_audio(self.user_input.strip())
                    with open(audio_path, "rb") as audio_file:
                        audio(audio_file, format="audio/mp3", autoplay=True)
                except Exception as e:
                    write(f"Error generating audio: {str(e)}")

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
                        new_flashcard = DataFrame({"English": [front_text], "Deutsch": [back_text]})
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
            # Convert DataFrame to Excel content as a bytes object
            output = BytesIO()
            with ExcelWriter(output, engine='xlsxwriter') as writer:
                flashcards_df.to_excel(writer, index=False, sheet_name='Flashcards')
            xlsx_data = output.getvalue()
            
            download_button(
                label="Download Excel",
                data=xlsx_data,
                file_name="flashcards.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )