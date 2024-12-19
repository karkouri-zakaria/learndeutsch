from io import StringIO
from streamlit import dialog, error, info, session_state, success
from Flashcards.flashquiz_csv_table import flashquiz_csv_table
from Flashcards.flashquiz_to_csv import flashquiz_to_csv

def Handle_file_upload(uploaded_file, success_value):
    """Handle file upload and processing."""
    csv_data, csv_file_like = None, None
    flashcards_df = None

    if uploaded_file:
        file_extension = uploaded_file.name.split(".")[-1].lower()

        if file_extension == "csv":
            try:
                # Process CSV file
                flashcards_df = flashquiz_csv_table(uploaded_file)
                if success_value:
                    show_dialog()
                    session_state.success_value = False
            except Exception as e:
                error(f"Error processing CSV file: {e}", icon="🚫")

        elif file_extension == "flashquiz":
            try:
                # Process .flashquiz file
                file_content = uploaded_file.read().decode("utf-8")
                
                # Check if the file content is empty or invalid
                if not file_content.strip():
                    raise ValueError("The .flashquiz file is empty. or corrupted. Please try again.")

                # Convert .flashquiz content to CSV
                csv_data = flashquiz_to_csv(file_content)
                csv_file_like = StringIO(csv_data)
                flashcards_df = flashquiz_csv_table(csv_file_like)
                
                if success_value:
                    show_dialog()
                    session_state.success_value = False
            except Exception as e:
                error(f"Error processing .flashquiz file: {e}", icon="🚫")

    if flashcards_df is None or flashcards_df.empty:
        info("No valid file uploaded or processed.", icon="ℹ️")

    return flashcards_df

@dialog("Upload a File 📂")
def show_dialog():
    success("CSV file uploaded successfully!", icon="✅")
