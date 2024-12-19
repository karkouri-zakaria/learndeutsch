from streamlit import button, dialog, file_uploader, rerun, session_state, write

@dialog("Upload a File 📂")
def file_upload_dialog():
    """
    Dialog to upload a `.csv` or `.flashquiz` file.
    """
    write("You can upload a `.csv` or `.flashquiz` file here:")
    uploaded_file = file_uploader(
        "Upload your file",
        type=["csv", "flashquiz"],
        key="file_upload_dialog",
    )
    if button("Submit"):
        if uploaded_file is not None:
            # Store the uploaded file in session state
            session_state.uploaded_file_data = uploaded_file
            rerun()  # Trigger a rerun to update the app