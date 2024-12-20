import pandas as pd
import streamlit as st

class FlashcardApp:
    def add_flashcard(self, flashcards_df):
        with st.sidebar.expander("Add a New Flashcard", expanded=True):
            with st.form(key="new_flashcard_form"):
                # Input fields for the new flashcard
                front_text = st.text_input("Front Text (English)")
                back_text = st.text_input("Back Text (Deutsch)")
                submit = st.form_submit_button("Add Flashcard", help="Submit the new flashcard")

                # Check if the form was submitted
                if submit:
                    st.write(submit)
                    # Validate inputs
                    if front_text and back_text:
                        # Prepend the new flashcard to the DataFrame
                        new_flashcard = pd.DataFrame({"FrontText": [front_text], "BackText": [back_text]})
                        flashcards_df = pd.concat([new_flashcard, flashcards_df], ignore_index=True)

                        # Save updated DataFrame to session state
                        st.session_state.flashcards_df = flashcards_df

                        # Display confirmation
                        st.success("✅ New flashcard added successfully!")
                    else:
                        st.warning("⚠️ Please fill in both fields!")
        
        return flashcards_df

# Initialize the app
if "flashcards_df" not in st.session_state:
    st.session_state.flashcards_df = pd.DataFrame(columns=["FrontText", "BackText"])

flashcard_app = FlashcardApp()
st.session_state.flashcards_df = flashcard_app.add_flashcard(st.session_state.flashcards_df)

# Display the flashcards
st.write("### Current Flashcards")
st.write(st.session_state.flashcards_df)
