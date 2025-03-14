from pandas import read_csv, read_excel
from streamlit import error, session_state, toast
def Handle_file_upload(uploaded_file, success_value):
    """Handle file upload and processing."""
    if uploaded_file:
        ext = uploaded_file.name.split(".")[-1].lower()
        try:
            if ext == "xlsx":
                df = read_excel(uploaded_file)
            elif ext == "csv":
                df = read_csv(uploaded_file)
            else:
                error(f"Unsupported file type: {ext}", icon="🚫")
            if not {"English", "Deutsch"}.issubset(df.columns):
                error("The file must have 'English' and 'Deutsch' columns.", icon="🚫")
            if success_value:
                toast("File uploaded successfully!", icon="✅")
                session_state.success_value = False
            return df
        except Exception as e:
            error(f"Error processing file: {e}", icon="🚫")