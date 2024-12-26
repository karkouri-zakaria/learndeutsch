from streamlit import session_state, set_page_config, sidebar, title
from Chatbot import Chatbot
from Files.Handle_file_upload import Handle_file_upload
from Viewer import Flashquiz_viewer_table
from Quiz import Quiz
from Sidebar.appSidebar import AppSidebar
from Files.Upload import file_upload_dialog
from huggingface_hub import InferenceClient


def main():
    set_page_config(layout="wide")

    # Initialize the Sidebar
    sidebar_manager = AppSidebar()
    sidebar_manager.get_user_input()
    bot = InferenceClient(api_key="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")


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
        if session_state.flashcards_df is not None:
            session_state.flashcards_df = session_state.flashcards_df.iloc[::-1].reset_index(drop=True)
    
        
    # Add navigation in the sidebar using a toggle
    table = sidebar.toggle("Show Table", key="show_quiz_toggle", value=False)

    # Reverse the order of the DataFrame

    if table:
        title("Tables by zakaria 📃")
        sidebar_manager.display_search_and_sort()
        Flashquiz_viewer_table(sidebar_manager, session_state.flashcards_df)
    else:
        title("Quiz by zakaria 🧪")
        Quiz(session_state.flashcards_df)
    
    with sidebar:
        Chatbot(bot)

if __name__ == "__main__":
    main()
