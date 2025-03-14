from streamlit import columns, dialog, rerun, session_state, set_page_config, sidebar, tabs, toast, write
from Answers.answers import save_results
from Audio_gen.generate_audio import generate_audios
from Files.Handle_file_upload import Handle_file_upload
from Sidebar.appSidebar import AppSidebar
from Files.Upload import file_upload_dialog
from Quiz_tab.Quiz import Quiz
from Flashcards.Viewer import viewer_table
@dialog("Awesome!")
def modal():
    write("🎉 Herzlichen Glückwunsch! Du hast das Quiz ohne Fehler bestanden – du bist so gut!")
    session_state.Results=[]
def main():
    set_page_config(
    page_title="Learndeutsch App",
    page_icon="🐦‍🔥",
    layout="centered",
    initial_sidebar_state="expanded",
    )
    sidebar_manager = AppSidebar()
    if 'flashcards_df' not in session_state: session_state.flashcards_df = None
    if 'uploaded_file_data' not in session_state: session_state.uploaded_file_data = None
    if 'original_flashcards_df' not in session_state: session_state.original_flashcards_df = None
    if 'success_value' not in session_state: session_state.success_value = False
    if 'shuffled' not in session_state: session_state.shuffled = False
    if 'shuffle_enabled' not in session_state: session_state.shuffle_enabled = False
    if 'auto_continue' not in session_state: session_state.auto_continue = False
    if 'Show_all_anwsers' not in session_state: session_state.Show_all_anwsers = False
    if 'Results' not in session_state: session_state.Results = []
    if 'show_wrongs' not in session_state: session_state.show_wrongs = False
    if 'flip_list' not in session_state: session_state.flip_list = False
    if session_state.uploaded_file_data is None:
        if sidebar.button("Upload", icon="📂", use_container_width=True):
            file_upload_dialog()
    else:
        if sidebar.button("Clear Data", icon="🗑️", use_container_width=True):
            session_state.flashcards_df = None
            session_state.uploaded_file_data = None
            session_state.success_value = False
    if "flashcards_df" not in session_state or session_state.flashcards_df is None:
        session_state.flashcards_df = Handle_file_upload(session_state.uploaded_file_data, session_state.success_value)
        if session_state.flashcards_df is not None:
            session_state.flashcards_df = session_state.flashcards_df.iloc[::-1].reset_index(drop=True)
            session_state.original_flashcards_df = session_state.flashcards_df.copy()
            try:
                generate_audios(session_state.flashcards_df)
            except Exception as e:
                toast(f"Error generating audio files: {e}", icon="🔊")
    if session_state.flashcards_df is not None:
        with sidebar:
            write("---")
            col1, col2 = columns(2)
            session_state.auto_continue = col1.toggle("⏩", key="auto", value=session_state.auto_continue, help="Automatically continue to the next flashcard after answering")
            session_state.Show_all_anwsers = col1.toggle("ℹ️", key="show", value=session_state.Show_all_anwsers, help="Show all answers")
            session_state.shuffle_enabled = col2.toggle("🔀", key="shuffle", value=session_state.shuffle_enabled, help="Randomize the flashcards order")
            session_state.flip_list = col2.toggle("🔄", key="flip", value=session_state.flip_list, help="Flip the flashcards order")
    if session_state.flip_list and len(session_state.flashcards_df) > 1:
        session_state.flashcards_df = session_state.flashcards_df.iloc[::-1].reset_index(drop=True)
    if session_state.Results and len(session_state.Results) > 0 and session_state.flashcards_df is not None:
        with sidebar:
            write("---")
            col1, col2 = columns([3,1], gap="small", vertical_alignment="center")
            col1.metric(
                f"Score:",
                f"{sum(1 if result[3] else 0 for result in session_state.Results)} / {len(session_state.Results)}",
                f"{'+1' if session_state.Results[-1][3] else '-1'}" if session_state.Results else None,
            )
        col2.button("", on_click=lambda: session_state.Results.clear(), icon="🧹", use_container_width=True)
        save_results()
        session_state.show_wrongs = col2.toggle("🤦🏼", key="wrongs", value=session_state.show_wrongs)
        session_state.flashcards_df = session_state.flashcards_df.iloc[[i for i, result in enumerate(session_state.Results) if not result[3]]] if session_state.show_wrongs else session_state.original_flashcards_df.copy()
    sidebar.write("---")
    sidebar_manager.get_user_input()
    quiz_tab, all_cards = tabs(["**Quiz** 🎮", "**All cards** 📓"])
    with quiz_tab:
        Quiz(session_state.flashcards_df)
        with sidebar:
            if session_state.flashcards_df is not None: 
                with sidebar.expander("Timer", icon="⏱️"):
                    sidebar_manager.timer()
                sidebar_manager.download_results()
    with all_cards:
        viewer_table(sidebar_manager, session_state.flashcards_df)
    if session_state.Results and len(session_state.Results) > 0 and session_state.flashcards_df is not None and sum(1 if result[3] else 0 for result in session_state.Results) == len(session_state.flashcards_df):
        modal()
        
if __name__ == "__main__":
    main()