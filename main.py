from streamlit import rerun, session_state, set_page_config, sidebar, tabs, toast
from Files.Handle_file_upload import Handle_file_upload
from Sidebar.appSidebar import AppSidebar
from Files.Upload import file_upload_dialog
from Quiz import Quiz
from Sidebar.timer import timer
from Viewer import viewer_table
def main():
    set_page_config(
    page_title="Learndeutsch App",
    page_icon="🐦‍🔥",
    layout="centered",
    initial_sidebar_state="expanded",
    )
    sidebar_manager = AppSidebar()
    if "flashcards_df" not in session_state:
        session_state.flashcards_df = None
    if "uploaded_file_data" not in session_state:
        session_state.uploaded_file_data = None
    if "success_value" not in session_state:
        session_state.success_value = False
    if 'Results' not in session_state:
        session_state.Results = []
    if session_state.uploaded_file_data is None:
        if sidebar.button("Upload", icon="📂", use_container_width=True):
            file_upload_dialog()
    else:
        if sidebar.button("Clear Data", icon="🗑️", use_container_width=True):
            session_state.flashcards_df = None
            session_state.uploaded_file_data = None
            session_state.success_value = False
            rerun()
    if "flashcards_df" not in session_state or session_state.flashcards_df is None:
        session_state.flashcards_df = Handle_file_upload(session_state.flashcards_df, session_state.uploaded_file_data, session_state.success_value)
        if session_state.flashcards_df is not None:
            session_state.flashcards_df = session_state.flashcards_df.iloc[::-1].reset_index(drop=True)
    if session_state.Results  is not None and len(session_state.Results) > 0:
        sidebar.metric(
            f"Score:",
            f"{sum(1 if result[3] else 0 for result in session_state.Results)} / {len(session_state.Results)}",
            f"{'+1' if session_state.Results[-1][3] else '-1'}" if session_state.Results else None
        )
        if sum(1 if result[3] else 0 for result in session_state.Results) == len(session_state.flashcards_df):
            toast("Congratulations! You have completed the quiz!", icon="🎉")
        sidebar.button("Clear Score", on_click=lambda: session_state.Results.clear(), icon="🧹", use_container_width=True)
    sidebar_manager.get_user_input()
    quiz, all = tabs(["**Quiz** 🎮", "**All cards** 📔"])
    with quiz:
        Quiz(session_state.flashcards_df)
        with sidebar:
            if session_state.flashcards_df is not None: 
                with sidebar.expander("Timer", icon="⏱️"):
                    timer()
    with all:
        viewer_table(sidebar_manager, session_state.flashcards_df)
if __name__ == "__main__":
    main()
