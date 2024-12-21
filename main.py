from streamlit import session_state, set_page_config, sidebar, title
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
    if "flashcards_df" not in session_state:
        session_state.flashcards_df = None
    if "uploaded_file_data" not in session_state:
        session_state.uploaded_file_data = None
    if "success_value" not in session_state:
        session_state.success_value = False
    if sidebar.button("Upload", icon="📂", use_container_width=True):
        file_upload_dialog()
    
    if "flashcards_df" not in session_state or session_state.flashcards_df is None:
        session_state.flashcards_df = Handle_file_upload(session_state.flashcards_df, session_state.uploaded_file_data, session_state.success_value)
    
        
    # Add navigation in the sidebar using a toggle
    table = sidebar.toggle("Show Table", key="show_quiz_toggle", value=False)
    
    # Reverse the order of the DataFrame
    session_state.flashcards_df = session_state.flashcards_df.iloc[::-1].reset_index(drop=True)

    if table:
        title("Tables")
        sidebar_manager.display_search_and_sort()
        Flashquiz_viewer_table(sidebar_manager, session_state.flashcards_df)
    else:
        title("Quiz")
        Quiz(session_state.flashcards_df)

if __name__ == "__main__":
    main()
