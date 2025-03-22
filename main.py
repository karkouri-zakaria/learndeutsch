from pathlib import Path
from time import sleep
from streamlit import audio, button, columns, dialog, expander, markdown, metric, rerun, session_state, set_page_config, sidebar, slider, tabs, toast, write
from Answers.answers import save_results
from Answers.colorize import colorize_noun
from Audio_gen.generate_audio import generate_audio, generate_audios
from Files.Handle_file_upload import Handle_file_upload
from Sidebar.appSidebar import AppSidebar
from Files.Upload import file_upload_dialog
from Quiz_tab.Quiz import Quiz
from Flashcards.Viewer import viewer_table
from mutagen.mp3 import MP3
@dialog("Awesome!")
def modal():
    write("🎉 Herzlichen Glückwunsch! Du hast das Quiz ohne Fehler bestanden – du bist so gut!")
    session_state.Results=[]
def main():
    set_page_config(page_title="Learndeutsch App", page_icon="🐦‍🔥", layout="centered", initial_sidebar_state="expanded")
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
            col1, col2 = columns(2)
            session_state.auto_continue = col1.toggle("⏩", key="auto", value=session_state.auto_continue, help="Automatically continue to the next flashcard after answering")
            session_state.Show_all_anwsers = col1.toggle("ℹ️", key="show", value=session_state.Show_all_anwsers, help="Show all answers")
            session_state.shuffle_enabled = col2.toggle("🔀", key="shuffle", value=session_state.shuffle_enabled, help="Randomize the flashcards order")
            session_state.flip_list = col2.toggle("🔄", key="flip", value=session_state.flip_list, help="Flip the flashcards order")
            write("---")
            left_button, right_button = columns([2,1], gap="small")
            left_button.metric(
                f"Score:",
                f"{sum(1 if result[3] else 0 for result in session_state.Results)} / {len(session_state.Results)}",
                f"{'+1' if session_state.Results[-1][3] else '-1'}" if session_state.Results else None,
            )
            if session_state.Results and len(session_state.Results) > 0 and session_state.flashcards_df is not None:
                if right_button.button("", on_click=lambda: session_state.Results.clear(), icon="🪣", use_container_width=True):
                    save_results()
            if session_state.Results and any(result[3] == False for result in session_state.Results):    
                if right_button.button("🤦🏼", type="primary" if session_state.show_wrongs else "secondary", use_container_width=True):
                    session_state.show_wrongs = not session_state.show_wrongs
                    rerun()
            left_button, right_button = columns([1,1], gap="small")
            current_index = session_state.flashcard_index if session_state.flashcard_index < len(session_state.flashcards_df ) else 0
            flashcard = session_state.flashcards_df.iloc[current_index]
            total_flashcards = len(session_state.flashcards_df )
            with left_button:
                if button("✖", key="wrong_button", use_container_width=True, type="primary" if any(result[0] == flashcard['Source'] and not result[2] for result in session_state.Results) else "secondary") and not session_state.show_wrongs:
                    session_state.Results = [result for result in session_state.Results if result[1] != flashcard['Source']]
                    session_state.Results.append([int(current_index)+1, flashcard['Source'], flashcard['Target'], False])
                    session_state.flashcard_index = (current_index + 1) % total_flashcards
                    save_results()
                    audio_path = Path(f"cached_audios/{flashcard['Target']}.mp3")
                    if not audio_path.exists():
                        audio_path = generate_audio(flashcard["Target"])
                    with open(audio_path, "rb") as audio_file:
                        audio(audio_file, format="audio/mp3", autoplay=True)
                    sleep(MP3(audio_path).info.length)
                    rerun()
            with right_button:
                if button("✔", key="correct_button", use_container_width=True, type="  " if any(result[0] == flashcard['Source'] and result[2] for result in session_state.Results) else "secondary") and not session_state.show_wrongs:
                    session_state.Results = [result for result in session_state.Results if result[1] != flashcard['Source']]
                    session_state.Results.append([int(current_index)+1, flashcard['Source'], flashcard['Target'], True])
                    session_state.flashcard_index = (current_index + 1) % total_flashcards
                    audio_path = Path(f"cached_audios/{flashcard['Target']}.mp3")
                    if not audio_path.exists():
                        audio_path = generate_audio(flashcard["Target"])
                    with open(audio_path, "rb") as audio_file:
                        audio(audio_file, format="audio/mp3", autoplay=True)
                    sleep(MP3(audio_path).info.length)
                    rerun()
            with left_button:
                if button("⮜", key="prev_button", use_container_width=True, type="primary"):
                    session_state.flashcard_index = (current_index - 1) % total_flashcards
                    rerun()
            with right_button:
                if button("⮞", key="next_button", use_container_width=True, type="primary"):
                    session_state.flashcard_index = (current_index + 1) % total_flashcards
                    write(session_state.flashcard_index)
                    rerun()
            if session_state.flip_list and len(session_state.flashcards_df) > 1:
                session_state.flashcards_df = session_state.flashcards_df.iloc[::-1].reset_index(drop=True)
            write("---")
        session_state.flashcards_df = session_state.flashcards_df.iloc[[i for i, result in enumerate(session_state.Results) if not result[3]]] if session_state.show_wrongs else session_state.original_flashcards_df.copy()            
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