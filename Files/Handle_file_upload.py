from streamlit import error, session_state, toast
from Flashcards.xlsx_table import xlsx_table

def Handle_file_upload(flashcards_df, uploaded_file, success_value):
    """Handle file upload and processing."""
    xlsx_data, xlsx_file_like = None, None

    if uploaded_file:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        try:
            # Process Excel file
            flashcards_df = xlsx_table(uploaded_file)
            if success_value:
                show_dialog()
                session_state.success_value = False
        except Exception as e:
            error(f"Error processing Excel file: {e}", icon="🚫")

    return flashcards_df

def show_dialog():
    toast("File uploaded successfully!", icon="✅")