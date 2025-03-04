from streamlit import button, dialog, file_uploader, info, rerun, session_state, write
@dialog("Upload a File 📂")
def file_upload_dialog():
    write("You can upload a `.xlsx` file here:")
    uploaded_file = file_uploader(
        "Upload your file",
        type="xlsx",
        key="file_upload_dialog",
    )
    info("Please upload a file and then click 'Submit'.")
    if button("**Submit**", icon="💾", use_container_width=True ) and uploaded_file is not None:
        session_state.uploaded_file_data = uploaded_file
        session_state.success_value = True
        rerun()
