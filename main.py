from streamlit import session_state, set_page_config, sidebar, write
from Files.Handle_file_upload import Handle_file_upload
from Flashcards.Viewer import Flashquiz_viewer_table
from Quiz import Quiz
from Sidebar.appSidebar import AppSidebar
from Files.Upload import file_upload_dialog

def main():
    set_page_config(layout="wide")

    # Initialize the Sidebar
    sidebar_manager = AppSidebar()
    sidebar.title("📚 Flashquiz By Zakaria")
    sidebar_manager.get_user_input()

    # File uploaders section in the sidebar
    if "uploaded_file_data" not in session_state:
        session_state.uploaded_file_data = None
    if sidebar.button("Upload", icon="📂", use_container_width=True):
        file_upload_dialog()

    
    # Manage flashcards DataFrame
    flashcards_df = Handle_file_upload(session_state.uploaded_file_data)

    if flashcards_df is not None:
        # Add navigation in the sidebar using a toggle
        table = sidebar.toggle("Show Table", key="show_quiz_toggle", value=False)
        if table:
            sidebar_manager.display_search_and_sort()
            Flashquiz_viewer_table(sidebar_manager, flashcards_df)
        else:
            Quiz(flashcards_df)

if __name__ == "__main__":
    main()
