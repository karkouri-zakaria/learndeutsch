from Sidebar.appSidebar import AppSidebar
from Flashcards.display_flashcards import display_flashcards
from Flashcards.process_flashcards import process_flashcards
from pandas import DataFrame
from streamlit import error

def Flashquiz_viewer_table(_sidebar_manager: AppSidebar, flashcards_df: DataFrame):

    if flashcards_df is not None:
        try:
            flashcards_df = process_flashcards(flashcards_df, _sidebar_manager)
            display_flashcards(flashcards_df, _sidebar_manager)
            _sidebar_manager.display_download_button(flashcards_df) 
        except Exception as e:
            error(f"Error parsing the file: {e}", icon="🚫")