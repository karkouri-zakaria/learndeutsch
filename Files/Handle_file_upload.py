from io import BytesIO
from streamlit import dialog, error, info, session_state, success, write
from Flashcards.flashquiz_xlsx_table import flashquiz_xlsx_table
from Flashcards.flashquiz_to_xlsx import flashquiz_to_xlsx

def Handle_file_upload(flashcards_df, uploaded_file, success_value):
    """Handle file upload and processing."""
    xlsx_data, xlsx_file_like = None, None

    if uploaded_file:
        file_extension = uploaded_file.name.split(".")[-1].lower()

        if file_extension == "xlsx":
            try:
                # Process Excel file
                flashcards_df = flashquiz_xlsx_table(uploaded_file)
                if success_value:
                    show_dialog()
                    session_state.success_value = False
            except Exception as e:
                error(f"Error processing Excel file: {e}", icon="🚫")

        elif file_extension == "flashquiz":
            try:
                # Process .flashquiz file
                file_content = uploaded_file.read().decode("utf-8")
                
                # Check if the file content is empty or invalid
                if not file_content.strip():
                    raise ValueError("The .flashquiz file is empty or corrupted. Please try again.")
                
                # Convert .flashquiz content to Excel
                xlsx_data = flashquiz_to_xlsx(file_content)
                xlsx_file_like = BytesIO(xlsx_data)
                flashcards_df = flashquiz_xlsx_table(xlsx_file_like)
                
                if success_value:
                    show_dialog()
                    session_state.success_value = False
            except Exception as e:
                error(f"Error processing .flashquiz file: {e}", icon="🚫")

    return flashcards_df

@dialog("Upload a File 📂")
def show_dialog():
    success("File uploaded successfully!", icon="✅")
